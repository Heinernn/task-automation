import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import organizer
import ticket_report


def test_category_for():
    assert organizer.category_for(Path("photo.JPG")) == "images"
    assert organizer.category_for(Path("cv.pdf")) == "documents"
    assert organizer.category_for(Path("setup.exe")) == "installers"
    assert organizer.category_for(Path("notes.unknown")) == "other"


def test_dry_run_does_not_move_files(tmp_path):
    (tmp_path / "a.pdf").write_text("x")
    organizer.organize(tmp_path, apply=False)
    assert (tmp_path / "a.pdf").exists()
    assert not (tmp_path / "documents").exists()


def test_apply_moves_files_and_keeps_duplicates(tmp_path):
    (tmp_path / "a.pdf").write_text("one")
    (tmp_path / "documents").mkdir()
    (tmp_path / "documents" / "a.pdf").write_text("already here")
    organizer.organize(tmp_path, apply=True)
    assert (tmp_path / "documents" / "a.pdf").read_text() == "already here"
    assert (tmp_path / "documents" / "a (1).pdf").read_text() == "one"
    assert not (tmp_path / "a.pdf").exists()


def test_hidden_files_and_folders_are_ignored(tmp_path):
    (tmp_path / ".hidden.txt").write_text("x")
    (tmp_path / "folder").mkdir()
    assert organizer.plan(tmp_path) == []


def test_ticket_summary():
    rows = ticket_report.load(Path(__file__).resolve().parents[1] / "sample_data" / "tickets.csv")
    summary = ticket_report.summarise(rows)
    assert summary["total"] == 10
    assert summary["by_status"] == {"closed": 8, "open": 2}
    assert summary["open"] == ["T-1005", "T-1008"]
    assert summary["average_hours_by_category"]["password"] == 0.4
    # network tickets closed: 4.5 h and 3.25 h -> 3.875 h
    assert summary["average_hours_by_category"]["network"] == 3.9


def test_hours_to_close_handles_open_tickets():
    assert ticket_report.hours_to_close({"opened": "2026-03-02 08:00", "closed": ""}) is None
    assert ticket_report.hours_to_close({"opened": "2026-03-02 08:00", "closed": "2026-03-02 09:30"}) == 1.5
