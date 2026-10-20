---
workflow: product-launch-video
flow: automation
storyboard: no
mode: autonomous
message: "CaliBodi réunit sport, nutrition, récupération et hydratation dans un seul coach IA qui s'adapte à toi."
destination: tiktok
aspect: 1080x1920
language: fr
audience: "Francophones 18-40 ans qui veulent se mettre ou se remettre au sport et jonglent entre plusieurs applis"
length: 63s
angle: "problem-solution — même film que videos/calibodi-promo, adapté au vertical"
narration: yes
voice: "google-tts fr-FR-Neural2-D, pitch -3, rate 0.97"
captions: skipped
---

## Intent

Version TikTok (9:16) de la promo CaliBodi de `videos/calibodi-promo`, demandée par le client le
2026-10-20. Même voix off, même musique, même timeline (`timeline.json` copié) ; chaque scène est
re-mise en page pour le vertical, pas recadrée.

## Assets

- Tous les assets sont copiés depuis `videos/calibodi-promo/assets` (écrans de l'app, photos N&B,
  boucles d'exercices, logo, voix, `audio/bed.wav`).

## Notes

- Zones de sécurité TikTok respectées : rien d'important au-dessus de y≈220 (onglets), sous y≈1480
  (pseudo, légende, musique) ni à droite de x≈920 entre y≈760 et y≈1480 (boutons d'action).
- Disponible sur l'App Store et Google Play : la fin montre les deux badges.
- Toute modification de la voix ou des timings se fait d'abord dans `videos/calibodi-promo`
  (scripts `tts_google.py`, `build_timeline.py`, `audio_bed.py`), puis on recopie `timeline.json`,
  `assets/voice/` et `assets/audio/bed.wav` ici.
