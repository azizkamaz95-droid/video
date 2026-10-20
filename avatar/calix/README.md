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
