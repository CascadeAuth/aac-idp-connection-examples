"""Every sample is valid JSON, carries placeholders, and is explained in its README."""

import json
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"<([A-Z][A-Z0-9_]*)>")
FORBIDDEN_FIELDS = {"jwks_static"}


def main() -> int:
    problems = []
    for directory in sorted(p for p in Path(".").iterdir() if (p / "README.md").is_file() and p.name != ".github"):
        readme = (directory / "README.md").read_text(encoding="utf-8")
        for sample in sorted(directory.glob("*.json")):
            text = sample.read_text(encoding="utf-8")
            try:
                document = json.loads(PLACEHOLDER.sub("placeholder", text))
            except json.JSONDecodeError as error:
                problems.append(f"{sample}: not valid JSON ({error})")
                continue
            if not PLACEHOLDER.search(text):
                problems.append(f"{sample}: carries no <PLACEHOLDER>")
            for field in FORBIDDEN_FIELDS & set(document):
                problems.append(f"{sample}: must not carry {field}")
            if f"`{sample.name}`" not in readme:
                problems.append(f"{sample}: not listed in {directory}/README.md")
            for name in set(PLACEHOLDER.findall(text)):
                if f"`{name}`" not in readme:
                    problems.append(f"{sample}: placeholder {name} not explained in {directory}/README.md")
    for problem in problems:
        print(problem)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
