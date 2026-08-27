#!/bin/sh
# End-to-end check of the reading-data pipeline against the LIVE site.
# Verifies what is stored, not merely that a request returned 200.
set -e
BASE="${1:-https://paleography.app}"
SID="verify-$$"

echo "1. GET is refused"
curl -s -o /dev/null -w "   http=%{http_code} (expect 405)\n" "$BASE/api/attempts"

echo "2. a malformed body is refused"
curl -s -X POST -H 'Content-Type: application/json' -d '{"nope":1}' \
  -w "\n   http=%{http_code} (expect 400, or 503 if unconfigured)\n" "$BASE/api/attempts"

echo "3. a valid attempt, carrying junk fields that must NOT be stored"
curl -s -X POST -H 'Content-Type: application/json' \
  -d "{\"attempts\":[{\"sid\":\"$SID\",\"t\":\"latin\",\"s\":2,\"n\":10,\"hit\":8,\"id\":\"probe\",\"page\":\"probe.jpg\",\"miss\":[\"r>n\",\"e>c\"],\"forgiving\":true,\"build\":\"verify\",\"typed\":\"SHOULD-NOT-BE-STORED\",\"text\":\"SHOULD-NOT-BE-STORED\"}]}" \
  -w "\n   http=%{http_code} (expect 200 stored:1)\n" "$BASE/api/attempts"

echo "4. keep-alive reaches the store"
curl -s -o /dev/null -w "   http=%{http_code} (expect 200)\n" "$BASE/api/keepalive"

echo
echo "Then in the Supabase SQL editor:"
echo "   select * from attempts where session = '$SID';   -- 1 row, no SHOULD-NOT-BE-STORED anywhere"
echo "   select * from confusions order by n desc limit 10;"
echo "   delete from attempts where session = '$SID';     -- tidy up the probe"
