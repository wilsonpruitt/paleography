# Deploy — paleography.app

**Live 2026-08-27.** Static single file on Vercel, DNS at Cloudflare.

| | |
|---|---|
| domain | `paleography.app`, registered at Cloudflare (at-cost, per `reference_domains-cloudflare.md`) |
| host | Vercel, team **wilson-pruitts-projects** (`team_sERwO8…` — the Labs team, not Covenant) |
| project | `paleography` |
| DNS | **A record at the apex, DNS-only.** Nameservers stay at Cloudflare — Vercel asks for `ns1/ns2.vercel-dns.com` and that request is declined on purpose |
| commit author | `littleeachdayapp@gmail.com` (this Vercel team rejects other authors) |

## Build and deploy

```sh
python3 tools/crop.py …            # line crops per witness
python3 tools/build_exercises.py --out build/payload --n 110 --max-w 1700 --quality 80
python3 tools/make_routes.py       # -> site/vercel.json + the API's track allowlist
python3 tools/make_site.py         # -> site/read/index.html + t-<track>.json
sh tools/acceptance.sh             # the bank must not have moved
cd site && npx vercel deploy --prod --yes   # ⚑ from site/ -- NEVER from the repo root
```

✅ **ONE build since 2026-08-28.** There used to be two, and the difference bit: the
Artifact build (`make_trainer.py`) deliberately had no doctype, head or body because the
claude.ai runtime supplied them, and serving that file raw put the browser in quirks mode
with no viewport — which shipped once. **The Artifact build is retired** (Wilson's call);
the site is canonical and `make_site.py` goes straight from `tools/trainer_shell.html`.

⚑ **The payload is split, one file per track.** `/read/index.html` is ~53 KB and inlines
only the ~2 KB index (languages, profiles, routes) because the tab strip and track
resolution are needed before first paint. Each track's lines and images are `t-<id>.json`,
fetched when that track is first opened — so a reader who comes for Greek fetches 5.2 MB,
not the 10.9 MB of everything. `make_site.py` deletes stale `t-*.json` before copying:
a retired track that kept serving its old bank would be invisible.

⛔ **Anything the trainer fetches must use an ABSOLUTE path.** The page lives at `/read/`
but is *reached* at `/greek`, `/latin`, `/latin-ii` — Vercel rewrites, so the browser's URL
stays as typed. A relative `t-greek.json` therefore resolves against `/greek` and 404s at the
apex. This shipped on 2026-08-28: `/read/` worked perfectly while every clean URL — i.e. every
link on the landing page — was broken, which is the worst shape a bug can take because the
obvious test passes. ⚑ It is also untestable locally: `python3 -m http.server` has no rewrites,
so `?track=` is the only form that works there. **Check a clean URL on the real domain after
any deploy that touches loading.**

⛔ **Never hand-edit `site/vercel.json` rewrites or the `TRACKS` allowlist in
`site/api/attempts.js`.** Both are generated from `registry/` by `tools/make_routes.py`;
`--check` fails if they have drifted. The allowlist is the one that fails silently — that
endpoint drops what it does not recognise, so a stale list loses a new language's reading
data without an error anywhere.

## Open items

- ✅ **Contact is `wilson.pruitt@gmail.com`** (Wilson's call: *"if this becomes an issue, that
  would be a good sign"*). Set in one place — `CONTACT` at the top of the trainer's script, and
  the mailto on the landing page. Left as plain text rather than assembled in JS: a mailto that
  breaks when a script fails is worse than a scraped address.
- ⬜ **No `www` CNAME.** The apex works; `www.paleography.app` does not resolve. Add
  `CNAME www → cname.vercel-dns.com`, DNS-only, if wanted.
- ⚠ **The page is 10.9 MB in one request** — every line image is inlined as base64, which is
  what the Artifact needs. It serves in ~1.5 s and there is no request waterfall, but for the
  public site the right shape is separate `.jpg` files fetched lazily. Worth doing before the
  bank grows much past 330 lines.

## Reading data — ✅ LIVE 2026-08-27

Supabase `qbcvyvuggjxpblfqidhr` (ca-central-1, `the owner account`; recorded in
`reference_supabase-registry.md`). Verified end to end with `tools/verify_collection.sh`:
GET refused 405 · malformed body refused 400 · valid attempt **stored** · keep-alive 200.
Cron `/api/keepalive` registered at `0 7 * * *`.

⭐ **`stored:1` is itself the proof that the junk fields were dropped.** The probe deliberately
carried `typed` and `text`; the table has no such columns, so had the allowlist leaked them
PostgREST would have rejected the whole insert and the endpoint would have answered
502 *store rejected the write*. A 200 can only mean they never reached the database.

### How it was wired (for the next project)

1. **Create a Supabase project** (free tier). Record it in `reference_supabase-registry.md`
   with the email that owns it, as with every other project.
2. **Run `sql/001_attempts.sql`** in the SQL editor. It creates `attempts`, the `confusions`
   view (the confusion matrix), and `stage_accuracy`.
3. **Set two env vars** on the Vercel project and redeploy:
   ```sh
   cd site
   npx vercel env add SUPABASE_URL production          # https://<ref>.supabase.co
   npx vercel env add SUPABASE_SERVICE_KEY production  # the SERVICE ROLE key
   npx vercel deploy --prod --yes
   ```

⚠ **The service key, not the anon key.** The table runs the deny-all posture — RLS on, **no
policies** — so writes only succeed through the serverless function, which bypasses RLS. This
is deliberate: there is then no key in the page at all, and nothing a browser can reach
directly. Never put the service key anywhere the client can see.

⚑ **A daily cron hits `/api/keepalive`.** Free-tier Supabase pauses after about a week idle,
and a low-traffic telemetry endpoint is exactly that shape; when it pauses, writes fail and
the data is simply lost. This is the failure georgia.wrootlabs.com hit in July 2026.

### What is collected, and what is refused

| sent | never sent |
|---|---|
| letter confusions, as `ink>typed` | **the text the reader typed** |
| chars attempted, chars right | any name, email or account |
| track, stage, line id, page | cookies, IP, fingerprint |
| a random per-browser id | anything identifying a person |

**Off unless the reader turns it on**, in the *What you are getting wrong* panel, and the
footer says so. The endpoint validates by **allowlist rather than blocklist** — verified by
test: a body carrying extra `text`/`typed` fields has them dropped rather than stored.

## The raw corpus is not kept locally (2026-08-27)

`corpus/raw/` — 2.2 GB of upstream clones and ÖNB page images — **was deleted.** The repo went
from 2.4 GB to 133 MB.

⚑ **Nothing about the live site depends on it.** Verified by rebuilding with it gone: the
exercise payload came back **byte-identical** (`b46b770305ed`). `build_exercises.py` reads
`corpus/crops/*/manifest.jsonl`, and the crops (64 MB) are kept.

**What still needs it, and how to get it back:**

| task | needs `corpus/raw` |
|---|---|
| rebuild the bank / redeploy the site | no |
| re-crop at different parameters, or add lines | **yes** |
| plate reads (`tools/plate.py`) | **yes** |
| PAGE XML export with true image dimensions | yes (falls back to polygon extents without) |

```sh
./tools/fetch-seeds.sh              # the four upstream GT repos, ~2.1 GB
python3 tools/fetch_iiif.py corpus/normalized/wien940.jsonl \
  "https://api.onb.ac.at/iiif/presentation/v3/manifest/10047947" \
  corpus/raw/wien940-images --tei corpus/raw/wien940/ONB_940.xml --offset -2 \
  --out-jsonl corpus/normalized/wien940-iiif.jsonl      # ÖNB images, ~92 MB
```

⚠ **iCloud was tried first and is the wrong tool here.** Moving files into iCloud Drive does
**not** free disk: they stay local until uploaded and then evicted, and after the move there
were *zero* dataless placeholders and ~1 GB of the payload was git packfiles that would never
be read. It reclaimed nothing while queueing 2.2 GB against the iCloud quota.
