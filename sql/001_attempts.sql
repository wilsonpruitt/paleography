-- Paleography — anonymous reading data.
-- Run once in the Supabase SQL editor.
--
-- What is here: letter-level confusions and per-line accuracy. What is NOT here, and must
-- never be added: the text a reader typed, any name, email, account, IP or cookie. The only
-- identifier is a random string the browser invents for itself, so one sitting can be
-- grouped without anyone being named.

create table if not exists public.attempts (
  id          bigint generated always as identity primary key,
  created_at  timestamptz not null default now(),
  session     text,                          -- random, browser-generated; not a person
  track       text not null check (track in ('latin','latin2','greek')),
  stage       smallint not null check (stage between 0 and 4),
  item_id     text,
  page        text,
  chars       int  not null check (chars >= 0),
  hits        int  not null check (hits >= 0 and hits <= chars),
  forgiving   boolean not null default true,
  miss        text[] not null default '{}',  -- 'truth>typed' pairs
  build       text
);

create index if not exists attempts_created_idx on public.attempts (created_at desc);
create index if not exists attempts_track_stage_idx on public.attempts (track, stage);

-- Deny-all posture: RLS on, and NO policies at all. Writes arrive only through the
-- serverless function using the service key, which bypasses RLS. Nothing reaches this table
-- from a browser directly, so there is no anon key in the page to leak.
alter table public.attempts enable row level security;

-- The confusion matrix -- which letter gets read as which. This is the table that makes the
-- learner side and the model side the same project.
create or replace view public.confusions as
select track,
       split_part(m, '>', 1) as ink,
       split_part(m, '>', 2) as typed,
       count(*)              as n
from public.attempts, unnest(miss) as m
group by 1, 2, 3
order by n desc;

-- Where readers are actually struggling, by stage.
create or replace view public.stage_accuracy as
select track, stage,
       count(*)                                    as attempts,
       sum(chars)                                  as chars,
       round(100.0 * sum(hits) / nullif(sum(chars),0), 1) as pct
from public.attempts
group by 1, 2
order by 1, 2;
