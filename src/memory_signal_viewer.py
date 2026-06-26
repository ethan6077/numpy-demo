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
import sys
import textwrap
from collections import OrderedDict

DEFAULT_CSV = "./input/dda_memory_signals_20260626.csv"

# pandas stores long CSV cells; raise the field-size limit so the big
# `attributes` JSON column never trips csv's default cap.
csv.field_size_limit(10 * 1024 * 1024)


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


def format_signals(signals):
    """Render the signals object as an indented key/value block."""
    if not signals:
        return "  (none)"
    lines = []
    width = max(len(str(k)) for k in signals)
    for key, value in signals.items():
        lines.append(f"  {str(key).ljust(width)} : {_format_value(value)}")
    return "\n".join(lines)


def _format_value(value):
    """Compactly render a single signal value (dicts/lists inline)."""
    if isinstance(value, dict):
        return ", ".join(f"{k}={_format_value(v)}" for k, v in value.items())
    if isinstance(value, list):
        return "[" + ", ".join(str(v) for v in value) + "]"
    return str(value)


def format_record(record, index, total):
    """Render a full record: header, signals panel, then raw message."""
    owner = record["owner_id"]
    header = (
        f"─── Owner {owner}  ·  record {index + 1}/{total}  ·  "
        f"{record['timestamp']} ───"
    )
    return "\n".join([
        header,
        "== SIGNALS ==",
        format_signals(record["signals"]),
        "== RAW MESSAGE ==",
        textwrap.indent(record["content"], "  "),
    ])


def select_owner(groups):
    """Show the owner menu and return the chosen owner_id, or None to quit."""
    owners = list(groups.keys())
    while True:
        print("\nData owners:")
        for i, owner in enumerate(owners):
            count = len(groups[owner])
            label = "record" if count == 1 else "records"
            print(f"  [{i + 1}] {owner}  ({count} {label})")
        try:
            choice = input("\nPick an owner number (q to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            return None

        if choice.lower() in ("q", "quit"):
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(owners):
            return owners[int(choice) - 1]
        print("Invalid choice, try again.")


def page_records(owner_id, records):
    """Page through one owner's records. Returns 'menu' or 'quit'."""
    total = len(records)
    index = 0
    while True:
        print("\n" + format_record(records[index], index, total))
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
    path = argv[0] if argv else DEFAULT_CSV

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
        owner_id = select_owner(groups)
        if owner_id is None:
            print("Bye.")
            return 0
        if page_records(owner_id, groups[owner_id]) == "quit":
            print("Bye.")
            return 0


if __name__ == "__main__":
    sys.exit(main())
