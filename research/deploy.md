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
python3 tools/build_exercises.py --out build/exercises.json --n 110 --max-w 1700 --quality 80
python3 tools/make_trainer.py      # -> build/scriptorium.html   (Artifact: no doctype)
python3 tools/make_site.py         # -> site/index.html          (web: full document)
cd site && npx vercel deploy --prod --yes
```

⚑ **Two outputs, and the difference is not cosmetic.** The Artifact runtime supplies
`<!doctype>`, `<head>` and `<body>` at publish time, so `trainer_shell.html` deliberately has
none. Served raw by a web host that same file falls into **quirks mode** — a different box
model — and has **no viewport meta**, so it renders at desktop width on a phone. The first
deploy went out that way. `make_site.py` wraps it properly; never point Vercel at the artifact
build.

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

## Reading data — wiring it up (2026-08-27)

Everything is built and deployed; it needs a store, which needs a dashboard login.
`/api/attempts` currently answers **503 `collection not configured`**, and the trainer keeps
working locally regardless — a missing backend must never break the tool.

**Three steps, about two minutes:**

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
