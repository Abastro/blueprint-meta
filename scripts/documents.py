#!/usr/bin/env python3
"""Reads and checks docs/documents.json, the list of documents.

Each document is {"dir", "name", "title"}: it lives in docs/<dir>/, its root
file is docs/<dir>/<name>.tex, and it builds to docs/<dir>/build/<name>.pdf.
The title is shown on the release page; the build does not use it.

Usage:
  documents.py check   check the manifest against docs/; exit 1 on problems
  documents.py list    check, then print "<dir>/<name>" per document (for make)
  documents.py json    check, then print the documents as a JSON array (for CI)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MANIFEST = DOCS / "documents.json"

FIELDS = ("dir", "name", "title")
# Plain file names, safe as make targets and in paths.
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
SHARED_DIR = "common"
# A dir is also a make target, so it must not shadow the Makefile's own.
RESERVED_DIRS = {SHARED_DIR, "all", "check", "clean"}


def rel(path):
    return path.relative_to(ROOT).as_posix()


def read_manifest():
    """Parses and validates the manifest. Returns (documents, errors)."""
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return [], [f"cannot read {rel(MANIFEST)}: {e}"]
    docs = data.get("documents") if isinstance(data, dict) else None
    if not isinstance(docs, list):
        return [], [f'{rel(MANIFEST)} must be an object with a "documents" array']

    errors = [] if docs else [f"{rel(MANIFEST)} lists no documents"]
    # PDFs are published side by side, so names must be unique, not just dirs.
    seen = {"dir": set(), "name": set()}
    for i, doc in enumerate(docs):
        at = f"documents[{i}]"
        if not isinstance(doc, dict):
            errors.append(f"{at} must be an object")
            continue
        errors += [f'{at} has unknown field "{k}"' for k in doc if k not in FIELDS]
        for k in FIELDS:
            value = doc.get(k)
            if not (isinstance(value, str) and value):
                errors.append(f"{at}.{k} must be a non-empty string")
            elif k in seen:
                if not ID.fullmatch(value):
                    errors.append(f'{at}.{k} "{value}" must match {ID.pattern}')
                elif value in seen[k]:
                    errors.append(f'{at}.{k} "{value}" is used more than once')
                elif k == "dir" and value in RESERVED_DIRS:
                    errors.append(f'{at}.dir "{value}" is reserved')
                seen[k].add(value)
    return docs, errors


def check_tree(docs):
    """Checks the manifest against docs/, both ways. Returns errors."""
    errors = []
    for doc in docs:
        folder = DOCS / doc["dir"]
        if not folder.is_dir():
            errors.append(f"{rel(folder)}/ is listed but does not exist")
            continue
        for file in (f"{doc['name']}.tex", ".latexmkrc"):
            if not (folder / file).is_file():
                errors.append(f"{rel(folder / file)} is missing")

    listed = {doc["dir"] for doc in docs}
    for folder in sorted(DOCS.iterdir()):
        if (folder.is_dir() and not folder.name.startswith(".")
                and folder.name != SHARED_DIR and folder.name not in listed):
            errors.append(f"{rel(folder)}/ is not listed in {rel(MANIFEST)}")
    return errors


def main(argv):
    command = argv[1] if len(argv) > 1 else "check"
    if len(argv) > 2 or command not in ("check", "list", "json"):
        print(__doc__.strip(), file=sys.stderr)
        return 2

    docs, errors = read_manifest()
    if not errors:
        errors = check_tree(docs)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if command == "check":
        paths = ", ".join(f"docs/{d['dir']}/{d['name']}.tex" for d in docs)
        print(f"{len(docs)} document(s) OK: {paths}")
    elif command == "list":
        for doc in docs:
            print(f"{doc['dir']}/{doc['name']}")
    else:
        print(json.dumps(docs, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
