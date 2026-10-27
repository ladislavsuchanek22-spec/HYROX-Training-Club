"""Workshopy FF Academy na hlavní stránce (všechny jazyky).

Nový workshop = nová položka v EVENTS. Po datu konání se z webu sám schová (web se builduje denně).
Texty karet jsou v EVENTS[...]["t"][jazyk], texty sekce v SEC[jazyk].
"""
import datetime
import json

EVENTS = [
    dict(
        id="hyrox-level-1",
        date="2026-11-28", start="09:00", end="17:00",
        price=4990, capacity=20, img="/img/group.webp",
        place="Form Factory Na Knížecí", address="Ostrovského 464/6, 150 00 Praha 5",
        buy="https://ucet.ff-academy.cz/calendar?view=Preview&schiid=37753180",
        info="https://www.ff-academy.cz/workshop/hyrox-level-1-zakladni-workshop-praha-5/",
        title="HYROX Level 1",
        t={
            "cs": dict(tag="Pro trenéry a instruktory", sub="Základní workshop",
                       txt="Jednodenní praktický workshop pro trenéry a instruktory, kteří chtějí vést HYROX lekce se strukturou a energií. Žádná teorie bez kontextu: reálný trénink, technika, programming a nakonec si sám odvedeš část lekce.",
                       li=["Struktura HYROX lekce a základy programmingu", "Technika stanovišť: saně, wall balls, výpady, ergometry", "Coaching skupiny s různou výkonností a škálování", "Při spolupráci s FF HYROX Foundation course zdarma"]),
            "en": dict(tag="For coaches and instructors", sub="Foundation workshop",
                       txt="A one-day, hands-on workshop for coaches and instructors who want to run HYROX classes with structure and energy. No theory without context: real training, technique, programming, and at the end you coach part of the session yourself.",
                       li=["HYROX class structure and programming basics", "Station technique: sleds, wall balls, lunges, ergs", "Coaching mixed-ability groups and scaling", "Free HYROX Foundation course if you go on to coach at FF"]),
            "de": dict(tag="Für Trainer und Instruktoren", sub="Grundlagen-Workshop",
                       txt="Eintägiger Praxis-Workshop für Trainer und Instruktoren, die HYROX-Kurse mit Struktur und Energie leiten wollen. Keine Theorie ohne Kontext: echtes Training, Technik, Programming, und am Ende leitest du selbst einen Teil der Einheit.",
                       li=["Aufbau einer HYROX-Einheit und Programming-Grundlagen", "Stationstechnik: Schlitten, Wall Balls, Lunges, Ergometer", "Coaching gemischter Gruppen und Skalierung", "Bei Zusammenarbeit mit FF: HYROX Foundation Course gratis"]),
            "pl": dict(tag="Dla trenerów i instruktorów", sub="Warsztat podstawowy",
                       txt="Jednodniowy praktyczny warsztat dla trenerów i instruktorów, którzy chcą prowadzić zajęcia HYROX ze strukturą i energią. Bez teorii oderwanej od praktyki: prawdziwy trening, technika, programming, a na koniec sam poprowadzisz część zajęć.",
                       li=["Struktura zajęć HYROX i podstawy programmingu", "Technika stacji: sanie, wall balls, wykroki, ergometry", "Prowadzenie grup o różnym poziomie i skalowanie", "Przy współpracy z FF kurs HYROX Foundation gratis"]),
        },
    ),
    dict(
        id="mental-game",
        date="2026-11-29", start="10:00", end="12:00",
        price=1299, capacity=40, img="/img/ria-mic.webp",
        place="Form Factory Na Knížecí", address="Ostrovského 464/6, 150 00 Praha 5",
        buy="https://ucet.ff-academy.cz/calendar?dayOnline&schiid=37778857&view=Preview",
        info="https://www.ff-academy.cz/instruktor/mental-game/",
        title="Mental Game",
        t={
            "cs": dict(tag="Pro všechny", sub="Hlava pod tlakem",
                       txt="Dvouhodinový workshop, který začíná 30minutovým HYROX workoutem. Nejde o čas ani výkon, ale o to, co se ti děje v hlavě, když už nemůžeš. Pak to rozebereme a přeneseme do práce i běžného života.",
                       li=["30 minut HYROX workoutu", "Hlava pod tlakem: vnitřní dialog, pozornost, emoce", "Mentální odolnost a práce s nepohodlím", "Vlastní mental game plan do sportu i života"]),
            "en": dict(tag="Open to everyone", sub="Your head under pressure",
                       txt="A two-hour workshop that starts with a 30-minute HYROX workout. It's not about your time or fitness, but about what goes on in your head when you want to stop. Then we unpack it and carry it over to work and everyday life.",
                       li=["30-minute HYROX workout", "Head under pressure: inner voice, focus, emotions", "Mental resilience and working with discomfort", "Your own mental game plan for sport and life"]),
            "de": dict(tag="Für alle", sub="Der Kopf unter Druck",
                       txt="Zweistündiger Workshop, der mit einem 30-minütigen HYROX-Workout beginnt. Es geht nicht um Zeit oder Fitness, sondern darum, was in deinem Kopf passiert, wenn du nicht mehr kannst. Danach arbeiten wir es auf und übertragen es auf Job und Alltag.",
                       li=["30 Minuten HYROX-Workout", "Kopf unter Druck: innerer Dialog, Fokus, Emotionen", "Mentale Stärke und Umgang mit Unbehagen", "Dein eigener Mental-Game-Plan für Sport und Leben"]),
            "pl": dict(tag="Dla wszystkich", sub="Głowa pod presją",
                       txt="Dwugodzinny warsztat, który zaczyna się 30-minutowym workoutem HYROX. Nie chodzi o czas ani formę, tylko o to, co dzieje się w twojej głowie, kiedy masz już dość. Potem to rozbieramy i przenosimy do pracy i codziennego życia.",
                       li=["30 minut workoutu HYROX", "Głowa pod presją: wewnętrzny dialog, uwaga, emocje", "Odporność psychiczna i praca z dyskomfortem", "Własny mental game plan do sportu i życia"]),
        },
    ),
]

SEC = {
    "cs": dict(eyebrow="Workshopy FF Academy", h="Workshopy s Riou Suchánek Hrušovskou.",
               lead="Listopadové workshopy ve Form Factory Na Knížecí s head coach HYROX Training Clubu. Prodej probíhá přes FF Academy.",
               date="Datum", time="Čas", place="Místo", cap="Kapacita", price="Cena", lector="Lektorka", seats="míst",
               buy="Koupit online →", info="Více na FF Academy", lang_note="",
               days=["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"], cur="Kč", thou=" "),
    "en": dict(eyebrow="FF Academy workshops", h="Workshops with Ria Suchánek Hrušovská.",
               lead="November workshops at Form Factory Na Knížecí, Prague, with the head coach of the HYROX Training Club. Tickets are sold through FF Academy.",
               date="Date", time="Time", place="Venue", cap="Capacity", price="Price", lector="Led by", seats="places",
               buy="Buy online →", info="More on FF Academy", lang_note="In Czech, English possible on request.",
               days=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], cur="CZK", thou=","),
    "de": dict(eyebrow="Workshops der FF Academy", h="Workshops mit Ria Suchánek Hrušovská.",
               lead="November-Workshops bei Form Factory Na Knížecí in Prag mit der Head Coach des HYROX Training Clubs. Tickets gibt es über die FF Academy.",
               date="Datum", time="Zeit", place="Ort", cap="Kapazität", price="Preis", lector="Leitung", seats="Plätze",
               buy="Online kaufen →", info="Mehr bei FF Academy", lang_note="Auf Tschechisch, Englisch nach Absprache möglich.",
               days=["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So."], cur="CZK", thou="."),
    "pl": dict(eyebrow="Warsztaty FF Academy", h="Warsztaty z Rią Suchánek Hrušovską.",
               lead="Listopadowe warsztaty w Form Factory Na Knížecí w Pradze z head coach HYROX Training Club. Sprzedaż odbywa się przez FF Academy.",
               date="Data", time="Godzina", place="Miejsce", cap="Liczba miejsc", price="Cena", lector="Prowadzi", seats="miejsc",
               buy="Kup online →", info="Więcej w FF Academy", lang_note="Po czesku, na życzenie także po angielsku.",
               days=["pon.", "wt.", "śr.", "czw.", "pt.", "sob.", "niedz."], cur="CZK", thou=" "),
}

CSS = """<style>
.ws-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.ws{border:1px solid var(--line);background:var(--surface);display:flex;flex-direction:column;min-width:0}
.ws-img{position:relative;aspect-ratio:16/9;overflow:hidden;background:var(--surface-2)}
.ws-img img{width:100%;height:100%;object-fit:cover}
.ws-date{position:absolute;left:0;bottom:0;background:var(--red);color:#fff;padding:10px 14px;display:grid;gap:2px}
.ws-date b{font:800 34px/1 var(--f-display);font-variant-numeric:tabular-nums}
.ws-date span{font:500 12px/1 var(--f-mono);letter-spacing:.1em;text-transform:uppercase}
.ws-body{padding:24px;display:grid;gap:12px;flex:1;align-content:start}
.ws-tag{font:500 12px/1 var(--f-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--red-hi)}
.ws h3{font-size:clamp(34px,3.6vw,46px)}
.ws h3 small{display:block;margin-top:6px;font:600 15px/1.2 var(--f-body);letter-spacing:.12em;color:var(--muted)}
.ws p{color:var(--muted);font-size:16px}
.ws ul{list-style:none;margin:0;padding:0;display:grid;gap:7px;font-size:15px}
.ws li{display:flex;gap:10px;line-height:1.4}
.ws li::before{content:"";flex:0 0 8px;height:8px;margin-top:6px;background:var(--red-hi)}
.ws dl{margin:6px 0 0;display:grid;grid-template-columns:auto 1fr;gap:8px 16px;padding-top:14px;border-top:1px dashed var(--line);font-size:15px}
.ws dt{font:500 11px/1.6 var(--f-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.ws dd{margin:0;font-variant-numeric:tabular-nums}
.ws .ws-price{font:800 28px/1 var(--f-display)}
.ws-links{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line)}
.ws-links a{padding:15px 10px;text-align:center;text-decoration:none;font:700 15px/1 var(--f-display);letter-spacing:.08em;text-transform:uppercase}
.ws-links a:first-child{background:var(--red);color:#fff}
.ws-links a:first-child:hover{background:var(--red-hi)}
.ws-links a:last-child:hover{background:var(--surface-2)}
@media (max-width:860px){.ws-grid{grid-template-columns:1fr}}
</style>"""


def _upcoming(today=None):
    today = today or datetime.date.today()
    return [e for e in EVENTS if datetime.date.fromisoformat(e["date"]) >= today]


def _fmt_date(d, lang):
    s = SEC[lang]
    day = s["days"][d.weekday()]
    if lang == "en":
        return f"{day} {d.day} {d.strftime('%b')} {d.year}"
    if lang == "cs":
        return f"{day} {d.day}. {d.month}. {d.year}"
    return f"{day} {d.day:02d}.{d.month:02d}.{d.year}"


def _price(n, lang):
    s = SEC[lang]
    return f"{n:,}".replace(",", s["thou"]) + " " + s["cur"]


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
        note = f' <i style="font-style:normal;color:var(--muted)">{s["lang_note"]}</i>' if s["lang_note"] else ""
        cards += f"""<article class="ws" id="ws-{e['id']}">
          <div class="ws-img"><img loading="lazy" decoding="async" src="{e['img']}" alt="{e['title']}"><div class="ws-date"><b>{d.day}. {d.month}.</b><span>{s['days'][d.weekday()]} · {d.year}</span></div></div>
          <div class="ws-body">
            <span class="ws-tag">{t['tag']}</span>
            <h3>{e['title']}<small>{t['sub']}</small></h3>
            <p>{t['txt']}</p>
            <ul>{li}</ul>
            <dl>
              <dt>{s['date']}</dt><dd>{_fmt_date(d, lang)}</dd>
              <dt>{s['time']}</dt><dd>{e['start']}–{e['end']}</dd>
              <dt>{s['place']}</dt><dd>{e['place']}<br>{e['address']}</dd>
              <dt>{s['lector']}</dt><dd>Ria Suchánek Hrušovská, MSc.{note}</dd>
              <dt>{s['cap']}</dt><dd>{e['capacity']} {s['seats']}</dd>
              <dt>{s['price']}</dt><dd class="ws-price">{_price(e['price'], lang)}</dd>
            </dl>
          </div>
          <div class="ws-links"><a href="{e['buy']}" target="_blank" rel="noopener">{s['buy']}</a><a href="{e['info']}" target="_blank" rel="noopener">{s['info']}</a></div>
        </article>"""
    return f"""
  <section class="workshops" id="workshopy">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{s['eyebrow']}</p>
        <h2>{s['h']}</h2>
        <p class="lead">{s['lead']}</p>
      </div>
      <div class="ws-grid">{cards}</div>
    </div>
  </section>
"""


def jsonld():
    evs = _upcoming()
    if not evs:
        return ""
    data = [{
        "@context": "https://schema.org", "@type": "EducationEvent",
        "name": f"{e['title']} – {e['t']['cs']['sub']}", "description": e["t"]["cs"]["txt"],
        "startDate": f"{e['date']}T{e['start']}:00+01:00", "endDate": f"{e['date']}T{e['end']}:00+01:00",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled",
        "inLanguage": "cs", "maximumAttendeeCapacity": e["capacity"],
        "location": {"@type": "Place", "name": e["place"], "address": {"@type": "PostalAddress", "streetAddress": "Ostrovského 464/6", "postalCode": "150 00", "addressLocality": "Praha 5", "addressCountry": "CZ"}},
        "performer": {"@type": "Person", "name": "Ria Suchánek Hrušovská"},
        "organizer": {"@type": "Organization", "name": "FF Academy", "url": "https://www.ff-academy.cz/"},
        "offers": {"@type": "Offer", "price": e["price"], "priceCurrency": "CZK", "url": e["buy"], "availability": "https://schema.org/InStock"},
        "url": e["info"],
    } for e in evs]
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"
