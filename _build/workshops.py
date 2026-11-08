"""Kurzy a workshopy FF Academy (HYROX) na hlavní stránce, ve všech jazycích.

Formát karet kopíruje ff-academy.cz/label/hyrox: štítky (typ, cílovka, město), datum, délka, cena, název.
Nový termín = nová položka v EVENTS. Po datu konání se z webu sám schová (web se builduje denně).
Zdroj dat: https://www.ff-academy.cz/label/hyrox/ (stav 8. 11. 2026).
"""
import datetime
import json

import raceprep

KNIZECI = dict(place="Form Factory Na Knížecí", address="Ostrovského 464/6, 150 00 Praha 5",
               street="Ostrovského 464/6", zip="150 00", city="Praha 5")
VINOHRADSKA = dict(place="Form Factory Vinohradská", address="Vinohradská 190, 130 00 Praha 3",
                   street="Vinohradská 190", zip="130 00", city="Praha 3")

RIA = "Ria Suchánek Hrušovská, MSc."
LADA = "Ladislav Suchánek"
KLEINER = "Ing. Robert Kleiner, MBA"

_L1_T = {
    "cs": dict(sub="Základní workshop",
               txt="Jednodenní praktický workshop pro trenéry a instruktory, kteří chtějí vést HYROX lekce se strukturou a energií. Reálný trénink, technika, programming a nakonec si sám odvedeš část lekce.",
               li=["Struktura HYROX lekce a základy programmingu", "Technika stanovišť a coaching skupiny", "Při spolupráci s FF HYROX Foundation course zdarma"]),
    "en": dict(sub="Foundation workshop",
               txt="A one-day, hands-on workshop for coaches and instructors who want to run HYROX classes with structure and energy. Real training, technique, programming, and at the end you coach part of the session yourself.",
               li=["HYROX class structure and programming basics", "Station technique and group coaching", "Free HYROX Foundation course if you go on to coach at FF"]),
    "de": dict(sub="Grundlagen-Workshop",
               txt="Eintägiger Praxis-Workshop für Trainer und Instruktoren, die HYROX-Kurse mit Struktur und Energie leiten wollen. Echtes Training, Technik, Programming, und am Ende leitest du selbst einen Teil der Einheit.",
               li=["Aufbau einer HYROX-Einheit und Programming-Grundlagen", "Stationstechnik und Gruppen-Coaching", "Bei Zusammenarbeit mit FF: HYROX Foundation Course gratis"]),
    "pl": dict(sub="Warsztat podstawowy",
               txt="Jednodniowy praktyczny warsztat dla trenerów i instruktorów, którzy chcą prowadzić zajęcia HYROX ze strukturą i energią. Prawdziwy trening, technika, programming, a na koniec sam poprowadzisz część zajęć.",
               li=["Struktura zajęć HYROX i podstawy programmingu", "Technika stacji i prowadzenie grupy", "Przy współpracy z FF kurs HYROX Foundation gratis"]),
}

EVENTS = [
    dict(
        id="hyrox-level-1", kind="workshop", aud=["instr", "pt"],
        date="2026-11-28", start="09:00", end="17:00", hours=8,
        price=4990, capacity=20, img="/img/group.webp", loc=KNIZECI, lectors=[RIA],
        buy="https://ucet.ff-academy.cz/calendar?view=Preview&schiid=37753180",
        info="https://www.ff-academy.cz/workshop/hyrox-level-1-zakladni-workshop-praha-5/",
        title="HYROX Level 1", t=_L1_T,
    ),
    dict(
        id="mental-game", kind="workshop", aud=["public"],
        date="2026-11-29", start="10:00", end="12:00", hours=2,
        price=1299, capacity=40, img="/img/ria-mic.webp", loc=KNIZECI, lectors=[RIA],
        buy="https://ucet.ff-academy.cz/calendar?dayOnline&schiid=37778857&view=Preview",
        info="https://www.ff-academy.cz/instruktor/mental-game/",
        title="Mental Game",
        t={
            "cs": dict(sub="Hlava pod tlakem",
                       txt="Dvouhodinový workshop, který začíná 30minutovým HYROX workoutem. Nejde o čas, ale o to, co se ti děje v hlavě, když už nemůžeš. Pak to rozebereme a přeneseme do práce i života.",
                       li=["30 minut HYROX workoutu", "Vnitřní dialog, pozornost, emoce pod tlakem", "Vlastní mental game plan do sportu i života"]),
            "en": dict(sub="Your head under pressure",
                       txt="A two-hour workshop that starts with a 30-minute HYROX workout. It's not about your time, but about what goes on in your head when you want to stop. Then we unpack it and carry it over to work and life.",
                       li=["30-minute HYROX workout", "Inner voice, focus and emotions under pressure", "Your own mental game plan for sport and life"]),
            "de": dict(sub="Der Kopf unter Druck",
                       txt="Zweistündiger Workshop, der mit einem 30-minütigen HYROX-Workout beginnt. Es geht nicht um die Zeit, sondern darum, was in deinem Kopf passiert, wenn du nicht mehr kannst. Danach übertragen wir es auf Job und Alltag.",
                       li=["30 Minuten HYROX-Workout", "Innerer Dialog, Fokus und Emotionen unter Druck", "Dein eigener Mental-Game-Plan für Sport und Leben"]),
            "pl": dict(sub="Głowa pod presją",
                       txt="Dwugodzinny warsztat, który zaczyna się 30-minutowym workoutem HYROX. Nie chodzi o czas, tylko o to, co dzieje się w twojej głowie, kiedy masz dość. Potem przenosimy to do pracy i życia.",
                       li=["30 minut workoutu HYROX", "Wewnętrzny dialog, uwaga i emocje pod presją", "Własny mental game plan do sportu i życia"]),
        },
    ),
    dict(
        id="hyrox-level-1-leden", kind="workshop", aud=["instr", "pt"],
        date="2027-01-16", start="09:00", end="17:00", hours=8,
        price=4990, capacity=20, img="/img/group.webp", loc=KNIZECI, lectors=[RIA],
        buy="https://ucet.ff-academy.cz/calendar?view=Preview&schiid=37799446",
        info="https://www.ff-academy.cz/workshop/hyrox-level-1-zakladni-workshop-praha-7/",
        title="HYROX Level 1", t=_L1_T,
    ),
    dict(
        id="12-weeks-race-prep", kind="course", aud=["public", "instr", "pt"],
        date="2027-01-17", start="", end="", hours=110, self_paced=True,
        price=8990, capacity=50, img="/img/coaches.webp", loc=KNIZECI, lectors=[LADA, RIA],
        buy="https://ucet.ff-academy.cz/calendar?view=Preview&schiid=37801412",
        info="https://www.ff-academy.cz/kurz/priprav-se-na-hyrox-systematicky/",
        internal="12-weeks-race-prep",
        title="HYROX 12 Weeks Race Prep",
        t={
            "cs": dict(sub="Připrav se na HYROX systematicky",
                       txt="Tříměsíční program pod vedením Rii a Ládi. Každé pondělí plán na celý týden, individuální pace zóny ze vstupního testu, vedené lekce ve Form Factory a 3 společné workshopy.",
                       li=["2 běžecké + 2 silové / HYROX tréninky týdně", "Edukační knihovna a PDF materiály", "Workshopy: vstupní testy, mid-check, výstupní testy"]),
            "en": dict(sub="On FF Academy as „Připrav se na HYROX systematicky“",
                       txt="A three-month programme coached by Ria and Láďa. A plan for the whole week every Monday, individual pace zones from your entry test, coached classes at Form Factory and 3 group workshops.",
                       li=["2 runs + 2 strength / HYROX sessions a week", "Education library and PDF guides", "Workshops: entry tests, mid-check, final tests"]),
            "de": dict(sub="Bei FF Academy als „Připrav se na HYROX systematicky“",
                       txt="Dreimonatiges Programm mit Ria und Láďa. Jeden Montag der Plan für die ganze Woche, individuelle Pace-Zonen aus dem Eingangstest, gecoachte Kurse bei Form Factory und 3 gemeinsame Workshops.",
                       li=["2 Lauf- + 2 Kraft- / HYROX-Einheiten pro Woche", "Wissensbibliothek und PDF-Guides", "Workshops: Eingangstest, Mid-Check, Abschlusstest"]),
            "pl": dict(sub="W FF Academy jako „Připrav se na HYROX systematicky“",
                       txt="Trzymiesięczny program z Rią i Láďą. W każdy poniedziałek plan na cały tydzień, indywidualne strefy tempa z testu wstępnego, zajęcia z trenerem w Form Factory i 3 wspólne warsztaty.",
                       li=["2 biegi + 2 treningi siłowe / HYROX w tygodniu", "Biblioteka wiedzy i przewodniki PDF", "Warsztaty: test wstępny, mid-check, test końcowy"]),
        },
    ),
    dict(
        id="hyrox-technicky", kind="workshop", aud=["instr", "pt"],
        date="2027-01-30", start="11:00", end="15:00", hours=4,
        price=2990, capacity=20, img="/img/sled.webp", loc=KNIZECI, lectors=[RIA],
        buy="https://ucet.ff-academy.cz/calendar?view=Preview&schiid=37799450",
        info="https://www.ff-academy.cz/workshop/hyrox-level-1-zakladni-workshop-praha-6/",
        title="HYROX Technický workshop",
        t={
            "cs": dict(sub="Koučování všech 8 stanic",
                       txt="Naučíš se koučovat HYROX stanice tak, aby lidi na tvých lekcích makali technicky správně, i když už nemůžou. Každou stanici si vyzkoušíš na sobě a hned ji koučuješ na ostatních.",
                       li=["Technika, chyby a krátké cues u všech 8 stanic", "Pravidla sezóny 26/27: no-repy a penalizace", "Skripta, drilly a certifikát o absolvování"]),
            "en": dict(sub="Coaching all 8 stations",
                       txt="Learn to coach the HYROX stations so people in your classes move well even when they're cooked. You try every station yourself and coach it on the others straight away. In Czech.",
                       li=["Technique, common faults and short cues for all 8 stations", "2026/27 rules: no-reps and penalties", "Handouts, drills and a certificate"]),
            "de": dict(sub="Coaching aller 8 Stationen",
                       txt="Du lernst, die HYROX-Stationen so zu coachen, dass deine Leute auch erschöpft technisch sauber arbeiten. Jede Station probierst du selbst und coachst sie sofort bei den anderen. Auf Tschechisch.",
                       li=["Technik, typische Fehler und kurze Cues für alle 8 Stationen", "Regeln 2026/27: No-Reps und Strafen", "Skript, Drills und Teilnahmezertifikat"]),
            "pl": dict(sub="Coaching wszystkich 8 stacji",
                       txt="Nauczysz się coachować stacje HYROX tak, żeby ludzie na twoich zajęciach pracowali technicznie poprawnie, nawet gdy już nie mają sił. Każdą stację testujesz na sobie i od razu coachujesz innych. Po czesku.",
                       li=["Technika, błędy i krótkie cues dla 8 stacji", "Zasady sezonu 2026/27: no-repy i kary", "Skrypty, drille i certyfikat"]),
        },
    ),
    dict(
        id="hyrox-running-masterclass", kind="workshop", aud=["public"],
        date="2027-02-14", start="10:00", end="12:00", hours=2,
        price=999, capacity=30, img="/img/stations.webp", loc=VINOHRADSKA, lectors=[KLEINER],
        buy="https://ucet.ff-academy.cz/calendar?view=Preview&schiid=37810200",
        info="https://www.ff-academy.cz/hyrox/hyrox-running-masterclass-jak-zvladnout-compromised-running-a-podat-optimalni-bezecky-vykon-strategie-treninku-a-bezecke-pripravy-2/",
        title="HYROX Running Masterclass",
        t={
            "cs": dict(sub="Compromised Running pro závodníky",
                       txt="Co se děje s tělem po odchodu ze stanice, proč jsou nohy těžké a jak v únavě pořád běžet. Pacing, rozložení sil a regenerace pro závodníky všech úrovní.",
                       li=["Běh v únavě a technika po silových stanicích", "Pacing, tep, dech a RPE", "Laktát, wattmetry a rychlejší regenerace"]),
            "en": dict(sub="Compromised running for racers",
                       txt="What happens to your body when you leave a station, why your legs feel heavy and how to keep running anyway. Pacing, effort distribution and recovery for racers of every level. In Czech.",
                       li=["Running under fatigue and form after strength stations", "Pacing, heart rate, breathing and RPE", "Lactate, power meters and faster recovery"]),
            "de": dict(sub="Compromised Running für Athleten",
                       txt="Was nach dem Verlassen einer Station im Körper passiert, warum die Beine schwer sind und wie du trotzdem läufst. Pacing, Kräfteeinteilung und Regeneration für alle Leistungsstufen. Auf Tschechisch.",
                       li=["Laufen unter Ermüdung und Technik nach Kraftstationen", "Pacing, Puls, Atmung und RPE", "Laktat, Leistungsmesser und schnellere Regeneration"]),
            "pl": dict(sub="Compromised running dla zawodników",
                       txt="Co dzieje się z ciałem po zejściu ze stacji, dlaczego nogi są ciężkie i jak mimo to biec. Pacing, rozkład sił i regeneracja dla zawodników na każdym poziomie. Po czesku.",
                       li=["Bieg w zmęczeniu i technika po stacjach siłowych", "Pacing, tętno, oddech i RPE", "Mleczan, waty i szybsza regeneracja"]),
        },
    ),
    dict(
        id="hyrox-running-metodika", kind="workshop", aud=["instr", "pt"],
        date="2027-02-14", start="13:00", end="15:00", hours=2,
        price=999, capacity=30, img="/img/test.webp", loc=VINOHRADSKA, lectors=[KLEINER, RIA],
        buy="https://ucet.ff-academy.cz/calendar?view=Preview&schiid=37810201",
        info="https://www.ff-academy.cz/hyrox/hyrox-running-bezecka-metodika-trenink-bezecka-priprava-a-zavodni-strategie-od-subjektivniho-pocitu-po-laktat-a-watty-2/",
        title="HYROX Running & Běžecká metodika",
        t={
            "cs": dict(sub="Od pocitu po laktát a watty",
                       txt="Jak připravit klienty na běh v HYROXu. Řízení tréninku od vnímané intenzity přes laktátovou diagnostiku po watty a běžeckou biomechaniku. Postupy, které použiješ hned.",
                       li=["Compromised Running a přechody ze stanic do běhu", "RPE, laktátoměr a watty (STRYD) pro zóny a pacing", "Hybridní tréninkový plán podle úrovně klienta"]),
            "en": dict(sub="From feel to lactate and watts",
                       txt="How to prepare clients for the running in HYROX. Steering training from perceived effort through lactate testing to power and running biomechanics. Methods you can use right away. In Czech.",
                       li=["Compromised running and station-to-run transitions", "RPE, lactate meter and power (STRYD) for zones and pacing", "Hybrid training plans by client level"]),
            "de": dict(sub="Vom Gefühl zu Laktat und Watt",
                       txt="Wie du Kunden auf das Laufen bei HYROX vorbereitest. Trainingssteuerung vom subjektiven Empfinden über Laktatdiagnostik bis zu Watt und Laufbiomechanik. Methoden, die du sofort nutzt. Auf Tschechisch.",
                       li=["Compromised Running und Übergänge von Station zu Lauf", "RPE, Laktatmessung und Watt (STRYD) für Zonen und Pacing", "Hybrider Trainingsplan je nach Niveau"]),
            "pl": dict(sub="Od odczuć po mleczan i waty",
                       txt="Jak przygotować klientów do biegania w HYROX. Sterowanie treningiem od odczuwanej intensywności przez diagnostykę mleczanu po waty i biomechanikę biegu. Metody do użycia od razu. Po czesku.",
                       li=["Compromised running i przejścia ze stacji do biegu", "RPE, mleczanomierz i waty (STRYD) do stref i pacingu", "Hybrydowy plan treningowy według poziomu klienta"]),
        },
    ),
]

SEC = {
    "cs": dict(eyebrow="Kurzy a workshopy FF Academy", h="HYROX vzdělávání ve Form Factory.",
               lead="Všechny HYROX kurzy a workshopy z FF Academy na jednom místě. Pro trenéry, instruktory i závodníky. Prodej probíhá přes FF Academy.",
               kinds={"course": "Kurz", "workshop": "Workshop"},
               aud={"instr": "Instruktor", "pt": "Osobní trenér", "public": "Veřejnost"},
               city="Praha", hours="h", approx="cca", self_paced="individuálně", start="Start",
               time="Čas", place="Místo", lector="Lektor", lectors="Lektoři", seats="míst", price="Cena",
               buy="Koupit online →", info="Detail na FF Academy", more="Více o programu",
               all="Všechny kurzy a workshopy na FF Academy →", lang_note="",
               days=["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"], cur="Kč", thou=" "),
    "en": dict(eyebrow="FF Academy courses & workshops", h="HYROX education at Form Factory.",
               lead="Every HYROX course and workshop from FF Academy in one place. For coaches, instructors and racers. Tickets are sold through FF Academy.",
               kinds={"course": "Course", "workshop": "Workshop"},
               aud={"instr": "Instructor", "pt": "Personal trainer", "public": "Public"},
               city="Prague", hours="h", approx="approx.", self_paced="self-paced", start="Starts",
               time="Time", place="Venue", lector="Led by", lectors="Led by", seats="places", price="Price",
               buy="Buy online →", info="Details on FF Academy", more="About the programme",
               all="All courses and workshops on FF Academy →", lang_note="Courses are taught in Czech; English on request.",
               days=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], cur="CZK", thou=","),
    "de": dict(eyebrow="Kurse & Workshops der FF Academy", h="HYROX-Ausbildung bei Form Factory.",
               lead="Alle HYROX-Kurse und -Workshops der FF Academy an einem Ort. Für Trainer, Instruktoren und Athleten. Tickets gibt es über die FF Academy.",
               kinds={"course": "Kurs", "workshop": "Workshop"},
               aud={"instr": "Instruktor", "pt": "Personal Trainer", "public": "Öffentlich"},
               city="Prag", hours="Std.", approx="ca.", self_paced="individuell", start="Start",
               time="Zeit", place="Ort", lector="Leitung", lectors="Leitung", seats="Plätze", price="Preis",
               buy="Online kaufen →", info="Details bei FF Academy", more="Mehr zum Programm",
               all="Alle Kurse und Workshops bei FF Academy →", lang_note="Unterricht auf Tschechisch, Englisch nach Absprache.",
               days=["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So."], cur="CZK", thou="."),
    "pl": dict(eyebrow="Kursy i warsztaty FF Academy", h="Edukacja HYROX w Form Factory.",
               lead="Wszystkie kursy i warsztaty HYROX z FF Academy w jednym miejscu. Dla trenerów, instruktorów i zawodników. Sprzedaż odbywa się przez FF Academy.",
               kinds={"course": "Kurs", "workshop": "Warsztat"},
               aud={"instr": "Instruktor", "pt": "Trener personalny", "public": "Dla wszystkich"},
               city="Praga", hours="godz.", approx="ok.", self_paced="we własnym tempie", start="Start",
               time="Godzina", place="Miejsce", lector="Prowadzi", lectors="Prowadzą", seats="miejsc", price="Cena",
               buy="Kup online →", info="Szczegóły w FF Academy", more="O programie",
               all="Wszystkie kursy i warsztaty w FF Academy →", lang_note="Zajęcia po czesku, na życzenie po angielsku.",
               days=["pon.", "wt.", "śr.", "czw.", "pt.", "sob.", "niedz."], cur="CZK", thou=" "),
}

ALL_URL = "https://www.ff-academy.cz/label/hyrox/"

CSS = """<style>
.ws-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.ws{border:1px solid var(--line);background:var(--surface);display:flex;flex-direction:column;min-width:0;border-radius:var(--radius);overflow:hidden}
.ws-img{position:relative;aspect-ratio:16/9;overflow:hidden;background:var(--surface-2)}
.ws-img img{width:100%;height:100%;object-fit:cover}
.ws-date{position:absolute;left:0;bottom:0;background:var(--red);color:#fff;padding:9px 13px;display:grid;gap:2px}
.ws-date b{font:800 28px/1 var(--f-display);font-variant-numeric:tabular-nums}
.ws-date span{font:500 11px/1 var(--f-mono);letter-spacing:.1em;text-transform:uppercase}
.ws-kind{position:absolute;right:10px;top:10px;background:#fff;color:#000;padding:6px 10px;border-radius:999px;font:700 12px/1 var(--f-display);letter-spacing:.08em;text-transform:uppercase}
.ws-kind.course{background:var(--yellow)}
.ws-body{padding:20px;display:grid;gap:11px;flex:1;align-content:start}
.ws-tags{display:flex;flex-wrap:wrap;gap:6px}
.ws-tags span{border:1px solid var(--line);border-radius:999px;padding:5px 9px;font:500 11px/1 var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.ws-meta{display:flex;flex-wrap:wrap;gap:6px 16px;font:600 14px/1.3 var(--f-body);font-variant-numeric:tabular-nums}
.ws-meta span{display:inline-flex;gap:6px;align-items:center}
.ws-meta svg{width:15px;height:15px;flex:none;color:var(--yellow)}
.ws h3{font-size:clamp(26px,2.3vw,32px)}
.ws h3 small{display:block;margin-top:6px;font:600 14px/1.25 var(--f-body);letter-spacing:.06em;color:var(--muted)}
.ws p{color:var(--muted);font-size:15px}
.ws ul{list-style:none;margin:0;padding:0;display:grid;gap:6px;font-size:14px}
.ws li{display:flex;gap:10px;line-height:1.4}
.ws li::before{content:"";flex:0 0 7px;height:7px;margin-top:6px;background:var(--red-hi)}
.ws dl{margin:4px 0 0;display:grid;grid-template-columns:auto 1fr;gap:6px 14px;padding-top:12px;border-top:1px dashed var(--line);font-size:14px}
.ws dt{font:500 11px/1.6 var(--f-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.ws dd{margin:0}
.ws .ws-price{font:800 26px/1 var(--f-display)}
.ws-links{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line)}
.ws-links a{padding:14px 8px;text-align:center;text-decoration:none;font:700 14px/1.1 var(--f-display);letter-spacing:.06em;text-transform:uppercase}
.ws .ws-links a:first-child{background:#fff;color:#000}
.ws .ws-links a:first-child:hover{background:var(--red-hi);color:#fff}
.ws-links a:last-child:hover{background:var(--surface-2)}
.ws-all{margin-top:22px;display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between;color:var(--muted);font-size:15px}
.ws-all a{color:var(--fg);font-weight:700}
@media (max-width:1060px){.ws-grid{grid-template-columns:1fr 1fr}}
@media (max-width:700px){.ws-grid{grid-template-columns:1fr}}
</style>"""

_ICO = {
    "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s7-6.1 7-12a7 7 0 1 0-14 0c0 5.9 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>',
}


def _utm(url, campaign, lang):
    """UTM značky, aby FF Academy ve své analytice viděla, že nákup přišel z hyroxtrainingclub.cz."""
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source=hyroxtrainingclub.cz&amp;utm_medium=referral&amp;utm_campaign={campaign}&amp;utm_content={lang}"


def _upcoming(today=None):
    today = today or datetime.date.today()
    evs = [e for e in EVENTS if datetime.date.fromisoformat(e["date"]) >= today]
    return sorted(evs, key=lambda e: (e["date"], e["start"]))


def _fmt_date(d, lang):
    if lang == "en":
        return f"{d.day} {d.strftime('%b')} {d.year}"
    if lang == "cs":
        return f"{d.day}. {d.month}. {d.year}"
    return f"{d.day:02d}.{d.month:02d}.{d.year}"


def _price(n, lang):
    s = SEC[lang]
    return f"{n:,}".replace(",", s["thou"]) + " " + s["cur"]


def _dur(e, lang):
    s = SEC[lang]
    if e.get("self_paced"):
        return f"{s['self_paced']} ({s['approx']} {e['hours']} {s['hours']})"
    return f"{e['start']}–{e['end']} ({e['hours']} {s['hours']})"


def section(lang):
    evs = _upcoming()
    if not evs:
        return ""
    s = SEC[lang]
    cards = ""
    for e in evs:
        t = e["t"][lang]
        d = datetime.date.fromisoformat(e["date"])
        li = "".join(f"<li>{x}</li>" for x in t["li"])
        tags = "".join(f"<span>{s['aud'][a]}</span>" for a in e["aud"]) + f"<span>{s['city']}</span>"
        date_txt = (f"{s['start']} " if e["kind"] == "course" else "") + _fmt_date(d, lang)
        lect_label = s["lectors"] if len(e["lectors"]) > 1 else s["lector"]
        if e.get("internal"):
            second = f'<a href="{raceprep.path(lang, e["internal"])}">{s["more"]}</a>'
        else:
            second = f'<a href="{_utm(e["info"], e["id"], lang)}" target="_blank" rel="noopener" data-ga="workshop_info" data-item="{e["id"]}" data-name="{e["title"]}">{s["info"]}</a>'
        cards += f"""<article class="ws" id="ws-{e['id']}">
          <div class="ws-img"><img loading="lazy" decoding="async" src="{e['img']}" alt="{e['title']}"><span class="ws-kind {e['kind']}">{s['kinds'][e['kind']]}</span><div class="ws-date"><b>{d.day}. {d.month}.</b><span>{s['days'][d.weekday()]} · {d.year}</span></div></div>
          <div class="ws-body">
            <div class="ws-tags">{tags}</div>
            <div class="ws-meta"><span>{_ICO['cal']}{date_txt}</span><span>{_ICO['clock']}{_dur(e, lang)}</span></div>
            <h3>{e['title']}<small>{t['sub']}</small></h3>
            <p>{t['txt']}</p>
            <ul>{li}</ul>
            <dl>
              <dt>{s['place']}</dt><dd>{e['loc']['place']}<br>{e['loc']['address']}</dd>
              <dt>{lect_label}</dt><dd>{'<br>'.join(e['lectors'])}</dd>
              <dt>{s['price']}</dt><dd class="ws-price">{_price(e['price'], lang)}</dd>
            </dl>
          </div>
          <div class="ws-links"><a href="{_utm(e['buy'], e['id'], lang)}" target="_blank" rel="noopener" data-ga="workshop_buy" data-item="{e['id']}" data-name="{e['title']}" data-price="{e['price']}">{s['buy']}</a>{second}</div>
        </article>"""
    note = f"<span>{s['lang_note']}</span>" if s["lang_note"] else "<span></span>"
    return f"""
  <section class="workshops" id="workshopy">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{s['eyebrow']}</p>
        <h2>{s['h']}</h2>
        <p class="lead">{s['lead']}</p>
      </div>
      <div class="ws-grid">{cards}</div>
      <div class="ws-all">{note}<a href="{_utm(ALL_URL, 'hyrox-label', lang)}" target="_blank" rel="noopener" data-ga="workshop_info" data-item="all" data-name="FF Academy HYROX">{s['all']}</a></div>
    </div>
  </section>
"""


IMG_BASE = "https://hyroxtrainingclub.cz"
# Od kdy je kurz v prodeji (Google „Události“ chce validFrom). Bez vlastního on_sale = den, kdy se objevil na webu.
ON_SALE_DEFAULT = "2026-10-27"


def jsonld():
    evs = _upcoming()
    if not evs:
        return ""
    data = []
    for e in evs:
        loc = e["loc"]
        item = {
            "@context": "https://schema.org", "@type": "EducationEvent",
            "name": f"{e['title']} – {e['t']['cs']['sub']}", "description": e["t"]["cs"]["txt"],
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled",
            "inLanguage": "cs", "maximumAttendeeCapacity": e["capacity"],
            "location": {"@type": "Place", "name": loc["place"], "address": {"@type": "PostalAddress", "streetAddress": loc["street"], "postalCode": loc["zip"], "addressLocality": loc["city"], "addressCountry": "CZ"}},
            "performer": [{"@type": "Person", "name": n.split(",")[0].replace("Ing. ", "")} for n in e["lectors"]],
            "organizer": {"@type": "Organization", "name": "FF Academy", "url": "https://www.ff-academy.cz/"},
            "image": [IMG_BASE + e["img"].rsplit(".", 1)[0] + ".jpg"],
            "offers": {"@type": "Offer", "price": e["price"], "priceCurrency": "CZK", "url": e["buy"], "availability": "https://schema.org/InStock",
                       "validFrom": e.get("on_sale", ON_SALE_DEFAULT) + "T00:00:00+01:00"},
            "url": e["info"],
        }
        if e.get("self_paced"):
            item["startDate"] = e["date"]
            item["endDate"] = (datetime.date.fromisoformat(e["date"]) + datetime.timedelta(weeks=12)).isoformat()
        else:
            item["startDate"] = f"{e['date']}T{e['start']}:00+01:00"
            item["endDate"] = f"{e['date']}T{e['end']}:00+01:00"
        data.append(item)
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"
