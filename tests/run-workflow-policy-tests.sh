#!/bin/sh
# Fixture tests for scripts/check-workflows.py (ERP-02/.github#27): every pass fixture passes, and every fail fixture
# reports exactly the rule named in its "# expect:" header and nothing else.
set -u
root=$(cd "$(dirname "$0")/.." && pwd)
check="python3 $root/scripts/check-workflows.py"
status=0
for f in "$root"/tests/workflows/pass/*.yml; do
  if out=$($check "$f"); then echo "ok   pass $(basename "$f")"; else echo "FAIL pass $(basename "$f")"; echo "$out"; status=1; fi
done
for f in "$root"/tests/workflows/fail/*.yml; do
  expect=$(sed -n 's/^# expect: //p' "$f")
  out=$($check "$f"); code=$?
  rules=$(printf '%s\n' "$out" | sed -n 's/^[^:]*: \([a-z-]*\): .*/\1/p' | sort -u | tr '\n' ' ')
  if [ "$code" -eq 1 ] && [ "$rules" = "$expect " ]; then echo "ok   fail $(basename "$f") ($expect)"
  else echo "FAIL fail $(basename "$f"): expected '$expect', got '$rules' (exit $code)"; echo "$out"; status=1; fi
done
[ "$status" -eq 0 ] && echo "PASS: workflow policy fixtures" || echo "FAIL: workflow policy fixtures"
exit "$status"
