# MCP setup

| Local registration | Role |
| --- | --- |
| SketchUp | Connects Codex to the installed SketchUp Ruby extension for model inspection and scene export. |
| ZWCAD | Connects to the open native drawing for inspection, drafting and verification. |
| Node REPL | Provides a persistent JavaScript session for supported tools and local automation. |

Canva, Google Drive/Sheets and GitHub are connected apps. Check access to the specific model, drawing, sheet or design before writing. Image generation is a built-in tool used by APR.

## SketchUp startup

The extension registers its localhost listener on port 9876. Apply the included startup patch to an installed extension with the matching menu block after taking a backup. SketchUp loads the change on its next launch. The listener starts once per application session and exits with SketchUp. Keep the loopback binding.

After restarting, open a model and make a read-only MCP query for its title and scene list. A successful launch or open window alone does not establish a live MCP connection. Use the backup to restore the extension if the startup change fails.

The startup patch was verified on SketchUp 2024 (24.0.594). After a fresh launch, a file-version warning paused startup. Once the warning was acknowledged, a read-only MCP query succeeded without using **Start Server**. If a startup dialog is present, resolve it before retrying the query. When opening a newer model for inspection, preserve the original file.
