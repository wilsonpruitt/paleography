-- Paleography — remove the verifier's probe rows.
-- Run in the Supabase SQL editor. Safe to run more than once.
--
-- tools/verify_collection.sh writes one row per run, with session 'verify-<pid>' and
-- build 'verify'. Those are synthetic and must not sit in the confusion matrix alongside
-- real reading. Nothing else matches this filter: a browser's session id is a random
-- 16-character string and its build is the bank's build date, never the word 'verify'.

-- 1. Look before deleting.
select id, created_at, session, track, stage, item_id, page, chars, hits, miss, build
from public.attempts
where session like 'verify-%' or build = 'verify'
order by created_at;

-- 2. Delete them, returning what went so the result pane shows exactly what was removed
--    rather than a bare row count.
delete from public.attempts
where session like 'verify-%' or build = 'verify'
returning id, session, build, created_at;

-- 3. What is left, which should be real reading only.
select count(*)                                  as rows_remaining,
       count(distinct session)                   as sessions,
       min(created_at)                           as first_seen,
       max(created_at)                           as last_seen
from public.attempts;

-- 4. The confusion matrix, now clean. Empty until someone ticks the contribute box.
select track, ink, typed, n
from public.confusions
order by n desc
limit 20;
