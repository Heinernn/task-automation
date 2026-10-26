# Task automation (Python)

Two small command line tools I wrote to automate chores I run into in IT support work. They use only the Python
standard library.

## organizer.py

Sorts the files of a folder into sub-folders (images, documents, spreadsheets, archives, installers, code, other).

- Dry run by default: it prints what it would move and changes nothing.
- `--apply` moves the files for real.
- If a file with the same name already exists in the destination, it keeps both (`report.pdf`, `report (1).pdf`).
- Hidden files and existing folders are ignored.

```bash
python organizer.py ~/Downloads            # preview
python organizer.py ~/Downloads --apply    # do it
```

## ticket_report.py

Reads a CSV export of support tickets and prints a summary: tickets by status, category and priority, the average
time to close for each category, and which tickets are still open.

```bash
python ticket_report.py sample_data/tickets.csv
```

Expected columns: `id, category, priority, status, opened, closed` (dates as `YYYY-MM-DD HH:MM`).
The sample file contains made-up tickets.

## Tests

```bash
pip install pytest
pytest
```

## Possible next steps

- Export the report to HTML or CSV.
- Let the organizer read its categories from a JSON file.
