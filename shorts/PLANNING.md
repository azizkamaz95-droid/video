# PLANNING — heures de publication (heure de Paris), à respecter sans redemander

Décision de l'utilisateur (2026-11-08) : il écrit le script chaque jour, je produis la voix puis la vidéo, il valide la vidéo,
et je m'occupe du reste (description, hashtags, miniature, planification) **aux heures ci-dessous, sans qu'il les redonne**.
La validation de la vidéo par l'utilisateur vaut accord de publication aux heures de ce fichier.

## Heures par réseau et par jour

| Jour | TikTok | Instagram | YouTube | Facebook |
|---|---|---|---|---|
| Lundi | 18:00 | 12:00 | 16:00 | 10:00 |
| Mardi | 18:00 | 12:00 | 16:00 | 10:00 |
| Mercredi | 18:00 | 12:15 | 16:00 | 12:00 |
| Jeudi | 10:15 | 12:00 | 16:00 | 10:00 |
| Vendredi | 10:15 | 12:00 | 16:00 | 10:00 |
| Samedi | 10:15 | 11:00 | 16:00 | 10:00 |
| Dimanche | 10:15 | 11:00 | 16:00 | 10:00 |

## D'où viennent ces heures
- **TikTok, YouTube, Facebook** : Metricool, `getBestTimeToPostByNetwork`, semaine du 9 au 15 novembre 2026, fuseau Europe/Paris. Pour chaque jour, on prend l'heure au score le plus haut. Pour TikTok, quand le soir (18 h) est à moins de 5 % du pic du matin (mardi, mercredi), on garde 18 h ; à partir de jeudi le pic de 10 h est nettement meilleur (6 % à 17 % de plus).
  - TikTok : pics à 10 h, 12 h et 18 h chaque jour. Lundi 18 h, jeudi à dimanche 10 h.
  - YouTube : pic à 16 h tous les jours.
  - Facebook : pic à 10 h, sauf mercredi (12 h).
- **Instagram : estimation.** Metricool ne renvoie que des zéros (compte non connecté). Heures prises sur le profil de Facebook (même public Meta) : midi en semaine, 11 h le week-end. **À remplacer dès qu'Instagram est connecté à Metricool.**
- Ces données sont celles de Metricool pour des comptes de ce type, pas encore les nôtres. Vérifier avec `analytics/` après quelques semaines et corriger ce tableau.
- Deux publications du même jour sont espacées d'au moins 10 minutes (les envois passent l'un après l'autre) : d'où 10:15 pour TikTok quand Facebook est à 10:00, et 12:15 pour Instagram le mercredi.

## Conversion en UTC (champ `publish_at` de `queue/…/metadata.json`)
Paris = UTC+1 jusqu'au 27 mars 2027 inclus, puis UTC+2 (à partir du 28 mars 2027). Exemple en hiver : 18:00 Paris = 17:00Z.

## Procédure quotidienne (sans redemander les heures)
1. L'utilisateur envoie son script. Je contrôle les prononciations (`lib/voice_preflight.py`), je génère la voix, il valide l'audio.
2. Je produis la vidéo et la miniature (une seule), l'utilisateur **valide la vidéo**.
3. Je génère le titre, la description, les 3 hashtags (`publication.md`) et je dépose les 4 dossiers `queue/AAAA-MM-JJ-nom-<réseau>/` avec les heures de ce tableau.
4. Jour de publication : le lendemain de la validation, ou le jour même si les 4 heures du jour sont encore à plus de 30 minutes. Une seule vidéo par jour : si le jour est déjà pris, le premier jour libre.
5. Je vérifie sur GitHub (Actions) que chaque envoi est parti, puis je confirme à l'utilisateur.
