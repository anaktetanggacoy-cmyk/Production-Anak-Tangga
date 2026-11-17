"""Read-only command-line client for the local SketchUp MCP Ruby bridge."""
import argparse
import json
import socket
import sys

ADDRESS = ("127.0.0.1", 9876)
MAX_RESPONSE = 1024 * 1024
MODEL_QUERY = (
    "m = Sketchup.active_model; "
    "{title: m.title, version: Sketchup.version, "
    "active_scene: m.pages.selected_page&.name, scenes: m.pages.map(&:name)}.to_json"
)


def read_model(timeout=10):
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "eval_ruby", "arguments": {"code": MODEL_QUERY}},
    }
    with socket.create_connection(ADDRESS, timeout=timeout) as connection:
        connection.sendall(json.dumps(request).encode("utf-8") + b"\n")
        with connection.makefile("rb") as response:
            line = response.readline(MAX_RESPONSE + 1)
    if not line.endswith(b"\n") or len(line) > MAX_RESPONSE:
        raise ValueError("The bridge returned an incomplete or oversized response.")
    envelope = json.loads(line)
    if envelope.get("id") != 1:
        raise ValueError("The bridge returned an unexpected request ID.")
    if "error" in envelope:
        raise ValueError(envelope["error"].get("message", "SketchUp bridge error"))
    result = envelope.get("result")
    blocks = result.get("content", []) if isinstance(result, dict) else []
    if (not isinstance(blocks, list) or len(blocks) != 1
            or not isinstance(blocks[0], dict)
            or blocks[0].get("type") != "text"
            or not isinstance(blocks[0].get("text"), str)):
        raise ValueError("The bridge returned an unexpected result format.")
    model = json.loads(blocks[0]["text"])
    if not isinstance(model, dict) or not isinstance(model.get("scenes"), list):
        raise ValueError("The bridge did not return a model and scene list.")
    return model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON for automation.")
    args = parser.parse_args()
    try:
        model = read_model()
    except OSError as error:
        print(f"Cannot reach SketchUp at 127.0.0.1:9876 ({error}). "
              "Open SketchUp, dismiss any startup dialog, and check the MCP extension.",
              file=sys.stderr)
        return 1
    except (ValueError, AttributeError) as error:
        print(f"SketchUp bridge response error: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(model, indent=2))
    else:
        print(f"Connected to SketchUp {model['version']}")
        print(f"Model: {model['title'] or '(untitled)'}")
        print(f"Active scene: {model['active_scene'] or '(none)'}")
        for index, scene in enumerate(model["scenes"], 1):
            print(f"{index:2}. {scene}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
