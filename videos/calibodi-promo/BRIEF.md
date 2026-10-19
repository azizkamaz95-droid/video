---
workflow: product-launch-video
flow: automation
storyboard: no
mode: autonomous
message: "CaliBodi réunit sport, nutrition, récupération et hydratation dans un seul coach IA qui s'adapte à toi."
destination: youtube-website
aspect: 1920x1080
language: fr
audience: "Francophones 18-40 ans qui veulent se mettre ou se remettre au sport et jonglent entre plusieurs applis"
length: 60s
angle: "problem-solution — l'éparpillement (une appli par besoin) face à un corps qui fonctionne comme un tout"
narration: yes
voice: "google-tts fr-FR-Neural2-D, pitch -3, rate 1.0"
vo_mode: restructured
captions: skipped
---

## Intent

Vidéo motion design pour vendre l'application CaliBodi (Android, Google Play). Elle présente l'app
de façon premium et parle des quatre piliers : sport, nutrition, récupération, hydratation. Ton :
énergique, sûr de lui, sportif, haut de gamme — direction « nuit de salle de sport » : photos noir & blanc
dramatiques, fond quasi noir, accents néon par pilier. Le client a délégué toutes les décisions
créatives (« montre-moi de quoi tu es capable », « tu es un designer senior »).

## Assets

- capture/app/dashboard.png — vrai écran Accueil (anneau Mouvement/Nutrition/Récup, Calix). Scène connexion.
- capture/app/nutrition.png — vrai écran Nutrition (1510/2880 kcal, macros, repas). Scène nutrition.
- capture/app/fitness.png — vrai écran Training (séance adaptée, modes Normal/Voyage/Fatigue/Express). Scène sport.
- capture/app/session.jpg — vrai écran de séance (Montées de genoux, compteur). Scène sport.
- capture/app/sleep.png — vrai écran Récupération (score 40, dette 3.5h, séance allégée). Scène récup.
- capture/app/hydration.png — vrai écran Hydratation (2250/3230 ml, +500 ml après séance). Scène hydratation.
- capture/app/progress.png — vrai écran Progression (streak, badges). Scène connexion / CTA.
- capture/brand/icon-512.png — logo CB (dégradé orange → rouge → bleu).
- capture/photos/*.jpg — photos N&B de l'app (salle, assiette, récupération, athlète, dos).
- capture/exercises/*.mp4 — animations anatomiques d'exercices de l'app (360x360, fond blanc).

## Customizations

- Voix off Google Cloud TTS (pas HeyGen) : fr-FR-Neural2-D, pitch -3 — choix validé avec le client.
- Musique et effets sonores composés en synthèse procédurale (pas de compte HeyGen, pas de MusicGen).
- Sous-titres classiques désactivés : la typographie cinétique reprend les mots-clés de la voix off.

## Notes

- Vrais écrans capturés depuis l'app locale (Next.js) avec un profil de démo « Thomas » pré-rempli.
- Faits produit vérifiés dans le code : 300+ recettes (361 entrées), scan photo IA multi-aliments,
  objectif d'eau = poids × 35 ml (+ bonus post-séance), séance allégée si dette de sommeil,
  coach vocal Calix, modes Express 5/10/15 · Voyage · Fatigue · Cycle, essai Premium 7 jours.
- Disponible sur Google Play uniquement (le site ne montre que ce store).
