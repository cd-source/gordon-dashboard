# Gordon Dashboard

Real-time paper trading portfolio dashboard. Hosted on Vercel, data stored in Supabase.

## Setup

### 1. Supabase
1. Create a project at [supabase.com](https://supabase.com)
2. Go to SQL Editor and run `migration.sql`
3. Copy your **Project URL** and **anon key** from Settings → API

### 2. Configure
- In `index.html`, replace `__SUPABASE_URL__` and `__SUPABASE_ANON_KEY__` with your values
- Add `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` to `../credentials.env`

### 3. Vercel
1. Push this repo to GitHub
2. Import in Vercel — it auto-deploys as static HTML
3. Dashboard is live at your Vercel URL

### 4. Gordon writes
Gordon runs `supabase_sync.py` after each screening/trade cycle to push data to Supabase.
