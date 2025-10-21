#!/usr/bin/env bash
set -euo pipefail

# Prompt for set id (e.g., base1, base4)
read -rp "Enter TCG Card Set ID (e.g., base1, base4): " SET_ID
if [ -z "$SET_ID" ]; then
  echo "Error: Set ID cannot be empty." >&2
  exit 1
fi

echo "Fetching cards for set: $SET_ID"
# Pokemon TCG API: all cards for a set id
# (No API key here—works for small/demo pulls. Your class test uses local JSON anyway.)
curl -sS "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}&orderBy=number" \
  -o "card_set_lookup/${SET_ID}.json"

echo "Wrote card_set_lookup/${SET_ID}.json"
