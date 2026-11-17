"""Export direct SketchUp PNGs and write a Canva Insert handoff manifest."""
import argparse
import json
from pathlib import Path
import re
import socket
import struct
import sys

ADDRESS = ("127.0.0.1", 9876)
MODEL = """m=Sketchup.active_model
{path:m.path, title:m.title, active_scene:m.pages.selected_page&.name,
 scenes:m.pages.map(&:name)}.to_json"""


def query(code):
    request = dict(jsonrpc="2.0", id=1, method="tools/call",
                   params=dict(name="eval_ruby", arguments=dict(code=code)))
    with socket.create_connection(ADDRESS, timeout=60) as connection:
        connection.sendall(json.dumps(request).encode() + b"\n")
        with connection.makefile("rb") as response:
            line = response.readline(1048577)
    if len(line) > 1048576 or not line.endswith(b"\n"):
        raise ValueError("Incomplete or oversized SketchUp reply.")
    reply = json.loads(line)
    if reply.get("id") != 1:
        raise ValueError("Unexpected SketchUp request ID.")
    if "error" in reply:
        raise ValueError(reply["error"].get("message", "SketchUp bridge error"))
    return json.loads(reply["result"]["content"][0]["text"])


def ruby_string(value):
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def export_view(model, scene, index, destination, width, height):
    name = re.sub(r"[^a-zA-Z0-9_-]+", "-", scene).strip("-") or "scene"
    target = destination / f"{index:02d}-{name[:65]}.png"
    code = f"""
m=Sketchup.active_model
raise 'The active SketchUp model changed' unless m.path == {ruby_string(model['path'])}
page=m.pages[{ruby_string(scene)}]
raise 'Saved scene missing' unless page
previous=m.pages.selected_page
raise 'Select a saved scene before exporting' unless previous
view=m.active_view
camera=view.camera
options=m.options['PageOptions']
transitions=options['ShowTransition']
begin
  options['ShowTransition']=false
  m.pages.selected_page=page
  view.refresh
  ok=view.write_image({ruby_string(target.as_posix())},{width},{height},true)
  {{saved:ok}}.to_json
ensure
  m.pages.selected_page=previous
  view.camera=camera
  options['ShowTransition']=transitions
end
"""
    if not query(code)["saved"]:
        raise ValueError(f"SketchUp could not export {scene}.")
    with target.open("rb") as stream:
        header = stream.read(24)
    if (len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n"
            or header[12:16] != b"IHDR"):
        raise ValueError(f"Invalid PNG: {target}")
    actual = struct.unpack(">II", header[16:24])
    if actual != (width, height):
        raise ValueError(f"Unexpected PNG dimensions: {actual}")
    return dict(scene=scene, view_title=scene, file=target.name,
                width=width, height=height, status="PNG verified; visual review pending")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List the model and scenes.")
    parser.add_argument("--scene", action="append", help="Exact saved scene name. Repeat to select several.")
    parser.add_argument("--all", action="store_true", help="Export all saved scenes in model order.")
    parser.add_argument("--output", type=Path, help="New output folder, required for exports.")
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=1000)
    args = parser.parse_args()
    if args.list == bool(args.all or args.scene) or (args.all and args.scene):
        parser.error("Choose --list, --all, or one or more --scene arguments.")
    if not args.list and args.output is None:
        parser.error("Pass --output for exports.")
    if not all(1 <= value <= 8192 for value in (args.width, args.height)):
        parser.error("Width and height must be between 1 and 8192 pixels.")
    try:
        model = query(MODEL)
        if args.list:
            print(json.dumps(model, indent=2))
            return 0
        if not model["path"] or not model["active_scene"]:
            raise ValueError("Open a saved model and select a saved scene first.")
        saved = model["scenes"]
        requested = set(args.scene or saved)
        if requested.difference(saved) or not requested:
            raise ValueError(f"No matching selection. Available scenes: {', '.join(saved)}")
        destination = args.output.resolve()
        destination.mkdir(parents=True, exist_ok=False)
        manifest = dict(workflow="APO", source_model=model["path"],
                        original_scene=model["active_scene"], exports=[])
        manifest_path = destination / "scene-to-page.json"
        try:
            for number, scene in enumerate(saved, 1):
                if scene in requested:
                    entry = export_view(model, scene, number, destination, args.width, args.height)
                    manifest["exports"].append(entry)
                    print(f"{scene}: {entry['file']}")
        finally:
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"Canva Insert handoff: {manifest_path}")
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        print(f"APO failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
