# PLAYBOOK — Créer et publier une vidéo CaliBodi par jour

Guide à suivre à la lettre, d'une session à l'autre. Il résume ce qu'on a appris sur 5 vidéos (abdos, métabolisme, éjaculation précoce, vidéos X, physique ou argent). Les règles de l'utilisateur passent avant tout le reste.

---

## 0. Règles non négociables

1. **Rien n'est publié sans accord explicite** de l'utilisateur sur le script, puis sur la vidéo finale, puis sur l'heure.
2. **Aucune femme** dans les images et vidéos (hommes de dos, silhouettes, mannequins 3D, objets, lieux). Aucun visage identifiable. Aucun logo ni marque. Rien de sexuel à l'image.
3. **Jamais de chiffre inventé.** Chaque chiffre vient d'une étude retrouvée sur le web, avec sa source affichée à l'écran. Si une étude est retirée ou fragile, on le dit (« retirée en 2021 », « petite étude »), on ne la présente jamais comme fausse sans preuve.
4. **Phrases simples et courtes**, une idée et un seul chiffre par phrase. L'utilisateur a déjà refusé des phrases compliquées (« cinq minutes quatre », « les femmes accordent plus d'importance… »).
5. **Une seule thématique par vidéo.** La question posée aux spectateurs porte sur le même sujet que la vidéo, jamais sur un autre.
6. **Promesse cohérente du début à la fin.** Si on annonce « 3 choses qui influencent X », les 3 doivent bien influencer X.
7. **Ne pas refaire d'anciennes vidéos** et ne pas aller relire l'historique pour rien : les crédits de l'utilisateur sont limités. On travaille uniquement sur la vidéo du jour.
8. Ne jamais écrire de clé ni de mot de passe dans un fichier. Les clés sont dans les variables d'environnement.
9. Écrire **CaliBodi** exactement ainsi (C et B majuscules).

---

## 1. Rythme quotidien (1 vidéo par jour, publiée à 18h heure de Paris)

| Étape | Qui | Ce qui se passe |
|---|---|---|
| 1 | Claude | Propose **3 sujets** variés (voir §2). |
| 2 | Utilisateur | Choisit un sujet. |
| 3 | Claude | Recherche les sources sur le web, écrit le **script** (§3) avec les sources. |
| 4 | Utilisateur | **Valide le script** (ou demande des changements). Rien ne se produit avant ce « go ». |
| 5 | Claude | Produit la vidéo (§5 à §8), la miniature (A et B) et la description. |
| 6 | Utilisateur | **Valide la vidéo** et choisit la miniature. |
| 7 | Claude | **Planifie** la publication dans `queue/` (§10). |

Pour économiser les crédits : pas de recherche inutile, on réutilise les modèles et scripts existants (`build_v4.py`, `shots.py`, `lib/*`), on ne vérifie que ce qui est nouveau.

---

## 2. Choisir les sujets

**Le sujet doit être provocateur, tabou ou débattu, mais honnête et vérifiable.** Il doit toujours se rattacher à ce que CaliBodi propose (entraînement, sommeil, alimentation, hydratation, suivi), pour que la conclusion mène naturellement à l'app.

**Catégories à faire tourner** (ne jamais enchaîner deux fois la même) :
- Mythe contre réalité (métabolisme, transpiration, abdos, graisse localisée…)
- Débat tranché : on prend un camp clair pour déclencher les commentaires (« physique ou argent ? C'est le physique. »)
- Sujet tabou ou intime traité par la science (sexualité, performance, désir, porno), ton factuel, jamais cru
- Chiffre choc (sommeil, sucre, sédentarité, hydratation)
- Erreur courante de salle de sport
- Nutrition : ce qu'on croit sain et ne l'est pas, ou l'inverse
- Récupération, sommeil, stress

**Règle de variété (anti-« contenu répétitif ») :** d'un jour à l'autre, changer au moins trois éléments : la catégorie, la couleur dominante du fond, la musique ou son placement, l'ordre des révélations, les poses de Calix, le type d'images (objets, lieux, mains, silhouettes).

**À éviter :** sujets médicaux graves sans source solide, promesses de résultat, comparaisons dénigrantes, mots très explicites dans l'accroche et dans les hashtags (risque de limitation de portée).

---

## 3. Structure du script (60 à 75 secondes)

Toujours **plus d'une minute** (monétisation). Chaque bloc est écrit en phrases très courtes.

| Temps | Bloc | Contenu |
|---|---|---|
| 0–3 s | **Accroche** | Le sujet + la promesse. Ex : « Physique ou argent ? Je vais te le dire. C'est le physique. » |
| 3–9 s | **Annonce des 3 faits** | « Trois faits que presque personne ne te dit. Le troisième va te surprendre. Reste jusqu'au bout. » (boucle ouverte : le plus fort est gardé pour la fin) |
| 9–25 s | **Fait n°1** | Un contexte, une étude, un chiffre. Le plus rassurant ou le plus attendu. |
| 25–40 s | **Fait n°2** | Monte d'un cran. Une transition courte (« Fait numéro deux. »). |
| 40–55 s | **Fait n°3, celui qui choque** | « Celui que je t'ai promis. » C'est le retournement : il contredit ce que le spectateur croyait, ou il change le sens des deux premiers faits. |
| 55–62 s | **Nuance honnête** | « Attention : ce sont des liens, pas des preuves. » / « Petite étude. » + « Parle-en à un médecin » si le sujet touche la santé. |
| 62–68 s | **Bonne nouvelle + pont vers CaliBodi** | Une solution simple et actionnable : « Entraînement, sommeil, alimentation. » |
| 68–72 s | **Question aux commentaires** | Sur le même sujet. Réponse simple (oui/non, 1-2-3, vrai/faux). Pour un débat : s'adresser directement au camp adverse (« Les filles, c'est vrai ou c'est faux ? »). |
| 72–78 s | **Appel à l'action** | Partage à quelqu'un qui doit l'entendre → « Abonne-toi : une nouvelle vidéo chaque jour à 18h. » → **CaliBodi** (§9). |

**Règles d'écriture :**
- 12 mots maximum par phrase quand c'est possible. Pas de subordonnées longues.
- Les chiffres s'écrivent à l'écran en chiffres, mais dans le fichier de voix (`say`) **en toutes lettres** : « dix mille », « soixante-dix pour cent ».
- Pas de guillemets « » dans le texte lu.
- Jamais « tu dois ». Plutôt « voilà ce que montre l'étude ».
- Le troisième fait doit **vraiment** être le plus surprenant, sinon l'annonce trompe le spectateur (et la rétention s'effondre).

---

## 4. Rétention : garder les gens jusqu'à la fin

Le signal le plus fort pour TikTok, Instagram et YouTube est que la vidéo soit regardée jusqu'au bout.

1. **Accroche dans les 3 premières secondes** : un mot-choc à l'écran en très gros (« X », « 3 », un chiffre) et la voix qui démarre dès 0,2 s.
2. **Boucle ouverte annoncée** dès le début : « le troisième va te surprendre ». Les faits 1 et 2 sont satisfaisants seuls, le 3 est gardé pour la fin.
3. **Un changement visuel toutes les 2 à 5 secondes** : nouvelle image, coupe, texte qui tombe, zoom.
4. **Barre de progression en haut** avec un repère à chaque fait : elle donne envie de voir la suite.
5. **Numérotation visible** : « FAIT N°1 », « FAIT N°2 », puis un gros « 3 » seul à l'écran avant le dernier fait, avec un flash ou un éclair.
6. **Sous-titres toujours à l'écran**, 1 à 2 mots à la fois, le mot dit en jaune.
7. **Durée utile** : 60 à 75 s, pas de blanc (> 0,5 s de silence dans la voix = on coupe).
8. **Question avant l'appel à l'action** pour pousser aux commentaires (l'algorithme valorise l'engagement).
9. **Fin qui incite à revoir** : le dernier plan (CaliBodi) reste net et simple.

---

## 5. Voix off

- Outil : `shorts/lib/tts_script.py` (Google Chirp3-HD `fr-FR-Chirp3-HD-Sadachbia`, vitesse **1.0**, `max_gap` 0,5 s).
- Écrire les phrases dans `source/script.json`. Regrouper deux phrases très courtes dans la même entrée pour qu'elles gardent une intonation naturelle (sinon la voix les dit trop vite).
- **Apostrophes :** l'outil colle automatiquement les élisions pour la voix (« nétait », « lâge ») car la voix coupe sinon les mots (« n est »). Exception : **« l'argent »** reste avec apostrophe (collé, il est lu « large »). Si un mot est mal dit, tester les variantes par transcription.
- **Contrôle obligatoire après génération :** `align_words.py` puis lire `source/transcript-edit-assemblyai.json`. Tous les mots doivent revenir corrects. Corriger tout mot déformé avant de monter.
- `calibodi.com` se lit « calibodi point com » (champ `say`).
- Pas de guillemets « » dans les textes lus.

---

## 6. Médias (images et vidéos)

- Source : **Pixabay** (licence commerciale). Script : `python3 lib/pixabay.py <épisode> video id:<id>` ; avec `PX_MIN=1920` pour récupérer la version 4K (nette en recadrage vertical).
- **Vérifier chaque vidéo image par image** avant de l'utiliser : pas de femme, pas de visage identifiable, pas de logo, pas de maillot de bain. Écarter les vidéos douteuses (ex. plage avec des gens, prise de tension avec un bras ambigu).
- Recadrer en vertical 1080×1920 avec `ffmpeg` (`crop` + `scale` lanczos), enlever l'audio (`-an -dn`), 30 images/s.
- Éléments utiles : mains sur un téléphone, ville de nuit, objets (sablier, horloge, billets, alliances, café, livre), silhouettes, mannequins 3D, ciel d'orage (éclair pour le « fait n°3 »), schémas dessinés (pictogrammes d'hommes pour les pourcentages).
- Pour un fond uni derrière une silhouette : détourage `chromakey` d'une silhouette sur fond vert, sur un dégradé bleu.
- Garder le fichier `assets/stock/credits.json` (source et auteur de chaque média).

---

## 7. Montage (style « v4 cinéma »)

Outils : `shorts/episodes/<épisode>/build_v4.py` + `shots.py` (liste des plans). Projet HyperFrames.

**Structure :**
- **Plein écran vertical**, un plan de 2 à 6 s par idée. Étalonnage `deep-contrast` (intensité 0,7) avec vignettage et grain léger. Éclaircir un plan trop sombre (`exposure`, `shadows`).
- **Peu d'éléments, très gros** : 1 chiffre géant ou 1 à 2 étiquettes par plan. Police Montserrat Black, étiquettes jaunes `#FFC93C` ou blanches, texte blanc avec ombre.
- **Chiffres animés** (comptage), pictogrammes qui s'allument (30 %, 7 sur 10, 33 sur 40), cartes, schémas simples.
- **Sources** en petit en haut de l'écran (sous la barre), jamais en bas (cachées par l'interface).

**Effets de caméra et transitions (à varier d'un plan à l'autre) :**
- **Whip pan** (balayage rapide), **zoom traversant**, **flash blanc** (surtout sur « Fait n°… »).
- **Punch-in** : petit zoom (1,04 à 1,10) sur chaque mot-clé ou chaque chiffre, avec retour lent.
- **Tremblement** de l'écran sur un mot fort (« contrôle », le chiffre 3).
- **Ken Burns** : zoom lent sur chaque plan (alterner zoom avant et arrière).
- Éclair ou flash sur « Fait numéro trois ».

**Sous-titres :** 1 à 2 mots, gros, au centre bas, contour sombre, mot actif en jaune, légère animation d'apparition.

**Calix (en bas à gauche) :**
- Il **respire et bouge en continu** (légers mouvements), et change de pose à chaque idée.
- **La pose doit correspondre à ce qui est dit** (l'utilisateur l'a signalé : une pose « bâille » sur un fait important est un défaut). Correspondances :
  - accroche, surprise : `choc` ; chiffre étonnant : `choc`
  - explication : `explique` ; doute, « pas forcément » : `sceptique`, `curieux`
  - numéros : `un`, `deux`, `trois` à leur fait
  - désigner, interpeller : `pointe` ; bien, rassurer : `pouce`
  - force, entraînement : `biceps` ; alimentation : `nutrition`
  - non, faux, erreur : `non` ; énervé : `enerve`
  - app CaliBodi : `app`
  - **Éviter `fatigue` et `endormi`** sauf si le sujet est le sommeil.

**Contrôles qualité avant rendu (obligatoires) :**
1. `npx hyperframes check` : 0 erreur (chevauchements de texte, contraste).
2. Captures de **chaque plan** (`snapshot`) : aucun texte coupé, aucune image noire, aucun chevauchement.
3. **Identifiants uniques** : ne jamais donner à une étiquette le même `id` qu'une vidéo du plan (la vidéo s'affiche mal, le montage plante).
4. Après rendu : transcription du fichier final pour vérifier que la voix est entière et correcte.

---

## 8. Audio

- **Musique : « The Plan »** (Pixabay), bouclée sur une phrase de 8 s (lecture de 0 à 48 s, puis reprise à 8 s, `music_loop: [8, 48]`). L'utilisateur la préfère à « Peace Morning ».
- **Bruitages** (`audio_short.py`) : whoosh sur chaque coupe, stamp sur chaque mot-clé, tick pour le chrono, thump sur les révélations, shimmer pour le « fait n°3 ». L'outil retire tout bruitage qui masquerait un mot.
- **Volume : master fort pour les haut-parleurs de téléphone** : `shorts/lib/master_loud.sh` (cible environ -10,5 LUFS, voix plus claire, basses de la musique rendues audibles sur petit haut-parleur). Contrôler : pic sous -1 dBFS.
- **Ne pas ajouter de son tendance** à la publication : la musique est déjà dans la vidéo.

---

## 9. CaliBodi à la fin (publicité de l'app)

Toujours dans les 6 dernières secondes, après la question et l'appel à l'abonnement :
1. **Voix :** « Pour suivre tes entraînements, ton sommeil et ton alimentation, découvre CaliBodi sur calibodi.com. »
2. **À l'écran :** 3 écrans de l'app qui montent (entraînement, sommeil, alimentation), puis le **logo**, **CaliBodi** en très gros, **calibodi.com** dans une étiquette jaune, **Play Store · App Store**.
3. **Calix** avec la pose `app` puis `pouce`.
4. Selon le sujet, adapter la liste (hydratation, progression…), toujours avec 3 éléments maximum.
5. **Pont naturel** juste avant : la « bonne nouvelle » doit mener à l'app (« Entraînement, sommeil, alimentation »).

---

## 10. Description, miniature, publication

**Miniature :** produire **2 versions** (A et B), 1080×1920, avec le logo CaliBodi en haut, un grand titre, Calix, un élément d'image. L'utilisateur choisit.

**Description (même texte pour les 4 réseaux) :**
- 1re ligne : sujet + promesse.
- Les 3 faits résumés en 1 à 2 lignes chacun, avec les chiffres.
- La nuance honnête (« ce sont des liens, pas des preuves », « petite étude »).
- La question aux commentaires.
- « Abonne-toi : une nouvelle vidéo chaque jour à 18h. »
- CaliBodi : `calibodi.com · Disponible sur Play Store et App Store.`
- Sources (auteurs, revue, année).
- « Vidéo générée par IA. »
- **3 hashtags maximum** (TikTok et Instagram refusent ou pénalisent au-delà ; Instagram refuse plus de 5). Hashtags liés au sujet, jamais explicites. Toujours `#calibodi`.
- **Pas de guillemets droits (")** dans le titre ni la description (ils cassent les commandes de publication). Les retours à la ligne sont acceptés.

**Cases à cocher à la main** dans chaque application : « contenu généré par IA ».

**Planifier la publication :**
1. Compresser la vidéo à environ **25 Mo** (H.264, 1080×1920, ≤ 90 s). Nom de fichier simple, sans caractères spéciaux ni points de suspension.
2. Déposer dans le dépôt `azizkamaz95-droid/calibodi-publish`, branche `main`, un dossier `queue/AAAA-MM-JJ-nom/` contenant la vidéo `.mp4` et un `metadata.json` :
```json
{
  "title": "Titre sans guillemets droits",
  "description": "Texte avec\nretours à la ligne et 3 hashtags #a #b #calibodi",
  "networks": ["youtube", "tiktok", "instagram", "facebook"],
  "publish_at": "2026-10-28T17:00:00Z"
}
```
3. `publish_at` est en **UTC** : 18h à Paris = **17:00Z en hiver** (jusqu'au 27 mars 2027), **16:00Z en été** (à partir du 28 mars 2027).
4. Toutes les 5 minutes, `scheduled.yml` déplace la vidéo due dans `videos/` et lance `publish.yml` (YouTube, TikTok, Instagram via Buffer, Facebook via Make), puis nettoie. GitHub peut retarder de quelques minutes.
5. **Toujours vérifier sur GitHub (Actions) qu'un envoi est réellement parti ou non** avant d'affirmer quoi que ce soit à l'utilisateur.

---

## 11. Problèmes déjà rencontrés (et solutions)

| Symptôme | Cause | Solution |
|---|---|---|
| La voix dit « n est », « le age » | Apostrophe | Collage automatique pour la voix (§5) ; vérifier par transcription |
| « l'argent » dit « large » | Collage inadapté à ce mot | Exception dans `tts_script.py` |
| Phrases dites trop vite | Phrases très courtes isolées | Les regrouper ; vitesse 1.0 |
| Son faible sur téléphone | Musique faite de basses, volume cible trop bas | `master_loud.sh` |
| Pose de Calix qui ne correspond pas | Poses mal choisies | Table du §7 |
| Facebook ne publie pas | Make avait des valeurs figées (ancien test) et un message mal formé | Mapper `video_url`, `title`, `description` ; envoi via `jq` |
| Instagram « media error » | Vidéo supprimée juste après l'envoi | Attendre 3 min avant le nettoyage (déjà en place) |
| TikTok « trop d'envois » | Limite quotidienne de Buffer | Réessayer le lendemain, `networks: ["tiktok"]` |
| Publication bloquée « Installer les dépendances » | Miroir Ubuntu (apt) trop lent | `ffmpeg` installé via `pip` (déjà en place) |
| Scénario Make inactif | Erreurs consécutives / connexion expirée | Reconnecter Facebook, vérifier l'interrupteur ON avant 18h |
| Vidéo publiée en double | Un envoi parti sans que je le voie | Vérifier systématiquement les exécutions sur GitHub |
| Vidéo noire dans le rendu | `<video>` sans identifiant unique, ou doublon d'`id` | Identifiants uniques |

---

## 12. Checklist finale avant de dire « c'est prêt »

- [ ] Script validé par l'utilisateur, sources affichées à l'écran
- [ ] Voix : transcription complète et correcte, durée entre 60 et 78 s, aucun blanc de plus de 0,5 s
- [ ] Médias : aucune femme, aucun logo, aucun visage identifiable ; crédits enregistrés
- [ ] `check` sans erreur ; chaque plan vérifié en capture ; Calix accordé à chaque phrase
- [ ] Master fort (≈ -10,5 LUFS), pic < -1 dBFS ; musique « The Plan »
- [ ] Fin CaliBodi : écrans de l'app, logo, calibodi.com, Play Store · App Store
- [ ] 2 miniatures (A/B) ; description avec 3 hashtags ; sans guillemets droits
- [ ] Vidéo compressée (≈ 25 Mo), nom simple, `metadata.json` valide, `publish_at` en UTC
- [ ] Scénario Make sur ON ; mention « contenu IA » rappelée à l'utilisateur
- [ ] Après dépôt dans `queue/` : vérifier sur GitHub que la file est bien enregistrée

---

## 13. Réglages techniques de référence

- Format : 1080×1920, 30 fps, H.264, AAC. Rendu `hyperframes render --quality delivery`, encodage final 2 passes ≈ 5 Mbit/s puis compression à ≈ 25 Mo pour l'envoi.
- Couleurs : fond sombre cinéma ou, pour les épisodes « papier », rotation Soleil / Cobalt / Corail ; jaune `#FFC93C` pour les accents.
- Dossiers : `shorts/episodes/AAAA-MM-JJ-sujet/` (script dans `source/script.json`, plans dans `shots.py`, montage dans `build_v4.py`, sorties dans `renders/`).
- Dernier épisode de référence : `2026-10-26-physique-argent` (copier ce dossier comme modèle).
