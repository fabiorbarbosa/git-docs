#!/usr/bin/env bash
set -euo pipefail

# Installs Headroom from GitHub main so the `headroom dashboard` command is
# available even when the latest PyPI release has not caught up with README.

HEADROOM_REF="${HEADROOM_REF:-main}"
HEADROOM_EXTRAS="${HEADROOM_EXTRAS:-all}"
HEADROOM_HOME="${HEADROOM_HOME:-$HOME/.headroom}"
HEADROOM_VENV="${HEADROOM_VENV:-$HEADROOM_HOME/venv}"
HEADROOM_PORT="${HEADROOM_PORT:-8787}"
HEADROOM_TELEMETRY="${HEADROOM_TELEMETRY:-on}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required." >&2
  exit 1
fi

PYTHON_BIN="$(command -v python3)"
PYTHON_VERSION="$("$PYTHON_BIN" - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)"

"$PYTHON_BIN" - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit("Error: Headroom requires Python 3.10+.")
PY

USER_BIN="$("$PYTHON_BIN" - <<'PY'
import site
from pathlib import Path
print(Path(site.USER_BASE) / "bin")
PY
)"

echo "Installing Headroom into: $HEADROOM_VENV"
mkdir -p "$HEADROOM_HOME" "$USER_BIN"

"$PYTHON_BIN" -m venv "$HEADROOM_VENV"
"$HEADROOM_VENV/bin/python" -m pip install --upgrade pip wheel setuptools
"$HEADROOM_VENV/bin/python" -m pip install --upgrade --no-cache-dir \
  "headroom-ai[$HEADROOM_EXTRAS] @ git+https://github.com/headroomlabs-ai/headroom.git@$HEADROOM_REF"

CERT_FILE="$("$HEADROOM_VENV/bin/python" - <<'PY'
import certifi
print(certifi.where())
PY
)"

cat > "$USER_BIN/headroom" <<EOF
#!/usr/bin/env bash
set -euo pipefail

export SSL_CERT_FILE="$CERT_FILE"
export REQUESTS_CA_BUNDLE="\$SSL_CERT_FILE"

exec "$HEADROOM_VENV/bin/headroom" "\$@"
EOF

chmod +x "$USER_BIN/headroom"

echo
echo "Installed wrapper: $USER_BIN/headroom"
echo "Headroom version:"
"$USER_BIN/headroom" --version

echo
echo "Checking dashboard command:"
"$USER_BIN/headroom" dashboard --help >/dev/null
echo "OK: headroom dashboard is available."

echo
echo "Next steps:"
echo "  1. Make sure this is on PATH before other Python script dirs:"
echo "     export PATH=\"$USER_BIN:\$PATH\""
echo
echo "  2. Start the proxy:"
echo "     HEADROOM_TELEMETRY=\"$HEADROOM_TELEMETRY\" headroom proxy --port $HEADROOM_PORT --memory --code-aware --telemetry"
echo
echo "  3. Open the dashboard:"
echo "     headroom dashboard"
echo "     # or: http://127.0.0.1:$HEADROOM_PORT/dashboard"
echo
echo "For a custom OpenAI-compatible gateway upstream:"
echo "     OPENAI_TARGET_API_URL=\"https://your-gateway.example.com\" HEADROOM_TELEMETRY=\"$HEADROOM_TELEMETRY\" headroom proxy --port $HEADROOM_PORT --memory --code-aware --telemetry"
