#!/bin/bash
# Trammel PE — verification gate
# Run before every commit that touches index.html.
# Usage: bash scripts/verify.sh
# Requires: python3, node (dev tools only — the app itself stays zero-dependency)

set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$REPO/index.html"
FAIL=0

echo "== Trammel PE verify =="
echo "Target: $HTML"

# 1. JS syntax — extract every <script> block and node --check it
echo ""
echo "[1/4] JS syntax (node --check)"
python3 - "$HTML" <<'EOF'
import re, sys
html = open(sys.argv[1]).read()
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
for i, s in enumerate(scripts):
    open(f'/tmp/trammel_verify_{i}.js', 'w').write(s)
print(f"extracted {len(scripts)} script block(s)")
EOF
for f in /tmp/trammel_verify_*.js; do
  if node --check "$f" 2>&1; then
    echo "  OK: $f"
  else
    echo "  SYNTAX ERROR in $f"
    FAIL=1
  fi
done
rm -f /tmp/trammel_verify_*.js

# 2. CJK contamination scan (user-facing text must be EN/ES/PT only)
echo ""
echo "[2/4] CJK contamination scan"
CJK=$(python3 -c "
import re
html = open('$HTML').read()
hits = re.findall(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', html)
print(len(hits))
")
if [ "$CJK" -eq 0 ]; then
  echo "  OK: 0 CJK characters"
else
  echo "  FAIL: $CJK CJK characters found"
  FAIL=1
fi

# 3. Critical element IDs present (regression tripwire)
echo ""
echo "[3/4] Critical DOM IDs"
for id in quickBuilder advancedBuilder quickPrompt objective previewFormatted previewMarkdown quickModeBtn advancedModeBtn; do
  if grep -q "id=\"$id\"" "$HTML"; then
    echo "  OK: #$id"
  else
    echo "  FAIL: missing #$id"
    FAIL=1
  fi
done

# 4. i18n key parity — every data-i18n key must exist in all 3 language packs
echo ""
echo "[4/4] i18n key usage check"
python3 - "$HTML" <<'EOF'
import re, sys
html = open(sys.argv[1]).read()
used = set(re.findall(r'data-i18n="([^"]+)"', html))
used |= set(re.findall(r'data-ph="([^"]+)"', html))
# crude per-language block check: each used key should appear at least 3 times as `key:` (en/es/pt)
missing = []
for k in sorted(used):
    count = len(re.findall(rf'\b{re.escape(k)}\s*:', html))
    if count < 3:
        missing.append(f"{k} (defined {count}x, expected >=3)")
if missing:
    print("  FAIL: keys not present in all 3 languages:")
    for m in missing: print("   -", m)
    sys.exit(1)
print(f"  OK: {len(used)} i18n keys present in EN/ES/PT")
EOF
[ $? -ne 0 ] && FAIL=1

echo ""
if [ $FAIL -eq 0 ]; then
  echo "RESULT: ALL GATES PASSED"
else
  echo "RESULT: FAILURES DETECTED — do not commit"
fi
exit $FAIL
