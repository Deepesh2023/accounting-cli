#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-../frontend/lib/api}"
OPENAPI_JSON="/tmp/printos-openapi.json"

echo "==> Starting backend to extract OpenAPI schema..."
uv run uvicorn src.main:app --host 127.0.0.1 --port 8179 &
SERVER_PID=$!

cleanup() {
  kill "$SERVER_PID" 2>/dev/null || true
  wait "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

# Wait for the server to be ready
for i in $(seq 1 20); do
  if curl -sf http://127.0.0.1:8179/openapi.json > /dev/null 2>&1; then
    break
  fi
  sleep 0.3
done

echo "==> Downloading OpenAPI spec..."
curl -sf http://127.0.0.1:8179/openapi.json > "$OPENAPI_JSON"

echo "==> Stopping server..."
cleanup
trap - EXIT

echo "==> Generating TypeScript client..."
mkdir -p "$OUT_DIR"

if command -v npx &>/dev/null; then
  npx --yes openapi-typescript "$OPENAPI_JSON" --output "$OUT_DIR/schema.d.ts"
  echo "==> Done! Types written to $OUT_DIR/schema.d.ts"
else
  echo "==> npx not found — copying raw OpenAPI spec instead"
  cp "$OPENAPI_JSON" "$OUT_DIR/openapi.json"
  echo "==> Done! Spec copied to $OUT_DIR/openapi.json"
fi
