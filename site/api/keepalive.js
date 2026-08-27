// GET /api/keepalive — touched daily by a Vercel cron.
//
// Free-tier Supabase pauses after about a week idle, and a low-traffic telemetry endpoint
// is exactly the shape that hits it. When it pauses, writes fail and the data is simply
// lost -- the failure georgia.wrootlabs.com hit in July 2026. One cheap read a day avoids it.
export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_KEY;
  if (!url || !key) return res.status(503).json({ ok: false, error: "not configured" });
  try {
    const r = await fetch(`${url}/rest/v1/attempts?select=id&limit=1`, {
      headers: { apikey: key, Authorization: `Bearer ${key}` },
    });
    return res.status(r.ok ? 200 : 502).json({ ok: r.ok, status: r.status });
  } catch (e) {
    return res.status(502).json({ ok: false, error: String(e).slice(0, 120) });
  }
}
