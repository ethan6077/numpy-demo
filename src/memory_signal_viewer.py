"""Interactive terminal viewer for AI memory signal records.

Loads `input/dda_memory_signals_20260626.csv`, groups records by
`data_owner_id`, and lets you page through one owner's records at a time
(oldest-first). Each record shows the parsed `signals` panel on top and the
raw conversation `raw_message` below.

Usage:
    python src/memory_signal_viewer.py [path-to-csv]

Defaults to ./input/dda_memory_signals_20260626.csv when no path is given.
Run from the project root so the relative path resolves.
"""

import csv
import json
import os
import sys
import textwrap
from collections import OrderedDict

DEFAULT_CSV = "./input/dda_memory_signals_20260626.csv"

# pandas stores long CSV cells; raise the field-size limit so the big
# `attributes` JSON column never trips csv's default cap.
csv.field_size_limit(10 * 1024 * 1024)


def color_enabled(stream, env, force_no_color=False):
    """Decide whether ANSI color should be used for `stream`.

    Off when `--no-color` is passed, when the NO_COLOR env var is present
    (https://no-color.org), or when the stream is not an interactive TTY.
    """
    if force_no_color:
        return False
    if env.get("NO_COLOR"):
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


class Palette:
    """Wraps text in ANSI codes when enabled; a no-op pass-through otherwise."""

    # role -> SGR code(s)
    _CODES = {
        "header": "1;36",   # bold cyan
        "section": "1;33",  # bold yellow
        "key": "36",        # cyan
        "value": "32",      # green
        "user": "1;35",     # bold magenta
        "agent": "1;34",    # bold blue
        "dim": "2",         # faint
    }

    def __init__(self, enabled):
        self.enabled = enabled

    def _wrap(self, text, role):
        if not self.enabled:
            return text
        return f"\033[{self._CODES[role]}m{text}\033[0m"

    def header(self, text):
        return self._wrap(text, "header")

    def section(self, text):
        return self._wrap(text, "section")

    def key(self, text):
        return self._wrap(text, "key")

    def value(self, text):
        return self._wrap(text, "value")

    def user(self, text):
        return self._wrap(text, "user")

    def agent(self, text):
        return self._wrap(text, "agent")

    def dim(self, text):
        return self._wrap(text, "dim")


def load_records(path):
    """Read the CSV and return a list of normalized record dicts.

    Each record is {owner_id, timestamp, signals, content, raw_id}. Rows whose
    `attributes` column is not valid JSON are skipped with a warning to stderr.
    """
    records = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_attributes = row.get("attributes", "")
            try:
                attributes = json.loads(raw_attributes)
            except (ValueError, TypeError):
                print(
                    f"warning: skipping row id={row.get('id')!r} "
                    "with unparseable attributes",
                    file=sys.stderr,
                )
                continue

            raw_message = attributes.get("raw_message") or {}
            timestamp = raw_message.get("timestamp") or row.get("event_time", "")

            records.append({
                "owner_id": row.get("data_owner_id", ""),
                "timestamp": timestamp,
                "signals": attributes.get("signals"),
                "content": raw_message.get("content", ""),
                "raw_id": row.get("id", ""),
            })
    return records


def group_by_owner(records):
    """Group records by owner_id, each group sorted oldest-first by timestamp.

    Returns an OrderedDict keyed by owner_id (owners in first-seen order).
    """
    groups = OrderedDict()
    for rec in records:
        groups.setdefault(rec["owner_id"], []).append(rec)
    for owner_records in groups.values():
        owner_records.sort(key=lambda r: r["timestamp"])
    return groups


def top_owners(groups, limit=10):
    """Return owner_ids ranked by record count (desc), capped at `limit`.

    Ties are broken by owner_id so the order is deterministic.
    """
    ranked = sorted(groups, key=lambda owner: (-len(groups[owner]), owner))
    return ranked[:limit]


def resolve_owner_choice(choice, displayed, valid_owners):
    """Map a menu input to an owner_id, or None if it matches nothing.

    A number picks from the `displayed` shortlist (1-based); otherwise the
    input is treated as a full owner_id and accepted if it's in `valid_owners`.
    """
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(displayed):
            return displayed[idx - 1]
        return None
    if choice in valid_owners:
        return choice
    return None


def format_signals(signals, paint=None):
    """Render the signals object as an indented key/value block."""
    paint = paint or Palette(enabled=False)
    if not signals:
        return paint.dim("  (none)")
    lines = []
    width = max(len(str(k)) for k in signals)
    for key, value in signals.items():
        label = paint.key(str(key).ljust(width))
        lines.append(f"  {label} : {paint.value(_format_value(value))}")
    return "\n".join(lines)


def _format_value(value):
    """Compactly render a single signal value (dicts/lists inline)."""
    if isinstance(value, dict):
        return ", ".join(f"{k}={_format_value(v)}" for k, v in value.items())
    if isinstance(value, list):
        return "[" + ", ".join(str(v) for v in value) + "]"
    return str(value)


def format_record(record, index, total, paint=None):
    """Render a full record: header, signals panel, then raw message."""
    paint = paint or Palette(enabled=False)
    owner = record["owner_id"]
    header = (
        f"─── Owner {owner}  ·  record {index + 1}/{total}  ·  "
        f"{record['timestamp']} ───"
    )
    return "\n".join([
        paint.header(header),
        paint.section("== SIGNALS =="),
        format_signals(record["signals"], paint),
        paint.section("== RAW MESSAGE =="),
        _format_content(record["content"], paint),
    ])


def _format_content(content, paint):
    """Indent the conversation and tint User:/Agent: turn lines."""
    lines = []
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("User:"):
            lines.append("  " + paint.user(line))
        elif stripped.startswith("Agent:"):
            lines.append("  " + paint.agent(line))
        else:
            lines.append("  " + line)
    return "\n".join(lines)


def select_owner(groups, paint=None, limit=10):
    """Show the owner menu and return the chosen owner_id, or None to quit.

    Shows only the top `limit` owners (by record count) to keep the list short;
    any other owner is reachable by typing its full owner_id.
    """
    paint = paint or Palette(enabled=False)
    total = len(groups)
    displayed = top_owners(groups, limit)
    while True:
        shown = min(limit, total)
        print("\n" + paint.section(f"Top {shown} of {total} data owners:"))
        for i, owner in enumerate(displayed):
            count = len(groups[owner])
            label = "record" if count == 1 else "records"
            num = paint.key(f"[{i + 1}]")
            print(f"  {num} {owner}  {paint.dim(f'({count} {label})')}")
        if total > shown:
            print(paint.dim(f"  …and {total - shown} more — type a full owner_id to open one."))
        try:
            choice = input("\nPick a number or owner_id (q to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            return None

        if choice.lower() in ("q", "quit"):
            return None
        owner_id = resolve_owner_choice(choice, displayed, groups.keys())
        if owner_id is not None:
            return owner_id
        print("Invalid choice, try again.")


def page_records(owner_id, records, paint=None):
    """Page through one owner's records. Returns 'menu' or 'quit'."""
    paint = paint or Palette(enabled=False)
    total = len(records)
    index = 0
    while True:
        print("\n" + format_record(records[index], index, total, paint))
        try:
            cmd = input(
                "\n[Enter/n]ext  [p]rev  [o]wner menu  [q]uit: "
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "quit"

        if cmd in ("", "n", "next"):
            if index + 1 < total:
                index += 1
            else:
                print("(last record for this owner)")
        elif cmd in ("p", "prev"):
            if index > 0:
                index -= 1
            else:
                print("(first record for this owner)")
        elif cmd in ("o", "owner"):
            return "menu"
        elif cmd in ("q", "quit"):
            return "quit"
        else:
            print("Unknown command.")


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    force_no_color = "--no-color" in argv
    positional = [a for a in argv if not a.startswith("-")]
    path = positional[0] if positional else DEFAULT_CSV

    paint = Palette(color_enabled(sys.stdout, os.environ, force_no_color))

    try:
        records = load_records(path)
    except FileNotFoundError:
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1

    if not records:
        print("No records found.")
        return 0

    groups = group_by_owner(records)
    print(f"Loaded {len(records)} records across {len(groups)} owners.")

    while True:
        owner_id = select_owner(groups, paint)
        if owner_id is None:
            print("Bye.")
            return 0
        if page_records(owner_id, groups[owner_id], paint) == "quit":
            print("Bye.")
            return 0


if __name__ == "__main__":
    sys.exit(main())
