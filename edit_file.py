# This file edits parlai/agents/transformer/transformer.py to skip large dependencies in production environment
# It removes lines relating to TorchClassifierAgent  

from pathlib import Path

original = "parlai/agents/transformer/transformer.py"
backup = "parlai/agents/transformer/transformer_backup.py"

def remove_dependency():
    folder = Path(__file__).resolve().parent
    filepath = folder / original
    backuppath = folder / backup

    with open(filepath, "r") as f:
        text = f.read()

    with open(backuppath, "w") as f:
        f.write(text)

    lines = text.split("\n")

    # Remove specific lines
    lines = lines[:403]
    lines.pop(13)
    newtext = "\n".join(lines)

    with open(filepath, "w") as f:
        f.write(newtext)



if __name__ == "__main__":
    remove_dependency()
