#!/usr/bin/env bash
# Copy the shared kit (Calix poses, fonts, GSAP, grain, app icon) into an episode.
# usage: shorts/lib/sync_assets.sh <episode_dir>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
EP="$1"
KIT="$ROOT/videos/calibodi-tiktok/assets"
mkdir -p "$EP/assets/calix" "$EP/assets/fonts" "$EP/assets/vendor" "$EP/assets/fx" "$EP/assets/brand"
cp "$ROOT"/avatar/calix/cutout/calix-*.png "$EP/assets/calix/"
cp "$KIT"/fonts/Inter-{400,500,600,700,800,900}.woff2 "$KIT"/fonts/IBMPlexMono-{500,600}.woff2 "$EP/assets/fonts/"
cp "$KIT/vendor/gsap.min.js" "$EP/assets/vendor/"
cp "$KIT/fx/grain.png" "$EP/assets/fx/"
cp "$KIT/brand/icon-512.png" "$EP/assets/brand/"
echo "kit synced into $EP/assets"
