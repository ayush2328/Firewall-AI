"""
shuffle_dataset.py
------------------
Run this script EVERY TIME before training to shuffle the dataset
so the AI model cannot memorize row order patterns.

Usage:
    python shuffle_dataset.py
    python shuffle_dataset.py --input my_rules.csv
    python shuffle_dataset.py --noise 10
"""

import csv, random, argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('--input',  default='rules_dataset_5000.csv', help='Input CSV filename')
parser.add_argument('--noise',  type=int, default=5, help='Max IP noise ±N (default 5)')
parser.add_argument('--output', default=None, help='Output filename (default: overwrites input)')
args = parser.parse_args()

base_dir  = os.path.dirname(os.path.abspath(__file__))
in_path   = os.path.join(base_dir, args.input)
out_path  = os.path.join(base_dir, args.output or args.input)

# Read
with open(in_path, newline='') as f:
    reader = csv.DictReader(f)
    rows   = list(reader)

print(f"Loaded  : {len(rows)} rows from {args.input}")

# Shuffle row order
random.shuffle(rows)

# Add small random noise to IP values so model sees slightly different numbers
noise = args.noise
for r in rows:
    s = int(r['start_ip']) + random.randint(-noise, noise)
    e = int(r['end_ip'])   + random.randint(-noise, noise)
    s = max(1, s)
    e = max(s + 1, e)
    r['start_ip'] = s
    r['end_ip']   = e

# Shuffle again after noise
random.shuffle(rows)

# Write back
with open(out_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['start_ip','end_ip','port','action','is_redundant'])
    writer.writeheader()
    writer.writerows(rows)

print(f"Shuffled: {len(rows)} rows  (noise ±{noise})")
print(f"Saved   : {out_path}")
print(f"\nNow upload this CSV to the dashboard and retrain the AI model.")
