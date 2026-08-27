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

- ⬜ **`corrections@paleography.app` does not exist yet.** The footer's *Report this line* link
  writes to it, carrying shelfmark, folio, line id, the transcription shown and which glosses
  fired. **Set up Cloudflare Email Routing to forward it**, or change `CONTACT` at the top of
  the trainer's script — one line. ⚠ A feedback channel that bounces is worse than none, and
  this is the address a scholar will use.
- ⬜ **No `www` CNAME.** The apex works; `www.paleography.app` does not resolve. Add
  `CNAME www → cname.vercel-dns.com`, DNS-only, if wanted.
- ⚠ **The page is 10.9 MB in one request** — every line image is inlined as base64, which is
  what the Artifact needs. It serves in ~1.5 s and there is no request waterfall, but for the
  public site the right shape is separate `.jpg` files fetched lazily. Worth doing before the
  bank grows much past 330 lines.
