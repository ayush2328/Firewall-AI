"""
shuffle_dataset.py
==================
Run this anytime BEFORE training to:
  1. Reshuffle all rows randomly
  2. Add noise (randomly flip ~3% of labels)
  3. Inject 50 brand-new random rules
  4. Save back to data/rules_dataset.csv

Usage:
    python shuffle_dataset.py

Run it as many times as you want — every run gives a different dataset
so your AI model learns general patterns, not memorized sequences.
"""

import csv, random, os, shutil
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
INPUT_FILE  = os.path.join(os.path.dirname(__file__), 'data', 'rules_dataset.csv')
NOISE_RATE  = 0.03   # 3% of labels randomly flipped
NEW_RULES   = 50     # fresh rules injected each run

PORTS = [80, 443, 22, 8080, 3306, 25, 110, 53, 21, 8443,
         3389, 5432, 6379, 27017, 9200, 8888, 4444, 2222,
         1433, 5900, 161, 123, 179, 389]

# ── Load ──────────────────────────────────────────────────────────────────────
with open(INPUT_FILE, newline='') as f:
    reader = csv.DictReader(f)
    rows   = list(reader)

print(f"Loaded  : {len(rows)} rows")

# ── Backup original ───────────────────────────────────────────────────────────
ts     = datetime.now().strftime('%Y%m%d_%H%M%S')
backup = INPUT_FILE.replace('.csv', f'_backup_{ts}.csv')
shutil.copy(INPUT_FILE, backup)
print(f"Backup  : {os.path.basename(backup)}")

# ── Inject 50 new random rules ────────────────────────────────────────────────
new_rows = []
for _ in range(NEW_RULES):
    port   = random.choice(PORTS)
    s      = random.randint(1, 65000)
    span   = random.randint(10, 400)
    e      = s + span
    action = random.choice(['ALLOW', 'DENY'])

    # randomly make it redundant by shadowing
    is_red = 0
    if random.random() < 0.4:
        is_red = 1

    new_rows.append({
        'start_ip':     str(s),
        'end_ip':       str(e),
        'port':         str(port),
        'action':       action,
        'is_redundant': str(is_red)
    })

rows.extend(new_rows)
print(f"Injected: +{NEW_RULES} new rules  (total: {len(rows)})")

# ── Add noise: flip 3% of labels randomly ────────────────────────────────────
flipped = 0
for row in rows:
    if random.random() < NOISE_RATE:
        row['is_redundant'] = '1' if row['is_redundant'] == '0' else '0'
        flipped += 1
print(f"Noise   : {flipped} labels flipped ({round(flipped/len(rows)*100,1)}%)")

# ── Triple shuffle ────────────────────────────────────────────────────────────
random.shuffle(rows)
random.shuffle(rows)
random.shuffle(rows)
print(f"Shuffled: 3x random shuffle done")

# ── Save ──────────────────────────────────────────────────────────────────────
with open(INPUT_FILE, 'w', newline='') as f:
    fieldnames = ['start_ip', 'end_ip', 'port', 'action', 'is_redundant']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# ── Stats ─────────────────────────────────────────────────────────────────────
allow = sum(1 for r in rows if r['action'] == 'ALLOW')
deny  = sum(1 for r in rows if r['action'] == 'DENY')
redun = sum(1 for r in rows if r['is_redundant'] == '1')
clean = len(rows) - redun

print(f"\n── Final Dataset ──────────────────────────────")
print(f"Total rows : {len(rows)}")
print(f"ALLOW      : {allow}  |  DENY : {deny}")
print(f"Redundant  : {redun}  |  Clean: {clean}")
print(f"Balance    : {round(redun/len(rows)*100,1)}% redundant")
print(f"\nDone! Run 'python app.py' and upload the new CSV.")
