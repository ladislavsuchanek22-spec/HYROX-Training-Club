"""STR2G HYROX 12 Weeks Race Prep: promo blok na hlavní stránce, stránka programu a portál účastníků.

Používá se z build.py. Texty všech jazyků jsou v raceprep_texts.py.
Portál: Netlify Identity (registrace jen na pozvánku) + funkce netlify/functions/portal-files.mjs.
"""
import json
from raceprep_texts import T as RT

SLUG = "12-weeks-race-prep"
PORTAL = "portal"
LANGS = ["cs", "en", "de", "pl"]

# Oficiální prodej programu na FF Academy. Až bude mít program vlastní stránku, stačí změnit tuhle adresu.
BUY = "https://www.ff-academy.cz/label/verejnost/add/hyrox/"
# Tréninková aplikace: Láďův profil na Strivee
STRIVEE = "https://train.strivee.app/p/str2g-hyrox"


def home(lang):
    return "/" if lang == "cs" else f"/{lang}/"


def path(lang, slug):
    return home(lang) + slug + "/"


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
.rp-bar{background:var(--red);text-align:center;padding:9px max(16px,env(safe-area-inset-left,0px))}
.rp-bar a{color:#fff;text-decoration:none;font:500 14px/1.35 var(--f-body)}
.rp-bar a b{font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.rp-bar a span{white-space:nowrap;text-decoration:underline;text-underline-offset:3px;margin-left:6px}
.rp-bar a:hover span{text-decoration-thickness:2px}
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
.rp-week .wsl{margin-left:8px;font:500 11px/1 var(--f-mono);letter-spacing:.08em;color:var(--blue);text-transform:uppercase}
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
.pt-dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(90px,1fr));gap:8px}
.pt-file.locked .btn{background:var(--surface-2);color:var(--muted);cursor:not-allowed}
.pt-links{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.pt-links a{border:1px solid var(--line);padding:18px;text-decoration:none;display:grid;gap:4px}
.pt-links a:hover{border-color:var(--blue)}
.pt-links b{font:700 20px/1.1 var(--f-display);text-transform:uppercase}
.pt-links span{color:var(--muted);font-size:14px}
@media (max-width:760px){.pt-links{grid-template-columns:1fr}}
.pt-toast{font:500 14px/1.4 var(--f-body);color:var(--fg);background:var(--surface-2);border-left:3px solid var(--blue);padding:12px 14px}
</style>"""

def bar(lang):
    s = RT[lang]
    return f'<div class="rp-bar"><a href="{path(lang, SLUG)}">{s["bar"]} <span>{s["bar_cta"]}</span></a></div>'


def nav_li(lang):
    return f'<li><a href="{path(lang, SLUG)}" class="rp-nav">12 Weeks</a></li>'


def promo(lang):
    s = RT[lang]
    facts = "".join(f"<div><strong>{n}</strong><span>{t}</span></div>" for n, t in s["facts"])
    return f"""
  <section class="rp-promo" aria-label="12 Weeks Race Prep">
    <div class="wrap">
      <div>
        <span class="rp-tag">{s["promo_tag"]}</span>
        <h2>HYROX 12 Weeks<br><span>Race Prep.</span></h2>
        <p class="lead">{s["promo_lead"]}</p>
        <div class="hero-cta">
          <a class="btn btn-red" href="{path(lang, SLUG)}">{s["promo_cta1"]}</a>
          <a class="btn btn-ghost" href="{BUY}" target="_blank" rel="noopener">{s["promo_cta2"]}</a>
        </div>
      </div>
      <div class="rp-facts">{facts}</div>
    </div>
  </section>
"""


def head(lang, slug, title, desc, site, robots="index,follow,max-image-preview:large"):
    url = site + path(lang, slug)
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{site}{path(l, slug)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{site}{path("cs", slug)}">'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="HYROX Training Club">
<meta property="og:locale" content="{RT[lang]["locale"]}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}/img/coaches.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
{alts}
<script src="/js/tracking.js"></script>
<link rel="icon" href="/favicon.png" type="image/png" sizes="160x160">
<link rel="apple-touch-icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
"""


def nav(lang, t, slug):
    s = RT[lang]
    langs = "".join(f'<a href="{path(l, slug)}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else "") + f'>{"CZ" if l == "cs" else l.upper()}</a>' for l in LANGS)
    return f"""<header class="nav">
  <div class="wrap">
    <a class="brand" href="{home(lang)}">
      <img src="/img/ff-logo.jpg" alt="Form Factory">
      <span><b>HYROX Training Club</b><small>{t["brand_sub"]}</small></span>
    </a>
    <ul>
      <li><a href="{path(lang, SLUG)}" class="rp-nav">12 Weeks</a></li>
      <li><a href="{path(lang, SLUG)}#obsah">{s["n_inc"]}</a></li>
      <li><a href="{path(lang, SLUG)}#cena">{s["n_price"]}</a></li>
      <li><a href="{path(lang, PORTAL)}">{s["n_portal"]}</a></li>
    </ul>
    <div class="nav-right">
      <nav class="langs" aria-label="Language">{langs}</nav>
      <a class="btn btn-red" href="{BUY}" target="_blank" rel="noopener" style="padding:11px 18px;font-size:15px">{s["n_buy"]}</a>
    </div>
  </div>
</header>
"""


def footer(lang, net, ff_hyrox):
    return f"""<footer>
  <div class="wrap">
    {net.block("htc", lang)}
    <span>HYROX Training Club · Form Factory × STR2G</span>
    <span><a href="{ff_hyrox}" target="_blank" rel="noopener">formfactory.cz/hyrox</a> · <a href="https://www.instagram.com/hyroxprague/" target="_blank" rel="noopener">@hyroxprague</a> · <a href="#" onclick="window.cookieSettings&&cookieSettings();return false">Cookies</a></span>
  </div>
</footer>
</body>
</html>
"""


def program_page(lang, T, STYLE, EXTRA_CSS, SITE, net, FF_HYROX):
    t, s = T[lang], RT[lang]
    cal = FF_HYROX[lang] + "#timetables"
    portal = path(lang, PORTAL)
    facts = "".join(f'<div class="stat"><strong>{n}</strong><span>{x}</span></div>' for n, x in s["facts"])
    who = "".join(f"<div><b>{a}</b><p>{b}</p></div>" for a, b in s["who"])
    inc = "".join(
        f'<article><span class="no">/ {i+1:02d}</span><h3>{h}</h3><p>{p}</p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></article>'
        for i, (h, p, li) in enumerate(s["included"]))
    wsl = f'<small class="wsl">{s["ws"]}</small>'
    weeks = ""
    for ph, rows in s["phases"]:
        weeks += f'<div class="rp-phase">{ph}</div>'
        weeks += "".join(f'<div class="rp-week{" ws" if ws else ""}"><span class="n">{n}</span><b>{f}{wsl if ws else ""}</b><span>{d}</span></div>' for n, f, d, ws in rows)
    price = "".join(f"<li>{x}</li>" for x in s["pr_list"])
    pdfs = "".join(f"<li>{p}</li>" for p in s["pdfs"])
    return head(lang, SLUG, s["title"], s["desc"], SITE) + STYLE + EXTRA_CSS + RP_CSS + """
<style>body{margin:0}[hidden]{display:none!important}.hero h1{font-size:clamp(52px,10vw,132px)}</style>
</head>
<body>
""" + nav(lang, t, SLUG) + f"""
<main id="top">
  <section class="hero">
    <div class="hero-img"><img src="/img/sled.webp" alt="{s["hero_alt"]}" style="object-position:center 55%"></div>
    <div class="wrap">
      <p class="crumbs"><a href="{home(lang)}">HYROX Training Club</a> / 12 Weeks Race Prep</p>
      <p class="eyebrow">{s["eyebrow"]}</p>
      <h1>HYROX<span>12 Weeks</span><em>Race Prep.</em></h1>
      <p class="lead">{s["lead"]}</p>
      <div class="hero-cta">
        <a class="btn btn-red" href="{BUY}" target="_blank" rel="noopener">{s["cta_buy"]}</a>
        <a class="btn btn-ghost" href="#obsah">{s["cta_more"]}</a>
      </div>
      <p class="cities"><b>Plan.</b> Train. <b>Perform.</b></p>
    </div>
  </section>

  <div class="stats" aria-label="{s["stats_label"]}"><div class="wrap">{facts}</div></div>

  <section class="rp-intro">
    <div class="wrap">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">{s["intro_eyebrow"]}</p>
        <h2>{s["intro_h"]}</h2>
        <p class="lead">{s["intro_lead"]}</p>
      </div>
      <div style="display:grid;gap:18px">
        <p>{s["intro_p1"]}</p>
        <p>{s["intro_p2"]}</p>
        <div class="rp-how">
          <b>{s["how_h"]}</b>
          <p>{s["how_p"].format(cal=cal)}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="programs">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{s["who_eyebrow"]}</p>
        <h2>{s["who_h"]}</h2>
      </div>
      <div class="rp-who">{who}</div>
    </div>
  </section>

  <section id="obsah">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{s["inc_eyebrow"]}</p>
        <h2>{s["inc_h"]}</h2>
        <p class="lead">{s["inc_lead"]}</p>
      </div>
      <div class="rp-inc">{inc}</div>
    </div>
  </section>

  <div class="lanes" aria-hidden="true"></div>

  <section class="race">
    <div class="wrap">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">{s["wk_eyebrow"]}</p>
        <h2>{s["wk_h"]}</h2>
        <p class="lead">{s["wk_lead"]}</p>
      </div>
      <div class="rp-weeks">{weeks}</div>
    </div>
  </section>

  <section class="rp-price programs" id="cena">
    <div class="wrap">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">{s["pr_eyebrow"]}</p>
        <h2>{s["pr_h"]}</h2>
        <p class="lead">{s["pr_lead"]}</p>
        <div class="rp-card">
          <span class="rp-tag" style="margin:0;width:max-content">12 Weeks Race Prep</span>
          <div class="amt">{s["price"]}<small>{s["cur"]}</small></div>
          <p>{s["pr_desc"]}</p>
          <a class="btn btn-red" href="{BUY}" target="_blank" rel="noopener" style="justify-content:center">{s["cta_buy"]}</a>
          <p style="font-size:14px">{s["pr_sale"].format(portal=portal)}</p>
        </div>
      </div>
      <div>
        <p class="eyebrow" style="margin-bottom:16px">{s["pr_incl"]}</p>
        <ul class="rp-list">{price}</ul>
        <p class="rp-note">{s["pr_note"]}</p>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap rp-portal-teaser">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">{s["pt_eyebrow"]}</p>
        <h2>{s["pt_h"]}</h2>
        <p class="lead">{s["pt_lead"]}</p>
        <div class="hero-cta"><a class="btn btn-ghost" href="{portal}">{s["pt_btn"]}</a></div>
      </div>
      <div class="rp-how">
        <b>{s["pt_pdf"]}</b>
        <ul class="rp-list" style="border-top:0">{pdfs}</ul>
      </div>
    </div>
  </section>

  <section class="programs">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{s["co_eyebrow"]}</p>
        <h2>{s["co_h"]}</h2>
        <p class="lead">{s["co_lead"]}</p>
      </div>
      <div class="rp-coaches">
        <article><img loading="lazy" src="/img/coach-ria.webp?v=2" alt="Ria Suchánek Hrušovská"><div><span>{s["ria_role"]}</span><b>Ria Suchánek Hrušovská</b><p>{s["ria_txt"]}</p></div></article>
        <article><img loading="lazy" src="/img/coach-lada.webp?v=2" alt="Ladislav Suchánek"><div><span>{s["lada_role"]}</span><b>Ladislav Suchánek</b><p>{s["lada_txt"]}</p></div></article>
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="wrap">
      <p class="eyebrow">{s["cta_eyebrow"]}</p>
      <h2>{s["cta_h"]}</h2>
      <p class="lead">{s["cta_lead"]}</p>
      <div class="cta-row">
        <a class="btn btn-red" href="{BUY}" target="_blank" rel="noopener">{s["cta_buy"]}</a>
        <a class="btn btn-ghost" href="{portal}">{s["cta_b2"]}</a>
      </div>
    </div>
  </section>
</main>
""" + footer(lang, net, FF_HYROX[lang])


PORTAL_JS = r"""
import { getUser, login, logout, handleAuthCallback, acceptInvite, requestPasswordRecovery, updateUser } from "https://cdn.jsdelivr.net/npm/@netlify/identity@2.0.0/+esm";
const L = JSON.parse(document.getElementById("pt-i18n").textContent);
const $ = (id) => document.getElementById(id);
if (location.hostname.startsWith("deploy-preview-")) $("pv-bar").hidden = false;
function view(name) { for (const v of ["pt-loading","pt-auth","pt-setpass","pt-dash"]) $(v).hidden = v !== name; }
function err(el, e) { el.hidden = false; el.textContent = e; }
const tabs = { log: [$("tab-log"), $("f-log")], forgot: [$("tab-forgot"), $("f-forgot")] };
function tab(k) { for (const [n, [b, f]] of Object.entries(tabs)) { b.setAttribute("aria-selected", n === k); f.hidden = n !== k; } }
$("tab-log").onclick = () => tab("log"); $("tab-forgot").onclick = () => tab("forgot");
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[c]);
const loc = (f, k) => (f.i18n && f.i18n[L.lang] && f.i18n[L.lang][k]) || f[k];
const order = (langs) => L.lang === "cs" ? langs : [...langs].sort((a, b) => (a === "en" ? -1 : b === "en" ? 1 : 0));

async function dashboard(user) {
  view("pt-dash");
  $("pt-who").textContent = user.name || user.email;
  try {
    const r = await fetch("/api/portal-files", { credentials: "same-origin", cache: "no-store" });
    if (!r.ok) throw new Error(r.status);
    const data = await r.json();
    $("pt-files").innerHTML = data.files.map((f) => {
      const langs = order(f.langs || []);
      const meta = f.available ? "PDF · " + langs.map((l) => L.langs[l] || l).join(" / ") : esc(loc(f, "note") || L.soon);
      const btns = f.available
        ? `<div class="pt-dl">${langs.map((l) => `<a class="btn btn-red" href="/api/portal-files?f=${encodeURIComponent(f.id)}&lang=${l}">${l === "cs" ? "CZ" : l.toUpperCase()} ↓</a>`).join("")}</div>`
        : `<button class="btn" type="button" disabled>${esc(L.locked)}</button>`;
      return `<div class="pt-file${f.available ? "" : " locked"}"><span class="ic">${esc(f.no || "PDF")}</span><b>${esc(loc(f, "name"))}</b><p>${esc(loc(f, "desc"))}</p><span class="meta">${meta}</span>${btns}</div>`;
    }).join("");
  } catch (e) { err($("d-err"), L.load); }
}

let pending = null;
$("f-set").onsubmit = async (e) => {
  e.preventDefault(); $("s-err").hidden = true;
  const p1 = $("s-pass").value, p2 = $("s-pass2").value;
  if (p1.length < 8) return err($("s-err"), L.short);
  if (p1 !== p2) return err($("s-err"), L.mismatch);
  try {
    const user = pending.type === "invite" ? await acceptInvite(pending.token, p1) : await updateUser({ password: p1 });
    history.replaceState(null, "", location.pathname);
    dashboard(user || await getUser());
  } catch (x) { err($("s-err"), L.save); }
};
$("f-log").onsubmit = async (e) => {
  e.preventDefault(); $("l-err").hidden = true;
  try { dashboard(await login($("l-mail").value.trim(), $("l-pass").value)); }
  catch (x) { err($("l-err"), L.login); }
};
$("f-forgot").onsubmit = async (e) => {
  e.preventDefault(); $("r-ok").hidden = true;
  try { await requestPasswordRecovery($("r-mail").value.trim()); } catch (x) {}
  $("r-ok").hidden = false;
};
$("pt-out").onclick = async () => { try { await logout(); } finally { view("pt-auth"); } };

(async () => {
  try {
    const cb = await handleAuthCallback();
    if (cb && cb.type === "invite") { pending = { type: "invite", token: cb.token }; view("pt-setpass"); return; }
    if (cb && cb.type === "recovery") { pending = { type: "recovery" }; $("set-title").textContent = L.rec_eyebrow; $("set-h").textContent = L.rec_h; view("pt-setpass"); return; }
  } catch (e) {}
  const user = await getUser();
  if (user) dashboard(user); else view("pt-auth");
})().catch(() => view("pt-auth"));
"""


def portal_page(lang, T, STYLE, EXTRA_CSS, SITE, net, FF_HYROX):
    t, s = T[lang], RT[lang]
    cal = FF_HYROX[lang] + "#timetables"
    i18n = dict(s["js"], lang=lang, rec_eyebrow=s["p_rec_eyebrow"], rec_h=s["p_rec_h"])
    return head(lang, PORTAL, s["p_title"], s["p_desc"], SITE, robots="noindex,nofollow") + STYLE + EXTRA_CSS + RP_CSS + """
<style>body{margin:0}[hidden]{display:none!important}.portal-hero{padding-block:clamp(56px,8vw,96px) 0}.portal-hero h1{font-size:clamp(48px,8vw,104px);line-height:.9}.pt-err{color:#ff8a9c;font-size:14px}.pt-ok{color:#9be3b0;font-size:14px}</style>
</head>
<body>
""" + f'<div class="pv-bar" id="pv-bar" hidden>{s["p_bar"]}</div>\n' + nav(lang, t, PORTAL) + f"""
<main id="top">
  <section class="portal-hero">
    <div class="wrap" style="display:grid;gap:18px">
      <p class="crumbs"><a href="{home(lang)}">HYROX Training Club</a> / <a href="{path(lang, SLUG)}">12 Weeks Race Prep</a> / {s["p_crumb"]}</p>
      <p class="eyebrow">{s["p_eyebrow"]}</p>
      <h1>12 Weeks<br>Race Prep.</h1>
    </div>
  </section>

  <section id="registrace">
    <div class="wrap">
      <p class="pt-toast" id="pt-loading">{s["p_loading"]}</p>

      <div class="pt-wrap" id="pt-auth" hidden>
        <div class="pt-box">
          <div class="pt-tabs" role="tablist">
            <button role="tab" id="tab-log" aria-selected="true" aria-controls="f-log" type="button">{s["p_tab_login"]}</button>
            <button role="tab" id="tab-forgot" aria-selected="false" aria-controls="f-forgot" type="button">{s["p_tab_forgot"]}</button>
          </div>
          <form class="pt-form" id="f-log">
            <label for="l-mail">{s["p_email"]}<input id="l-mail" type="email" autocomplete="email" placeholder="{s["p_email_ph"]}" required></label>
            <label for="l-pass">{s["p_pass"]}<input id="l-pass" type="password" autocomplete="current-password" required></label>
            <button class="btn btn-red" type="submit">{s["p_login_btn"]}</button>
            <p class="pt-err" id="l-err" hidden></p>
          </form>
          <form class="pt-form" id="f-forgot" hidden>
            <label for="r-mail">{s["p_email"]}<input id="r-mail" type="email" autocomplete="email" placeholder="{s["p_email_ph"]}" required></label>
            <button class="btn btn-red" type="submit">{s["p_forgot_btn"]}</button>
            <p class="pt-ok" id="r-ok" hidden>{s["p_forgot_ok"]}</p>
          </form>
        </div>
        <div>
          <div class="sec-head" style="margin:0 0 20px"><h2>{s["p_steps_h"]}</h2></div>
          <div class="pt-steps">
            <div><span class="n">1</span><div><b>{s["p_s1h"]}</b><p>{s["p_s1p"].format(buy=BUY)}</p></div></div>
            <div><span class="n">2</span><div><b>{s["p_s2h"]}</b><p>{s["p_s2p"]}</p></div></div>
            <div><span class="n">3</span><div><b>{s["p_s3h"]}</b><p>{s["p_s3p"]}</p></div></div>
          </div>
        </div>
      </div>

      <div class="pt-wrap" id="pt-setpass" hidden>
        <div class="pt-box">
          <form class="pt-form" id="f-set">
            <p class="eyebrow" id="set-title">{s["p_set_eyebrow"]}</p>
            <h2 style="font-size:36px" id="set-h">{s["p_set_h"]}</h2>
            <label for="s-pass">{s["p_newpass"]}<input id="s-pass" type="password" autocomplete="new-password" minlength="8" placeholder="{s["p_pass_ph"]}" required></label>
            <label for="s-pass2">{s["p_again"]}<input id="s-pass2" type="password" autocomplete="new-password" minlength="8" required></label>
            <button class="btn btn-red" type="submit">{s["p_set_btn"]}</button>
            <p class="pt-err" id="s-err" hidden></p>
          </form>
        </div>
      </div>

      <div class="pt-dash" id="pt-dash" hidden>
        <div class="pt-hello">
          <div>
            <p class="eyebrow">{s["p_logged"]} <span id="pt-who"></span></p>
            <h2>{s["p_welcome"]}</h2>
          </div>
          <button class="btn btn-ghost" type="button" id="pt-out">{s["p_logout"]}</button>
        </div>
        <div>
          <p class="eyebrow" style="margin-bottom:16px">{s["p_files"]}</p>
          <div class="pt-files" id="pt-files"></div>
          <p class="pt-err" id="d-err" hidden></p>
        </div>
        <div class="pt-links">
          <a href="#" onclick="return false"><b>{s["p_wa_h"]}</b><span>{s["p_wa_p"]}</span></a>
          <a href="{STRIVEE}" target="_blank" rel="noopener"><b>{s["p_app_h"]}</b><span>{s["p_app_p"]}</span></a>
          <a href="{cal}" target="_blank" rel="noopener"><b>{s["p_ff_h"]}</b><span>{s["p_ff_p"]}</span></a>
        </div>
      </div>
    </div>
  </section>
</main>
<script type="application/json" id="pt-i18n">{json.dumps(i18n, ensure_ascii=False).replace("</", "<\\/")}</script>
<script type="module">{PORTAL_JS}</script>
""" + footer(lang, net, FF_HYROX[lang])
