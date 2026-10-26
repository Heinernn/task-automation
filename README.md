# Task Automation

Two command line tools in Python for chores that come up constantly in IT support work. Both use only the standard
library, so they run on any machine with Python 3 and nothing to install.

| Tool | Purpose |
|------|---------|
| `organizer.py` | Sorts the files in a folder into category sub-folders, safely |
| `ticket_report.py` | Summarizes a CSV export of support tickets |

## organizer.py

Sorts a folder into sub-folders by file type: images, documents, spreadsheets, archives, installers, code and other.

- **Preview by default.** It prints what it would move and changes nothing.
- **`--apply`** performs the move.
- **Never overwrites.** If the destination already has a file with the same name, both are kept
  (`report.pdf`, `report (1).pdf`).
- Hidden files and existing folders are ignored.

```bash
python organizer.py ~/Downloads            # preview
python organizer.py ~/Downloads --apply    # move the files
```

## ticket_report.py

Reads a CSV export of support tickets and prints tickets by status, category and priority, the average time to close
per category, and the tickets that are still open.

```bash
python ticket_report.py sample_data/tickets.csv
```

Example output:

```
Tickets: 10

By status
  closed         8
  open           2

Average time to close (hours)
  hardware       22.8
  network        3.9
  password       0.4
  software       7.4
  overall        6.7

Still open: T-1005, T-1008
```

Expected columns: `id, category, priority, status, opened, closed`, with dates formatted as `YYYY-MM-DD HH:MM`.
The sample file contains fictional tickets.

## Tests

```bash
pip install pytest
pytest
```

## Possible next steps

- Export the report as HTML or CSV.
- Load the organizer's categories from a JSON configuration file.
