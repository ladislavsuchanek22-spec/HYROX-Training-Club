"""Weby STR2G: jeden zdroj pro blok odkazů v patičce.

Stejný seznam je ve všech čtyřech webech (hyrox-prague.eu, str2g.com,
hyroxtrainingclub.cz, formfactorygames.cz). Od 10/2026 v něm je i riahrusovska.cz. Když tu něco změníš,
změň to i v ostatních repozitářích.
"""

LANGS = ["cs", "en", "pl", "de"]

HEADING = {"cs": "Weby STR2G", "en": "STR2G websites", "pl": "Strony STR2G", "de": "STR2G-Websites"}

# klíč: (název, doména, URL podle jazyka, popis podle jazyka)
SITES = {
    "hp": ("HYROX Prague", "hyrox-prague.eu",
           {"cs": "https://hyrox-prague.eu/", "en": "https://hyrox-prague.eu/en/",
            "pl": "https://hyrox-prague.eu/pl/", "de": "https://hyrox-prague.eu/de/"},
           {"cs": "HYROX trénink a příprava na závod", "en": "HYROX training and race prep",
            "pl": "Trening HYROX i przygotowanie do zawodów", "de": "HYROX-Training und Wettkampfvorbereitung"}),
    "s2": ("STR2G Online", "str2g.com",
           {"cs": "https://str2g.com/cs/", "en": "https://str2g.com/",
            "pl": "https://str2g.com/pl/", "de": "https://str2g.com/de/"},
           {"cs": "Online HYROX programy", "en": "Online HYROX programs",
            "pl": "Programy HYROX online", "de": "Online-HYROX-Programme"}),
    "htc": ("HYROX Training Club", "hyroxtrainingclub.cz",
            {"cs": "https://hyroxtrainingclub.cz/", "en": "https://hyroxtrainingclub.cz/en/",
             "pl": "https://hyroxtrainingclub.cz/pl/", "de": "https://hyroxtrainingclub.cz/de/"},
            {"cs": "HYROX tréninky v Praze, Brně a Ostravě", "en": "HYROX classes in Prague, Brno and Ostrava",
             "pl": "Treningi HYROX w Pradze, Brnie i Ostrawie", "de": "HYROX-Training in Prag, Brno und Ostrava"}),
    "ffg": ("Form Factory Games", "formfactorygames.cz",
            {"cs": "https://formfactorygames.cz/", "en": "https://formfactorygames.cz/en/",
             "pl": "https://formfactorygames.cz/pl/", "de": "https://formfactorygames.cz/de/"},
            {"cs": "Závod · 5. 12. 2026", "en": "Race · 5 Dec 2026",
             "pl": "Zawody · 5.12.2026", "de": "Wettkampf · 5.12.2026"}),
    "ls": ("Ladislav Suchánek", "ladislavsuchanek.cz",
           {"cs": "https://www.ladislavsuchanek.cz/", "en": "https://www.ladislavsuchanek.cz/en/",
            "pl": "https://www.ladislavsuchanek.cz/pl/", "de": "https://www.ladislavsuchanek.cz/de/"},
           {"cs": "Osobní trénink, výživa a masáže", "en": "Personal training, nutrition &amp; massage",
            "pl": "Trening personalny, dieta i masaże", "de": "Personal Training, Ernährung &amp; Massage"}),
    "ria": ("Ria Suchánek Hrušovská", "riahrusovska.cz",
            {"cs": "https://riahrusovska.cz/", "en": "https://riahrusovska.cz/en/",
             "pl": "https://riahrusovska.cz/en/", "de": "https://riahrusovska.cz/en/"},
            {"cs": "Mentální koučink pro sportovce", "en": "Mental coaching for athletes",
             "pl": "Coaching mentalny dla sportowców", "de": "Mentalcoaching für Sportler"}),
}
ORDER = ["hp", "s2", "htc", "ffg", "ls", "ria"]


def url(key, lang):
    return SITES[key][2][lang]


def block(current, lang):
    items = []
    for k in ORDER:
        if k == current:
            continue
        name, dom, urls, desc = SITES[k]
        items.append(f'<li><a href="{urls[lang]}" target="_blank" rel="noopener"><b>{name}</b>'
                     f'<span>{desc[lang]}</span><i>{dom}</i></a></li>')
    return (f'<nav class="net" aria-label="{HEADING[lang]}"><p class="net-h">{HEADING[lang]}</p>'
            f'<ul>{"".join(items)}</ul></nav>')
