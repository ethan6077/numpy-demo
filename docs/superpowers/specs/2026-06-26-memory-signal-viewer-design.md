# Memory Signal Viewer — Design

**Date:** 2026-06-26
**File:** `src/memory_signal_viewer.py`
**Data:** `input/dda_memory_signals_20260626.csv`

## Purpose

A standalone interactive terminal script to browse AI memory signal records. The
operator picks a data owner, then pages through that owner's records one at a
time (oldest-first), viewing the parsed `signals` and the raw conversation
`raw_message` for each.

## Data Source

`input/dda_memory_signals_20260626.csv` — 727 data rows. Relevant columns:

- `data_owner_id` — the grouping key (a UUID).
- `attributes` — a JSON blob. Two nested parts of interest:
  - `signals` (optional) — structured prefs: `location_preference`,
    `buy_price_range` / `rent_price_range`, `property_intent_type`, etc.
  - `raw_message` — `{ "content": "<User/Agent conversation>", "timestamp": "<ISO8601>" }`.
- `event_time` — fallback timestamp if `raw_message.timestamp` is missing.
- `id` — record id, shown in the header.

Some rows have only `raw_message` and no `signals`.

## Flow

1. **Load & parse** — read CSV with pandas. For each row, parse `attributes`
   JSON and normalize to `{owner_id, timestamp, signals, content, raw_id}`.
2. **Group by owner** — group records by `data_owner_id`; sort each owner's
   records by `timestamp` **oldest-first** (`raw_message.timestamp`, falling back
   to `event_time`).
3. **Owner selection menu** — numbered list of every `data_owner_id` with record
   count, e.g. `[3] 0186bb3c…  (2 records)`. Operator types a number.
4. **Pager** — step through the chosen owner's records one at a time.

## Display Format

Signals panel on top, full-width raw_message below (stacked, not columns, because
`raw_message.content` is long multi-paragraph markdown).

```
─── Owner 0186bb3c…  ·  record 2/3  ·  2026-06-25T23:51:31 ───
== SIGNALS ==
  property_intent_type : buyer
  location_preference  : suburbs=[Cherrybrook]
  buy_price_range      : max=850000
== RAW MESSAGE ==
  User: What's driving my realEstimate?
  Agent: Your realEstimate for 70 Shepherds Drive...
```

If `signals` is absent → `== SIGNALS ==  (none)`.

## Pager Controls

- `Enter` / `n` → next record
- `p` → previous record
- `o` → back to owner menu
- `q` → quit

## Components

Small, focused functions:

- `load_records(path)` → list of normalized dicts `{owner_id, timestamp, signals, content, raw_id}`.
- `group_by_owner(records)` → ordered mapping `owner_id → [records sorted oldest-first]`.
- `format_signals(signals)` → display string for the signals panel.
- `format_record(record, index, total)` → full display string for one record.
- `select_owner(groups)` → interactive owner-menu loop; returns chosen owner_id or None.
- `page_records(owner_id, records)` → pager loop.
- `main()` → wires it together.

## Error Handling

- Rows with unparseable `attributes` JSON → warn to stderr, skip the row, continue.
- Empty CSV → print a message and exit cleanly.
- EOF / Ctrl-C / Ctrl-D at any prompt → exit gracefully (no traceback).

## Dependencies

No new dependencies. `pandas` is already in the project; otherwise stdlib only
(`json`, `textwrap`, `sys`).
