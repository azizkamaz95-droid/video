# Calix — avatar CaliBodi

16 poses du personnage Calix (fournies par le client le 2026-10-20, dossier `calix/` de la branche par défaut).

- `source/` — images d'origine renommées (`calix-<pose>.jpg|png`)
- `cutout/` — PNG 1024×1024 détourés (fond transparent), prêts pour HyperFrames
- `poses.json` — pose → usage dans le montage

Refaire un détourage :

```bash
npx hyperframes remove-background source/calix-<pose>.jpg -o /tmp/raw.png
python3 clean_cutout.py source/calix-<pose>.jpg /tmp/raw.png cutout/calix-<pose>.png 2
# pose qui tient un objet (assiette, gourde, téléphone) : garder l'objet avant le nettoyage
python3 keep_objects.py source/calix-<pose>.jpg /tmp/raw.png /tmp/union.png [--dark-objects]
python3 clean_cutout.py source/calix-<pose>.jpg /tmp/union.png cutout/calix-<pose>.png 2
```

`--dark-objects` pour la gourde et le téléphone (objets non blancs) ; sans l'option pour l'assiette blanche.

Pose dont le « fond transparent » est un damier dessiné dans l'image (ex. `calix-endormi`, dans son lit) :

```bash
python3 key_checker.py source/calix-endormi.png cutout/calix-endormi.png 90   # rayon des coins arrondis
```

Pose sur fond chargé (ex. `calix-crunch`, salle de sport) : le modèle de détourage perd le pantalon noir sur le sol
sombre. Le matte final = modèle ∪ pixels sombres et neutres dans un contour de jambe tracé à la main, bord gauche
(jambes coupées par le cadre) lissé. `apercu-crunch-abdos.jpg` montre les deux autocollants sur les fonds v3.
