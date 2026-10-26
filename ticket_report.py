"""Summarise a CSV export of support tickets.

Expected columns: id, category, priority, status, opened, closed
Dates use the format YYYY-MM-DD HH:MM. `closed` is empty while a ticket is open.

    python ticket_report.py sample_data/tickets.csv
"""
import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M"


def load(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def hours_to_close(row):
    if not row["closed"]:
        return None
    opened = datetime.strptime(row["opened"], DATE_FORMAT)
    closed = datetime.strptime(row["closed"], DATE_FORMAT)
    return (closed - opened).total_seconds() / 3600


def summarise(rows):
    by_status = Counter(r["status"] for r in rows)
    by_category = Counter(r["category"] for r in rows)
    by_priority = Counter(r["priority"] for r in rows)

    durations = defaultdict(list)
    for row in rows:
        hours = hours_to_close(row)
        if hours is not None:
            durations[row["category"]].append(hours)

    average_hours = {category: round(sum(values) / len(values), 1) for category, values in durations.items()}
    all_hours = [h for values in durations.values() for h in values]
    return {
        "total": len(rows),
        "by_status": dict(by_status),
        "by_category": dict(by_category),
        "by_priority": dict(by_priority),
        "average_hours_by_category": average_hours,
        "average_hours_overall": round(sum(all_hours) / len(all_hours), 1) if all_hours else None,
        "open": [r["id"] for r in rows if not r["closed"]],
    }


def render(summary):
    lines = [f"Tickets: {summary['total']}", ""]
    for title, key in (("By status", "by_status"), ("By category", "by_category"), ("By priority", "by_priority")):
        lines.append(title)
        for name, count in sorted(summary[key].items(), key=lambda item: -item[1]):
            lines.append(f"  {name:<14} {count}")
        lines.append("")
    lines.append("Average time to close (hours)")
    for category, hours in sorted(summary["average_hours_by_category"].items()):
        lines.append(f"  {category:<14} {hours}")
    if summary["average_hours_overall"] is not None:
        lines.append(f"  {'overall':<14} {summary['average_hours_overall']}")
    lines += ["", "Still open: " + (", ".join(summary["open"]) or "none")]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv_file")
    args = parser.parse_args()
    print(render(summarise(load(args.csv_file))))


if __name__ == "__main__":
    main()
