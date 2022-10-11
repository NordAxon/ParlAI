from pathlib import Path


def main():
    "Modifies requirements.txt by removing lines matching packages in uninstall.txt"

    cwd = Path(__file__).resolve().parent

    with open(cwd / "ignoreinstall.txt", "r") as f:
        text = f.read()
        uninstall = text.split("\n")

    with open(cwd / "requirements.txt", "r") as f:
        text = f.read()
        reqs = text.split("\n")

    newreqs = []
    for req in reqs:
        if not any(un in req.lower() for un in uninstall):
            newreqs.append(req)
        else:
            print("Removing", req)

    requirements = '\n'.join(newreqs)
    with open(cwd / "requirements.txt", "w") as f:
        f.write(requirements)


if __name__ == "__main__":
    main()
