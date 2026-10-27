#!/usr/bin/env python3
"""Generate the HYROX Training Club site in CZ, EN, DE, PL.
Usage: python3 build.py <style.css> <out_dir>
"""
import sys, os, html, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import net

STYLE = open(sys.argv[1]).read().replace('url("img/sled.webp")', 'url("/img/sled.webp")')
OUT = sys.argv[2]

EXTRA_CSS = """<style>
.langs{display:flex;gap:2px;border:1px solid var(--line)}
.langs a{font:600 13px/1 var(--f-mono);letter-spacing:.06em;text-decoration:none;color:var(--muted);padding:8px 8px}
.langs a:hover{color:var(--fg)}
.langs a[aria-current]{background:var(--fg);color:var(--bg)}
.nav-right{display:flex;align-items:center;gap:12px}
@media (max-width:1100px){.brand small{display:none}}
@media (max-width:520px){.nav .btn{display:none}.langs a{padding:7px 6px;font-size:12px}}
.lead a{color:var(--fg);text-decoration-color:var(--red-hi);text-underline-offset:3px}
.coach .site{font:500 13px/1.3 var(--f-mono);color:var(--red-hi);text-decoration:none}
.coach .site:hover{text-decoration:underline}
.coach-grid{grid-template-columns:repeat(3,1fr)!important}
.coach{align-content:start}
.coach .ph{display:block;margin:-28px -28px 6px;overflow:hidden;background:var(--surface-2)}
.coach .ph img{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:center 20%}
.coach h3 .aka{display:block;margin-top:6px;font:500 13px/1 var(--f-mono);letter-spacing:.08em;color:var(--muted);text-transform:none}
@media (max-width:960px){.coach-grid{grid-template-columns:1fr!important}.coach .ph img{aspect-ratio:4/3;object-position:center 25%}}
.prog-note a{color:var(--fg);text-decoration-color:var(--red-hi);text-underline-offset:3px}
.net{flex-basis:100%;padding-bottom:24px;margin-bottom:8px;border-bottom:1px solid var(--line)}
.net-h{margin:0 0 14px;font:500 12px/1 var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.net ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px 24px}
.net a{display:grid;gap:3px;text-decoration:none;color:var(--fg)}
.net b{font:700 20px/1.05 var(--f-display);text-transform:uppercase;letter-spacing:.02em}
.net span{font-size:14px;line-height:1.35;color:var(--muted)}
.net i{font:500 12px/1.2 var(--f-mono);font-style:normal;color:var(--muted)}
.net a:hover b{color:var(--red-hi)}
.hero h1 .h1-sub{display:block;margin-top:22px;font:600 15px/1.35 var(--f-body);letter-spacing:.14em;text-transform:uppercase;color:var(--fg);-webkit-text-stroke:0}
.club-more{display:inline-block;margin-top:14px;font:500 13px/1.3 var(--f-mono);color:var(--red-hi);text-decoration:none}
.club-more:hover{text-decoration:underline}
.city-faq details{border-top:1px solid var(--line);padding:16px 0}
.city-faq summary{cursor:pointer;font:700 20px/1.2 var(--f-display);text-transform:uppercase}
.city-faq p{color:var(--muted);max-width:720px}
.crumbs{font:500 12px/1 var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 18px}
.crumbs a{color:var(--muted)}
.city-other{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
</style>"""

LANGS = ["cs", "en", "de", "pl"]
PATH = {"cs": "/", "en": "/en/", "de": "/de/", "pl": "/pl/"}
LABEL = {"cs": "CZ", "en": "EN", "de": "DE", "pl": "PL"}
SITE = "https://hyroxtrainingclub.cz"

T = {}

T["cs"] = dict(
  h1_sub="Skupinové HYROX tréninky v Praze, Brně a Ostravě",
  title="HYROX Training Club Praha, Brno, Ostrava | Form Factory",
  meta_desc="Oficiální HYROX Training Club ve Form Factory. HYROX trénink v Praze, Brně a Ostravě podle programu HYROX365. Skupinové lekce s HYROX trenéry, pro začátečníky i závodníky.",
  og_locale="cs_CZ",
  og_desc="Trénink podle oficiálního programu HYROX365. Praha, Brno, Ostrava.",
  brand_sub="Form Factory · Praha · Brno · Ostrava",
  nav_prog="Programy", nav_race="Závod", nav_coach="Trenéři", nav_clubs="Kluby", nav_book="Rezervovat",
  hero_eyebrow="Oficiální HYROX Training Club",
  hero_lead="Trénink podle oficiálního programu HYROX365. Běh, síla, stanice a práce pod únavou. Vedou tě trenéři, kteří závodí sami. Žádný náhodný workout, ale plán, který má směr.",
  hero_cta1="Vybrat lekci →", hero_cta2="Najít klub",
  cities='<b>Praha</b> Na Knížecí · Vinohradská &nbsp;/&nbsp; <b>Brno</b> Campus &nbsp;/&nbsp; <b>Ostrava</b> Hrabová',
  hero_alt="Trenér vede briefing před HYROX simulací ve Form Factory",
  stats_label="HYROX v číslech",
  st1="běhu v závodě", st2="funkčních stanic", st3="tréninkové směry HYROX365", st4="kluby Form Factory",
  ab_eyebrow="Co je HYROX Training Club",
  ab_h="Trénink se strukturou. Ne jen těžký.",
  ab_p1="<strong>HYROX Training Club je akreditované místo, kde se trénuje podle oficiálního programu HYROX.</strong> Lekce nevymýšlíme z hlavy. Stojí na metodice HYROX365, kterou vytvořil přímo HYROX, a na zkušenostech trenérů, kteří závody sami jezdí.",
  ab_p2="HYROX překládá principy závodu do tréninku pro každého. Nemusíš mířit na start. Stačí chtít být silnější, vydržet víc a vidět, že se posouváš. A když na start míříš, budeš připravený.",
  p1h="Běh", p1t="Tempo, které udržíš i po saních.",
  p2h="Síla", p2t="Taková, co funguje pod únavou.",
  p3h="Stanice", p3t="Technika, která šetří sekundy i energii.",
  p4h="Hlava", p4t="Zabrat, vydržet, nepustit se.",
  ab_alt="Sportovci po benchmark testu na běžeckých drahách klubu",
  ab_cap="Benchmark test · Form Factory Na Knížecí",
  pr_eyebrow="HYROX365 Group Training", pr_h="Čtyři směry. Jeden výkon.",
  pr_lead="Lidi nejsou stejní, takže jedna lekce nesedne všem. HYROX365 proto pracuje se čtyřmi formáty. Každý rozvíjí jinou část výkonu, dohromady tě připraví na závod i na život mimo fitko.",
  int="Intenzita", who="Pro koho:",
  f_tag="Základ", f_claim="Kruhový trénink, který má smysl.",
  f_l1="síla a vytrvalost v jednom", f_l2="aerobní kapacita", f_l3="technika, obratnost, mobilita",
  f_who="pro začátečníky ideální, pro pokročilé pořád poctivá práce. Škáluje se na každou úroveň.",
  e_tag="Kondice", e_claim="Větší motor. Delší výkon.",
  e_l1="aerobní výkon a tempo", e_l2="laktátový práh a tolerance", e_l3="efektivita na ergometrech",
  e_who="pro silné lidi, kterým chybí výdrž, běh nebo jistota na SkiErgu a veslu.",
  p_tag="Síla", p_claim="Síla, která drží i v 7. kilometru.",
  p_l1="maximální a opakovaná síla", p_l2="silová vytrvalost a výbušnost", p_l3="práce se zátěží v čase",
  p_who="pro běžce a vytrvalce, kterým na saních, výpadech a farmers carry dochází síla.",
  c_tag="Race-specific", c_claim="HYROX v tréninkové podobě.",
  c_l1="běh, stanice a přechody", c_l2="kondice a síla zároveň", c_l3="závodní rytmus a hlava",
  c_who="pro každého, kdo má datum závodu v kalendáři a chce vědět, co ho čeká.",
  pr_note="<b>Směr si nevybíráš, program ho střídá za tebe.</b> Přijdeš na lekci a trenér ví, na čem se dnes pracuje. V průběhu týdnů projdeš základem, kondicí, silou i závodním propojením. Přesně tak se staví výkon, který vydrží celých 8 kilometrů.",
  rc_eyebrow="Formát závodu", rc_h="8× 1 km běhu. 8× stanice.",
  rc_lead="Pořadí je na každém závodě světa stejné. Proto se na něj dá cíleně připravit. A proto u nás každý trénink odněkud vychází a někam vede.",
  rc_alt="Závodnice na stanicích Sled Pull, Sandbag Lunges a Wall Balls",
  track_label="Pořadí stanic v závodě HYROX", reps="opak.",
  t1h="Rozhoduje běh", t1t="Polovina času v závodě je běh. Kdo neumí běžet po stanici, ztrácí na každém kilometru.",
  t2h="Přechody a tempo", t2t="Roxzone, nástup do stanice, první kroky po saních. Tady se ztrácí minuty, které nikdo nevidí.",
  t3h="Hlava na konci", t3t="Wall balls po 7 km běhu jsou jiný cvik než čerstvý. Trénujeme práci pod únavou, ne jen sílu.",
  hw_alt="Head coach Ria hecuje skupinu během HYROX simulace",
  hw_eyebrow="Jak to funguje", hw_h="Přijdeš. Zabereš. Posuneš se.",
  s1h="Rezervuješ lekci", s1t="V aplikaci Moje Form Factory nebo na webu. Lekce jsou součástí členství.",
  s2h="Trenér vede, ty makáš", s2t="Rozcvička, technika, hlavní blok. Váhy a tempo se upraví podle tvé úrovně.",
  s3h="Měříš progres", s3t="Benchmark testy a simulace ukážou, kde jsi teď a co se za pár týdnů změnilo.",
  w1h="Začínáš", w1t="Nepotřebuješ zkušenost ani formu. Potřebuješ přijít.",
  w2h="Jsi silový", w2t="Přidáme výdrž a běh, aby ti síla nedošla v půlce.",
  w3h="Běháš", w3t="Přidáme sílu, aby tě saně nezastavily.",
  w4h="Chystáš se na závod", w4t="Dostaneš strukturu, tempo a plán na závodní den.",
  co_eyebrow="Trenéři", co_h="Učí to lidi, kteří to sami jezdí.",
  co_lead="Za HYROX Training Clubem stojí tým STR2G (Stronger Together). Trénujeme, závodíme a víme, jak bolí sedmý kilometr.",
  co_alt="Ria Suchánek Hrušovská a Ladislav Suchánek na HYROX závodě",
  ria_role="Head coach · HYROX Performance Coach",
  ria_txt="Head coach HYROX Training Clubu, trenérka a závodnice. Stojí za tréninkovou metodikou klubů. Technika, stabilita a hlava. Ví, jak dostat ze skupiny energii a z každého jednotlivce maximum, aniž by se rozbil.",
  lada_role="Coach · HYROX Performance Coach",
  lada_txt="Trenér a aktivní HYROX závodník. Spojuje sílu, kondici, běh a mentální přípravu do tréninku, který dává smysl. Trénuje lidi v klubech i online po celém světě.",
  mich_role='Coach · Les Mills &amp; HYROX', mich_txt='Sport má v sobě od dětství. Deset let závodně plaval, vystudoval FTVS v Praze a pak zakotvil ve fitness. Od roku 2012 vede Les Mills lekce BODYPUMP, BODYCOMBAT, BODYBALANCE a GRIT a jako assessor pomáhá novým instruktorům na jejich cestě. V roce 2026 naplno propadl HYROXu: závodí a vede skupinové lekce ve Form Factory. Nejvíc ho baví pocit totálně zničeného těla po tréninku, který člověka posune zase o kus dál.', mich_chip='HYROX závodník', ph_ria='Ria Suchánek Hrušovská vede HYROX lekci', ph_lada='Ladislav Suchánek na HYROX závodě', ph_mich='Michal Holotík ve Form Factory',
  chip_mental="Mental Coach", chip_nutri="Nutrition Specialist", chip_run="Running Coach", chip_mass="Sportovní masér",
  cl_eyebrow="Kde trénujeme", cl_h="Čtyři kluby. Tři města.",
  cl_lead="Všechny kluby mají HYROX zónu se saněmi, SkiErgy, vesly a běžeckými drahami. Po tréninku sauna, ta je v ceně členství.",
  addr="Adresa", open="Otevřeno", contact="Kontakt", sched="Rozvrh", map="Mapa",
  wk="Po–Pá", we="So–Ne",
  prague5="Praha 5 · Nový Smíchov", prague3="Praha 3 · Vinohrady", brno="Brno · Starý Lískovec", ostrava="Ostrava · Hrabová",
  gal_label="Fotky z klubu",
  g1="Společná fotka členů HYROX Training Clubu", g2="Sled push v HYROX zóně Form Factory", g3="Po benchmark testu", g4="Členové HYROX Training Clubu po tréninku",
  cta_eyebrow="První lekce",
  cta_lead="Vezmi si tenisky, ručník a pití. Přijď pár minut dřív. Zbytek uděláme spolu.",
  cta_b1="Rezervovat lekci →", cta_b2="První vstup do Form Factory",
  lada_link='Osobní trénink a online coaching · hyrox-prague.eu →', ria_link='Mentální koučink · riahrusovska.cz →', co_more='Online programy STR2G →', ffg_b='Form Factory Games · 5. 12. 2026', ffg_t='Vyzkoušej si závodní den naostro. Individuální závod ve Form Factory Vinohradská: tři workouty, čtyři kategorie, 100 atletů.', ffg_link='Více o závodě →',
)

T["en"] = dict(
  h1_sub="HYROX group classes in Prague, Brno and Ostrava",
  title="HYROX Training Club Prague, Brno, Ostrava | Form Factory",
  meta_desc="Official HYROX Training Club at Form Factory. HYROX training in Prague, Brno and Ostrava on the HYROX365 programme. Group classes with HYROX coaches, for beginners and racers.",
  og_locale="en_GB",
  og_desc="Training on the official HYROX365 programme. Prague, Brno, Ostrava.",
  brand_sub="Form Factory · Prague · Brno · Ostrava",
  nav_prog="Programmes", nav_race="The race", nav_coach="Coaches", nav_clubs="Clubs", nav_book="Book",
  hero_eyebrow="Official HYROX Training Club",
  hero_lead="Training on the official HYROX365 programme. Running, strength, stations and work under fatigue. Coached by people who race themselves. Not a random workout. A plan with a direction.",
  hero_cta1="Book a class →", hero_cta2="Find a club",
  cities='<b>Prague</b> Na Knížecí · Vinohradská &nbsp;/&nbsp; <b>Brno</b> Campus &nbsp;/&nbsp; <b>Ostrava</b> Hrabová',
  hero_alt="Coach giving a briefing before a HYROX simulation at Form Factory",
  stats_label="HYROX in numbers",
  st1="of running in a race", st2="functional stations", st3="HYROX365 training focuses", st4="Form Factory clubs",
  ab_eyebrow="What is a HYROX Training Club",
  ab_h="Training with structure. Not just hard.",
  ab_p1="<strong>A HYROX Training Club is an accredited gym that trains on the official HYROX programme.</strong> We don't make sessions up on the spot. They're built on the HYROX365 method, created by HYROX itself, and on coaches who race.",
  ab_p2="HYROX turns race principles into training for everyone. You don't need a start line in mind. You just need to want to get stronger, last longer and see yourself improve. And if you are aiming for a race, you'll be ready.",
  p1h="Run", p1t="A pace you can hold even after the sled.",
  p2h="Strength", p2t="The kind that works when you're tired.",
  p3h="Stations", p3t="Technique that saves seconds and energy.",
  p4h="Head", p4t="Push, hold on, don't let go.",
  ab_alt="Athletes after a benchmark test on the club's running lanes",
  ab_cap="Benchmark test · Form Factory Na Knížecí",
  pr_eyebrow="HYROX365 Group Training", pr_h="Four focuses. One performance.",
  pr_lead="People aren't the same, so one class can't fit everyone. That's why HYROX365 uses four formats. Each builds a different part of performance. Together they get you ready for race day and for life outside the gym.",
  int="Intensity", who="Who it's for:",
  f_tag="Base", f_claim="Circuit training with a purpose.",
  f_l1="strength and endurance in one", f_l2="aerobic capacity", f_l3="technique, agility, mobility",
  f_who="ideal for beginners, still honest work for advanced athletes. Scales to every level.",
  e_tag="Conditioning", e_claim="Bigger engine. Longer output.",
  e_l1="aerobic power and pacing", e_l2="lactate threshold and tolerance", e_l3="efficiency on the ergs",
  e_who="strong people who lack endurance, running or confidence on the SkiErg and rower.",
  p_tag="Strength", p_claim="Strength that holds at kilometre 7.",
  p_l1="max and repeated strength", p_l2="strength endurance and power", p_l3="moving load over time",
  p_who="runners and endurance athletes who run out of strength on the sled, lunges and farmers carry.",
  c_tag="Race-specific", c_claim="HYROX in training form.",
  c_l1="running, stations and transitions", c_l2="conditioning and strength together", c_l3="race rhythm and mindset",
  c_who="anyone with a race date in the calendar who wants to know what's coming.",
  pr_note="<b>You don't pick the focus. The programme rotates it for you.</b> You show up and the coach knows what today is about. Over the weeks you go through base, conditioning, strength and race-specific work. That's how you build performance that lasts all 8 kilometres.",
  rc_eyebrow="Race format", rc_h="8× 1 km run. 8× station.",
  rc_lead="The order is the same at every race in the world. So you can prepare for it on purpose. And that's why every session here starts somewhere and leads somewhere.",
  rc_alt="Athletes on the Sled Pull, Sandbag Lunges and Wall Balls stations",
  track_label="Station order in a HYROX race", reps="reps",
  t1h="Running decides", t1t="Half of your race time is running. If you can't run after a station, you lose time on every kilometre.",
  t2h="Transitions and pacing", t2t="The Roxzone, getting into a station, the first steps after the sled. That's where the minutes nobody sees go.",
  t3h="The head at the end", t3t="Wall balls after 7 km of running are a different exercise than fresh. We train work under fatigue, not just strength.",
  hw_alt="Head coach Ria firing up the group during a HYROX simulation",
  hw_eyebrow="How it works", hw_h="Show up. Work. Improve.",
  s1h="Book a class", s1t="In the Moje Form Factory app or online. Classes are included in the membership.",
  s2h="The coach leads, you work", s2t="Warm-up, technique, main block. Weights and pace are scaled to your level.",
  s3h="Track your progress", s3t="Benchmark tests and simulations show where you are now and what changed after a few weeks.",
  w1h="Just starting", w1t="You don't need experience or fitness. You need to show up.",
  w2h="Strength athlete", w2t="We add endurance and running so your strength doesn't fade halfway.",
  w3h="Runner", w3t="We add strength so the sled doesn't stop you.",
  w4h="Preparing for a race", w4t="You get structure, pacing and a plan for race day.",
  co_eyebrow="Coaches", co_h="Coached by people who race it.",
  co_lead="The HYROX Training Club is run by team STR2G (Stronger Together). We train, we race, and we know how kilometre seven feels.",
  co_alt="Ria Suchánek Hrušovská and Ladislav Suchánek at a HYROX race",
  ria_role="Head coach · HYROX Performance Coach",
  ria_txt="Head coach of the HYROX Training Club, coach and athlete. She's behind the clubs' training method. Technique, stability and mindset. She knows how to get energy out of a group and the most out of every individual without breaking them.",
  lada_role="Coach · HYROX Performance Coach",
  lada_txt="Coach and active HYROX racer. He combines strength, conditioning, running and mental preparation into training that makes sense. Coaches athletes in the clubs and online worldwide.",
  mich_role='Coach · Les Mills &amp; HYROX', mich_txt='Sport has been part of his life since childhood. Ten years of competitive swimming, a sports degree from FTVS in Prague, then the world of fitness. Since 2012 he has taught Les Mills BODYPUMP, BODYCOMBAT, BODYBALANCE and GRIT, and as an assessor he helps new instructors on their way. In 2026 he fell hard for HYROX: he races and coaches group classes at Form Factory. What he loves most is the feeling of a completely wrecked body after a session that moves you another step forward.', mich_chip='HYROX athlete', ph_ria='Ria Suchánek Hrušovská coaching a HYROX class', ph_lada='Ladislav Suchánek at a HYROX race', ph_mich='Michal Holotík at Form Factory',
  chip_mental="Mental Coach", chip_nutri="Nutrition Specialist", chip_run="Running Coach", chip_mass="Sports massage therapist",
  cl_eyebrow="Where we train", cl_h="Four clubs. Three cities.",
  cl_lead="Every club has a HYROX zone with sleds, SkiErgs, rowers and running lanes. Sauna after training, included in the membership.",
  addr="Address", open="Opening hours", contact="Contact", sched="Timetable", map="Map",
  wk="Mon–Fri", we="Sat–Sun",
  prague5="Prague 5 · Nový Smíchov", prague3="Prague 3 · Vinohrady", brno="Brno · Starý Lískovec", ostrava="Ostrava · Hrabová",
  gal_label="Photos from the club",
  g1="Group photo of HYROX Training Club members", g2="Sled push in the Form Factory HYROX zone", g3="After the benchmark test", g4="HYROX Training Club members after training",
  cta_eyebrow="First class",
  cta_lead="Bring trainers, a towel and a drink. Come a few minutes early. We'll do the rest together.",
  cta_b1="Book a class →", cta_b2="First visit to Form Factory",
  lada_link='Personal training and online coaching · hyrox-prague.eu →', ria_link='Mental coaching · riahrusovska.cz →', co_more='STR2G online programs →', ffg_b='Form Factory Games · 5 Dec 2026', ffg_t='Try race day for real. An individual competition at Form Factory Vinohradská: three workouts, four divisions, 100 athletes.', ffg_link='About the race →',
)

T["de"] = dict(
  h1_sub="HYROX-Gruppentraining in Prag, Brünn und Ostrava",
  title="HYROX Training Club Prag, Brünn, Ostrava | Form Factory",
  meta_desc="Offizieller HYROX Training Club bei Form Factory. HYROX-Training in Prag, Brünn und Ostrava nach dem HYROX365-Programm. Gruppentraining mit HYROX-Coaches, für Einsteiger und Athleten.",
  og_locale="de_DE",
  og_desc="Training nach dem offiziellen HYROX365-Programm. Prag, Brünn, Ostrava.",
  brand_sub="Form Factory · Prag · Brünn · Ostrava",
  nav_prog="Programme", nav_race="Das Rennen", nav_coach="Coaches", nav_clubs="Clubs", nav_book="Buchen",
  hero_eyebrow="Offizieller HYROX Training Club",
  hero_lead="Training nach dem offiziellen HYROX365-Programm. Laufen, Kraft, Stationen und Arbeit unter Ermüdung. Gecoacht von Leuten, die selbst Rennen laufen. Kein zufälliges Workout, sondern ein Plan mit Richtung.",
  hero_cta1="Kurs buchen →", hero_cta2="Club finden",
  cities='<b>Prag</b> Na Knížecí · Vinohradská &nbsp;/&nbsp; <b>Brünn</b> Campus &nbsp;/&nbsp; <b>Ostrava</b> Hrabová',
  hero_alt="Coach beim Briefing vor einer HYROX-Simulation bei Form Factory",
  stats_label="HYROX in Zahlen",
  st1="Laufen im Rennen", st2="funktionelle Stationen", st3="HYROX365-Trainingsschwerpunkte", st4="Form Factory Clubs",
  ab_eyebrow="Was ist ein HYROX Training Club",
  ab_h="Training mit Struktur. Nicht nur hart.",
  ab_p1="<strong>Ein HYROX Training Club ist ein akkreditiertes Studio, das nach dem offiziellen HYROX-Programm trainiert.</strong> Wir denken uns die Einheiten nicht spontan aus. Sie basieren auf der HYROX365-Methodik, die HYROX selbst entwickelt hat, und auf Coaches, die selbst Rennen laufen.",
  ab_p2="HYROX überträgt die Prinzipien des Rennens in ein Training für alle. Du musst keinen Start planen. Es reicht, stärker werden zu wollen, länger durchzuhalten und Fortschritt zu sehen. Und wenn du ein Rennen planst, bist du bereit.",
  p1h="Laufen", p1t="Ein Tempo, das du auch nach dem Schlitten hältst.",
  p2h="Kraft", p2t="Die auch unter Ermüdung funktioniert.",
  p3h="Stationen", p3t="Technik, die Sekunden und Energie spart.",
  p4h="Kopf", p4t="Anziehen, durchhalten, nicht loslassen.",
  ab_alt="Athleten nach einem Benchmark-Test auf den Laufbahnen des Clubs",
  ab_cap="Benchmark-Test · Form Factory Na Knížecí",
  pr_eyebrow="HYROX365 Group Training", pr_h="Vier Schwerpunkte. Eine Leistung.",
  pr_lead="Menschen sind verschieden, also passt nicht ein Kurs für alle. Deshalb arbeitet HYROX365 mit vier Formaten. Jedes entwickelt einen anderen Teil der Leistung. Zusammen bereiten sie dich auf das Rennen und auf das Leben außerhalb des Gyms vor.",
  int="Intensität", who="Für wen:",
  f_tag="Basis", f_claim="Zirkeltraining mit Sinn.",
  f_l1="Kraft und Ausdauer in einem", f_l2="aerobe Kapazität", f_l3="Technik, Beweglichkeit, Mobilität",
  f_who="ideal für Einsteiger, auch für Fortgeschrittene ehrliche Arbeit. Skalierbar für jedes Level.",
  e_tag="Kondition", e_claim="Größerer Motor. Längere Leistung.",
  e_l1="aerobe Leistung und Pacing", e_l2="Laktatschwelle und -toleranz", e_l3="Effizienz auf den Ergometern",
  e_who="für Starke, denen Ausdauer, Laufen oder Sicherheit auf SkiErg und Rudergerät fehlen.",
  p_tag="Kraft", p_claim="Kraft, die auch bei Kilometer 7 hält.",
  p_l1="Maximal- und Wiederholungskraft", p_l2="Kraftausdauer und Explosivität", p_l3="Arbeit mit Last über Zeit",
  p_who="für Läufer und Ausdauersportler, denen beim Schlitten, bei Lunges und Farmers Carry die Kraft ausgeht.",
  c_tag="Race-specific", c_claim="HYROX in Trainingsform.",
  c_l1="Laufen, Stationen und Übergänge", c_l2="Kondition und Kraft zugleich", c_l3="Rennrhythmus und Kopf",
  c_who="für alle, die ein Renndatum im Kalender haben und wissen wollen, was sie erwartet.",
  pr_note="<b>Den Schwerpunkt wählst du nicht, das Programm wechselt ihn für dich.</b> Du kommst zum Kurs und der Coach weiß, woran heute gearbeitet wird. Über die Wochen durchläufst du Basis, Kondition, Kraft und rennspezifische Arbeit. Genau so entsteht eine Leistung, die alle 8 Kilometer hält.",
  rc_eyebrow="Rennformat", rc_h="8× 1 km Laufen. 8× Station.",
  rc_lead="Die Reihenfolge ist bei jedem Rennen weltweit gleich. Deshalb kann man sich gezielt darauf vorbereiten. Und deshalb hat bei uns jede Einheit einen Ausgangspunkt und ein Ziel.",
  rc_alt="Athletinnen an den Stationen Sled Pull, Sandbag Lunges und Wall Balls",
  track_label="Reihenfolge der Stationen im HYROX-Rennen", reps="Wdh.",
  t1h="Laufen entscheidet", t1t="Die Hälfte der Rennzeit ist Laufen. Wer nach einer Station nicht laufen kann, verliert auf jedem Kilometer.",
  t2h="Übergänge und Tempo", t2t="Roxzone, Einstieg in die Station, die ersten Schritte nach dem Schlitten. Hier gehen Minuten verloren, die niemand sieht.",
  t3h="Der Kopf am Ende", t3t="Wall Balls nach 7 km Laufen sind eine andere Übung als frisch. Wir trainieren Arbeit unter Ermüdung, nicht nur Kraft.",
  hw_alt="Head Coach Ria feuert die Gruppe bei einer HYROX-Simulation an",
  hw_eyebrow="So funktioniert's", hw_h="Kommen. Anpacken. Besser werden.",
  s1h="Kurs buchen", s1t="In der App Moje Form Factory oder online. Die Kurse sind in der Mitgliedschaft enthalten.",
  s2h="Der Coach führt, du arbeitest", s2t="Aufwärmen, Technik, Hauptteil. Gewichte und Tempo werden an dein Level angepasst.",
  s3h="Fortschritt messen", s3t="Benchmark-Tests und Simulationen zeigen, wo du stehst und was sich nach ein paar Wochen verändert hat.",
  w1h="Einsteiger", w1t="Du brauchst keine Erfahrung und keine Form. Du musst nur kommen.",
  w2h="Kraftsportler", w2t="Wir ergänzen Ausdauer und Laufen, damit dir die Kraft nicht auf halber Strecke ausgeht.",
  w3h="Läufer", w3t="Wir ergänzen Kraft, damit dich der Schlitten nicht stoppt.",
  w4h="Rennvorbereitung", w4t="Du bekommst Struktur, Pacing und einen Plan für den Renntag.",
  co_eyebrow="Coaches", co_h="Gecoacht von Leuten, die es selbst laufen.",
  co_lead="Hinter dem HYROX Training Club steht das Team STR2G (Stronger Together). Wir trainieren, wir starten bei Rennen und wissen, wie sich Kilometer sieben anfühlt.",
  co_alt="Ria Suchánek Hrušovská und Ladislav Suchánek bei einem HYROX-Rennen",
  ria_role="Head Coach · HYROX Performance Coach",
  ria_txt="Head Coach des HYROX Training Clubs, Trainerin und Athletin. Sie steht hinter der Trainingsmethodik der Clubs. Technik, Stabilität und Kopf. Sie holt Energie aus der Gruppe und das Maximum aus jedem Einzelnen heraus, ohne ihn zu verheizen.",
  lada_role="Coach · HYROX Performance Coach",
  lada_txt="Trainer und aktiver HYROX-Athlet. Er verbindet Kraft, Kondition, Laufen und mentale Vorbereitung zu einem Training, das Sinn ergibt. Coacht Athleten in den Clubs und online weltweit.",
  mich_role='Coach · Les Mills &amp; HYROX', mich_txt='Sport gehört seit seiner Kindheit zu seinem Leben. Zehn Jahre Leistungsschwimmen, Sportstudium an der FTVS in Prag, danach die Fitnesswelt. Seit 2012 unterrichtet er Les Mills BODYPUMP, BODYCOMBAT, BODYBALANCE und GRIT und begleitet als Assessor neue Instruktoren. 2026 hat ihn HYROX voll gepackt: Er startet bei Rennen und leitet Gruppenkurse bei Form Factory. Am meisten liebt er das Gefühl eines komplett zerstörten Körpers nach einem Training, das einen wieder ein Stück weiterbringt.', mich_chip='HYROX-Athlet', ph_ria='Ria Suchánek Hrušovská leitet einen HYROX-Kurs', ph_lada='Ladislav Suchánek bei einem HYROX-Rennen', ph_mich='Michal Holotík bei Form Factory',
  chip_mental="Mental Coach", chip_nutri="Ernährungsspezialistin", chip_run="Lauftrainer", chip_mass="Sportmasseur",
  cl_eyebrow="Wo wir trainieren", cl_h="Vier Clubs. Drei Städte.",
  cl_lead="Alle Clubs haben eine HYROX-Zone mit Schlitten, SkiErgs, Rudergeräten und Laufbahnen. Nach dem Training Sauna, in der Mitgliedschaft enthalten.",
  addr="Adresse", open="Öffnungszeiten", contact="Kontakt", sched="Kursplan", map="Karte",
  wk="Mo–Fr", we="Sa–So",
  prague5="Prag 5 · Nový Smíchov", prague3="Prag 3 · Vinohrady", brno="Brünn · Starý Lískovec", ostrava="Ostrava · Hrabová",
  gal_label="Fotos aus dem Club",
  g1="Gruppenfoto der Mitglieder des HYROX Training Clubs", g2="Sled Push in der HYROX-Zone von Form Factory", g3="Nach dem Benchmark-Test", g4="Mitglieder des HYROX Training Clubs nach dem Training",
  cta_eyebrow="Erster Kurs",
  cta_lead="Bring Schuhe, Handtuch und etwas zu trinken mit. Komm ein paar Minuten früher. Den Rest machen wir zusammen.",
  cta_b1="Kurs buchen →", cta_b2="Erster Besuch bei Form Factory",
  lada_link='Personal Training und Online-Coaching · hyrox-prague.eu →', ria_link='Mentalcoaching · riahrusovska.cz →', co_more='STR2G Online-Programme →', ffg_b='Form Factory Games · 5.12.2026', ffg_t='Erlebe den Wettkampftag live. Einzelwettkampf bei Form Factory Vinohradská: drei Workouts, vier Kategorien, 100 Athleten.', ffg_link='Mehr zum Wettkampf →',
)

T["pl"] = dict(
  h1_sub="Grupowe treningi HYROX w Pradze, Brnie i Ostrawie",
  title="HYROX Training Club Praga, Brno, Ostrawa | Form Factory",
  meta_desc="Oficjalny HYROX Training Club w Form Factory. Trening HYROX w Pradze, Brnie i Ostrawie według programu HYROX365. Zajęcia grupowe z trenerami HYROX, dla początkujących i zawodników.",
  og_locale="pl_PL",
  og_desc="Trening według oficjalnego programu HYROX365. Praga, Brno, Ostrawa.",
  brand_sub="Form Factory · Praga · Brno · Ostrawa",
  nav_prog="Programy", nav_race="Zawody", nav_coach="Trenerzy", nav_clubs="Kluby", nav_book="Zapisz się",
  hero_eyebrow="Oficjalny HYROX Training Club",
  hero_lead="Trening według oficjalnego programu HYROX365. Bieganie, siła, stacje i praca w zmęczeniu. Prowadzą cię trenerzy, którzy sami startują. Nie przypadkowy workout, tylko plan z kierunkiem.",
  hero_cta1="Wybierz zajęcia →", hero_cta2="Znajdź klub",
  cities='<b>Praga</b> Na Knížecí · Vinohradská &nbsp;/&nbsp; <b>Brno</b> Campus &nbsp;/&nbsp; <b>Ostrawa</b> Hrabová',
  hero_alt="Trener prowadzi odprawę przed symulacją HYROX w Form Factory",
  stats_label="HYROX w liczbach",
  st1="biegu w zawodach", st2="stacji funkcjonalnych", st3="kierunki treningu HYROX365", st4="kluby Form Factory",
  ab_eyebrow="Czym jest HYROX Training Club",
  ab_h="Trening ze strukturą. Nie tylko ciężki.",
  ab_p1="<strong>HYROX Training Club to akredytowane miejsce, w którym trenuje się według oficjalnego programu HYROX.</strong> Nie wymyślamy zajęć z głowy. Opierają się na metodyce HYROX365 stworzonej przez sam HYROX i na doświadczeniu trenerów, którzy sami startują.",
  ab_p2="HYROX przekłada zasady zawodów na trening dla każdego. Nie musisz planować startu. Wystarczy, że chcesz być silniejszy, wytrzymać więcej i widzieć postęp. A jeśli celujesz w start, będziesz gotowy.",
  p1h="Bieg", p1t="Tempo, które utrzymasz nawet po saniach.",
  p2h="Siła", p2t="Taka, która działa w zmęczeniu.",
  p3h="Stacje", p3t="Technika, która oszczędza sekundy i energię.",
  p4h="Głowa", p4t="Docisnąć, wytrzymać, nie odpuścić.",
  ab_alt="Sportowcy po teście benchmark na bieżni klubu",
  ab_cap="Test benchmark · Form Factory Na Knížecí",
  pr_eyebrow="HYROX365 Group Training", pr_h="Cztery kierunki. Jeden wynik.",
  pr_lead="Ludzie są różni, więc jedne zajęcia nie pasują do wszystkich. Dlatego HYROX365 pracuje w czterech formatach. Każdy rozwija inną część wydolności, a razem przygotują cię na zawody i na życie poza siłownią.",
  int="Intensywność", who="Dla kogo:",
  f_tag="Podstawa", f_claim="Trening obwodowy z sensem.",
  f_l1="siła i wytrzymałość w jednym", f_l2="wydolność tlenowa", f_l3="technika, zwinność, mobilność",
  f_who="idealny dla początkujących, dla zaawansowanych nadal uczciwa praca. Skaluje się na każdy poziom.",
  e_tag="Kondycja", e_claim="Większy silnik. Dłuższy wysiłek.",
  e_l1="moc tlenowa i tempo", e_l2="próg mleczanowy i tolerancja", e_l3="efektywność na ergometrach",
  e_who="dla silnych osób, którym brakuje wytrzymałości, biegu lub pewności na SkiErgu i wioślarzu.",
  p_tag="Siła", p_claim="Siła, która trzyma nawet na 7. kilometrze.",
  p_l1="siła maksymalna i powtórzeniowa", p_l2="wytrzymałość siłowa i moc", p_l3="praca z obciążeniem w czasie",
  p_who="dla biegaczy i wytrzymałościowców, którym na saniach, wykrokach i farmers carry brakuje siły.",
  c_tag="Race-specific", c_claim="HYROX w formie treningu.",
  c_l1="bieg, stacje i przejścia", c_l2="kondycja i siła jednocześnie", c_l3="rytm zawodów i głowa",
  c_who="dla każdego, kto ma datę zawodów w kalendarzu i chce wiedzieć, co go czeka.",
  pr_note="<b>Kierunku nie wybierasz, program zmienia go za ciebie.</b> Przychodzisz na zajęcia, a trener wie, nad czym dziś pracujemy. W ciągu tygodni przechodzisz przez podstawę, kondycję, siłę i pracę startową. Tak buduje się wynik, który wytrzyma całe 8 kilometrów.",
  rc_eyebrow="Format zawodów", rc_h="8× 1 km biegu. 8× stacja.",
  rc_lead="Kolejność jest taka sama na każdych zawodach na świecie. Dlatego można się do niej celowo przygotować. I dlatego u nas każdy trening ma swój punkt wyjścia i cel.",
  rc_alt="Zawodniczki na stacjach Sled Pull, Sandbag Lunges i Wall Balls",
  track_label="Kolejność stacji w zawodach HYROX", reps="powt.",
  t1h="Bieg decyduje", t1t="Połowa czasu zawodów to bieg. Kto nie umie biec po stacji, traci na każdym kilometrze.",
  t2h="Przejścia i tempo", t2t="Roxzone, wejście na stację, pierwsze kroki po saniach. Tu giną minuty, których nikt nie widzi.",
  t3h="Głowa na końcu", t3t="Wall balls po 7 km biegu to inne ćwiczenie niż na świeżo. Trenujemy pracę w zmęczeniu, nie tylko siłę.",
  hw_alt="Head coach Ria dopinguje grupę podczas symulacji HYROX",
  hw_eyebrow="Jak to działa", hw_h="Przyjdź. Zrób robotę. Idź do przodu.",
  s1h="Rezerwujesz zajęcia", s1t="W aplikacji Moje Form Factory lub na stronie. Zajęcia są w cenie członkostwa.",
  s2h="Trener prowadzi, ty pracujesz", s2t="Rozgrzewka, technika, część główna. Ciężary i tempo dostosujemy do twojego poziomu.",
  s3h="Mierzysz postęp", s3t="Testy benchmark i symulacje pokażą, gdzie jesteś teraz i co zmieniło się po kilku tygodniach.",
  w1h="Zaczynasz", w1t="Nie potrzebujesz doświadczenia ani formy. Potrzebujesz przyjść.",
  w2h="Trenujesz siłowo", w2t="Dodamy wytrzymałość i bieg, żeby siła nie skończyła się w połowie.",
  w3h="Biegasz", w3t="Dodamy siłę, żeby sanie cię nie zatrzymały.",
  w4h="Szykujesz się na zawody", w4t="Dostaniesz strukturę, tempo i plan na dzień startu.",
  co_eyebrow="Trenerzy", co_h="Uczą ludzie, którzy sami startują.",
  co_lead="Za HYROX Training Club stoi zespół STR2G (Stronger Together). Trenujemy, startujemy i wiemy, jak boli siódmy kilometr.",
  co_alt="Ria Suchánek Hrušovská i Ladislav Suchánek na zawodach HYROX",
  ria_role="Head coach · HYROX Performance Coach",
  ria_txt="Head coach HYROX Training Club, trenerka i zawodniczka. Stoi za metodyką treningową klubów. Technika, stabilizacja i głowa. Wie, jak wydobyć energię z grupy i maksimum z każdego, nie niszcząc go.",
  lada_role="Coach · HYROX Performance Coach",
  lada_txt="Trener i aktywny zawodnik HYROX. Łączy siłę, kondycję, bieg i przygotowanie mentalne w trening, który ma sens. Prowadzi sportowców w klubach i online na całym świecie.",
  mich_role='Coach · Les Mills &amp; HYROX', mich_txt='Sport jest częścią jego życia od dzieciństwa. Dziesięć lat pływania wyczynowego, studia na FTVS w Pradze, a potem świat fitnessu. Od 2012 roku prowadzi zajęcia Les Mills BODYPUMP, BODYCOMBAT, BODYBALANCE i GRIT, a jako assessor pomaga nowym instruktorom. W 2026 roku na dobre wciągnął go HYROX: startuje w zawodach i prowadzi zajęcia grupowe w Form Factory. Najbardziej lubi uczucie totalnie wykończonego ciała po treningu, który przesuwa człowieka o kawałek dalej.', mich_chip='Zawodnik HYROX', ph_ria='Ria Suchánek Hrušovská prowadzi zajęcia HYROX', ph_lada='Ladislav Suchánek na zawodach HYROX', ph_mich='Michal Holotík w Form Factory',
  chip_mental="Mental Coach", chip_nutri="Specjalistka ds. żywienia", chip_run="Trener biegania", chip_mass="Masażysta sportowy",
  cl_eyebrow="Gdzie trenujemy", cl_h="Cztery kluby. Trzy miasta.",
  cl_lead="Każdy klub ma strefę HYROX z saniami, SkiErgami, wioślarzami i bieżnią. Po treningu sauna, w cenie członkostwa.",
  addr="Adres", open="Godziny otwarcia", contact="Kontakt", sched="Grafik", map="Mapa",
  wk="Pon–Pt", we="Sob–Nd",
  prague5="Praga 5 · Nový Smíchov", prague3="Praga 3 · Vinohrady", brno="Brno · Starý Lískovec", ostrava="Ostrawa · Hrabová",
  gal_label="Zdjęcia z klubu",
  g1="Wspólne zdjęcie członków HYROX Training Club", g2="Sled push w strefie HYROX Form Factory", g3="Po teście benchmark", g4="Członkowie HYROX Training Club po treningu",
  cta_eyebrow="Pierwsze zajęcia",
  cta_lead="Weź buty, ręcznik i coś do picia. Przyjdź kilka minut wcześniej. Resztę zrobimy razem.",
  cta_b1="Zapisz się na zajęcia →", cta_b2="Pierwsza wizyta w Form Factory",
  lada_link='Trening personalny i coaching online · hyrox-prague.eu →', ria_link='Coaching mentalny · riahrusovska.cz →', co_more='Programy online STR2G →', ffg_b='Form Factory Games · 5.12.2026', ffg_t='Sprawdź dzień zawodów na serio. Zawody indywidualne w Form Factory Vinohradská: trzy workouty, cztery kategorie, 100 zawodników.', ffg_link='Więcej o zawodach →',
)

FF_HYROX = {"cs": "https://www.formfactory.cz/hyrox/", "en": "https://www.formfactory.cz/en/hyrox/",
            "de": "https://www.formfactory.cz/en/hyrox/", "pl": "https://www.formfactory.cz/en/hyrox/"}
FF_FIRST = {"cs": "https://www.formfactory.cz/prvni-vstup/", "en": "https://www.formfactory.cz/en/",
            "de": "https://www.formfactory.cz/en/", "pl": "https://www.formfactory.cz/en/"}

CLUBS = [
  ("prague5", "Na Knížecí", "Ostrovského 464/6<br>150 00 Praha 5", "6:30–22:00", "8:00–21:00", "+420 773 798 400", "naknizeci@formfactory.cz", "https://naknizeci.formfactory.cz/calendar", "https://maps.app.goo.gl/doW5HCVQpwKnfNVX9"),
  ("prague3", "Vinohradská", "Vinohradská 190<br>130 00 Praha 3", "6:00–23:00", "8:00–21:00", "+420 770 399 902", "vinohradska@formfactory.cz", "https://vinohradska.formfactory.cz/calendar", "https://www.google.com/maps/search/?api=1&amp;query=Form+Factory+Vinohradsk%C3%A1+190+Praha"),
  ("brno", "Campus", "Palachovo náměstí 726/2<br>625 00 Brno", "6:00–22:00", "8:00–21:00", "+420 778 732 586", "campus@formfactory.cz", "https://campusbrno.formfactory.cz/calendar", "https://maps.app.goo.gl/tgAFsQ54cxxRUjnD7"),
  ("ostrava", "Hrabová", "Krmelínská 646/22<br>720 00 Ostrava 20", "6:00–21:00", "8:00–20:00", "+420 776 361 057", "hrabova@formfactory.cz", "https://hrabova.formfactory.cz/calendar", "https://maps.app.goo.gl/NYk2WWFvBfmfdWLE7"),
]

STATIONS = [("SkiErg", "1 000 m"), ("Sled Push", "50 m"), ("Sled Pull", "50 m"), ("Burpee Broad Jump", "80 m"),
            ("Rowing", "1 000 m"), ("Farmers Carry", "200 m"), ("Sandbag Lunges", "100 m"), ("Wall Balls", "100 {reps}")]


def meter(n, t):
    return f'<div class="meter" aria-label="{t["int"]} {n}/5">' + "".join('<i class="on"></i>' if i < n else "<i></i>" for i in range(5)) + "</div>"


def prog(key, name, n, t):
    return f'''<article class="prog">
          <span class="tag">{t[key+"_tag"]}</span>
          <h3>{name}</h3>
          {meter(n, t)}
          <p class="claim">{t[key+"_claim"]}</p>
          <ul><li>{t[key+"_l1"]}</li><li>{t[key+"_l2"]}</li><li>{t[key+"_l3"]}</li></ul>
          <p class="who"><b>{t["who"]}</b> {t[key+"_who"]}</p>
        </article>'''


def jsonld(lang):
    t = T[lang]
    places = []
    for key, name, adr, wk, we, ph, em, cal, mp in CLUBS:
        street, rest = adr.split("<br>")
        postal, city = re.match(r"(\d{3} \d{2}) (.+)", rest).groups()
        places.append({"@type": "SportsActivityLocation", "name": "Form Factory " + name,
                       "address": {"@type": "PostalAddress", "streetAddress": street, "postalCode": postal,
                                   "addressLocality": city, "addressCountry": "CZ"},
                       "telephone": ph.replace(" ", ""), "hasMap": mp.replace("&amp;", "&")})
    data = {"@context": "https://schema.org", "@graph": [
        {"@type": "SportsOrganization", "@id": SITE + "/#club", "name": "HYROX Training Club",
         "url": SITE + PATH[lang], "logo": SITE + "/img/ff-logo.jpg", "description": t["meta_desc"], "sport": "HYROX",
         "parentOrganization": {"@type": "Organization", "name": "Form Factory", "url": "https://www.formfactory.cz/"},
         "brand": {"@type": "Brand", "name": "STR2G", "url": "https://str2g.com/"},
         "memberOf": {"@type": "Organization", "@id": "https://strongertogether.cz/#org", "name": "Stronger Together", "url": "https://strongertogether.cz/"},
         "sameAs": ["https://www.instagram.com/hyroxprague/"],
         "location": places,
         "member": [{"@id": "https://hyrox-prague.eu/#ria"}, {"@id": "https://hyrox-prague.eu/#lada"}, {"@id": SITE + "/#michal"}]},
        {"@type": "Person", "@id": SITE + "/#michal", "name": "Michal Holotík", "alternateName": "Mike Holo", "jobTitle": "HYROX Coach"},
        {"@type": "Person", "@id": "https://hyrox-prague.eu/#ria", "name": "Ria Suchánek Hrušovská", "jobTitle": "Mental Coach",
         "url": "https://riahrusovska.cz/", "sameAs": ["https://riahrusovska.cz/", "https://www.instagram.com/riahrusovskaofficial/"]},
        {"@type": "Person", "@id": "https://hyrox-prague.eu/#lada", "name": "Ladislav Suchánek",
         "url": "https://hyrox-prague.eu/",
         "sameAs": ["https://www.ladislavsuchanek.cz/", "https://www.instagram.com/22segge_coach/"]},
    ]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def page(lang):
    t = T[lang]
    book = FF_HYROX[lang] + "#timetables"
    langs = "".join(f'<a href="{PATH[l]}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else "") + f'>{LABEL[l]}</a>' for l in LANGS)
    alternates = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{PATH[l]}">' for l in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    legs = "".join(f'<div class="leg" role="listitem"><span class="run">1 km run →</span><span class="no">0{i+1}</span><b>{n}</b><span>{d.format(reps=t["reps"])}</span></div>' for i, (n, d) in enumerate(STATIONS))
    clubs = ""
    for key, name, adr, wk, we, ph, em, cal, mp in CLUBS:
        clubs += f'''<article class="club">
          <div class="club-top"><span class="city">{t[key]}</span><h3>{name}</h3></div>
          <dl>
            <div><dt>{t["addr"]}</dt><dd>{adr}</dd></div>
            <div><dt>{t["open"]}</dt><dd>{t["wk"]} {wk}<br>{t["we"]} {we}</dd></div>
            <div><dt>{t["contact"]}</dt><dd><a class="ct" href="tel:+420722077070">{ph}</a><br><a class="ct" href="mailto:info@hyrox-czech.cz">{em}</a></dd></div>
          </dl>
          <div class="club-links"><a href="{cal}" target="_blank" rel="noopener">{t["sched"]}</a><a href="{mp}" target="_blank" rel="noopener">{t["map"]}</a></div>
          {CITY_LINK[key] if lang == "cs" else ""}
        </article>'''
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{t["title"]}</title>
<meta name="description" content="{t["meta_desc"]}">
<meta name="google-site-verification" content="Kzs4h_GLxSKewaL5_z4ibvPSfkfjBjpCLB9cq3RR-Ts" />
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="HYROX Training Club">
<meta property="og:locale" content="{t["og_locale"]}">
<meta property="og:url" content="{SITE}{PATH[lang]}">
<meta property="og:title" content="{t["title"]}">
<meta property="og:description" content="{t["og_desc"]}">
<meta property="og:image" content="{SITE}/img/hero.jpg">
<meta property="og:image:width" content="1800">
<meta property="og:image:height" content="1200">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE}{PATH[lang]}">
{alternates}
{jsonld(lang)}
<script src="/js/tracking.js"></script>
<link rel="icon" href="/favicon.png" type="image/png" sizes="160x160">
<link rel="apple-touch-icon" href="/favicon.png">
<link rel="preload" as="image" href="/img/hero.webp" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
{STYLE}
{EXTRA_CSS}
<style>body{{margin:0}}[hidden]{{display:none!important}}</style>
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="{PATH[lang]}">
      <img src="/img/ff-logo.jpg" alt="Form Factory">
      <span><b>HYROX Training Club</b><small>{t["brand_sub"]}</small></span>
    </a>
    <ul>
      <li><a href="#programy">{t["nav_prog"]}</a></li>
      <li><a href="#zavod">{t["nav_race"]}</a></li>
      <li><a href="#treneri">{t["nav_coach"]}</a></li>
      <li><a href="#kluby">{t["nav_clubs"]}</a></li>
    </ul>
    <div class="nav-right">
      <nav class="langs" aria-label="Language">{langs}</nav>
      <a class="btn btn-red" href="{book}" target="_blank" rel="noopener">{t["nav_book"]}</a>
    </div>
  </div>
</header>

<main id="top">
  <section class="hero">
    <div class="hero-img"><img src="/img/hero.webp" alt="{t["hero_alt"]}"></div>
    <div class="wrap">
      <p class="eyebrow">{t["hero_eyebrow"]}</p>
      <h1>HYROX <span>Training</span> <em>Club</em><small class="h1-sub">{t["h1_sub"]}</small></h1>
      <p class="lead">{t["hero_lead"]}</p>
      <div class="hero-cta">
        <a class="btn btn-red" href="{book}" target="_blank" rel="noopener">{t["hero_cta1"]}</a>
        <a class="btn btn-ghost" href="#kluby">{t["hero_cta2"]}</a>
      </div>
      <p class="cities">{t["cities"]}</p>
    </div>
  </section>

  <div class="stats" aria-label="{t["stats_label"]}">
    <div class="wrap">
      <div class="stat"><strong>8 km</strong><span>{t["st1"]}</span></div>
      <div class="stat"><strong>8</strong><span>{t["st2"]}</span></div>
      <div class="stat"><strong>4</strong><span>{t["st3"]}</span></div>
      <div class="stat"><strong>4</strong><span>{t["st4"]}</span></div>
    </div>
  </div>

  <section class="about" id="klub">
    <div class="wrap">
      <div class="about-text">
        <p class="eyebrow">{t["ab_eyebrow"]}</p>
        <h2>{t["ab_h"]}</h2>
        <p>{t["ab_p1"]}</p>
        <p>{t["ab_p2"]}</p>
        <div class="pillars">
          <div><b>{t["p1h"]}</b><span>{t["p1t"]}</span></div>
          <div><b>{t["p2h"]}</b><span>{t["p2t"]}</span></div>
          <div><b>{t["p3h"]}</b><span>{t["p3t"]}</span></div>
          <div><b>{t["p4h"]}</b><span>{t["p4t"]}</span></div>
        </div>
      </div>
      <figure class="about-img" style="margin:0">
        <img loading="lazy" decoding="async" src="/img/test.webp" alt="{t["ab_alt"]}">
        <figcaption>{t["ab_cap"]}</figcaption>
      </figure>
    </div>
  </section>

  <div class="lanes" aria-hidden="true"></div>

  <section class="programs" id="programy">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{t["pr_eyebrow"]}</p>
        <h2>{t["pr_h"]}</h2>
        <p class="lead">{t["pr_lead"]}</p>
      </div>
      <div class="prog-grid">
        {prog("f", "Foundational", 2, t)}
        {prog("e", "Engine", 4, t)}
        {prog("p", "Power", 4, t)}
        {prog("c", "Complete", 5, t)}
      </div>
      <div class="prog-note"><span class="ic">↻</span><p>{t["pr_note"]}</p></div>
    </div>
  </section>

  <section class="race" id="zavod">
    <div class="wrap">
      <div class="race-top">
        <div class="sec-head" style="margin:0">
          <p class="eyebrow">{t["rc_eyebrow"]}</p>
          <h2>{t["rc_h"]}</h2>
          <p class="lead">{t["rc_lead"]}</p>
        </div>
        <img loading="lazy" decoding="async" src="/img/stations.webp" alt="{t["rc_alt"]}">
      </div>
      <div class="track" role="list" aria-label="{t["track_label"]}">{legs}</div>
      <div class="truths">
        <div><b>{t["t1h"]}</b><p>{t["t1t"]}</p></div>
        <div><b>{t["t2h"]}</b><p>{t["t2t"]}</p></div>
        <div><b>{t["t3h"]}</b><p>{t["t3t"]}</p></div>
      </div>
      <div class="prog-note"><span class="ic">→</span><p><b>{t["ffg_b"]}.</b> {t["ffg_t"]} <a href="{net.url("ffg", lang)}" target="_blank" rel="noopener">{t["ffg_link"]}</a></p></div>
    </div>
  </section>

  <section class="how">
    <div class="wrap">
      <div class="how-img"><img loading="lazy" decoding="async" src="/img/ria-mic.webp" alt="{t["hw_alt"]}" style="aspect-ratio:4/5"></div>
      <div class="how-body">
        <div class="sec-head" style="margin:0">
          <p class="eyebrow">{t["hw_eyebrow"]}</p>
          <h2>{t["hw_h"]}</h2>
        </div>
        <div class="steps">
          <div class="step"><span class="n">1</span><div><b>{t["s1h"]}</b><p>{t["s1t"]}{FIRST_LINK if lang == "cs" else ""}</p></div></div>
          <div class="step"><span class="n">2</span><div><b>{t["s2h"]}</b><p>{t["s2t"]}</p></div></div>
          <div class="step"><span class="n">3</span><div><b>{t["s3h"]}</b><p>{t["s3t"]}</p></div></div>
        </div>
        <div class="forwho">
          <div><b>{t["w1h"]}</b>{t["w1t"]}</div>
          <div><b>{t["w2h"]}</b>{t["w2t"]}</div>
          <div><b>{t["w3h"]}</b>{t["w3t"]}</div>
          <div><b>{t["w4h"]}</b>{t["w4t"]}</div>
        </div>
      </div>
    </div>
  </section>

  <section class="coaches" id="treneri">
    <div class="wrap">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">{t["co_eyebrow"]}</p>
        <h2>{t["co_h"]}</h2>
        <p class="lead">{t["co_lead"]} <a href="{net.url("s2", lang)}" target="_blank" rel="noopener">{t["co_more"]}</a></p>
      </div>
    </div>
    <div class="wrap">
      <div class="coach-grid" style="margin-top:48px">
        <article class="coach">
          <picture class="ph"><source srcset="/img/coach-ria.webp?v=2" type="image/webp"><img loading="lazy" decoding="async" src="/img/coach-ria.jpg?v=2" alt="{t["ph_ria"]}" width="800" height="1000"></picture>
          <span class="role">{t["ria_role"]}</span>
          <h3>Ria Suchánek Hrušovská, MSc.</h3>
          <p>{t["ria_txt"]}</p>
          <div class="chips"><span>HYROX Performance Coach</span><span>CrossFit L2</span><span>{t["chip_mental"]}</span><span>Aarmy Coach</span><span>Les Mills</span><span>{t["chip_nutri"]}</span><span>DNS</span></div>
          <a class="site" href="{net.url("ria", lang)}" target="_blank" rel="noopener">{t["ria_link"]}</a>
        </article>
        <article class="coach">
          <picture class="ph"><source srcset="/img/coach-lada.webp?v=2" type="image/webp"><img loading="lazy" decoding="async" src="/img/coach-lada.jpg?v=2" alt="{t["ph_lada"]}" width="800" height="1000"></picture>
          <span class="role">{t["lada_role"]}</span>
          <h3>Ladislav Suchánek</h3>
          <p>{t["lada_txt"]}</p>
          <div class="chips"><span>HYROX Performance Coach L1</span><span>CrossFit L1</span><span>OPEX CCP</span><span>Precision Nutrition L1</span><span>{t["chip_run"]}</span><span>{t["chip_mass"]}</span></div>
          <a class="site" href="{net.url("hp", lang)}" target="_blank" rel="noopener">{t["lada_link"]}</a>
        </article>
        <article class="coach">
          <picture class="ph"><source srcset="/img/coach-michal.webp?v=2" type="image/webp"><img loading="lazy" decoding="async" src="/img/coach-michal.jpg?v=2" alt="{t["ph_mich"]}" width="800" height="1000"></picture>
          <span class="role">{t["mich_role"]}</span>
          <h3>Michal Holotík <small class="aka">aka Mike Holo</small></h3>
          <p>{t["mich_txt"]}</p>
          <div class="chips"><span>FTVS UK</span><span>Les Mills Assessor</span><span>BODYPUMP</span><span>BODYCOMBAT</span><span>BODYBALANCE</span><span>GRIT</span><span>{t["mich_chip"]}</span></div>
        </article>
      </div>
    </div>
  </section>

  <section class="clubs" id="kluby">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{t["cl_eyebrow"]}</p>
        <h2>{t["cl_h"]}</h2>
        <p class="lead">{t["cl_lead"]}</p>
      </div>
      <div class="club-grid">{clubs}</div>
    </div>
  </section>

  <section class="gallery" aria-label="{t["gal_label"]}">
    <div class="wrap">
      <div class="gal">
        <img loading="lazy" decoding="async" class="a" src="/img/group-v.webp" alt="{t["g1"]}">
        <img loading="lazy" decoding="async" src="/img/sled.webp" alt="{t["g2"]}">
        <img loading="lazy" decoding="async" src="/img/test.webp" alt="{t["g3"]}" style="object-position:center 60%">
        <img loading="lazy" decoding="async" class="d" src="/img/group.webp" alt="{t["g4"]}">
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="wrap">
      <p class="eyebrow">{t["cta_eyebrow"]}</p>
      <h2>Stronger<br>together.</h2>
      <p class="lead">{t["cta_lead"]}</p>
      <div class="cta-row">
        <a class="btn btn-red" href="{book}" target="_blank" rel="noopener">{t["cta_b1"]}</a>
        <a class="btn btn-ghost" href="{FF_FIRST[lang]}" target="_blank" rel="noopener">{t["cta_b2"]}</a>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    {net.block("htc", lang)}
    <span>HYROX Training Club · Form Factory × STR2G</span>
    <span><a href="{FF_HYROX[lang]}" target="_blank" rel="noopener">formfactory.cz/hyrox</a> · <a href="https://www.instagram.com/hyroxprague/" target="_blank" rel="noopener">@hyroxprague</a> · <a href="#" onclick="window.cookieSettings&&cookieSettings();return false">Cookies</a></span>
  </div>
</footer>
</body>
</html>
'''


# sanity: every language has the same keys
base = set(T["cs"])
for l in LANGS:
    missing = base ^ set(T[l])
    assert not missing, (l, missing)



# ---------------------------------------------------------------------------
# Městské stránky (jen CZ): /praha/, /brno/, /ostrava/
# Cílí na dotazy typu „hyrox praha“, „hyrox brno“, „hyrox ostrava“.
# ---------------------------------------------------------------------------
CITY_LINK = {
    "prague5": '<a class="club-more" href="/praha/">HYROX v Praze →</a>',
    "prague3": '<a class="club-more" href="/praha/">HYROX v Praze →</a>',
    "brno": '<a class="club-more" href="/brno/">HYROX v Brně →</a>',
    "ostrava": '<a class="club-more" href="/ostrava/">HYROX v Ostravě →</a>',
}

CITIES = {
  "praha": dict(
    clubs=["prague5", "prague3"], name="Praha", loc="v Praze",
    title="HYROX Praha: tréninky a rozvrh lekcí · Smíchov, Vinohrady",
    desc="HYROX v Praze: skupinové tréninky ve Form Factory Na Knížecí (Praha 5) a Vinohradská (Praha 3) podle programu HYROX365. Aktuální rozvrh lekcí a rezervace online.",
    h1="HYROX trénink Praha", sub="Na Knížecí · Vinohradská",
    lead="V Praze trénujeme ve dvou klubech Form Factory: Na Knížecí na Smíchově a na Vinohradské. Lekce jedou podle oficiálního programu HYROX365. Běh, síla, stanice a práce pod únavou. Přijď jako začátečník i jako závodník.",
    img="/img/group.webp",
    faq_extra=("Který pražský klub si vybrat?", "Ten, který máš blíž. Program HYROX365 je v obou klubech stejný, liší se jen rozvrh a otevírací doba."),
  ),
  "brno": dict(
    clubs=["brno"], name="Brno", loc="v Brně",
    title="HYROX Brno: tréninky a rozvrh lekcí · Form Factory Campus",
    desc="HYROX v Brně: skupinové tréninky ve Form Factory Campus podle programu HYROX365, pro začátečníky i závodníky. Aktuální rozvrh lekcí a rezervace online.",
    h1="HYROX trénink Brno", sub="Form Factory Campus",
    lead="V Brně trénujeme ve Form Factory Campus ve Starém Lískovci. Stejný program HYROX365 jako v Praze a Ostravě: běh, síla, stanice a práce pod únavou. Lekci si rezervuješ online.",
    img="/img/sled.webp",
    faq_extra=("Je program v Brně stejný jako v Praze?", "Ano. Všechny kluby jedou podle stejné metodiky HYROX365, takže můžeš trénovat v Brně a přijet na lekci do Prahy nebo Ostravy."),
  ),
  "ostrava": dict(
    clubs=["ostrava"], name="Ostrava", loc="v Ostravě",
    title="HYROX Ostrava: tréninky a rozvrh lekcí · Form Factory Hrabová",
    desc="HYROX v Ostravě: skupinové tréninky ve Form Factory Hrabová podle programu HYROX365, pro začátečníky i závodníky. Aktuální rozvrh lekcí a rezervace online.",
    h1="HYROX trénink Ostrava", sub="Form Factory Hrabová",
    lead="V Ostravě trénujeme ve Form Factory Hrabová. Stejný program HYROX365 jako v Praze a Brně: běh, síla, stanice a práce pod únavou. Lekci si rezervuješ online.",
    img="/img/group-v.webp",
    faq_extra=("Je program v Ostravě stejný jako v Praze?", "Ano. Všechny kluby jedou podle stejné metodiky HYROX365, takže můžeš trénovat v Ostravě a přijet na lekci do Prahy nebo Brna."),
  ),
}


# ---------- ROZVRH (z _build/timetable.json, plní ho _build/timetable.py přes GitHub Action každý den)
TT_DAYS = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]


def _tt_load():
    import json as _json
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timetable.json")
    try:
        with open(p, encoding="utf-8") as f:
            return _json.load(f)
    except (OSError, ValueError):
        return None


def timetable_html(keys, loc):
    import datetime as _dt
    tt = _tt_load()
    if not tt:
        return ""
    d0, d1 = _dt.date.fromisoformat(tt["from"]), _dt.date.fromisoformat(tt["to"])
    days = [d0 + _dt.timedelta(days=i) for i in range((d1 - d0).days + 1)]
    upd = _dt.date.fromisoformat(tt["updated"])
    blocks = []
    for key in keys:
        club = next(x for x in CLUBS if x[0] == key)
        cal = club[7]
        rows = tt["clubs"].get(key, [])
        cols = []
        for d in days:
            ds = d.isoformat()
            slots = "".join(
                f'<a class="tt-slot{" tt-ev" if "experience" in r["name"].lower() else ""}" href="{cal}?day={d.strftime("%d.%m.%Y")}&amp;view=DayByHour" target="_blank" rel="noopener">{r["start"]}–{r["end"]}'
                + ('<small>HYROX Experience</small>' if "experience" in r["name"].lower() else "") + "</a>"
                for r in rows if r["date"] == ds)
            cols.append(f'<div class="tt-day"><b>{TT_DAYS[d.weekday()]} {d.day}. {d.month}.</b>{slots or "<span class=\"tt-none\">–</span>"}</div>')
        blocks.append(f'''<div class="tt-club">
        <h3>Form Factory {club[1]}</h3>
        <div class="tt-grid">{"".join(cols)}</div>
      </div>''')
    return f'''
  <section class="tt" id="rozvrh">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Rozvrh lekcí</p>
        <h2>Rozvrh HYROX lekcí {loc}</h2>
        <p class="lead">HYROX lekce na nejbližších 7 dní ({d0.day}. {d0.month}. – {d1.day}. {d1.month}.), aktualizováno {upd.day}. {upd.month}. {upd.year}. Kliknutím na čas otevřeš rezervaci. Rezervovat můžeš 48 hodin předem v aplikaci Moje Form Factory nebo online.</p>
      </div>
      {"".join(blocks)}
    </div>
  </section>
'''


def club_card(key, t):
    for k, name, adr, wk, we, ph, em, cal, mp in CLUBS:
        if k == key:
            return f'''<article class="club">
          <div class="club-top"><span class="city">{t[k]}</span><h3>Form Factory {name}</h3></div>
          <dl>
            <div><dt>{t["addr"]}</dt><dd>{adr}</dd></div>
            <div><dt>{t["open"]}</dt><dd>{t["wk"]} {wk}<br>{t["we"]} {we}</dd></div>
            <div><dt>{t["contact"]}</dt><dd><a class="ct" href="tel:+420722077070">{ph}</a><br><a class="ct" href="mailto:info@hyrox-czech.cz">{em}</a></dd></div>
          </dl>
          <div class="club-links"><a href="{cal}" target="_blank" rel="noopener">{t["sched"]}</a><a href="{mp}" target="_blank" rel="noopener">{t["map"]}</a></div>
        </article>'''


def city_jsonld(slug, c, faqs):
    url = f"{SITE}/{slug}/"
    places = []
    for k, name, adr, wk, we, ph, em, cal, mp in CLUBS:
        if k not in c["clubs"]:
            continue
        street, rest = adr.split("<br>")
        postal, city = re.match(r"(\d{3} \d{2}) (.+)", rest).groups()
        places.append({"@type": "SportsActivityLocation", "@id": f"{url}#{k}", "name": f"Form Factory {name} – HYROX Training Club",
                       "url": url, "sport": "HYROX", "image": SITE + c["img"].replace(".webp", ".webp"),
                       "address": {"@type": "PostalAddress", "streetAddress": street, "postalCode": postal,
                                   "addressLocality": city, "addressCountry": "CZ"},
                       "telephone": ph.replace(" ", ""), "hasMap": mp.replace("&amp;", "&"),
                       "parentOrganization": {"@id": SITE + "/#club"}})
    data = {"@context": "https://schema.org", "@graph": places + [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "HYROX Training Club", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": c["h1"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]},
    ]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def city_page(slug):
    t = T["cs"]
    c = CITIES[slug]
    url = f"{SITE}/{slug}/"
    cal = next(x[7] for x in CLUBS if x[0] == c["clubs"][0]) if len(c["clubs"]) == 1 else FF_HYROX["cs"] + "#timetables"
    cards = "".join(club_card(k, t) for k in c["clubs"])
    faqs = [
        ("Musím mít s HYROXem zkušenosti?", "Ne. " + t["w1t"] + " Váhy i tempo se upraví podle tvé úrovně."),
        ("Jak si lekci zarezervuju?", t["s1t"]),
        (f"Kdy jsou HYROX lekce {c['loc']}?", 'Několikrát týdně ráno, v poledne i večer, podle klubu. Aktuální rozvrh na 7 dní je <a href="#rozvrh">nahoře na této stránce</a>, rezervace v aplikaci Moje Form Factory.'),
        ("Kolik stojí první vstup?", f'Podmínky prvního vstupu najdeš na <a href="{FF_FIRST["cs"]}" target="_blank" rel="noopener">webu Form Factory</a>.'),
        ("Co si mám vzít s sebou?", t["cta_lead"]),
        c["faq_extra"],
    ]
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    others = "".join(f'<a class="btn btn-ghost" href="/{s}/">HYROX {CITIES[s]["name"]}</a>' for s in CITIES if s != slug)
    return f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{c["title"]}</title>
<meta name="description" content="{c["desc"]}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="HYROX Training Club">
<meta property="og:locale" content="cs_CZ">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{c["title"]}">
<meta property="og:description" content="{c["desc"]}">
<meta property="og:image" content="{SITE}/img/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
{city_jsonld(slug, c, faqs)}
<script src="/js/tracking.js"></script>
<link rel="icon" href="/favicon.png" type="image/png" sizes="160x160">
<link rel="apple-touch-icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
{STYLE}
{EXTRA_CSS}
<style>body{{margin:0}}[hidden]{{display:none!important}}.hero h1{{font-size:clamp(48px,9vw,120px)}}</style>
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="/">
      <img src="/img/ff-logo.jpg" alt="Form Factory">
      <span><b>HYROX Training Club</b><small>{t["brand_sub"]}</small></span>
    </a>
    <ul>
      <li><a href="/praha/">Praha</a></li>
      <li><a href="/brno/">Brno</a></li>
      <li><a href="/ostrava/">Ostrava</a></li>
      <li><a href="/#programy">{t["nav_prog"]}</a></li>
    </ul>
    <div class="nav-right">
      <a class="btn btn-red" href="{cal}" target="_blank" rel="noopener">{t["nav_book"]}</a>
    </div>
  </div>
</header>

<main id="top">
  <section class="hero">
    <div class="hero-img"><img src="{c["img"]}" alt="HYROX trénink ve Form Factory {c["name"]}"></div>
    <div class="wrap">
      <p class="crumbs"><a href="/">HYROX Training Club</a> / {c["name"]}</p>
      <p class="eyebrow">{t["hero_eyebrow"]}</p>
      <h1>{c["h1"]}<small class="h1-sub">{c["sub"]}</small></h1>
      <p class="lead">{c["lead"]}</p>
      <div class="hero-cta">
        <a class="btn btn-red" href="{cal}" target="_blank" rel="noopener">Rozvrh a rezervace →</a>
        <a class="btn btn-ghost" href="#rozvrh">Rozvrh na tento týden</a>
      </div>
    </div>
  </section>

{timetable_html(c["clubs"], c["loc"])}
  <section class="clubs" id="kluby">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{t["cl_eyebrow"]}</p>
        <h2>HYROX {c["loc"]}</h2>
        <p class="lead">{t["cl_lead"]}</p>
      </div>
      <div class="club-grid">{cards}</div>
    </div>
  </section>

  <section class="programs" id="programy">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{t["pr_eyebrow"]}</p>
        <h2>{t["pr_h"]}</h2>
        <p class="lead">{t["pr_lead"]}</p>
      </div>
      <div class="prog-grid">
        {prog("f", "Foundational", 2, t)}
        {prog("e", "Engine", 4, t)}
        {prog("p", "Power", 4, t)}
        {prog("c", "Complete", 5, t)}
      </div>
      <div class="prog-note"><span class="ic">↻</span><p>{t["pr_note"]}</p></div>
    </div>
  </section>

  <section class="how">
    <div class="wrap">
      <div class="how-img"><img loading="lazy" decoding="async" src="/img/ria-mic.webp" alt="{t["hw_alt"]}" style="aspect-ratio:4/5"></div>
      <div class="how-body">
        <div class="sec-head" style="margin:0">
          <p class="eyebrow">{t["hw_eyebrow"]}</p>
          <h2>{t["hw_h"]}</h2>
        </div>
        <div class="steps">
          <div class="step"><span class="n">1</span><div><b>{t["s1h"]}</b><p>{t["s1t"]}{FIRST_LINK}</p></div></div>
          <div class="step"><span class="n">2</span><div><b>{t["s2h"]}</b><p>{t["s2t"]}</p></div></div>
          <div class="step"><span class="n">3</span><div><b>{t["s3h"]}</b><p>{t["s3t"]}</p></div></div>
        </div>
      </div>
    </div>
  </section>

  <section class="coaches">
    <div class="wrap">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">Časté otázky</p>
        <h2>HYROX {c["loc"]}: co potřebuješ vědět</h2>
      </div>
      <div class="city-faq">{faq_html}</div>
      <p class="lead" style="margin-top:28px">Chceš individuální přípravu na závod? <a href="https://www.ladislavsuchanek.cz/hyrox-coaching/">HYROX trenér Praha – osobní coaching 1:1</a>. Trénuješ sám? <a href="{net.url("s2", "cs")}" target="_blank" rel="noopener">Online HYROX programy STR2G</a>.</p>
      <div class="city-other"><a class="btn btn-ghost" href="/">Všechny kluby</a>{others}</div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    {net.block("htc", "cs")}
    <span>HYROX Training Club · Form Factory × STR2G</span>
    <span><a href="{FF_HYROX["cs"]}" target="_blank" rel="noopener">formfactory.cz/hyrox</a> · <a href="https://www.instagram.com/hyroxprague/" target="_blank" rel="noopener">@hyroxprague</a> · <a href="#" onclick="window.cookieSettings&&cookieSettings();return false">Cookies</a></span>
  </div>
</footer>
</body>
</html>
'''


FIRST_LINK = ' <a href="/prvni-hyrox-lekce/">Jdeš poprvé? Co tě čeká →</a>'

# ---------- ČLÁNKY (jednoduché stránky s FAQ). draft=True = zatím nezveřejňovat.
ARTICLES = {
  "prvni-hyrox-lekce": dict(
    draft=False,
    title="První HYROX lekce: co tě čeká a jak se připravit | HYROX Training Club",
    desc="Jdeš na první HYROX lekci ve Form Factory? Jak lekce probíhá, jak se přihlásit, co si vzít a jak se nebát, když jsi začátečník. Praha, Brno, Ostrava.",
    h1="První HYROX lekce", sub="Co tě čeká a jak se připravit",
    img="/img/group.webp",
    lead="Na první HYROX lekci nepotřebuješ zkušenost ani formu. Potřebuješ přijít. Tady je, jak lekce v HYROX Training Clubu probíhá a co si vzít s sebou.",
    body="""
<h2>Jak HYROX lekce probíhá</h2>
<p>Lekce trvá 45 až 60 minut podle klubu a času. Kombinuje kardio a sílu, vede ji trenér a jede se v týmové energii s hudbou. Na začátku je rozcvička a technika, pak hlavní blok. Váhy i tempo se upraví podle tvé úrovně.</p>
<p>Lekce jedou podle oficiálního programu HYROX365 ve čtyřech formátech: Foundational, Engine, Power a Complete. Formát si nevybíráš, program ho během týdnů střídá za tebe. Přehled formátů je na <a href="/#programy">hlavní stránce</a>.</p>
<h2>Jak se přihlásit</h2>
<p>Lekci si rezervuješ v aplikaci Moje Form Factory nebo na webu Form Factory. Lekce jsou součástí členství. Podmínky prvního vstupu najdeš na <a href="https://www.formfactory.cz/prvni-vstup/" target="_blank" rel="noopener">webu Form Factory</a>.</p>
<h2>Co si vzít s sebou</h2>
<ul>
<li>Sportovní oblečení, ve kterém se dobře hýbeš</li>
<li>Čisté sálové tenisky</li>
<li>Ručník a pití</li>
</ul>
<p>Přijď pár minut dřív, ať stihneš převléknout a pozdravit trenéra. Řekni mu, že jsi tu poprvé.</p>
<h2>Tipy na první lekci</h2>
<ul>
<li><strong>Nezačínej naplno.</strong> První lekce je na to, abys poznal stanice a tempo. Výkon přijde.</li>
<li><strong>Ptej se.</strong> Saně, SkiErg nebo wall balls jsou pro hodně lidí nové. Trenér ti ukáže techniku.</li>
<li><strong>Přijď znovu do týdne.</strong> Rozdíl ucítíš po třech, čtyřech lekcích, ne po první.</li>
</ul>
<h2>Kde trénujeme</h2>
<p>V Praze ve Form Factory Na Knížecí a Vinohradská, v Brně ve Form Factory Campus a v Ostravě ve Form Factory Hrabová. Adresy a otevírací doby: <a href="/praha/">Praha</a>, <a href="/brno/">Brno</a>, <a href="/ostrava/">Ostrava</a>.</p>
<p>Chystáš se rovnou na závod? Co tě na HYROX čeká a jaké jsou váhy, najdeš v článku <a href="https://www.ladislavsuchanek.cz/l/hyrox-vahy-a-stanice/">HYROX váhy a stanice</a>.</p>
""",
    faqs=[
      ("Můžu na HYROX lekci jako úplný začátečník?", "Ano. Předchozí zkušenost není potřeba. Lekce jsou vedené tak, aby se v nich zorientovali i úplní začátečníci, a váhy i tempo se upraví podle tvé úrovně."),
      ("Jak dlouho trvá HYROX lekce?", "45 až 60 minut podle klubu a času. Kombinuje se běh, síla a HYROX stanice. Přesný čas každé lekce najdeš v rozvrhu na stránce svého města."),
      ("Jak si HYROX lekci zarezervuju?", "V aplikaci Moje Form Factory nebo na webu Form Factory. Lekce jsou součástí členství."),
      ("Co si vzít na HYROX lekci?", "Sportovní oblečení, čisté sálové tenisky, ručník a pití."),
      ("Musím být ve formě?", "Nemusíš. Důležité je chtít začít. Forma přijde s pravidelným tréninkem."),
    ],
  ),
  "hyrox-simulace": dict(
    draft=True,
    title="HYROX simulace: jak ji udělat a co ti řekne | HYROX Training Club",
    desc="Jak udělat HYROX simulaci v tréninku: plná, poloviční a zkrácená verze, kdy ji zařadit před závodem a co si z ní vzít. Praha, Brno, Ostrava.",
    h1="HYROX simulace", sub="Jak ji udělat a co ti řekne",
    img="/img/test.webp",
    lead="Simulace je nejbližší věc závodu, kterou můžeš udělat v tréninku. Ukáže ti tempo, slabá místa a jak hlava zvládá únavu. Jen ji nesmíš dělat moc často.",
    body="""
<h2>Proč simulovat</h2>
<p>V tréninku děláš běh, sílu a stanice zvlášť. Na závodě se to všechno sejde v jednom kuse. Simulace ti ukáže, jestli tempo, které si plánuješ, opravdu udržíš, a na které stanici se ti závod láme.</p>
<h2>Tři verze simulace</h2>
<ul>
<li><strong>Plná simulace:</strong> 8 × 1 km a všech 8 stanic se závodními vahami. Náročná, potřebuješ po ní pár dní na regeneraci. Jednou za přípravu, nejpozději 3–4 týdny před závodem.</li>
<li><strong>Poloviční simulace:</strong> 4 × 1 km a 4 stanice, třeba první nebo druhá polovina závodu. Dá se dělat častěji, jednou za 2–3 týdny.</li>
<li><strong>Zkrácená simulace:</strong> 8 × 500 m běhu a stanice na poloviční objem. Dobrá pro začátečníky a pro dny, kdy nechceš tělo vyždímat.</li>
</ul>
<h2>Na co se soustředit</h2>
<ul>
<li><strong>Tempo běhu:</strong> drž plánované tempo od prvního kilometru. Simulace není závod, je to test plánu.</li>
<li><strong>Mezičasy:</strong> zapisuj si čas každého běhu a každé stanice. Uvidíš, kde ztrácíš.</li>
<li><strong>Přechody:</strong> mezi během a stanicí nestůj. Přesně jako v Roxzone.</li>
<li><strong>Výbava a jídlo:</strong> vyzkoušej boty, oblečení a co sníš před startem.</li>
</ul>
<h2>Co si z ní vzít</h2>
<p>Nejcennější není celkový čas, ale rozdíly. Pokud ti běhy po saních padají o minutu, potřebuješ trénovat běh pod únavou. Pokud stojíš u wall balls, potřebuješ plán sérií. Simulace ti řekne, na čem pracovat dalších pár týdnů.</p>
<h2>Simulace v HYROX Training Clubu</h2>
<p>Benchmark testy a simulace jsou součástí programu HYROX365, podle kterého jedeme lekce ve Form Factory. Uvidíš, kde jsi teď a co se za pár týdnů změnilo. Kluby a rozvrh: <a href="/praha/">Praha</a>, <a href="/brno/">Brno</a>, <a href="/ostrava/">Ostrava</a>.</p>
<p>Jdeš na lekci poprvé? Přečti si <a href="/prvni-hyrox-lekce/">První HYROX lekce</a>. Kompletní přehled stanic a vah je v článku <a href="https://www.ladislavsuchanek.cz/l/hyrox-vahy-a-stanice/">HYROX váhy a stanice</a>.</p>
""",
    faqs=[
      ("Jak často dělat HYROX simulaci?", "Plnou simulaci jednou za přípravu, nejpozději 3–4 týdny před závodem. Poloviční nebo zkrácenou jednou za 2–3 týdny."),
      ("Mám dělat plnou simulaci v týdnu před závodem?", "Ne. Regenerace po plné simulaci trvá několik dní. Před závodem stačí krátké úseky v závodním tempu."),
      ("Co mi HYROX simulace ukáže?", "Jestli udržíš plánované tempo, na které stanici ztrácíš nejvíc času a jak zvládáš běh po stanicích."),
    ],
  ),
}


def article_page(slug):
    t = T["cs"]
    a = ARTICLES[slug]
    url = f"{SITE}/{slug}/"
    faq_html = "".join(f"<details><summary>{q}</summary><p>{x}</p></details>" for q, x in a["faqs"])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "HYROX Training Club", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": a["h1"], "item": url}]},
        {"@type": "Article", "headline": a["h1"], "description": a["desc"], "inLanguage": "cs", "mainEntityOfPage": url,
         "image": SITE + a["img"], "publisher": {"@id": SITE + "/#club"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", x)}} for q, x in a["faqs"]]},
    ]}
    cal = FF_HYROX["cs"] + "#timetables"
    return f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{a["title"]}</title>
<meta name="description" content="{a["desc"]}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:site_name" content="HYROX Training Club">
<meta property="og:locale" content="cs_CZ">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{a["title"]}">
<meta property="og:description" content="{a["desc"]}">
<meta property="og:image" content="{SITE}/img/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script src="/js/tracking.js"></script>
<link rel="icon" href="/favicon.png" type="image/png" sizes="160x160">
<link rel="apple-touch-icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
{STYLE}
{EXTRA_CSS}
<style>body{{margin:0}}[hidden]{{display:none!important}}.hero h1{{font-size:clamp(48px,9vw,120px)}}.art{{max-width:760px}}.art h2{{margin:44px 0 14px}}.art p,.art li{{font-size:18px;line-height:1.6}}.art ul{{padding-left:22px}}.art a{{color:inherit;text-decoration:underline}}</style>
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="/">
      <img src="/img/ff-logo.jpg" alt="Form Factory">
      <span><b>HYROX Training Club</b><small>{t["brand_sub"]}</small></span>
    </a>
    <ul>
      <li><a href="/praha/">Praha</a></li>
      <li><a href="/brno/">Brno</a></li>
      <li><a href="/ostrava/">Ostrava</a></li>
      <li><a href="/#programy">{t["nav_prog"]}</a></li>
    </ul>
    <div class="nav-right">
      <a class="btn btn-red" href="{cal}" target="_blank" rel="noopener">{t["nav_book"]}</a>
    </div>
  </div>
</header>

<main id="top">
  <section class="hero">
    <div class="hero-img"><img src="{a["img"]}" alt="{a["h1"]} ve Form Factory"></div>
    <div class="wrap">
      <p class="crumbs"><a href="/">HYROX Training Club</a> / {a["h1"]}</p>
      <p class="eyebrow">{t["hero_eyebrow"]}</p>
      <h1>{a["h1"]}<small class="h1-sub">{a["sub"]}</small></h1>
      <p class="lead">{a["lead"]}</p>
      <div class="hero-cta">
        <a class="btn btn-red" href="{cal}" target="_blank" rel="noopener">Rozvrh a rezervace →</a>
      </div>
    </div>
  </section>

  <section class="coaches">
    <div class="wrap">
      <div class="art">{a["body"]}</div>
    </div>
  </section>

  <section class="coaches">
    <div class="wrap">
      <div class="sec-head" style="margin:0">
        <p class="eyebrow">Časté otázky</p>
        <h2>{a["h1"]}: co potřebuješ vědět</h2>
      </div>
      <div class="city-faq">{faq_html}</div>
      <div class="city-other"><a class="btn btn-ghost" href="/">Všechny kluby</a><a class="btn btn-ghost" href="/praha/">HYROX Praha</a><a class="btn btn-ghost" href="/brno/">HYROX Brno</a><a class="btn btn-ghost" href="/ostrava/">HYROX Ostrava</a></div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    {net.block("htc", "cs")}
    <span>HYROX Training Club · Form Factory × STR2G</span>
    <span><a href="{FF_HYROX["cs"]}" target="_blank" rel="noopener">formfactory.cz/hyrox</a> · <a href="https://www.instagram.com/hyroxprague/" target="_blank" rel="noopener">@hyroxprague</a> · <a href="#" onclick="window.cookieSettings&&cookieSettings();return false">Cookies</a></span>
  </div>
</footer>
</body>
</html>
'''


for slug, a in ARTICLES.items():
    if a.get("draft"):
        continue
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(article_page(slug))
    print("wrote", os.path.join(d, "index.html"))


for slug in CITIES:
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(city_page(slug))
    print("wrote", os.path.join(d, "index.html"))


for l in LANGS:
    d = os.path.join(OUT, PATH[l].strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(page(l))
    print("wrote", os.path.join(d, "index.html"))
