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

## 1. Rythme quotidien (1 vidéo par jour, un horaire par réseau)

| Étape | Qui | Ce qui se passe |
|---|---|---|
| 1 | Claude | Propose **3 sujets** variés (voir §2). |
| 2 | Utilisateur | Choisit un sujet. |
| 3 | Claude | Recherche les sources sur le web, écrit le **script** (§3) avec les sources. |
| 4 | Utilisateur | **Valide le script** (ou demande des changements). Rien ne se produit avant ce « go ». |
| 5 | Claude | Produit la vidéo (§5 à §8), **choisit lui-même la miniature** (une seule), la colle en 1re image (§10) et écrit la description. |
| 6 | Utilisateur | **Valide la vidéo** (la miniature est déjà choisie par Claude ; l'utilisateur ne la choisit plus, sauf s'il demande un changement). |
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
| 72–78 s | **Appel à l'action** | Partage à quelqu'un qui doit l'entendre → « Abonne-toi : une nouvelle vidéo chaque jour. » (**ne plus jamais dire ni afficher « 18h »** : les réseaux sont publiés à des heures différentes) → **CaliBodi** (§9). |

**Règles d'écriture :**
- 12 mots maximum par phrase quand c'est possible. Pas de subordonnées longues.
- Les chiffres s'écrivent à l'écran en chiffres, mais dans le fichier de voix (`say`) **en toutes lettres** : « dix mille », « soixante-dix pour cent ».
- Pas de guillemets « » dans le texte lu.
- Jamais « tu dois ». Plutôt « voilà ce que montre l'étude ».
- Le troisième fait doit **vraiment** être le plus surprenant, sinon l'annonce trompe le spectateur (et la rétention s'effondre).

---

## 3bis. Écrire comme un humain (règle de l'utilisateur, à appliquer à CHAQUE script)
- Phrases courtes : 12 mots maximum, une seule idée par phrase. Si une phrase a une virgule et un « qui / que / dont », la couper en deux.
- Écrire pour l'oreille : lire le script à voix haute dans sa tête. Si on reprend son souffle au milieu, c'est trop long.
- Zéro contradiction : avant de proposer, relire tout le script et vérifier que chaque fait est cohérent avec la prise de position annoncée dans l'accroche et la conclusion (pas de « mais en fait » qui annule ce qu'on vient de dire sans l'assumer).
- Une seule thèse, dite dès le début, répétée à la fin avec d'autres mots.
- Mots du quotidien, pas de jargon ; chaque chiffre s'explique par une image simple.
- Ton parlé : « Regarde », « Imagine », « Et là ». Pas de style « article ».
- Français correct : une preuve est féminine (« première, deuxième, troisième preuve ») et on ne « t'explique » pas « en trois preuves » : les preuves appuient une affirmation. Dire « J'ai trois preuves. » ou « Voici trois preuves. ».
- Voix : éviter les phrases où « n'est », « n'y », « qu'un » se suivent ou se collent (la voix lit « ce ness », « il n y »). Préférer une tournure sans ces élisions, puis relire la transcription de CHAQUE phrase avant de monter. Si la voix est régénérée, copier d'abord `assets/voice/segments.json` vers `source/segments-v1.json` : `build_v4.py` recale alors tous les plans (le son `plan.json` se recale à part).
- **Ponctuation de la voix (règle de l'utilisateur) :** la ponctuation du champ `say` dicte l'intonation. Une affirmation se termine par un point, jamais par « ! » ni « ... » (« La dernière va te surprendre. » sonnait comme une interjection avec « ... !»). Question = « ? ». « ! » seulement pour une vraie exclamation, très rare. L'énergie vient de la voix choisie et du rythme, pas d'une ponctuation forcée. Relire chaque phrase une à une et noter son type (affirmation, question, ordre) avant de générer.
- **Accentuer sans « ! » (règle de l'utilisateur) :** pour donner du relief, utiliser « : » pour introduire (« Première preuve : »), des virgules pour détacher, « ? » pour une vraie question, et des pauses `[pause short]` avant un mot fort. Les balises de pause ne fonctionnent qu'en mode `markup` de l'API (géré par `tts_script.py` dès qu'un `[pause` est présent) ; en mode texte, la voix les lit à voix haute. Toujours vérifier à la transcription que « pause » n'est pas lu.
- Relecture finale obligatoire : compter les mots de chaque phrase, signaler et réécrire celles de plus de 12 mots avant de montrer le script à l'utilisateur.

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

- Outil : `shorts/lib/tts_script.py` (Google Chirp3-HD, vitesse **1.0**, `max_gap` 0,5 s). **Voix choisie par l'utilisateur le 2026-11-06 : `fr-FR-Chirp3-HD-Iapetus`** (plus d'intonation que Sadachbia, qui était jugée monotone). Écrire le champ `say` avec une ponctuation expressive (« ! », une pause « ... » avant une surprise) sans changer les mots.
- Écrire les phrases dans `source/script.json`. Regrouper deux phrases très courtes dans la même entrée pour qu'elles gardent une intonation naturelle (sinon la voix les dit trop vite).
- **Apostrophes :** l'outil colle automatiquement les élisions pour la voix (« nétait », « lâge ») car la voix coupe sinon les mots (« n est »). Exception : **« l'argent »** reste avec apostrophe (collé, il est lu « large »). Si un mot est mal dit, tester les variantes par transcription.
- **Contrôle obligatoire après génération :** `align_words.py` puis lire `source/transcript-edit-assemblyai.json`. Tous les mots doivent revenir corrects. Corriger tout mot déformé avant de monter.
- `calibodi.com` se lit « calibodi point com » (champ `say`).
- **Prononciation des apostrophes (règle de l'utilisateur) :** le collage « nest » était lu « ness ». `tts_script.py` impose maintenant une prononciation IPA aux mots avec apostrophe listés dans `shorts/lib/pronunciations.json` (n'est, c'est, d'eau, l'Anses, qu'un, quelqu'un…). Le fichier utilise `ɛ̃` pour « un » (`œ̃` est refusé par l'API). Tout nouveau mot avec apostrophe doit y être ajouté avec son IPA ; sinon l'ancien collage s'applique. **Avant de monter**, envoyer la voix seule (mp3) à l'utilisateur pour écoute : la transcription ne détecte pas ces défauts.
- Pas de guillemets « » dans les textes lus.

---

### Recette de voix validée par l'utilisateur (2026-11-06) : à appliquer à CHAQUE vidéo
1. Voix `fr-FR-Chirp3-HD-Iapetus`, vitesse 1.0.
2. Champ `say` écrit phrase par phrase, avec le **type** de chaque phrase relu : affirmation = point ; question = « ? » ; ordre/appel (« Réponds en commentaire », « Partage », « Abonne-toi ») = « ! ». Jamais « ... » ni « ! » sur une affirmation.
3. **Accentuer** : « : » pour introduire (« Première preuve : »), virgules pour détacher les chiffres, `[pause short]` avant un mot fort ou une surprise (mode markup géré par `tts_script.py`).
4. Aucun mot ajouté ni retiré par rapport au script validé (les sous-titres viennent du champ `text`).
5. Apostrophes : IPA imposée via `lib/pronunciations.json` (compléter la liste si un nouveau mot apparaît).
6. Contrôle : transcription (aucune balise lue, tous les mots corrects) **puis envoi de la voix seule (mp3) à l'utilisateur pour écoute avant le rendu**.
7. Si la voix est régénérée après le montage : copier `assets/voice/segments.json` vers `source/segments-prev.json` avant, puis recaler `plan.json` (sons) ; `build_v4.py` recale les plans à partir de `source/segments-v1.json`.

## 6. Médias (images et vidéos)

- Source : **Pixabay** (licence commerciale). Script : `python3 lib/pixabay.py <épisode> video id:<id>` ; avec `PX_MIN=1920` pour récupérer la version 4K (nette en recadrage vertical).
- **Analyse obligatoire de CHAQUE clip avant montage (règle de l'utilisateur) :** extraire au moins 5 images réparties sur la durée du clip coupé, à taille lisible, et les regarder. Rejeter : déchets (bouteille plastique abandonnée, ordures), eau sale ou boueuse, bouteilles pouvant évoquer l'alcool, fumée ou scènes menaçantes, femmes, visages, logos. Rechercher les images avec des mots-clés en français (Pixabay indexe en français : « verre d'eau », « robinet eau »…).
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

- **Musique adaptée au sujet, alternée quand c'est possible (règle de l'utilisateur, 2026-11-06).** Lancer `python3 shorts/lib/pick_music.py <épisode> --energy <1-5>` avant `audio_short.py`. **L'énergie de la musique suit le sujet** (règle de l'utilisateur) : 1 = très calme, 2 = calme/explicatif, 3 = léger/quotidien, 4 = dynamique/énergique, 5 = dramatique/choc. Barème : explication scientifique ou santé posée (eau, sommeil, récupération) = 2 ; mythe à démonter, habitude du quotidien (petit-déjeuner, sport à jeun) = 3 ; performance, entraînement, résultats, danger modéré (assis 8 h) = 4 ; sujet choc, risque grave, révélation forte = 5. **La compatibilité avec le sujet passe avant l'alternance** (décision de l'utilisateur) : le script prend la piste de `shorts/music/catalog.json` (champ `energy`) dont l'énergie est la plus proche de celle demandée, même si elle a servi pour la vidéo précédente ; l'alternance ne départage que des pistes aussi adaptées l'une que l'autre (la moins récemment utilisée), la copie dans l'épisode, règle `plan.json` (`music_file`, `music_loop`) et note le choix dans `shorts/music/history.json` (à committer). Pistes : the-plan, documentaire-motivation, corporate-motivation, motivation-quotidienne, epique-trailer. Pour ajouter une piste : mp3 dans `shorts/music/` + une ligne dans `catalog.json`. Changer de musique ne demande que `audio_short.py` + `master_loud.sh` (pas de nouveau rendu des images). Noter la musique utilisée dans `publication.md`. **Licence :** les 4 pistes « audiocoffee » viennent de Freesound, licence non vérifiée ; si elle exige une mention (CC-BY), l'ajouter à la description.
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

**Miniature (décision de l'utilisateur : Claude la choisit, une seule version) :** même style à chaque fois, 1080×1920 : **logo CaliBodi en haut, centré** ; **un titre intrigant** (gros, lisible, 2 à 4 lignes max, un mot ou un chiffre en couleur d'accent) ; **Calix avec une expression intrigante** (sceptique, choqué, curieux selon le sujet) ; **un arrière-plan qui correspond au sujet** (image de la vidéo). Pas de femme, pas de visage, pas de texte qui déborde. Envoyer la miniature avec la vidéo pour information, sans demander de choix.

**Description (même texte pour les 4 réseaux) :**
- 1re ligne : sujet + promesse.
- Les 3 faits résumés en 1 à 2 lignes chacun, avec les chiffres.
- La nuance honnête (« ce sont des liens, pas des preuves », « petite étude »).
- La question aux commentaires.
- « Abonne-toi : une nouvelle vidéo chaque jour. » (**ne plus jamais dire ni afficher « 18h »** : les réseaux sont publiés à des heures différentes)
- CaliBodi : `calibodi.com · Disponible sur Play Store et App Store.`
- Sources (auteurs, revue, année).
- « Vidéo générée par IA. »
- **3 hashtags maximum** (TikTok et Instagram refusent ou pénalisent au-delà ; Instagram refuse plus de 5). Hashtags liés au sujet, jamais explicites. Toujours `#calibodi`.
- **Pas de guillemets droits (")** dans le titre ni la description (ils cassent les commandes de publication). Les retours à la ligne sont acceptés.

**Cases à cocher à la main** dans chaque application : « contenu généré par IA ».

**Planifier la publication :**
0. **Miniature sur la 1re image, pour TOUTES les vidéos et TOUS les réseaux** (décision de l'utilisateur) : après `master_loud.sh`, lancer `shorts/lib/add_cover.sh <master.mp4> <miniature-choisie.jpg> <sortie.mp4>` : la miniature occupe **0,1 s (3 images)**, invisible à l'œil, avec du silence ajouté au son (rien ne se décale). Compresser ensuite cette sortie à la place du master. À faire dès que la miniature est faite (celle que Claude a choisie). Ne pas utiliser `miniature.jpg` dans la file : la miniature est déjà dans la vidéo.
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
   **Un horaire par réseau** : déposer la même vidéo en 4 dossiers `queue/AAAA-MM-JJ-nom-<réseau>/`, chacun avec `"networks": ["<réseau>"]` et son `publish_at` (au moins 10 min d'écart, car les publications passent l'une après l'autre). Horaires validés (heure de Paris) : **Facebook 10h, Instagram 12h, YouTube 16h, TikTok 18h**. Sources : Metricool (TikTok, YouTube), articles (Facebook), estimation (Instagram). Vérifier ses propres statistiques après quelques semaines. Ne pas laisser passer un créneau : proposer les horaires avant qu'ils soient dépassés.
4. Toutes les 5 minutes, `scheduled.yml` déplace la vidéo due dans `videos/` et lance `publish.yml` (YouTube, TikTok, Instagram via Buffer, Facebook via Make), puis nettoie. GitHub peut retarder de quelques minutes.
5. **Toujours vérifier sur GitHub (Actions) qu'un envoi est réellement parti ou non** avant d'affirmer quoi que ce soit à l'utilisateur.

---

## 10bis. Variété et dynamisme (règles de l'utilisateur, à appliquer à CHAQUE vidéo)

**Les vidéos ne doivent pas se ressembler** (les réseaux pénalisent le contenu répétitif) **et doivent être vivantes dès la première seconde.**

**Couleurs : aucune couleur n'est « la » couleur de CaliBodi pour les vidéos.** Choisir un accent différent des deux dernières vidéos : jaune `#FFC93C`, vert menthe `#3DE0C0`, orange `#FF6B35`, cyan `#35C7FF`, magenta `#FF3D81`, vert lime `#B6F23B`, violet `#9B6BFF`, rouge `#FF4D4D`… Le changer partout (`YEL` dans `build_v4.py` et les couleurs de `shots.py`). Varier aussi le fond (sombre, clair, coloré), le grade de couleur et le type d'images. Noter l'accent utilisé dans `publication.md` pour ne pas le répéter.

**Sons : changer le jeu d'effets d'une vidéo à l'autre**, pas toujours les mêmes « whoosh » et « stamp ». Utiliser selon le sujet : clic d'appareil photo (sur un chiffre ou une révélation), caisse enregistreuse, notification, frappe de clavier, battement de cœur, montée (riser), impact grave, glitch, étincelle / ding, rayure de disque, page qui se tourne, tic-tac, applaudissements, pas, vélo… **Si un son manque, le demander à l'utilisateur** (il peut les télécharger sur Pixabay Sound Effects) en donnant la liste précise. Varier aussi le placement de la musique (autre passage, autre filtre) et les effets de mixage.

**Dynamique dès le début (les 2 premières secondes décident) :**
- Un effet **dans la 1re seconde** : zoom d'entrée (punch-in) ou secousse, un son marqué sur le 1er mot, et le titre ou le chiffre qui apparaît tout de suite (jamais de plan statique).
- **Un plan toutes les 1,5 à 4 s**, avec des enchaînements variés (zoom, flash, whip, glitch, flash d'appareil photo) ; ne pas répéter le même enchaînement 3 fois de suite.
- **Zoom (punch-in) sur chaque chiffre clé**, légère secousse sur les moments choc, mouvement lent (Ken Burns) sur les plans plus longs.
- Un **élément qui bouge à chaque idée** (texte qui claque, barre, compteur, icône) ; des chiffres qui s'animent plutôt que posés.
- Vérifier au rendu qu'**aucun plan ne reste immobile plus de 2 s** sans texte ni mouvement.

---

## 10ter. Viralité : méthode ajoutée le 2026-11-06 (idées reprises du skill MIT « instagram-agent-skill », réécrites)

**Constat de départ (données Metricool, TikTok, 17 vidéos) :** toutes les vidéos plafonnent entre 0,93x et 1,32x la médiane (≈ 257 vues), quel que soit le sujet. Le sujet ne décide donc pas de la diffusion ; ce qui compte est l'accroche, la rétention et les partages. Voir `shorts/analytics/report-*.txt`.

**À chaque vidéo, dans cet ordre :**
1. **Accroche** : proposer à l'utilisateur, avec le script, **3 accroches** (formules de `shorts/hooks/formules.json`, une formule différente de la dernière vidéo si possible), notées par `python3 shorts/lib/hook_check.py --hook "…" --hook "…"`. Garder la meilleure. Outil : repère les accroches faibles (> 12 mots, aucun chiffre, aucun enjeu, salutation), il ne devine pas la gagnante.
2. **Première seconde** : dès l'image 1, un gros mot ou un chiffre qui bouge (déjà dans le montage v4) ; la première phrase dite = la thèse ou la question, jamais une mise en route.
3. **Fin en boucle** : la dernière phrase avant l'appel à l'action reprend un mot ou le chiffre de l'accroche (« Aucun chiffre n'est vrai pour tout le monde » → « pas de chiffre magique »), pour donner envie de revoir.
4. **Fin CaliBodi courte (test sur les deux prochaines vidéos)** : au lieu de la longue phrase, dire « Retrouve CaliBodi sur calibodi.com. » (≈ 3 s) avec les écrans de l'app puis le logo ; viser une fin totale de 4 s au lieu de 7 s. Noter `outro_s` dans `analytics/log.json` et comparer le taux d'interaction.
5. **Rythme** : après `build_v4.py`, lancer `python3 shorts/lib/check_rhythm.py <épisode>` ; corriger tout plan de plus de 3 s sans nouvel élément à l'écran.
6. **Légendes par réseau** : TikTok = légende courte (`calibodi-publish/scripts/captions.py` : titre, question, « Vidéo générée par IA. », 3 à 5 hashtags du sujet, jamais de hashtag hors sujet) ; Instagram et Facebook : la phrase d'accroche dans les 125 premiers caractères, 5 hashtags au plus ; YouTube : description complète avec sources.
7. **Analyse à 48 h** : tirer les chiffres via Metricool (TikTok, YouTube), les enregistrer dans `shorts/analytics/raw/`, lancer `python3 shorts/lib/analytics_report.py <relevé>` et compléter `analytics/log.json` (sujet, formule, énergie, musique, voix, durée, outro). Utiliser le rapport pour proposer les sujets suivants : refaire ce qui dépasse 1,5x la médiane, abandonner ce qui reste sous 1x deux fois de suite.
8. **Limites à rappeler à l'utilisateur** : Instagram et Facebook ne sont pas reliés à Metricool (pas de chiffres) ; le taux de visionnage complet TikTok est vide ; la viralité n'est jamais garantie.

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
| Scénario Make inactif | Erreurs consécutives / connexion expirée | Reconnecter Facebook, vérifier l'interrupteur ON avant la 1re publication de la journée |
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
- [ ] Accroche notée (`hook_check.py`), rythme contrôlé (`check_rhythm.py`), légende TikTok courte, musique choisie par énergie (`pick_music.py`)
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
