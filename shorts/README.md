# Shorts Calix — pipeline

Un mémo vocal sur un sujet fitness → un short TikTok 1080×1920 avec Calix, sous-titres, schémas,
musique discrète et effets sonores. Les règles de montage sont dans [SIGNATURE.md](SIGNATURE.md).

## Ce que fait le client

1. Enregistrer le mémo vocal (m4a, mp3 ou wav), 45 s à 90 s.
2. Le déposer sur GitHub dans `shorts/inbox/` (ou l'envoyer dans la conversation) et donner le sujet en une phrase.

## Ce que fait Claude, épisode par épisode

```bash
EP=shorts/episodes/AAAA-MM-JJ-sujet
(cd shorts/episodes && npx hyperframes init "$(basename "$EP")" --example blank --resolution portrait --non-interactive)
shorts/lib/sync_assets.sh "$EP"                      # poses Calix, polices, GSAP, grain, icône
mkdir -p "$EP/source" && cp memo.m4a "$EP/source/voice-memo.m4a"

# 1. transcription du mémo : AssemblyAI (clé ASSEMBLYAI_API_KEY dans l'environnement, jamais dans le code)
python3 shorts/lib/transcribe_assemblyai.py "$EP/source/voice-memo.m4a" "$EP/source/transcript-memo.json"
#    secours : python3 avatar/transcribe_google.py <memo> <out.json> 55   (GOOGLE_CLOUD_API_KEY, coupes < 60 s)
# 2. relire le texte, écrire plan.json : corrections, respirations, mots-clés, poses, blocs, effets
# 3. nettoyage + suppression des blancs (respirations gardées après les phrases clés)
python3 shorts/lib/cut_silences.py "$EP/source/voice-memo.m4a" "$EP/source/transcript-memo.json" "$EP/plan.json" "$EP/assets/voice"
# 4. minutages des mots sur la voix montée (AssemblyAI si la clé est là, sinon Google), puis filet de sécurité
python3 shorts/lib/align_words.py "$EP"
python3 shorts/lib/refine_words.py "$EP"
# (option) photos / vidéos libres de droits, tracées dans assets/stock/credits.json (PIXABAY_API_KEY)
python3 shorts/lib/pixabay.py "$EP" photo "verre d'eau" 2
python3 shorts/lib/pixabay.py "$EP" video "boire de l'eau" 1
# 5. musique + effets (contrôle anti-masquage), puis composition
python3 shorts/lib/audio_short.py "$EP"              # rapport : $EP/renders/audio-report.txt
python3 shorts/lib/build_short.py "$EP"
(cd "$EP" && npx hyperframes check)
# 6. rendu, puis encodage web (~4 Mb/s, -14 LUFS)
(cd "$EP" && npx hyperframes render --quality delivery --output renders/master.mp4)
```

## plan.json

| clé | rôle |
| --- | --- |
| `corrections` | `{index du mot: "texte corrigé"}` (orthographe, noms propres) |
| `breath_after` | index des mots suivis d'une respiration de 0,38 s (sinon les blancs sont réduits à 0,14 s) |
| `keywords` | `{couleur: [mots]}` surlignés dans les sous-titres |
| `poses` | `[temps, pose]` — poses dans `avatar/calix/poses.json` |
| `camera`, `shakes` | mouvements de caméra simulés ; vibrations réservées aux révélations |
| `science` | plages d'explication : musique baissée de 5 dB, sans batterie |
| `blocks` | graphismes : `myth`, `word_drops`, `banner`, `science`, `scale`, `versus`, `list`, `outro` |
| `sfx` | `[nom, temps]` — `whoosh_in`, `whoosh`, `stamp`, `thump`, `plinks`, `tick`, `click`, `warn`, `check`, `shimmer`, `pop` |

Effets sonores : un fichier déposé dans `shorts/sfx/` (ex. `pop.mp3`, téléchargé sur Pixabay) remplace l'effet
synthétisé du même nom. Le `.gitignore` d'un épisode doit exclure `assets/stock/*` sauf `credits.json`.

## Garanties du mixage

- Voix à -16 LUFS ; musique instrumentale à -29,5 LUFS, creusée entre 1 et 4 kHz et baissée de 7 dB
  quand Calix parle (≈ 19 dB sous la voix dans la bande de la parole).
- Effets déplacés vers la respiration la plus proche et joués entiers dans les respirations ; là où ils touchent
  un mot, seuls leurs graves (< 150 Hz) et leurs aigus (> 2,5 kHz) restent, plafonnés sous les consonnes de la
  phrase, baissés de 4 dB sur l'attaque d'un mot, supprimés s'il faut les baisser de plus de 15 dB.
  Le rapport liste chaque décision.
