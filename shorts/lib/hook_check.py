#!/usr/bin/env python3
"""Contrôle d'accroche (français). Idée : le skill MIT « instagram-agent-skill », réécrit pour nos shorts.

usage: hook_check.py <episode_dir>            note l'accroche (2 premières phrases de source/script.json)
       hook_check.py --hook "phrase" [--hook "autre"]   compare plusieurs accroches candidates
Cinq contrôles sur 100 : LONGUEUR (≈ 3 s de voix), CONCRET (chiffre, nom précis), ENJEU (mot qui met quelque chose en
jeu), ADRESSE (tu / ton), OUVERTURE (pas de salutation ni de préambule). Il repère les accroches faibles ; il ne
devine pas laquelle sera virale (l'auteur du skill d'origine a mesuré 0,56 de réussite à ce jeu-là)."""
import json, os, re, sys

ENJEU = {"danger", "risque", "erreur", "mythe", "faux", "fausse", "vrai", "vraie", "jamais", "perdre", "perds", "arrête", "arrete",
         "menti", "mensonge", "personne", "secret", "vérité", "verite", "piège", "piege", "non", "pas", "aucun", "aucune",
         "pire", "gaspille", "inutile", "attention", "surprendre", "surprend", "choc", "vraiment", "contre", "sans", "plus", "moins",
         "dangereux", "mort", "mourir", "maigrir", "grossir", "graisse", "annule", "annuler", "pourquoi", "comment", "où", "combien"}
ADRESSE = {"tu", "t'", "te", "toi", "ton", "ta", "tes", "vous", "votre", "vos"}
NOMBRES = {"un", "une", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "vingt", "trente", "cent", "mille",
           "million", "moitié", "demi", "litre", "litres", "heures", "minutes", "kilos", "calories"}
OUVERTURES_FAIBLES = [r"^\s*(salut|bonjour|coucou|hey|hello|yo|bienvenue)\b", r"\baujourd'hui\b", r"\bdans cette vid[ée]o\b",
                      r"\bje vais te (montrer|expliquer|parler)\b", r"\bje t'explique\b", r"\bstop scroll", r"\bn'oublie pas de\b",
                      r"^\s*(alors|donc|bon|ok|euh)\b"]
FORMULES = [("mythe", r"\?\s*(non|faux)\b|\bmythe\b|on t'a menti"), ("chiffre-faux", r"\bou (deux|trois|2|3)\b"),
            ("personne-ne-dit", r"\bpersonne ne (te|vous) dit\b"), ("stop", r"^\s*(arr[eê]te|stop)\b"),
            ("permission", r"\b(tu n'as pas besoin|pas besoin de)\b"), ("danger-bonne-nouvelle", r"\ben danger\b|\bbonne nouvelle\b"),
            ("tu-fais-faux", r"\btu .{3,40}\bpour\b.{0,30}\?"), ("versus", r"\b\w+ ou \w+ \?"), ("ou-part", r"^\s*o[uù] (part|va|vont)\b"),
            ("statistique", r"\d+\s?%|\bseulement \d"), ("objection", r"^\s*[«\"]"), ("cible", r"\b(si tu|tu t'entra[iî]nes|tu travailles)\b")]


def mots(t):
    return re.findall(r"[\wàâäéèêëîïôöùûüçœ']+", t.lower())


def noter(h):
    w = mots(h)
    n = len(w)
    long_ = 100 if n <= 12 else max(0, 100 - (n - 12) * 9)
    concret = 100 if re.search(r"\d", h) else (70 if any(x in NOMBRES for x in w) else 30)
    enjeu = min(100, 35 * sum(1 for x in w if x in ENJEU)) if w else 0
    adresse = 100 if any(x in ADRESSE or x.startswith("t'") for x in w) else 25
    faible = [p for p in OUVERTURES_FAIBLES if re.search(p, h.lower())]
    ouverture = 0 if faible else 100
    score = round(0.2 * long_ + 0.25 * concret + 0.25 * enjeu + 0.15 * adresse + 0.15 * ouverture, 1)
    if faible:
        score = min(score, 45)
    formule = next((f for f, p in FORMULES if re.search(p, h.lower())), "-")
    checks = {"LONGUEUR": long_, "CONCRET": concret, "ENJEU": enjeu, "ADRESSE": adresse, "OUVERTURE": ouverture}
    return score, checks, formule, n, bool(faible)


def verdict(s):
    return "FORT" if s >= 70 else "MOYEN" if s >= 50 else "FAIBLE"


def main():
    hooks = []
    a = sys.argv[1:]
    if "--hook" in a:
        hooks = [a[i + 1] for i, x in enumerate(a) if x == "--hook"]
    else:
        ep = os.path.abspath(a[0])
        S = json.load(open(os.path.join(ep, "source/script.json")))["sentences"]
        first = S[0]["text"]
        hooks = [first]
        print(f"Accroche lue dans {os.path.basename(ep)} : première entrée de script.json")
    res = sorted(((noter(h), h) for h in hooks), key=lambda x: -x[0][0])
    for (s, ch, f, n, faible), h in res:
        print(f"\n{s:5.1f}  {verdict(s):6}  {n} mots · formule : {f}\n   « {h} »")
        print("   " + " · ".join(f"{k} {v}" for k, v in ch.items()))
        if faible:
            print("   ! ouverture faible (salutation ou préambule) : à supprimer")
        pire = min(ch, key=ch.get)
        if ch[pire] < 60:
            print(f"   point faible : {pire}")


if __name__ == "__main__":
    main()
