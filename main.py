#!/usr/bin/env python3
"""r19 pickup-line courier: validate repo entry, ship to the output dir."""
import json
import os

CAP = 200
TAG = "pickup-1125"
NOTE = "r19 courier pass"


class Courier:
    def __init__(self, ceiling):
        self.ceiling = ceiling
        self.log = []

    def fetch(self):
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, "entry.txt"), encoding="utf-8") as stream:
            return stream.read().replace("\r", "").strip()

    def guard(self, line):
        if not line or not line.strip():
            raise ValueError("empty")
        if len(line) > self.ceiling:
            raise ValueError("over cap: %d/%d" % (len(line), self.ceiling))
        self.log.append("guard ok")

    def deliver(self, line):
        out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        os.makedirs(out, exist_ok=True)
        path = os.path.join(out, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(line)
        with open(path, encoding="utf-8") as stream:
            if stream.read() != line:
                raise ValueError("re-read differs")
        return path


def main():
    box = Courier(CAP)
    line = box.fetch()
    box.guard(line)
    where = box.deliver(line)
    print(json.dumps({"tag": TAG, "note": NOTE, "path": where,
                      "chars": len(line), "steps": box.log}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
