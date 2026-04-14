"""
Gordon → Supabase sync utility.
Reads local data.json and upserts to Supabase portfolio_state table.
Also callable as a module: sync_to_supabase(data_dict) for direct writes.

Usage:
  python supabase_sync.py                    # sync from local data.json
  python supabase_sync.py --from-stdin       # read JSON from stdin
"""

import json
import os
import sys
import urllib.request
import urllib.error

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', 'credentials.env')
DATA_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'data.json')


def load_credentials():
    creds = {}
    if os.path.exists(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    creds[k.strip()] = v.strip()

    url = creds.get('SUPABASE_URL') or os.environ.get('SUPABASE_URL')
    key = creds.get('SUPABASE_SERVICE_KEY') or os.environ.get('SUPABASE_SERVICE_KEY')

    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY required in credentials.env or env vars")
        sys.exit(1)

    return url, key


def sync_to_supabase(data, url=None, key=None):
    if url is None or key is None:
        url, key = load_credentials()

    payload = json.dumps({'data': data, 'updated_at': data.get('last_updated', 'now()')}).encode()

    req = urllib.request.Request(
        f"{url}/rest/v1/portfolio_state?id=eq.1",
        data=payload,
        method='PATCH',
        headers={
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal',
        }
    )

    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in (200, 204):
                print(f"Synced to Supabase ({len(payload)} bytes)")
                return True
            else:
                print(f"Unexpected status: {resp.status}")
                return False
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Supabase error {e.code}: {body}")
        return False
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}")
        return False


if __name__ == '__main__':
    if '--from-stdin' in sys.argv:
        data = json.load(sys.stdin)
    else:
        with open(DATA_JSON_PATH) as f:
            data = json.load(f)

    sync_to_supabase(data)
