#!/usr/bin/env bash
set -euo pipefail

echo "Refreshing all existing card sets in card_set_lookup/ ..."
shopt -s nullglob
for FILE in card_set_lookup/*.json; do
  SET_ID=$(basename "$FILE" .json)
  echo "Updating set: $SET_ID"
  curl -sS "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}&orderBy=number" -o "$FILE"
  echo "Updated: $FILE"
done
echo "All card sets refreshed."
