#!/usr/bin/env python3
"""Report LF-normalized character counts for the GRA editions.

Per PRD GRA-PRD-v9.0.0-2026-06-10 section 7.1 measurement spec: sizes are
characters after LF normalization (CRLF counted as one). Reports the agent
behavioral body (between the v9 body markers in skills/gra/SKILL.md, with and
without the v9 marker comments), the full SKILL.md, and the generated chat
artifact. Eliminates byte/character confusion (Codex review, 2026-06-10).
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "gra" / "SKILL.md"
CHAT = REPO / "research" / "research-assistant-v9.0.0-chat.md"

BODY_RE = re.compile(r"<!-- v9:body:start -->(.*?)<!-- v9:body:end -->", re.DOTALL)
MARKER_RE = re.compile(r"[ \t]*<!-- v9:[^>]*-->\n?")


def lf(text: str) -> str:
    return text.replace("\r\n", "\n")


def report(label: str, text: str) -> None:
    print(f"{label}: {len(text)} chars (LF), {len(text.encode('utf-8'))} UTF-8 bytes")


def main() -> None:
    skill = lf(SKILL.read_text(encoding="utf-8"))
    report("SKILL.md (full file)", skill)
    match = BODY_RE.search(skill)
    if match:
        body = match.group(1).strip()
        report("agent body (with v9 markers)", body)
        report("agent body (markers stripped)", MARKER_RE.sub("", body))
        agent_total = len(MARKER_RE.sub("", body))
        ceiling = "inside" if agent_total <= 11264 else "OVER"
        print(f"  -> agent soft ceiling (~10-11 KB): {ceiling}")
    else:
        print("agent body: v9 body markers NOT FOUND")
    if CHAT.exists():
        chat = lf(CHAT.read_text(encoding="utf-8"))
        report("chat artifact", chat)
        print(f"  -> chat hard gate (<8,000 chars): "
              f"{'PASS' if len(chat) < 8000 else 'FAIL'}")
    else:
        print("chat artifact: not yet generated")


if __name__ == "__main__":
    main()
