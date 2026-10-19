---
format: 1920x1080
duration: 63s
message: "CaliBodi réunit sport, nutrition, récupération et hydratation dans un seul coach IA qui s'adapte à toi."
arc: Chaos → Déclic → Révélation → Sport → Nutrition → Récupération → Hydratation → Tout connecté → CTA
audience: Francophones 18-40 ans qui jonglent entre plusieurs applis fitness
mode: autonomous
music: host — synthwave/sport 120 BPM composée en synthèse (assets/audio/bed.wav), drop sur la révélation
captions: skipped (la typographie cinétique porte les mots-clés)
---

## Video direction

- **Look:** « salle de sport la nuit ». Fond `#0A0A0F`, photos noir & blanc assombries, vrais écrans de l'app
  dans un téléphone sombre. Une seule couleur d'accent par scène (loi des piliers dans `frame.md`).
- **Type:** Inter 900 minuscule à -0.04em pour les affirmations ; IBM Plex Mono majuscule, 0.14em, pour
  le chrome (kicker « 01 — SPORT », compteurs, labels).
- **Chrome:** barre haute (marque à gauche, index de pilier à droite) + filet bas qui se remplit dans la
  couleur du pilier. Supprimé sur Chaos, Déclic, Révélation et CTA.
- **Motion:** entrées `expo.out`/`power4.out` 0.5–0.9 s, masques de texte ligne par ligne, chiffres qui
  comptent, anneaux qui se remplissent, téléphones qui flottent (bob lent). Sorties rapides 0.25–0.35 s
  juste avant chaque coupe. Coupes sur le temps fort ; balayage de couleur du pilier suivant entre les piliers.
- **Texture:** grain fin et vignette sur toute la vidéo.
- **Audio:** voix grave Neural2-D, musique ducker sous la voix (pré-mixée), SFX synthétisés : pings de
  notification, whooshs, impacts, clics, scan, goutte d'eau.

## Frame 1 — Le chaos

- scene: Une pile de mots se construit (entraînement / calories / eau / sommeil ?) pendant que des icônes d'applis et des notifications envahissent l'écran.
- duration: 8s
- start: 0
- transition_in: cut
- status: animated
- voiceover: "Une appli pour t'entraîner. Une autre pour tes calories. Une gourde que tu oublies… Et ton sommeil ? Personne ne s'en occupe."
- src: compositions/frames/01-chaos.html
- asset_candidates: none (icônes dessinées)

0.6 s « une appli pour t'entraîner » : tuile d'appli haltère tombe à droite + mot « entraînement. » à gauche.
2.1 s « une autre pour tes calories » : tuile fourchette « 1 847 kcal » ; le mot précédent recule (opacité 0.5).
3.6 s « une gourde que tu oublies » : tuile gourde + toast « Rappel : bois de l'eau » ; pile en 1 / 0.5 / 0.22.
5.2 s « et ton sommeil ? » : emplacement vide en pointillés avec lune ; mot « sommeil ? » en orange.
6.3 s « personne ne s'en occupe » : badges 3 / 12 / 99+ et toasts s'empilent, léger tremblement.
7.6 s : implosion de tout vers le centre (sortie 0.4 s).

## Frame 2 — Le déclic

- scene: Le dos d'un athlète en N&B découpé en 5 tranches décalées se recolle d'un coup ; « pas en morceaux. »
- duration: 3s
- start: 8
- transition_in: cut
- status: animated
- voiceover: "Pourtant, ton corps ne fonctionne pas en morceaux."
- src: compositions/frames/02-declic.html
- asset_candidates: capture/photos/profile.jpg

0.0 s tranches décalées verticalement, dérive lente. 0.3 s « ton corps » apparaît. 1.6 s sur « morceaux » :
les tranches claquent ensemble (`back.out`), flash blanc bref, « pas en morceaux. » en display.

## Frame 3 — Révélation

- scene: Drop musical : l'icône CB jaillit avec onde de choc, le nom CaliBodi se monte lettre par lettre, quatre points-piliers en orbite.
- duration: 5.5s
- start: 11
- transition_in: cut
- status: animated
- voiceover: "Voici CaliBodi. Un seul coach, propulsé par l'IA, pour tout ton corps."
- src: compositions/frames/03-reveal.html
- asset_candidates: capture/brand/icon-512.png

0.0 s impact : anneau de choc + icône `back.out` + halo dégradé. 0.6 s « CaliBodi » lettres qui montent.
1.9 s trois puces mono : « UN SEUL COACH » · « PROPULSÉ PAR L'IA » · « POUR TOUT TON CORPS » calées sur la voix.
Points orange/vert/violet/bleu en orbite autour de l'icône. 5.2 s sortie : zoom vers l'icône.

## Frame 4 — Sport

- scene: Photo N&B d'athlète à gauche, vrai écran Training dans le téléphone ; puces niveau/objectif/temps ; bascule sur l'écran de séance et la bulle vocale de Calix.
- duration: 8.5s
- start: 16.5
- transition_in: wipe (orange)
- status: animated
- voiceover: "Des séances guidées, taillées pour ton niveau, ton objectif et ton emploi du temps. Et Calix, ton coach vocal, te pousse jusqu'à la dernière répétition."
- src: compositions/frames/04-sport.html
- asset_candidates: capture/photos/training.jpg, capture/app/fitness.png, capture/app/session.jpg, capture/exercises/high_knees.mp4, capture/exercises/squat.mp4, capture/exercises/pushup.mp4

Phase A (0–4.6 s) : kicker « 01 — SPORT », display « séances guidées. », puces « NIVEAU · INTERMÉDIAIRE »,
« OBJECTIF · PRISE DE MASSE », « 16 MIN » sur les mots de la voix ; téléphone Training + 3 cartes d'exercices animées.
Phase B (4.6–8.5 s) : l'écran glisse vers la séance « Montées de genoux », bulle Calix avec forme d'onde
« Allez, encore 3 ! », display « calix te pousse. », compteur de répétitions 7 → 10.

## Frame 5 — Nutrition

- scene: Viseur photo sur une assiette N&B, boîtes de détection vert néon, calories et macros qui comptent ; puis 300+ recettes et la liste de courses qui se coche toute seule.
- duration: 10s
- start: 25
- transition_in: wipe (vert)
- status: animated
- voiceover: "Prends ton assiette en photo : l'IA reconnaît chaque aliment, et calcule tes calories et tes macros. Plus de trois cents recettes… et ta liste de courses se remplit toute seule."
- src: compositions/frames/05-nutrition.html
- asset_candidates: capture/photos/nutrition.jpg, capture/app/nutrition.png

Phase A (0–5.0 s) : déclic d'obturateur, ligne de scan, 3 boîtes de détection avec étiquettes, panneau
« 412 kcal » + barres protéines/glucides/lipides. Phase B (5.0–10 s) : « 300+ » géant qui compte,
cartes de recettes qui défilent, téléphone Nutrition, liste de courses (saumon, riz, avocat, skyr) cochée une à une.

## Frame 6 — Récupération

- scene: Photo N&B récupération, hypnogramme violet qui se dessine, score nuit 40, curseur d'intensité qui descend à 70 %, vrai écran Récup.
- duration: 6.5s
- start: 35
- transition_in: wipe (violet)
- status: animated
- voiceover: "Nuit trop courte ? CaliBodi le voit, et allège ta séance automatiquement. Tu progresses, sans te cramer."
- src: compositions/frames/06-recup.html
- asset_candidates: capture/photos/sleep.jpg, capture/app/sleep.png

## Frame 7 — Hydratation

- scene: Colonne d'eau bleue avec vague, équation 78 kg × 35 ml = 2 730 ml, puis « +500 ml » après la séance → 3 230 ml ; vrai écran Hydratation.
- duration: 5s
- start: 41.5
- transition_in: wipe (bleu)
- status: animated
- voiceover: "Ton objectif d'eau est calculé selon ton poids… et il grimpe après chaque entraînement."
- src: compositions/frames/07-hydratation.html
- asset_candidates: capture/app/hydration.png

## Frame 8 — Tout est connecté

- scene: Les quatre piliers s'allument un par un, des liens se tracent entre eux, puis tout converge dans l'anneau du score du jour qui compte jusqu'à 87.
- duration: 8s
- start: 46.5
- transition_in: cut
- status: animated
- voiceover: "Sport. Nutrition. Récupération. Hydratation. Tout est connecté, et tout se résume dans un seul score, chaque jour."
- src: compositions/frames/08-connecte.html
- asset_candidates: none (diagramme dessiné, anneau d'après le dashboard)

## Frame 9 — Appel à l'action

- scene: Trois téléphones en éventail (Nutrition, Accueil, Hydratation), logo, « tout ton corps. une seule app. », pastille 7 jours gratuits, badge Google Play.
- duration: 8.5s
- start: 54.5
- transition_in: cut
- status: animated
- voiceover: "CaliBodi. Tout ton corps, une seule app. Essaie-la gratuitement pendant sept jours, sur Google Play."
- src: compositions/frames/09-cta.html
- asset_candidates: capture/brand/icon-512.png, capture/app/dashboard.png, capture/app/nutrition.png, capture/app/hydration.png
