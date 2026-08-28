// POST /api/attempts — receive anonymous reading data from the trainer.
//
// Deliberately narrow. What arrives is letter-level confusions and per-line accuracy;
// the reader's raw typing is NEVER sent, and there is no account, cookie or IP stored.
// The only identifier is a random id the browser makes for itself, so a sitting can be
// grouped without anyone being named.
//
// Degrades safely: with no Supabase env vars configured this answers 503 and the client
// carries on recording locally. A missing backend must never break the tool.

const MAX_BATCH = 60;

// --- BEGIN GENERATED TRACKS (tools/make_routes.py; do not edit by hand) ---
const TRACKS = new Set(["latin", "latin2", "greek", "fabliaux"]);
// --- END GENERATED TRACKS ---
//
// Generated from registry/ rather than typed, because a hand-kept copy here is the
// third copy of the track list and the worst one to let drift: attempts from a new
// language would be dropped in silence, since discarding unrecognised input is
// precisely this endpoint's job. Written as a literal rather than imported from JSON
// so it carries no dependency on the runtime's JSON-module support -- this function is
// the only path the reading data has, and it degrades to 503, never to a stack trace.

function bad(res, code, msg) {
  res.status(code).json({ ok: false, error: msg });
  return null;
}

// Keep only fields we expect, in the shape we expect. Anything else is dropped rather
// than stored: this endpoint is public, so treat every body as hostile.
function clean(a) {
  if (!a || typeof a !== "object") return null;
  if (!TRACKS.has(a.t)) return null;
  const stage = Number(a.s);
  if (!Number.isInteger(stage) || stage < 0 || stage > 4) return null;
  const n = Number(a.n), hit = Number(a.hit);
  if (!Number.isFinite(n) || !Number.isFinite(hit) || n < 0 || n > 400 || hit < 0 || hit > n)
    return null;
  const miss = Array.isArray(a.miss)
    ? a.miss.filter((m) => typeof m === "string" && m.length <= 12).slice(0, 120)
    : [];
  return {
    session: String(a.sid || "").slice(0, 40),
    track: a.t,
    stage,
    item_id: String(a.id || "").slice(0, 40),
    page: String(a.page || "").slice(0, 80),
    chars: n,
    hits: hit,
    forgiving: !!a.forgiving,
    miss,
    build: String(a.build || "").slice(0, 20),
  };
}

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") return bad(res, 405, "POST only");

  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_KEY;
  if (!url || !key) return bad(res, 503, "collection not configured");

  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch { return bad(res, 400, "bad json"); }
  }
  const list = Array.isArray(body && body.attempts) ? body.attempts : null;
  if (!list) return bad(res, 400, "expected {attempts:[…]}");
  if (list.length > MAX_BATCH) return bad(res, 413, "batch too large");

  const rows = list.map(clean).filter(Boolean);
  if (!rows.length) return res.status(200).json({ ok: true, stored: 0 });

  const r = await fetch(`${url}/rest/v1/attempts`, {
    method: "POST",
    headers: {
      apikey: key,
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
      Prefer: "return=minimal",
    },
    body: JSON.stringify(rows),
  });
  if (!r.ok) {
    const t = await r.text();
    console.error("supabase insert failed", r.status, t.slice(0, 300));
    return bad(res, 502, "store rejected the write");
  }
  return res.status(200).json({ ok: true, stored: rows.length });
}
