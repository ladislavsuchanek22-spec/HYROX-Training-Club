"""Stáhne rozvrh HYROX lekcí z rezervačního systému Form Factory (eFitness) a uloží _build/timetable.json.

Spouští ho GitHub Action každý den (.github/workflows/timetable.yml), pak se web přegeneruje.
Bere jen lekce HYROX®️ (program HYROX365) a HYROX®️ Experience, ne LM CEREMONY HYROX.
Ručně: python3 _build/timetable.py
"""
import datetime as dt
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

CLUBS = {
    "prague5": "https://naknizeci.formfactory.cz/calendar",
    "prague3": "https://vinohradska.formfactory.cz/calendar",
    "brno": "https://campusbrno.formfactory.cz/calendar",
    "ostrava": "https://hrabova.formfactory.cz/calendar",
}
DAYS = 7
OUT = Path(__file__).with_name("timetable.json")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (HYROX Training Club timetable sync; hyroxtrainingclub.cz)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse_week(page):
    """Vrátí [(date, start, end, name)] z týdenního pohledu kalendáře."""
    table = re.search(r'<table class="calendar_table[^"]*">(.*?)</table>', page, re.S)
    if not table:
        raise ValueError("calendar table not found")
    t = table.group(1)
    dates = re.findall(r'meta:date="(\d\d)\.(\d\d)\.(\d{4})"', t)
    body = t.split("</thead>", 1)[1] if "</thead>" in t else t
    cells = re.findall(r"<td[^>]*>(.*?)</td>", body, re.S)
    out = []
    for (d, m, y), cell in zip(dates, cells):
        day = dt.date(int(y), int(m), int(d))
        for ev in re.findall(r'<div class="event".*?</div>', cell, re.S):
            tm = re.search(r'class="eventlength">\s*(\d\d:\d\d)-(\d\d:\d\d)', ev)
            nm = re.search(r'class="event_name">(.*?)</p>', ev, re.S)
            if tm and nm:
                out.append((day, tm.group(1), tm.group(2), html.unescape(nm.group(1)).strip()))
    return out


def is_htc(name):
    n = name.upper()
    return n.startswith("HYROX") and "CEREMONY" not in n


def main():
    today = dt.date.today()
    end = today + dt.timedelta(days=DAYS - 1)
    data = {"updated": today.isoformat(), "from": today.isoformat(), "to": end.isoformat(), "clubs": {}}
    old = {}
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8")).get("clubs", {})
    for key, url in CLUBS.items():
        events = []
        try:
            for start in (today, today + dt.timedelta(days=7)):
                page = fetch(f"{url}?day={start.strftime('%d.%m.%Y')}")
                events += parse_week(page)
        except Exception as e:  # jeden klub nesmí shodit ostatní
            print(f"::warning::{key}: {type(e).__name__}: {e}")
            data["clubs"][key] = [r for r in old.get(key, []) if r["date"] >= today.isoformat()]
            continue
        seen, rows = set(), []
        for day, a, b, name in sorted(events):
            if today <= day <= end and is_htc(name) and (day, a, name) not in seen:
                seen.add((day, a, name))
                rows.append({"date": day.isoformat(), "start": a, "end": b, "name": name})
        data["clubs"][key] = rows
        print(key, len(rows), "lekcí")
    if sum(len(v) for v in data["clubs"].values()) == 0:
        print("::error::žádné lekce – rozvrh nepřepisuju")
        sys.exit(1)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
