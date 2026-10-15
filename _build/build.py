#!/usr/bin/env python3
"""Generate the HYROX Training Club site in CZ, EN, DE, PL.
Usage: python3 build.py <style.css> <out_dir>
"""
import sys, os, html, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import net

STYLE = open(sys.argv[1]).read().replace('url("img/sled.jpg")', 'url("/img/sled.jpg")')
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
.prog-note a{color:var(--fg);text-decoration-color:var(--red-hi);text-underline-offset:3px}
.net{flex-basis:100%;padding-bottom:24px;margin-bottom:8px;border-bottom:1px solid var(--line)}
.net-h{margin:0 0 14px;font:500 12px/1 var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.net ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px 24px}
.net a{display:grid;gap:3px;text-decoration:none;color:var(--fg)}
.net b{font:700 20px/1.05 var(--f-display);text-transform:uppercase;letter-spacing:.02em}
.net span{font-size:14px;line-height:1.35;color:var(--muted)}
.net i{font:500 12px/1.2 var(--f-mono);font-style:normal;color:var(--muted)}
.net a:hover b{color:var(--red-hi)}
</style>"""

LANGS = ["cs", "en", "de", "pl"]
PATH = {"cs": "/", "en": "/en/", "de": "/de/", "pl": "/pl/"}
LABEL = {"cs": "CZ", "en": "EN", "de": "DE", "pl": "PL"}
SITE = "https://hyroxtrainingclub.cz"

T = {}

T["cs"] = dict(
  meta_desc="Oficiální HYROX Training Club ve Form Factory. Trénink podle programu HYROX365 v Praze, Brně a Ostravě.",
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
  lada_link='Osobní trénink a online coaching · hyrox-prague.eu →', co_more='Online programy STR2G →', ffg_b='Form Factory Games · 5. 12. 2026', ffg_t='Vyzkoušej si závodní den naostro. Individuální závod ve Form Factory Vinohradská: tři workouty, čtyři kategorie, 100 atletů.', ffg_link='Více o závodě →',
)

T["en"] = dict(
  meta_desc="Official HYROX Training Club at Form Factory. Training on the HYROX365 programme in Prague, Brno and Ostrava.",
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
  lada_link='Personal training and online coaching · hyrox-prague.eu →', co_more='STR2G online programs →', ffg_b='Form Factory Games · 5 Dec 2026', ffg_t='Try race day for real. An individual competition at Form Factory Vinohradská: three workouts, four divisions, 100 athletes.', ffg_link='About the race →',
)

T["de"] = dict(
  meta_desc="Offizieller HYROX Training Club bei Form Factory. Training nach dem HYROX365-Programm in Prag, Brünn und Ostrava.",
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
  lada_link='Personal Training und Online-Coaching · hyrox-prague.eu →', co_more='STR2G Online-Programme →', ffg_b='Form Factory Games · 5.12.2026', ffg_t='Erlebe den Wettkampftag live. Einzelwettkampf bei Form Factory Vinohradská: drei Workouts, vier Kategorien, 100 Athleten.', ffg_link='Mehr zum Wettkampf →',
)

T["pl"] = dict(
  meta_desc="Oficjalny HYROX Training Club w Form Factory. Trening według programu HYROX365 w Pradze, Brnie i Ostrawie.",
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
  lada_link='Trening personalny i coaching online · hyrox-prague.eu →', co_more='Programy online STR2G →', ffg_b='Form Factory Games · 5.12.2026', ffg_t='Sprawdź dzień zawodów na serio. Zawody indywidualne w Form Factory Vinohradská: trzy workouty, cztery kategorie, 100 zawodników.', ffg_link='Więcej o zawodach →',
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
         "sameAs": ["https://www.instagram.com/hyroxprague/"],
         "location": places,
         "member": [{"@id": "https://hyrox-prague.eu/#ria"}, {"@id": "https://hyrox-prague.eu/#lada"}]},
        {"@type": "Person", "@id": "https://hyrox-prague.eu/#ria", "name": "Ria Suchánek Hrušovská",
         "url": "https://hyrox-prague.eu/", "sameAs": ["https://www.instagram.com/riahrusovskaofficial/"]},
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
        </article>'''
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>HYROX Training Club</title>
<meta name="description" content="{t["meta_desc"]}">
<meta name="google-site-verification" content="Kzs4h_GLxSKewaL5_z4ibvPSfkfjBjpCLB9cq3RR-Ts" />
<meta property="og:title" content="HYROX Training Club · Form Factory">
<meta property="og:description" content="{t["og_desc"]}">
<meta property="og:image" content="{SITE}/img/hero.jpg">
<link rel="canonical" href="{SITE}{PATH[lang]}">
{alternates}
{jsonld(lang)}
<link rel="icon" href="/img/ff-logo.jpg">
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
    <div class="hero-img"><img src="/img/hero.jpg" alt="{t["hero_alt"]}"></div>
    <div class="wrap">
      <p class="eyebrow">{t["hero_eyebrow"]}</p>
      <h1>HYROX<span>Training</span><em>Club</em></h1>
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
        <img src="/img/test.jpg" alt="{t["ab_alt"]}">
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
        <img src="/img/stations.jpg" alt="{t["rc_alt"]}">
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
      <div class="how-img"><img src="/img/ria-mic.jpg" alt="{t["hw_alt"]}" style="aspect-ratio:4/5"></div>
      <div class="how-body">
        <div class="sec-head" style="margin:0">
          <p class="eyebrow">{t["hw_eyebrow"]}</p>
          <h2>{t["hw_h"]}</h2>
        </div>
        <div class="steps">
          <div class="step"><span class="n">1</span><div><b>{t["s1h"]}</b><p>{t["s1t"]}</p></div></div>
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
    <figure class="coach-banner" style="margin-inline:0;margin-bottom:0;margin-top:48px">
      <img src="/img/coaches.jpg" alt="{t["co_alt"]}">
    </figure>
    <div class="wrap">
      <div class="coach-grid">
        <article class="coach">
          <span class="role">{t["ria_role"]}</span>
          <h3>Ria Suchánek Hrušovská, MSc.</h3>
          <p>{t["ria_txt"]}</p>
          <div class="chips"><span>HYROX Performance Coach</span><span>CrossFit L2</span><span>{t["chip_mental"]}</span><span>Aarmy Coach</span><span>Les Mills</span><span>{t["chip_nutri"]}</span><span>DNS</span></div>
        </article>
        <article class="coach">
          <span class="role">{t["lada_role"]}</span>
          <h3>Ladislav Suchánek</h3>
          <p>{t["lada_txt"]}</p>
          <div class="chips"><span>HYROX Performance Coach L1</span><span>CrossFit L1</span><span>OPEX CCP</span><span>Precision Nutrition L1</span><span>{t["chip_run"]}</span><span>{t["chip_mass"]}</span></div>
          <a class="site" href="{net.url("hp", lang)}" target="_blank" rel="noopener">{t["lada_link"]}</a>
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
        <img class="a" src="/img/group-v.jpg" alt="{t["g1"]}">
        <img src="/img/sled.jpg" alt="{t["g2"]}">
        <img src="/img/test.jpg" alt="{t["g3"]}" style="object-position:center 60%">
        <img class="d" src="/img/group.jpg" alt="{t["g4"]}">
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
    <span><a href="{FF_HYROX[lang]}" target="_blank" rel="noopener">formfactory.cz/hyrox</a> · <a href="https://www.instagram.com/hyroxprague/" target="_blank" rel="noopener">@hyroxprague</a></span>
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

for l in LANGS:
    d = os.path.join(OUT, PATH[l].strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(page(l))
    print("wrote", os.path.join(d, "index.html"))
