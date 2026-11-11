"""Kvíz „Najdi svou první lekci“ na homepage (CZ, EN, DE, PL).

Výsledek: klub + nejbližší lekce z _build/timetable.json (rozvrh se denně
aktualizuje GitHub Action, web se přegeneruje), formát HYROX365, na který se
zaměřit, a odkazy podle odpovědí. Texty jsou tady ve slovníku F.
"""
import json

CSS = """<style>
.finder .wrap>.fbox{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(24px,4vw,48px)}
.finder [hidden]{display:none!important}
#finder{scroll-margin-top:96px}
.f-intro{display:grid;grid-template-columns:1fr auto;gap:14px 40px;align-items:end}
.f-intro h2{margin:0}
.f-intro .lead{margin:0;max-width:620px}
.f-intro .btn{grid-row:1/4;grid-column:2;cursor:pointer}
@media (max-width:760px){.f-intro{grid-template-columns:1fr}.f-intro .btn{grid-row:auto;grid-column:auto;justify-self:start;margin-top:8px}}
.f-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.f-link{background:none;border:0;padding:0;color:var(--muted);font:600 13px/1 var(--f-body);letter-spacing:.14em;text-transform:uppercase;cursor:pointer;text-decoration:none}
.f-link:hover{color:var(--fg)}
.f-count{font:600 13px/1 var(--f-body);letter-spacing:.14em;color:var(--red-hi)}
.f-bar{height:3px;background:var(--line);margin-bottom:32px;border-radius:2px;overflow:hidden}
.f-bar i{display:block;height:100%;width:0;background:var(--red-hi);transition:width .35s}
.f-q h3{font:700 clamp(28px,4vw,44px)/1 var(--f-display);text-transform:uppercase;margin:0 0 24px}
.f-opts{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
@media (max-width:640px){.f-opts{grid-template-columns:1fr}}
.f-opts button{display:flex;align-items:center;gap:14px;text-align:left;background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:var(--radius);font:500 17px/1.3 var(--f-body);padding:17px 18px;cursor:pointer;transition:border-color .15s,background .15s}
.f-opts button:hover{border-color:var(--red-hi)}
.f-opts button i{flex:0 0 20px;height:20px;border:1.5px solid var(--muted);border-radius:4px;display:grid;place-items:center}
.f-opts button.on{border-color:var(--red-hi);background:#1a070c}
.f-opts button.on i{background:var(--red-hi);border-color:var(--red-hi)}
.f-opts button.on i::after{content:"";width:5px;height:10px;border:solid #fff;border-width:0 2.5px 2.5px 0;transform:rotate(45deg) translate(-1px,-1px)}
.f-opts small{display:block;color:var(--muted);font-size:14px;margin-top:2px}
.f-in{animation:fIn .35s ease}
@keyframes fIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.f-res h3{font:700 clamp(32px,5vw,56px)/.95 var(--f-display);text-transform:uppercase;margin:10px 0 6px}
.f-addr{color:var(--muted);margin:0}
.f-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:28px}
@media (max-width:860px){.f-grid{grid-template-columns:1fr}}
.f-card{border:1px solid var(--line);border-radius:var(--radius);padding:22px}
.f-card .eyebrow{margin-bottom:14px}
.f-slots{display:grid;gap:8px}
.f-slots a{display:flex;justify-content:space-between;align-items:center;gap:12px;text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:12px 14px;font-weight:600}
.f-slots a:hover{border-color:var(--red-hi)}
.f-slots a span{color:var(--red-hi);font-size:14px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
.f-none{color:var(--muted);margin:0 0 10px}
.f-fmt b{display:block;font:700 34px/1 var(--f-display);text-transform:uppercase}
.f-fmt .claim{margin:8px 0 10px;font-weight:600}
.f-fmt p{margin:0;color:var(--muted)}
.f-tips{list-style:none;padding:0;margin:16px 0 0;display:grid;gap:8px}
.f-tips a{display:flex;justify-content:space-between;gap:16px;align-items:center;text-decoration:none;border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px}
.f-tips a:hover{border-color:var(--red-hi)}
.f-tips b{display:block}
.f-tips span{color:var(--muted);font-size:15px}
.f-tips em{font-style:normal;color:var(--red-hi);font-weight:700}
.f-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.f-again{margin-top:24px}
</style>"""

F = {
 "cs": dict(
  eyebrow="Najdi svou první lekci", h="6 otázek. Jeden plán, kde začít.",
  lead="Vybereme ti klub, nejbližší lekce v čase, který ti sedí, a na co se v tréninku zaměřit.",
  start="Začít →", back="← Zpět", again="↺ Znovu",
  q=[("club","Kde chceš trénovat?",[("prague5","Praha · Na Knížecí","Praha 5 · Nový Smíchov"),("prague3","Praha · Vinohradská","Praha 3 · Vinohrady"),("brno","Brno · Campus","Starý Lískovec"),("ostrava","Ostrava · Hrabová","Ostrava 20")]),
     ("time","Kdy ti to nejvíc sedí?",[("am","Ráno","do 9:00"),("day","Přes den","9:00–16:00"),("pm","Večer","od 16:00"),("any","Je mi to jedno","")]),
     ("exp","Jakou máš zkušenost?",[("zero","Začínám od nuly",""),("fit","Trénuju, ale HYROX ne",""),("htc","HYROX lekce znám",""),("race","Závodím","")]),
     ("gap","Co ti chybí nejvíc?",[("run","Výdrž a běh",""),("str","Síla",""),("tech","Technika na stanicích",""),("pace","Závodní tempo a hlava",""),("all","Nevím, chci všechno","")]),
     ("goal","Míříš na závod?",[("soon","Ano, do 12 týdnů",""),("later","Ano, ale později",""),("no","Zatím ne",""),("ffg","Láká mě Form Factory Games","23. 1. 2027 · Vinohradská")]),
     ("member","Jsi členem Form Factory?",[("yes","Ano",""),("no","Ne","")])],
  r_eyebrow="Tvůj klub", slots_h="Nejbližší lekce", slots_none="V tomhle čase teď lekci nemáme. Nejbližší termíny:", slots_empty="Rozvrh na tyhle dny ještě není venku. Mrkni do kalendáře klubu.",
  book="Rezervovat", fmt_h="Na co se zaměřit",
  fmt_note="Formáty se v rozvrhu střídají, takže projdeš všemi. Tenhle tě ale posune nejvíc.",
  tips_h="Než přijdeš", cta1="Rezervovat lekci →", cta2="Mám dotaz",
  t_first=("Jak vypadá první HYROX lekce","Co tě čeká a jak se připravit."),
  t_member=("Ještě nejsi členem?","První vstup do Form Factory."),
  t_rp=("12 Weeks Race Prep","Do závodu méně než 12 týdnů? Připrav se systematicky."),
  t_sim=("HYROX simulace","Zjisti, kde jsi a co trénovat."),
  t_ffg=("Form Factory Games","23. 1. 2027 · individuální závod ve Form Factory Vinohradská."),
  days=["Po","Út","St","Čt","Pá","So","Ne"], today="Dnes", tomorrow="Zítra",
 ),
 "en": dict(
  eyebrow="Find your first class", h="6 questions. One plan for where to start.",
  lead="We'll match you with a club, the next classes at a time that suits you, and what to focus on in training.",
  start="Start →", back="← Back", again="↺ Start again",
  q=[("club","Where do you want to train?",[("prague5","Prague · Na Knížecí","Prague 5 · Nový Smíchov"),("prague3","Prague · Vinohradská","Prague 3 · Vinohrady"),("brno","Brno · Campus","Starý Lískovec"),("ostrava","Ostrava · Hrabová","Ostrava 20")]),
     ("time","When suits you best?",[("am","Morning","before 9:00"),("day","Daytime","9:00–16:00"),("pm","Evening","from 16:00"),("any","I don't mind","")]),
     ("exp","How experienced are you?",[("zero","Starting from zero",""),("fit","I train, but not HYROX",""),("htc","I know HYROX classes",""),("race","I race","")]),
     ("gap","What are you missing most?",[("run","Endurance and running",""),("str","Strength",""),("tech","Station technique",""),("pace","Race pace and mindset",""),("all","Not sure, I want it all","")]),
     ("goal","Are you aiming for a race?",[("soon","Yes, within 12 weeks",""),("later","Yes, but later",""),("no","Not yet",""),("ffg","Form Factory Games sounds good","23 Jan 2027 · Vinohradská")]),
     ("member","Are you a Form Factory member?",[("yes","Yes",""),("no","No","")])],
  r_eyebrow="Your club", slots_h="Next classes", slots_none="No class at that time right now. Next ones:", slots_empty="The timetable for these days isn't out yet. Check the club calendar.",
  book="Book", fmt_h="What to focus on",
  fmt_note="Formats rotate in the timetable, so you'll do them all. This one will move you forward the most.",
  tips_h="Before you come", cta1="Book a class →", cta2="Ask us",
  t_first=None,
  t_member=("Not a member yet?","Your first visit to Form Factory."),
  t_rp=("12 Weeks Race Prep","Race less than 12 weeks out? Prepare systematically."),
  t_sim=None,
  t_ffg=("Form Factory Games","23 Jan 2027 · individual race at Form Factory Vinohradská."),
  days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], today="Today", tomorrow="Tomorrow",
 ),
 "de": dict(
  eyebrow="Finde deinen ersten Kurs", h="6 Fragen. Ein Plan für deinen Start.",
  lead="Wir finden deinen Club, die nächsten Kurse zu einer Zeit, die dir passt, und worauf du dich im Training konzentrieren solltest.",
  start="Los →", back="← Zurück", again="↺ Neu starten",
  q=[("club","Wo willst du trainieren?",[("prague5","Prag · Na Knížecí","Prag 5 · Nový Smíchov"),("prague3","Prag · Vinohradská","Prag 3 · Vinohrady"),("brno","Brno · Campus","Starý Lískovec"),("ostrava","Ostrava · Hrabová","Ostrava 20")]),
     ("time","Wann passt es dir am besten?",[("am","Morgens","vor 9:00"),("day","Tagsüber","9:00–16:00"),("pm","Abends","ab 16:00"),("any","Egal","")]),
     ("exp","Wie viel Erfahrung hast du?",[("zero","Ich fange bei null an",""),("fit","Ich trainiere, aber nicht HYROX",""),("htc","Ich kenne HYROX-Kurse",""),("race","Ich starte bei Rennen","")]),
     ("gap","Was fehlt dir am meisten?",[("run","Ausdauer und Laufen",""),("str","Kraft",""),("tech","Technik an den Stationen",""),("pace","Renntempo und Kopf",""),("all","Weiß nicht, ich will alles","")]),
     ("goal","Hast du ein Rennen im Blick?",[("soon","Ja, in den nächsten 12 Wochen",""),("later","Ja, aber später",""),("no","Noch nicht",""),("ffg","Form Factory Games reizt mich","23. 1. 2027 · Vinohradská")]),
     ("member","Bist du Form Factory Mitglied?",[("yes","Ja",""),("no","Nein","")])],
  r_eyebrow="Dein Club", slots_h="Nächste Kurse", slots_none="Zu dieser Zeit gibt es gerade keinen Kurs. Die nächsten Termine:", slots_empty="Der Kursplan für diese Tage ist noch nicht online. Schau in den Kalender des Clubs.",
  book="Buchen", fmt_h="Worauf du dich konzentrierst",
  fmt_note="Die Formate wechseln im Kursplan, du machst also alle. Dieses bringt dich aber am weitesten.",
  tips_h="Bevor du kommst", cta1="Kurs buchen →", cta2="Frag uns",
  t_first=None,
  t_member=("Noch kein Mitglied?","Dein erster Besuch bei Form Factory."),
  t_rp=("12 Weeks Race Prep","Rennen in weniger als 12 Wochen? Bereite dich systematisch vor."),
  t_sim=None,
  t_ffg=("Form Factory Games","23. 1. 2027 · Einzelrennen bei Form Factory Vinohradská."),
  days=["Mo","Di","Mi","Do","Fr","Sa","So"], today="Heute", tomorrow="Morgen",
 ),
 "pl": dict(
  eyebrow="Znajdź swoje pierwsze zajęcia", h="6 pytań. Jeden plan na start.",
  lead="Dobierzemy klub, najbliższe zajęcia w porze, która Ci pasuje, i to, na czym skupić się w treningu.",
  start="Start →", back="← Wstecz", again="↺ Od nowa",
  q=[("club","Gdzie chcesz trenować?",[("prague5","Praga · Na Knížecí","Praga 5 · Nový Smíchov"),("prague3","Praga · Vinohradská","Praga 3 · Vinohrady"),("brno","Brno · Campus","Starý Lískovec"),("ostrava","Ostrawa · Hrabová","Ostrawa 20")]),
     ("time","Kiedy pasuje Ci najbardziej?",[("am","Rano","przed 9:00"),("day","W ciągu dnia","9:00–16:00"),("pm","Wieczorem","od 16:00"),("any","Wszystko jedno","")]),
     ("exp","Jakie masz doświadczenie?",[("zero","Zaczynam od zera",""),("fit","Trenuję, ale nie HYROX",""),("htc","Znam zajęcia HYROX",""),("race","Startuję w zawodach","")]),
     ("gap","Czego brakuje Ci najbardziej?",[("run","Wytrzymałości i biegu",""),("str","Siły",""),("tech","Techniki na stacjach",""),("pace","Tempa startowego i głowy",""),("all","Nie wiem, chcę wszystkiego","")]),
     ("goal","Celujesz w zawody?",[("soon","Tak, w ciągu 12 tygodni",""),("later","Tak, ale później",""),("no","Jeszcze nie",""),("ffg","Kuszą mnie Form Factory Games","23.01.2027 · Vinohradská")]),
     ("member","Jesteś członkiem Form Factory?",[("yes","Tak",""),("no","Nie","")])],
  r_eyebrow="Twój klub", slots_h="Najbliższe zajęcia", slots_none="O tej porze nie mamy teraz zajęć. Najbliższe terminy:", slots_empty="Grafik na te dni jeszcze nie jest gotowy. Zajrzyj do kalendarza klubu.",
  book="Zapisz się", fmt_h="Na czym się skupić",
  fmt_note="Formaty zmieniają się w grafiku, więc przejdziesz przez wszystkie. Ten jednak da Ci najwięcej.",
  tips_h="Zanim przyjdziesz", cta1="Zapisz się na zajęcia →", cta2="Zapytaj nas",
  t_first=None,
  t_member=("Nie jesteś jeszcze członkiem?","Pierwsza wizyta w Form Factory."),
  t_rp=("12 Weeks Race Prep","Zawody za mniej niż 12 tygodni? Przygotuj się systematycznie."),
  t_sim=None,
  t_ffg=("Form Factory Games","23.01.2027 · zawody indywidualne w Form Factory Vinohradská."),
  days=["Pn","Wt","Śr","Cz","Pt","So","Nd"], today="Dziś", tomorrow="Jutro",
 ),
}

FFG = {"cs": "https://formfactorygames.cz/", "en": "https://formfactorygames.cz/en/",
       "de": "https://formfactorygames.cz/de/", "pl": "https://formfactorygames.cz/pl/"}
RP = {"cs": "/12-weeks-race-prep/", "en": "/en/12-weeks-race-prep/", "de": "/de/12-weeks-race-prep/", "pl": "/pl/12-weeks-race-prep/"}


def _opt(v, label, sub):
    s = f"<small>{sub}</small>" if sub else ""
    return f'<button type="button" data-v="{v}"><i></i><span>{label}{s}</span></button>'


def section(lang, t, clubs, ff_first, timetable):
    """t = T[lang] z build.py (formáty HYROX365), clubs = CLUBS, timetable = obsah timetable.json nebo None."""
    f = F[lang]
    qs = "".join(
        f'<div class="f-q" data-q="{k}" hidden><h3>{title}</h3><div class="f-opts">{"".join(_opt(*o) for o in opts)}</div></div>'
        for k, title, opts in f["q"])
    data = {
        "clubs": {c[0]: {"name": "Form Factory " + c[1], "addr": c[2].replace("<br>", ", "), "cal": c[7]} for c in clubs},
        "tt": (timetable or {}).get("clubs", {}),
        "fmt": {k: {"name": n, "claim": t[k + "_claim"], "who": t[k + "_who"]}
                for k, n in (("f", "Foundational"), ("e", "Engine"), ("p", "Power"), ("c", "Complete"))},
        "tips": {k: (list(f[k]) if f[k] else None) for k in ("t_first", "t_member", "t_rp", "t_sim", "t_ffg")},
        "links": {"t_first": "/prvni-hyrox-lekce/", "t_member": ff_first, "t_rp": RP[lang],
                  "t_sim": "/hyrox-simulace/", "t_ffg": FFG[lang]},
        "days": f["days"], "today": f["today"], "tomorrow": f["tomorrow"], "book": f["book"],
    }
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f"""{CSS}
  <section class="finder" id="najdi-lekci">
    <div class="wrap"><div class="fbox" id="finder">
      <div class="f-intro">
        <p class="eyebrow">{f["eyebrow"]}</p>
        <h2>{f["h"]}</h2>
        <p class="lead">{f["lead"]}</p>
        <button type="button" class="btn btn-red f-start">{f["start"]}</button>
      </div>
      <div class="f-top" hidden><button type="button" class="f-link f-back">{f["back"]}</button><span class="f-count"></span></div>
      <div class="f-bar" hidden><i></i></div>
      {qs}
      <div class="f-res" hidden aria-live="polite">
        <p class="eyebrow">{f["r_eyebrow"]}</p>
        <h3 class="f-club"></h3>
        <p class="f-addr"></p>
        <div class="f-grid">
          <div class="f-card"><p class="eyebrow">{f["slots_h"]}</p><p class="f-none" hidden>{f["slots_none"]}</p><div class="f-slots"></div><p class="f-empty f-none" hidden>{f["slots_empty"]}</p></div>
          <div class="f-card f-fmt"><p class="eyebrow">{f["fmt_h"]}</p><b></b><p class="claim"></p><p class="who"></p><p style="margin-top:12px">{f["fmt_note"]}</p></div>
        </div>
        <div class="f-tipsw"><p class="eyebrow" style="margin-top:28px">{f["tips_h"]}</p><ul class="f-tips"></ul></div>
        <div class="f-actions"><a class="btn btn-red f-book" target="_blank" rel="noopener">{f["cta1"]}</a><a class="btn btn-ghost" href="mailto:info@hyrox-czech.cz">{f["cta2"]}</a></div>
        <button type="button" class="f-link f-again">{f["again"]}</button>
      </div>
    </div></div>
  </section>
<script>
(function(){{
  var D={blob};
  var F=document.getElementById('finder'); if(!F) return;
  var $=function(s,r){{return (r||F).querySelector(s)}}, $$=function(s,r){{return Array.prototype.slice.call((r||F).querySelectorAll(s))}};
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ev=function(n,p){{try{{if(window.gtag)gtag('event',n,p||{{}})}}catch(e){{}}}};
  var Q=$$('.f-q'), a={{}}, step=-1;
  function show(el){{el.hidden=false;el.classList.remove('f-in');void el.offsetWidth;el.classList.add('f-in')}}
  function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
  function render(){{
    $$('.f-q,.f-res').forEach(function(e){{e.hidden=true}});
    $('.f-intro').hidden=step>-1;
    var inQ=step>-1&&step<Q.length;
    $('.f-top').hidden=$('.f-bar').hidden=!inQ;
    if(step<0) return;
    if(!inQ) return result();
    var q=Q[step];
    $('.f-back').style.visibility=step?'visible':'hidden';
    $('.f-count').textContent=('0'+(step+1)).slice(-2)+' / '+('0'+Q.length).slice(-2);
    $('.f-bar i').style.width=((step+1)/Q.length*100)+'%';
    $$('button',q).forEach(function(b){{b.classList.toggle('on',a[q.dataset.q]===b.dataset.v)}});
    show(q);
  }}
  function slots(club){{
    var now=new Date(), pad=function(n){{return ('0'+n).slice(-2)}};
    var today=now.getFullYear()+'-'+pad(now.getMonth()+1)+'-'+pad(now.getDate()), hm=pad(now.getHours())+':'+pad(now.getMinutes());
    var all=(D.tt[club]||[]).filter(function(r){{return r.date>today||(r.date===today&&r.start>hm)}});
    var fit=all.filter(function(r){{return a.time==='am'?r.start<'09:00':a.time==='day'?(r.start>='09:00'&&r.start<'16:00'):a.time==='pm'?r.start>='16:00':true}});
    return {{list:(fit.length?fit:all).slice(0,3),fb:!fit.length&&all.length>0}};
  }}
  function label(ds){{
    var d=new Date(ds+'T12:00:00'), n=new Date(); n.setHours(12,0,0,0);
    var diff=Math.round((d-n)/864e5);
    if(diff===0) return D.today; if(diff===1) return D.tomorrow;
    return D.days[(d.getDay()+6)%7]+' '+d.getDate()+'. '+(d.getMonth()+1)+'.';
  }}
  function result(){{
    var c=D.clubs[a.club], r=$('.f-res');
    $('.f-club').textContent=c.name; $('.f-addr').textContent=c.addr;
    var so=slots(a.club), s=so.list, box=$('.f-slots'); box.innerHTML='';
    s.forEach(function(x){{
      var p=x.date.split('-'), el=document.createElement('a');
      el.href=c.cal+'?day='+p[2]+'.'+p[1]+'.'+p[0]+'&view=DayByHour'; el.target='_blank'; el.rel='noopener';
      el.innerHTML=esc(label(x.date))+' · '+esc(x.start)+'–'+esc(x.end)+'<span>'+esc(D.book)+' →</span>';
      el.onclick=function(){{ev('quiz_book_click',{{quiz:'htc_finder',club:a.club}})}};
      box.appendChild(el);
    }});
    $('.f-none:not(.f-empty)').hidden=!so.fb; $('.f-empty').hidden=s.length>0;
    var k={{run:'e',str:'p',tech:'f',pace:'c'}}[a.gap]||((a.goal==='soon'||a.exp==='race')?'c':(a.exp==='zero'?'f':'c'));
    var fm=D.fmt[k], fb=$('.f-fmt');
    fb.querySelector('b').textContent=fm.name; fb.querySelector('.claim').textContent=fm.claim; fb.querySelector('.who').textContent=fm.who;
    var tips=[];
    if(a.exp==='zero'||a.exp==='fit') tips.push('t_first');
    if(a.member==='no') tips.push('t_member');
    if(a.goal==='soon') tips.push('t_rp');
    if(a.goal==='later'||a.exp==='race') tips.push('t_sim');
    if(a.goal==='ffg') tips.push('t_ffg');
    var ul=$('.f-tips'); ul.innerHTML='';
    tips.filter(function(t){{return D.tips[t]}}).forEach(function(t){{
      var li=document.createElement('li'), ext=/^https?:/.test(D.links[t]);
      li.innerHTML='<a href="'+esc(D.links[t])+'"'+(ext?' target="_blank" rel="noopener"':'')+'><div><b>'+esc(D.tips[t][0])+'</b><span>'+esc(D.tips[t][1])+'</span></div><em>→</em></a>';
      ul.appendChild(li);
    }});
    $('.f-tipsw').hidden=!ul.children.length;
    $('.f-book').href=c.cal;
    $('.f-book').onclick=function(){{ev('quiz_book_click',{{quiz:'htc_finder',club:a.club}})}};
    show(r);
    F.scrollIntoView({{behavior:reduce?'auto':'smooth',block:'start'}});
    ev('quiz_result',{{quiz:'htc_finder',club:a.club,format:fm.name}});
  }}
  $('.f-start').onclick=function(){{step=0;ev('quiz_start',{{quiz:'htc_finder'}});render();F.scrollIntoView({{behavior:reduce?'auto':'smooth',block:'start'}})}};
  $('.f-back').onclick=function(){{step--;render()}};
  $('.f-again').onclick=function(){{a={{}};step=0;render()}};
  Q.forEach(function(q){{$$('button',q).forEach(function(b){{b.onclick=function(){{
    a[q.dataset.q]=b.dataset.v;
    $$('button',q).forEach(function(x){{x.classList.toggle('on',x===b)}});
    ev('quiz_answer',{{quiz:'htc_finder',question:q.dataset.q,answer:b.dataset.v}});
    setTimeout(function(){{step++;render()}},200);
  }}}})}});
}})();
</script>
"""
