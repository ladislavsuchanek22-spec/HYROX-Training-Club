"""STR2G HYROX 12 Weeks Race Prep: promo blok na hlavní stránce, stránka programu a portál účastníků.

Používá se z build.py (STYLE, EXTRA_CSS a hlavičku dodává build). Zatím jen česky.
Portál je v této fázi jen vizuální náhled: formuláře nic neodesílají.
"""

SLUG = "12-weeks-race-prep"
PORTAL = "portal"

RP_CSS = """<style>
/* 12 Weeks Race Prep */
.rp-promo{position:relative;overflow:hidden;isolation:isolate;border-block:1px solid var(--line)}
.rp-promo::before{content:"";position:absolute;inset:0;z-index:-2;background:url("/img/coaches.webp") center 30%/cover}
.rp-promo::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(9,11,19,.97) 0%,rgba(9,11,19,.86) 50%,rgba(165,15,45,.55) 100%)}
.rp-promo .wrap{display:grid;grid-template-columns:1.3fr .7fr;gap:clamp(24px,5vw,64px);align-items:center;padding-block:clamp(44px,6vw,72px)}
.rp-promo h2{font-size:clamp(40px,6vw,76px)}
.rp-promo h2 span{color:var(--red-hi)}
.rp-promo .lead{color:#C9CFE4;margin-top:14px}
.rp-promo .hero-cta{margin-top:24px}
.rp-tag{display:inline-block;font:500 12px/1 var(--f-mono);letter-spacing:.14em;text-transform:uppercase;background:var(--red);color:#fff;padding:7px 10px;margin-bottom:16px}
.rp-facts{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line)}
.rp-facts div{background:rgba(9,11,19,.82);padding:18px}
.rp-facts strong{display:block;font:800 44px/1 var(--f-display);font-variant-numeric:tabular-nums}
.rp-facts span{color:var(--muted);font-size:14px;line-height:1.3}
@media (max-width:860px){.rp-promo .wrap{grid-template-columns:1fr}}
.nav ul a.rp-nav{color:var(--fg);border-bottom:2px solid var(--red-hi);padding-bottom:3px}

.rp-intro .wrap{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,72px);align-items:start}
.rp-intro p{color:var(--muted);max-width:60ch}
.rp-intro p strong{color:var(--fg);font-weight:600}
.rp-how{border:1px solid var(--line);background:var(--surface);padding:24px;display:grid;gap:10px}
.rp-how b{font:700 22px/1.1 var(--f-display);text-transform:uppercase}
@media (max-width:860px){.rp-intro .wrap{grid-template-columns:1fr}}

.rp-who{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.rp-who div{border:1px solid var(--line);background:var(--bg);padding:22px;display:grid;gap:8px;align-content:start}
.rp-who b{font:700 22px/1.1 var(--f-display);text-transform:uppercase}
.rp-who p{color:var(--muted);font-size:16px}
@media (max-width:1000px){.rp-who{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.rp-who{grid-template-columns:1fr}}

.rp-inc{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.rp-inc article{border:1px solid var(--line);background:var(--surface);padding:24px;display:grid;gap:10px;align-content:start}
.rp-inc .no{font:500 12px/1 var(--f-mono);color:var(--red-hi);letter-spacing:.1em}
.rp-inc h3{font-size:28px}
.rp-inc p{color:var(--muted);font-size:15px}
.rp-inc ul{list-style:none;margin:6px 0 0;padding:12px 0 0;border-top:1px dashed var(--line);display:grid;gap:7px;font-size:15px}
.rp-inc li{display:flex;gap:10px;line-height:1.4}
.rp-inc li::before{content:"";flex:0 0 8px;height:8px;margin-top:6px;background:var(--red-hi)}
@media (max-width:1000px){.rp-inc{grid-template-columns:1fr 1fr}}
@media (max-width:620px){.rp-inc{grid-template-columns:1fr}}

.rp-weeks{border:1px solid var(--line)}
.rp-phase{font:500 12px/1 var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--red-hi);background:var(--surface);padding:12px 18px;border-bottom:1px solid var(--line)}
.rp-week{display:grid;grid-template-columns:64px 180px 1fr;gap:16px;align-items:baseline;padding:14px 18px;border-bottom:1px solid var(--line)}
.rp-weeks .rp-week:last-child{border-bottom:0}
.rp-week .n{font:800 30px/1 var(--f-display);font-variant-numeric:tabular-nums}
.rp-week b{font:700 20px/1 var(--f-display);text-transform:uppercase;letter-spacing:.03em}
.rp-week span{color:var(--muted);font-size:16px}
.rp-week.ws{background:rgba(74,99,255,.08)}
.rp-week.ws b::after{content:" · workshop";font:500 11px/1 var(--f-mono);letter-spacing:.08em;color:var(--blue);text-transform:uppercase}
@media (max-width:620px){.rp-week{grid-template-columns:44px 1fr}.rp-week span{grid-column:2}}

.rp-price .wrap{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(28px,5vw,64px);align-items:start}
.rp-card{border:2px solid var(--red);background:var(--surface);padding:30px;display:grid;gap:14px}
.rp-card .amt{font:800 clamp(64px,9vw,104px)/.9 var(--f-display);font-variant-numeric:tabular-nums}
.rp-card .amt small{font-size:.32em;color:var(--muted);margin-left:8px}
.rp-card p{color:var(--muted)}
.rp-list{list-style:none;margin:0;padding:0;display:grid;gap:0;border-top:1px solid var(--line)}
.rp-list li{display:flex;gap:12px;padding:13px 0;border-bottom:1px solid var(--line);font-size:16px}
.rp-list li::before{content:"✓";color:var(--red-hi);font-weight:700}
.rp-note{margin-top:16px;color:var(--muted);font-size:15px;border-left:3px solid var(--blue);padding-left:14px}
@media (max-width:860px){.rp-price .wrap{grid-template-columns:1fr}}

.rp-portal-teaser{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,64px);align-items:center}
@media (max-width:860px){.rp-portal-teaser{grid-template-columns:1fr}}
.rp-coaches{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.rp-coaches article{display:grid;grid-template-columns:140px 1fr;gap:18px;border:1px solid var(--line);background:var(--surface);align-items:center}
.rp-coaches img{width:140px;height:175px;object-fit:cover;display:block}
.rp-coaches div{padding:16px 18px 16px 0}
.rp-coaches b{display:block;font:700 24px/1.05 var(--f-display);text-transform:uppercase}
.rp-coaches span{font:500 12px/1.3 var(--f-mono);letter-spacing:.06em;color:var(--red-hi);text-transform:uppercase}
.rp-coaches p{color:var(--muted);font-size:15px;margin-top:6px}
@media (max-width:760px){.rp-coaches{grid-template-columns:1fr}}

/* portal */
.pv-bar{background:var(--blue);color:#fff;text-align:center;font:500 13px/1.4 var(--f-mono);letter-spacing:.04em;padding:9px max(16px,env(safe-area-inset-left,0px))}
.pt-wrap{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,72px);align-items:start}
@media (max-width:860px){.pt-wrap{grid-template-columns:1fr}}
.pt-box{border:1px solid var(--line);background:var(--surface)}
.pt-tabs{display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid var(--line)}
.pt-tabs button{all:unset;cursor:pointer;text-align:center;padding:16px;font:700 17px/1 var(--f-display);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.pt-tabs button[aria-selected="true"]{color:var(--fg);box-shadow:inset 0 -3px 0 var(--red-hi)}
.pt-tabs button:focus-visible{outline:2px solid var(--blue);outline-offset:-2px}
.pt-form{padding:26px;display:grid;gap:14px}
.pt-form label{display:grid;gap:6px;font:500 12px/1 var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.pt-form input{font:400 16px/1.3 var(--f-body);color:var(--fg);background:var(--bg);border:1px solid var(--line);padding:13px 14px;border-radius:0}
.pt-form input:focus{outline:2px solid var(--blue);outline-offset:0;border-color:var(--blue)}
.pt-form .chk{display:flex;gap:10px;align-items:flex-start;text-transform:none;letter-spacing:0;font:400 14px/1.4 var(--f-body)}
.pt-form .chk input{margin-top:3px;padding:0}
.pt-form .btn{justify-content:center;border:0;cursor:pointer}
.pt-form small{color:var(--muted);font-size:13px}
.pt-steps{display:grid;gap:0;border-top:1px solid var(--line)}
.pt-steps div{display:grid;grid-template-columns:44px 1fr;gap:14px;padding:16px 0;border-bottom:1px solid var(--line)}
.pt-steps .n{font:800 32px/1 var(--f-display);color:var(--red-hi)}
.pt-steps b{display:block;font:700 20px/1.1 var(--f-display);text-transform:uppercase;margin-bottom:4px}
.pt-steps p{color:var(--muted);font-size:15px}
.pt-dash{display:grid;gap:24px}
.pt-hello{display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px;align-items:end;border-bottom:1px solid var(--line);padding-bottom:22px}
.pt-hello h2{font-size:clamp(36px,5vw,58px)}
.pt-prog{display:grid;gap:8px;min-width:240px}
.pt-prog span{font:500 12px/1 var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.pt-bar{height:8px;background:var(--line)}
.pt-bar i{display:block;height:100%;background:var(--red-hi)}
.pt-files{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.pt-file{border:1px solid var(--line);background:var(--surface);padding:20px;display:grid;gap:10px;align-content:start}
.pt-file .ic{font:800 13px/1 var(--f-mono);color:#fff;background:var(--red);width:max-content;padding:6px 8px;letter-spacing:.06em}
.pt-file b{font:700 22px/1.05 var(--f-display);text-transform:uppercase}
.pt-file p{color:var(--muted);font-size:14px}
.pt-file .meta{font:500 12px/1 var(--f-mono);color:var(--muted)}
.pt-file .btn{padding:11px 14px;font-size:14px;justify-content:center;border:0;cursor:pointer}
.pt-file.locked{opacity:.6}
.pt-file.locked .btn{background:var(--surface-2);color:var(--muted);cursor:not-allowed}
.pt-links{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.pt-links a{border:1px solid var(--line);padding:18px;text-decoration:none;display:grid;gap:4px}
.pt-links a:hover{border-color:var(--blue)}
.pt-links b{font:700 20px/1.1 var(--f-display);text-transform:uppercase}
.pt-links span{color:var(--muted);font-size:14px}
@media (max-width:760px){.pt-links{grid-template-columns:1fr}}
.pt-toast{font:500 14px/1.4 var(--f-body);color:var(--fg);background:var(--surface-2);border-left:3px solid var(--blue);padding:12px 14px}
</style>"""

FACTS = [("12", "týdnů přípravy"), ("4", "tréninky týdně"), ("3", "společné workshopy"), ("8", "stanovišť do detailu")]

WHO = [
    ("Začátečníci", "Chceš s HYROX začít a nevíš, jak na to. Program tě provede od nuly."),
    ("Účastníci lekcí FF", "Chodíš na HYROX lekce a chceš k tomu strukturovaný programming, který tě posune dál."),
    ("První závodníci", "Máš přihlášku na první HYROX a potřebuješ jistotu, že jsi připravený."),
    ("Zkušení závodníci", "Závod už máš za sebou a chceš zlepšit čas. Program má úrovně pro pokročilé."),
]

INCLUDED = [
    ("Týdenní programming", "Každé pondělí plán na celý týden. Přesně naplánovaný, jasně vysvětlený. Odjíždíš ho sám, ve svém čase.",
     ["2 běžecké tréninky týdně", "2 silové / HYROX tréninky týdně", "Doporučené HYROX lekce ve FF", "Deload a tapering fáze", "Individuální pace zóny z testu"]),
    ("Edukační knihovna", "Videa přímo v tréninkové aplikaci. Odemykají se postupně během programu.",
     ["Technika všech 8 HYROX stanovišť", "Běžecká technika a pacing", "Silový trénink pro HYROX", "Mobilita a regenerace", "Race week a závodní den"]),
    ("3 společné workshopy", "Tři osobní setkání s trenéry a komunitou. Testování, edukace, společný trénink.",
     ["Workshop 1 · Kick-off, vstupní testy", "Workshop 2 · Mid-program check", "Workshop 3 · Výstupní testy, vyhodnocení"]),
    ("PDF materiály", "Praktičtí průvodci ke stažení a vytištění. Najdeš je v portálu účastníků a zůstanou ti i po programu.",
     ["Průvodce programem", "Kompletní průvodce výživou", "Warm-up protokol", "Mobilita a regenerace", "Závodní den + checklisty"]),
    ("WhatsApp komunita", "Uzavřená skupina jen pro účastníky. Motivace, dotazy, sdílení pokroku, podpora trenérů.",
     ["Denní tipy a motivace", "Odpovědi na dotazy 2× denně", "Sdílení tréninků a výsledků", "50 lidí se stejným cílem"]),
    ("Mentální příprava", "Praktický obsah, který ti pomůže zvládnout tréninkovou zátěž i závodní stres.",
     ["Práce s motivací a disciplínou", "Zvládání nervozity před závodem", "Vizualizace a nastavení cílů", "Krizové momenty v závodě"]),
]

PHASES = [
    ("Fáze 1 · Základ", [("01", "Adaptace", "Kick-off, vstupní testy, nastavení rytmu", True), ("02", "Základ", "Budování základny, technika stanovišť", False),
                         ("03", "Technika", "Zdokonalení techniky, zvýšení objemu", False), ("04", "Objem", "Delší tréninky, aerobní kapacita", False)]),
    ("Fáze 2 · Výkon", [("05", "Intenzita", "Práce s HR zónami, VO2max", False), ("06", "Deload", "Regenerace + Workshop 2", True),
                        ("07", "Specifická", "Race pace, hybrid workouty", False), ("08", "Simulace", "HYROX simulace, 6 stanovišť", False),
                        ("09", "Peak week", "Nejvyšší intenzita programu", False)]),
    ("Fáze 3 · Závod", [("10", "Tapering", "Snížení objemu, udržení ostrosti", False), ("11", "Race week", "Aktivace, příprava na závod", False),
                        ("12", "Finále", "Workshop 3, výstupní testy", True)]),
]

PRICE_LIST = ["12 týdnů programmingu, plán každé pondělí", "Individuální pace zóny ze vstupního testu", "Edukační knihovna v aplikaci",
              "3 společné workshopy s trenéry", "PDF materiály v portálu účastníků", "WhatsApp komunita a podpora trenérů", "Mentální příprava"]

PDFS = [
    ("Průvodce programem", "Jak program funguje, týdenní rytmus, zóny a pravidla.", "Odemčeno", False),
    ("Kompletní průvodce výživou", "Jídlo kolem tréninku, regenerace a závodní den.", "Odemčeno", False),
    ("Warm-up protokol", "Rozcvička před během, silou i závodem.", "Odemčeno", False),
    ("Mobilita a regenerace", "Rutiny na dny mezi tréninky a po workshopech.", "Odemkne se v týdnu 4", True),
    ("Závodní den + checklisty", "Co si zabalit, timeline závodního dne a taktika.", "Odemkne se v týdnu 10", True),
]


def promo():
    facts = "".join(f"<div><strong>{n}</strong><span>{t}</span></div>" for n, t in FACTS)
    return f'''
  <section class="rp-promo" aria-label="12 Weeks Race Prep">
    <div class="wrap">
      <div>
        <span class="rp-tag">Nový program · Form Factory × STR2G</span>
        <h2>HYROX 12 Weeks<br><span>Race Prep.</span></h2>
        <p class="lead">Strukturovaná příprava na závod. Běh, síla, stanoviště a taktika v jednom plánu, pod vedením Rii a Ládi. Plán každé pondělí, 3 společné workshopy a portál s materiály ke stažení.</p>
        <div class="hero-cta">
          <a class="btn btn-red" href="/{SLUG}/">Chci do programu →</a>
          <a class="btn btn-ghost" href="/{SLUG}/#cena">8 999 Kč · co je v ceně</a>
        </div>
      </div>
      <div class="rp-facts">{facts}</div>
    </div>
  </section>
'''


def head(title, desc, url, site, robots="index,follow,max-image-preview:large"):
    return f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="HYROX Training Club">
<meta property="og:locale" content="cs_CZ">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}/img/coaches.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
<script src="/js/tracking.js"></script>
<link rel="icon" href="/favicon.png" type="image/png" sizes="160x160">
<link rel="apple-touch-icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
'''


def nav(t, cal):
    return f'''<header class="nav">
  <div class="wrap">
    <a class="brand" href="/">
      <img src="/img/ff-logo.jpg" alt="Form Factory">
      <span><b>HYROX Training Club</b><small>{t["brand_sub"]}</small></span>
    </a>
    <ul>
      <li><a href="/{SLUG}/" class="rp-nav">12 Weeks</a></li>
      <li><a href="/{SLUG}/#obsah">Co je v programu</a></li>
      <li><a href="/{SLUG}/#cena">Cena</a></li>
      <li><a href="/{PORTAL}/">Portál</a></li>
    </ul>
    <div class="nav-right">
      <a class="btn btn-red" href="/{PORTAL}/#registrace">Registrace</a>
    </div>
  </div>
</header>
'''


def footer(net, ff_hyrox):
    return f'''<footer>
  <div class="wrap">
    {net.block("htc", "cs")}
    <span>HYROX Training Club · Form Factory × STR2G</span>
    <span><a href="{ff_hyrox}" target="_blank" rel="noopener">formfactory.cz/hyrox</a> · <a href="https://www.instagram.com/hyroxprague/" target="_blank" rel="noopener">@hyroxprague</a> · <a href="#" onclick="window.cookieSettings&&cookieSettings();return false">Cookies</a></span>
  </div>
</footer>
</body>
</html>
'''


def program_page(T, STYLE, EXTRA_CSS, SITE, net, FF_HYROX):
    t = T["cs"]
    cal = FF_HYROX["cs"] + "#timetables"
    url = f"{SITE}/{SLUG}/"
    title = "HYROX 12 Weeks Race Prep | STR2G × Form Factory"
    desc = "12týdenní příprava na HYROX pod vedením Rii a Ládi. Plán každé pondělí, individuální pace zóny, 3 workshopy, PDF materiály a WhatsApp komunita. 8 999 Kč."
    facts = "".join(f'<div class="stat"><strong>{n}</strong><span>{x}</span></div>' for n, x in FACTS)
    who = "".join(f"<div><b>{a}</b><p>{b}</p></div>" for a, b in WHO)
    inc = "".join(
        f'<article><span class="no">/ {i+1:02d}</span><h3>{h}</h3><p>{p}</p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></article>'
        for i, (h, p, li) in enumerate(INCLUDED))
    weeks = ""
    for ph, rows in PHASES:
        weeks += f'<div class="rp-phase">{ph}</div>'
        weeks += "".join(f'<div class="rp-week{" ws" if ws else ""}"><span class="n">{n}</span><b>{f}</b><span>{d}</span></div>' for n, f, d, ws in rows)
    price = "".join(f"<li>{x}</li>" for x in PRICE_LIST)
    pdfs = "".join(f"<li>{p[0]}</li>" for p in PDFS)
    return head(title, desc, url, SITE) + STYLE + EXTRA_CSS + RP_CSS + '''
<style>body{margin:0}[hidden]{display:none!important}.hero h1{font-size:clamp(52px,10vw,132px)}</style>
</head>
<body>
''' + nav(t, cal) + f'''
<main id="top">
  <section class="hero">
    <div class="hero-img"><img src="/img/coaches.webp" alt="Ria Suchánek Hrušovská a Ladislav Suchánek na HYROX závodě" style="object-position:center 25%"></div>
    <div class="wrap">
      <p class="crumbs"><a href="/">HYROX Training Club</a> / 12 Weeks Race Prep</p>
      <p class="eyebrow">Form Factory × STR2G · 12týdenní příprava</p>
      <h1>HYROX<span>12 Weeks</span><em>Race Prep.</em></h1>
      <p class="lead">Strukturovaná příprava na HYROX. Běh, síla, stanoviště a taktika v jednom plánu. Pod vedením Rii a Ládi.</p>
      <div class="hero-cta">
        <a class="btn btn-red" href="/{PORTAL}/#registrace">Registrovat se →</a>
        <a class="btn btn-ghost" href="#obsah">Co je v programu</a>
      </div>
      <p class="cities"><b>Plan.</b> Train. <b>Perform.</b></p>
    </div>
  </section>

  <div class="stats" aria-label="Program v číslech"><div class="wrap">{facts}</div></div>

  <section class="rp-intro">
    <div class="wrap">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">01 · O programu</p>
        <h2>Trénink, který má hlavu a patu.</h2>
        <p class="lead"><strong>HYROX není náhodný workout.</strong> Výkon stojí na běhu, síle, technice stanovišť, přechodech a taktice. A hlavně na schopnosti držet výkon pod únavou.</p>
      </div>
      <div style="display:grid;gap:18px">
        <p>Většina lidí, kteří jdou do HYROX, trénuje bez struktury. Chodí na lekce, občas si zaběhá, občas zvedne činku. A pak se diví, proč se posun zastavil.</p>
        <p>Tenhle program to řeší. <strong>12 týdnů, jasný plán, individuálně nastavené zóny podle vstupního testu.</strong> Programming, který funguje pro začátečníka i pro zkušeného závodníka. K tomu podpora trenérů a komunita, která tě posune dál, než bys šel sám.</p>
        <div class="rp-how">
          <b>Jak to celé funguje</b>
          <p>Tréninkový plán si odjíždíš sám. Každé pondělí dostaneš rozpis na celý týden a plníš ho ve svém čase a tempu. K tomu doporučujeme <a href="{cal}" target="_blank" rel="noopener" style="color:var(--fg)">vedené HYROX lekce ve Form Factory</a>, kde si pod trenérem vyladíš techniku stanovišť a práci pod únavou. Lekce nejsou součástí ceny programu.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="programs">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">02 · Pro koho</p>
        <h2>Pro každého, kdo to myslí vážně.</h2>
      </div>
      <div class="rp-who">{who}</div>
    </div>
  </section>

  <section id="obsah">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">03 · Co je součástí</p>
        <h2>Kompletní příprava, ne jen plán.</h2>
        <p class="lead">Programming, edukace, workshopy, komunita, materiály. Všechno, co potřebuješ, na jednom místě. Nejsi na to sám.</p>
      </div>
      <div class="rp-inc">{inc}</div>
    </div>
  </section>

  <div class="lanes" aria-hidden="true"></div>

  <section class="race">
    <div class="wrap">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">04 · Struktura programu</p>
        <h2>12 týdnů. Každý s jasným cílem.</h2>
        <p class="lead">Postupná stavba výkonu od základů přes peak week až po tapering před závodem. Modře jsou týdny se společným workshopem.</p>
      </div>
      <div class="rp-weeks">{weeks}</div>
    </div>
  </section>

  <section class="rp-price programs" id="cena">
    <div class="wrap">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">05 · Cena</p>
        <h2>Jedna cena. Celá příprava.</h2>
        <p class="lead">Platíš jednou, za celý program. Žádné předplatné, žádné doplatky.</p>
        <div class="rp-card">
          <span class="rp-tag" style="margin:0;width:max-content">12 Weeks Race Prep</span>
          <div class="amt">8 999<small>Kč</small></div>
          <p>Kompletní 12týdenní příprava na HYROX.</p>
          <a class="btn btn-red" href="/{PORTAL}/#registrace" style="justify-content:center">Registrovat se do programu →</a>
        </div>
      </div>
      <div>
        <p class="eyebrow" style="margin-bottom:16px">V ceně</p>
        <ul class="rp-list">{price}</ul>
        <p class="rp-note">Vedené HYROX lekce ve Form Factory nejsou v ceně. Řešíš je sám, přes vlastní členství nebo jednotlivé vstupy.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap rp-portal-teaser">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">Portál účastníků</p>
        <h2>Všechny materiály na jednom místě.</h2>
        <p class="lead">Po registraci dostaneš přístup do portálu. Najdeš tam PDF průvodce ke stažení a vytištění, odkaz do WhatsApp komunity a termíny workshopů. Nové materiály se odemykají postupně, jak program běží.</p>
        <div class="hero-cta"><a class="btn btn-ghost" href="/{PORTAL}/">Podívat se do portálu</a></div>
      </div>
      <div class="rp-how">
        <b>PDF ke stažení</b>
        <ul class="rp-list" style="border-top:0">{pdfs}</ul>
      </div>
    </div>
  </section>

  <section class="programs">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Vedení programu</p>
        <h2>Ria &amp; Láďa.</h2>
        <p class="lead">Head coaches HYROX Training Clubu. Trénují, závodí a stojí za metodikou HYROX lekcí ve Form Factory.</p>
      </div>
      <div class="rp-coaches">
        <article><img loading="lazy" src="/img/coach-ria.webp?v=2" alt="Ria Suchánek Hrušovská"><div><span>Head coach · Mental coach</span><b>Ria Suchánek Hrušovská</b><p>Technika, stabilita a hlava. Mentální příprava v programu je její.</p></div></article>
        <article><img loading="lazy" src="/img/coach-lada.webp?v=2" alt="Ladislav Suchánek"><div><span>Head coach · HYROX Performance Coach</span><b>Ladislav Suchánek</b><p>Běh, síla a programming. Stojí za týdenními plány a pace zónami.</p></div></article>
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="wrap">
      <p class="eyebrow">Plan. Train. Perform.</p>
      <h2>12 týdnů.<br>Jasný plán. Tvůj čas.</h2>
      <p class="lead">Registruj se, zaplať jednou a v pondělí dostaneš první týden. Stronger together.</p>
      <div class="cta-row">
        <a class="btn btn-red" href="/{PORTAL}/#registrace">Registrovat se →</a>
        <a class="btn btn-ghost" href="/">HYROX Training Club</a>
      </div>
    </div>
  </section>
</main>
''' + footer(net, FF_HYROX["cs"])


def portal_page(T, STYLE, EXTRA_CSS, SITE, net, FF_HYROX):
    t = T["cs"]
    cal = FF_HYROX["cs"] + "#timetables"
    url = f"{SITE}/{PORTAL}/"
    files = ""
    for name, d, meta, locked in PDFS:
        btn = '<button class="btn" type="button" disabled>Zamčeno</button>' if locked else '<button class="btn btn-red dl" type="button">Stáhnout PDF ↓</button>'
        files += f'<div class="pt-file{" locked" if locked else ""}"><span class="ic">PDF</span><b>{name}</b><p>{d}</p><span class="meta">{meta}</span>{btn}</div>'
    return head("Portál účastníků | HYROX 12 Weeks Race Prep", "Portál účastníků programu HYROX 12 Weeks Race Prep: PDF materiály ke stažení, komunita a workshopy.", url, SITE, robots="noindex,nofollow") + STYLE + EXTRA_CSS + RP_CSS + '''
<style>body{margin:0}[hidden]{display:none!important}.portal-hero{padding-block:clamp(56px,8vw,96px) 0}.portal-hero h1{font-size:clamp(48px,8vw,104px);line-height:.9}</style>
</head>
<body>
<div class="pv-bar">NÁHLED · Registrace a přihlášení zatím nic neodesílají, jde jen o ukázku vzhledu.</div>
''' + nav(t, cal) + f'''
<main id="top">
  <section class="portal-hero">
    <div class="wrap" style="display:grid;gap:18px">
      <p class="crumbs"><a href="/">HYROX Training Club</a> / <a href="/{SLUG}/">12 Weeks Race Prep</a> / Portál</p>
      <p class="eyebrow">Portál účastníků</p>
      <h1>12 Weeks<br>Race Prep.</h1>
    </div>
  </section>

  <section id="registrace">
    <div class="wrap">
      <div class="pt-wrap" id="pt-auth">
        <div class="pt-box">
          <div class="pt-tabs" role="tablist">
            <button role="tab" id="tab-reg" aria-selected="true" aria-controls="f-reg" type="button">Registrace</button>
            <button role="tab" id="tab-log" aria-selected="false" aria-controls="f-log" type="button">Přihlášení</button>
          </div>
          <form class="pt-form" id="f-reg" novalidate>
            <label for="r-name">Jméno a příjmení<input id="r-name" autocomplete="name" placeholder="Jan Novák" required></label>
            <label for="r-mail">E-mail<input id="r-mail" type="email" autocomplete="email" placeholder="jan@email.cz" required></label>
            <label for="r-pass">Heslo<input id="r-pass" type="password" autocomplete="new-password" placeholder="Alespoň 8 znaků" required></label>
            <label for="r-club">Domovský klub (nepovinné)<input id="r-club" placeholder="Na Knížecí, Vinohradská, Campus, Hrabová"></label>
            <label class="chk" for="r-gdpr"><input id="r-gdpr" type="checkbox"> Souhlasím se zpracováním osobních údajů pro účely programu.</label>
            <button class="btn btn-red" type="submit">Registrovat a pokračovat k platbě →</button>
            <small>Po zaplacení 8 999 Kč se ti portál odemkne a dostaneš e-mail s odkazem do WhatsApp komunity.</small>
          </form>
          <form class="pt-form" id="f-log" hidden novalidate>
            <label for="l-mail">E-mail<input id="l-mail" type="email" autocomplete="email" placeholder="jan@email.cz"></label>
            <label for="l-pass">Heslo<input id="l-pass" type="password" autocomplete="current-password"></label>
            <button class="btn btn-red" type="submit">Přihlásit se →</button>
            <small>Zapomenuté heslo? Pošleme ti odkaz na e-mail.</small>
          </form>
        </div>
        <div>
          <div class="sec-head" style="margin:0 0 20px">
            <h2>Jak to funguje</h2>
          </div>
          <div class="pt-steps">
            <div><span class="n">1</span><div><b>Zaregistruješ se</b><p>Jméno, e-mail, heslo. Za minutu máš účet.</p></div></div>
            <div><span class="n">2</span><div><b>Zaplatíš program</b><p>8 999 Kč jednou, za celých 12 týdnů.</p></div></div>
            <div><span class="n">3</span><div><b>Odemkne se portál</b><p>PDF průvodci, termíny workshopů a odkaz do komunity. Další materiály přibývají během programu.</p></div></div>
          </div>
          <p class="pt-toast" style="margin-top:20px">V náhledu stačí kliknout na „Registrovat“ nebo „Přihlásit se“ a uvidíš, jak portál vypadá po přihlášení.</p>
        </div>
      </div>

      <div class="pt-dash" id="pt-dash" hidden>
        <div class="pt-hello">
          <div>
            <p class="eyebrow">Přihlášen jako <span id="pt-who">Jan Novák</span></p>
            <h2>Vítej v programu.</h2>
          </div>
          <div class="pt-prog">
            <span>Týden 3 z 12</span>
            <div class="pt-bar" role="progressbar" aria-valuemin="0" aria-valuemax="12" aria-valuenow="3"><i style="width:25%"></i></div>
            <span>Další workshop: Mid-program check · týden 6</span>
          </div>
        </div>
        <div>
          <p class="eyebrow" style="margin-bottom:16px">Materiály ke stažení</p>
          <div class="pt-files">{files}</div>
        </div>
        <div class="pt-links">
          <a href="#" onclick="return false"><b>WhatsApp komunita</b><span>Uzavřená skupina účastníků a trenérů</span></a>
          <a href="#" onclick="return false"><b>Tréninková aplikace</b><span>Týdenní plán a edukační videa</span></a>
          <a href="{cal}" target="_blank" rel="noopener"><b>HYROX lekce ve FF</b><span>Rozvrh a rezervace →</span></a>
        </div>
        <p class="pt-toast" id="pt-msg" hidden></p>
        <div><button class="btn btn-ghost" type="button" id="pt-out">Odhlásit se</button></div>
      </div>
    </div>
  </section>
</main>
<script>
(function(){{
  var tabs={{reg:document.getElementById('tab-reg'),log:document.getElementById('tab-log')}};
  var forms={{reg:document.getElementById('f-reg'),log:document.getElementById('f-log')}};
  function show(k){{for(var x in tabs){{tabs[x].setAttribute('aria-selected',x===k);forms[x].hidden=x!==k;}}}}
  tabs.reg.onclick=function(){{show('reg')}}; tabs.log.onclick=function(){{show('log')}};
  if(location.hash==='#prihlaseni')show('log');
  function enter(name){{document.getElementById('pt-auth').hidden=true;document.getElementById('pt-dash').hidden=false;document.getElementById('pt-who').textContent=name||'Jan Novák';window.scrollTo(0,document.getElementById('registrace').offsetTop-80);}}
  forms.reg.onsubmit=function(e){{e.preventDefault();enter(document.getElementById('r-name').value.trim());}};
  forms.log.onsubmit=function(e){{e.preventDefault();enter('');}};
  document.getElementById('pt-out').onclick=function(){{document.getElementById('pt-dash').hidden=true;document.getElementById('pt-auth').hidden=false;}};
  var msg=document.getElementById('pt-msg');
  document.querySelectorAll('.dl').forEach(function(b){{b.onclick=function(){{msg.hidden=false;msg.textContent='Náhled: tady se ve skutečném portálu stáhne PDF „'+b.parentNode.querySelector('b').textContent+'“.';}}}});
}})();
</script>
''' + footer(net, FF_HYROX["cs"])
