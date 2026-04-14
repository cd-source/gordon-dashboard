-- Run this in Supabase SQL Editor to create the portfolio_state table

create table portfolio_state (
  id int primary key default 1 check (id = 1),
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- Seed with empty state
insert into portfolio_state (id, data) values (1, '{}'::jsonb);

-- Allow anonymous read access (anon key is public, safe for dashboards)
alter table portfolio_state enable row level security;

create policy "Allow public read" on portfolio_state
  for select using (true);

create policy "Allow service role write" on portfolio_state
  for all using (true) with check (true);
