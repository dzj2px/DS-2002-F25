#!/usr/bin/env bash
set -Eeuo pipefail

API_URL="https://aviationweather.gov/api/data/metar"

# resolve paths relative to this script
script_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
OUTPUT_DIR="$script_dir/raw_metars"
AIRPORT_CODES_FILE="$script_dir/airport_codes.txt"

mkdir -p "$OUTPUT_DIR"
echo "Fetching METAR data for airports..."

# read each ICAO, strip any Windows CR, skip blanks
while IFS= read -r line || [ -n "$line" ]; do
  code=${line%$'\r'}
  [ -z "$code" ] && continue

  url="$API_URL?ids=$code&hours=2&format=json"
  out="$OUTPUT_DIR/$code.json"

  echo "  -> $code"
  echo "     URL: $url"

  # fetch. -f fail on HTTP errors, -s silent, -S show errors
  http_code=$(curl -fsS -A "curl-lab3" -w "%{http_code}" -o "$out" "$url" || echo 000)
  echo "     HTTP $http_code"

  if [ "$http_code" != 200 ] || [ ! -s "$out" ] || [ "$(jq 'length' "$out")" -eq 0 ]; then
    echo "     Warning. no data saved for $code."
  else
    echo "     Saved $out with $(jq 'length' "$out") record(s)."
  fi
done < "$AIRPORT_CODES_FILE"

echo "Done. Check $OUTPUT_DIR"
