"""Launch an Anak Tangga workflow in the local Codex CLI."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

PROFILES = {
    "cad": ("CAD Drafting.md", "cad-drafting"),
    "boq": ("QC BoQ & RAB.md", "qc-boq-rab"),
    "apo": ("presentation AO.md", "presentation-ao"),
    "apr": ("Presentation Render.md", "presentation-render"),
    "api": ("Canva Insert.md", "canva-insert"),
    "apm": ("Canva Material.md", "canva-material"),
    "apf": ("Canva Floor Plan.md", "canva-floor-plan"),
    "aps": ("Canva Section Plan.md", "canva-section-plan"),
}


def locate_workspace(explicit):
    default = Path.home() / "Documents" / "Anak Tangga Opperational"
    candidates = [explicit] if explicit else [
        Path.cwd(), Path.cwd() / "Anak Tangga Opperational",
        Path(__file__).resolve().parent, default / default.name, default,
    ]
    for root in candidates:
        if (root / "AGENTS.md").is_file():
            if any((root / local).is_file() for local, _ in PROFILES.values()) or (
                root / "docs" / "presentation-ao-workflow.md"
            ).is_file():
                return root.resolve()
    raise ValueError("Anak Tangga workspace not found. Supply --workspace.")


def build_prompt(workspace, stages, brief):
    files = []
    for stage in stages:
        local, public = PROFILES[stage]
        candidates = [workspace / local, workspace / "docs" / f"{public}-workflow.md"]
        profile = next((p for p in candidates if p.is_file()), None)
        if profile is None:
            raise ValueError(f"Missing profile for {stage.upper()}: {local}")
        files.append(str(profile.relative_to(workspace)))
    steps = "\n".join(f"{index}. {stage.upper()} — {file}"
                      for index, (stage, file) in enumerate(zip(stages, files), 1))
    return (
        "Read AGENTS.md and the listed profiles before taking action. "
        "Run the requested stages in order using verified inputs and configured MCP tools. "
        "For a new Canva run or revision, create a fresh copy or new design and carry it "
        "through the stages. Follow the active tools' approval requirements. "
        "Verify the outcome and report any remaining blockers.\n\n"
        f"Workflow stages:\n{steps}\n\n"
        f"User brief:\n{brief}"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--print-prompt", action="store_true",
                        help="Print a prompt to paste into Codex Desktop.")
    modes = parser.add_subparsers(dest="mode", required=True)
    modes.add_parser("list", help="List the eight profiles.")
    run = modes.add_parser("run", help="Run one profile.")
    run.add_argument("agent", choices=PROFILES)
    run.add_argument("brief")
    presentation = modes.add_parser("presentation", help="Run a full presentation.")
    presentation.add_argument("route", choices=("apo", "apr"))
    presentation.add_argument("brief")
    export = modes.add_parser("export", prefix_chars="+",
                              help="Run the direct Python APO exporter.")
    export.add_argument("export_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.mode == "list":
            for key, (name, _) in PROFILES.items():
                print(f"{key.upper():3}  {Path(name).stem}")
            return 0
        if args.mode == "export":
            exporter = Path(__file__).resolve().with_name("presentation_ao.py")
            if not exporter.is_file():
                raise ValueError("Keep presentation_ao.py beside this launcher.")
            return subprocess.call([sys.executable, str(exporter), *args.export_args])
        workspace = locate_workspace(args.workspace)
        stages = ((args.agent,) if args.mode == "run"
                  else (args.route, "api", "apm", "apf", "aps"))
        prompt = build_prompt(workspace, stages, args.brief)
        if args.print_prompt:
            print(prompt)
            return 0
        codex = shutil.which("codex")
        if codex is None:
            raise ValueError("Codex CLI is missing from PATH. Use --print-prompt in Codex Desktop.")
        return subprocess.call([codex, "--", prompt], cwd=workspace)
    except (OSError, ValueError) as error:
        print(f"Anak Tangga: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
