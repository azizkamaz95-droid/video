# Design — CaliBodi shorts v2 (3D kinetic)

Concept : un « laboratoire du mythe » en 3D — les mots sont des objets qui volent vers la caméra, la chaleur (orange/rouge)
affronte l'eau (cyan), et chaque révélation est un tampon qui claque.

- Fond `#0A0A0F`, panneaux `#15151F`, filets `#2A2A3A`, texte `#F4F1EC` (blanc chaud).
- Chaleur `#FF6B35`, alerte/faux `#FF2D55`, eau `#00D4FF`, positif `#00FF87`. Une couleur dominante par scène.
- Display : League Gothic (majuscules, extrusion 3D par text-shadow, interlignage 0.86, approche -0.01em).
- Sous-titres et accroches secondaires : Montserrat 900. Étiquettes / métadonnées : IBM Plex Mono 700, capitales, approche 0.14em.
- Profondeur : perspective 1600px par scène, entrées en z/rotationX/rotationY, cartes qui pivotent (backface hidden).
- Zones : graphismes y 230–1100, sous-titres y 1130–1290 (x 60–900), Calix bas-gauche (haut ≈ y 1330). Rien d'essentiel à droite de x 920 entre y 760 et 1480.
- Fond vivant permanent : sol en grille 3D qui défile, halos colorés par section, particules en profondeur, grain + vignette.
