#!/usr/bin/env python3
"""Report LF-normalized character counts for the GRA editions.

Per PRD GRA-PRD-v9.0.0-2026-06-10 section 7.1 measurement spec: sizes are
characters after LF normalization (CRLF counted as one). Reports the agent
behavioral body (between the v9 body markers in skills/gra/SKILL.md, with and
without the v9 marker comments), the full SKILL.md, and the generated chat
artifact. Eliminates byte/character confusion (Codex review, 2026-06-10).
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "gra" / "SKILL.md"
CHAT = REPO / "research" / "research-assistant-v9.2.0-chat.md"
CHAT_CHAR_LIMIT = 8000

BODY_RE = re.compile(r"<!-- v9:body:start -->(.*?)<!-- v9:body:end -->", re.DOTALL)
MARKER_RE = re.compile(r"[ \t]*<!-- v9:[^>]*-->\n?")


def lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def report(label: str, text: str) -> None:
    print(f"{label}: {len(text)} chars (LF), {len(text.encode('utf-8'))} UTF-8 bytes")


class ChatSizeError(ValueError):
    """Raised when the shipped chat body fails its hard size gate."""


def load_valid_chat(path: Path = CHAT) -> str:
    """Load a present, nonempty chat artifact below 8,000 characters."""
    if not path.is_file():
        raise ChatSizeError(f"chat artifact is missing: {path}")
    chat = lf(path.read_text(encoding="utf-8"))
    if not chat.strip():
        raise ChatSizeError(f"chat artifact is empty: {path}")
    if len(chat) >= CHAT_CHAR_LIMIT:
        raise ChatSizeError(
            f"chat artifact is {len(chat)} characters; hard gate is "
            f"<{CHAT_CHAR_LIMIT}"
        )
    return chat


def main() -> int:
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
        return 1

    try:
        chat = load_valid_chat(CHAT)
    except ChatSizeError as error:
        print(f"chat hard gate: FAIL ({error})")
        return 1

    report("chat artifact", chat)
    print("  -> chat hard gate (<8,000 chars): PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
