# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Running Scripts

```bash
python src/main.py              # NumPy/pandas/JSON demos
python src/sklearn_demo.py      # Scikit-learn classification demo
python src/reconcile_cs_dynamodb.py  # Compare CS vs DynamoDB datasets
python src/merge_dynamodb_json.py    # Merge DynamoDB JSON exports
```

## Architecture

This is a collection of standalone Python scripts for data analysis and library experimentation — not a unified application. Each script in `src/` runs independently.

- `input/` — CSV and JSON data files (gitignored)
- `output/` — Generated results (gitignored)
- `.env/` — Local virtualenv (gitignored)

Key libraries: numpy, pandas, matplotlib, scikit-learn.

Scripts use relative paths (`./input/`, `./output/`), so run from the project root.
