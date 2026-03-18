from flask import Flask, request, jsonify, render_template
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from optimizer import merge_sort, remove_redundant, remove_shadowed
from search import binary_search_packet
from ai_model import FirewallAIModel

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

ai_model = FirewallAIModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ── API: Optimize rules ──────────────────────────────────────────────────────
@app.route('/api/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    rules = data.get('rules', [])

    if not rules:
        return jsonify({'error': 'No rules provided'}), 400

    original_count = len(rules)

    # Step 1 – Sort (Merge Sort O(n log n))
    sorted_rules = merge_sort(rules, key=lambda r: (r['start_ip'], r['end_ip'], r['port']))

    # Step 2 – Greedy removal of duplicates + shadowed rules O(n)
    deduped = remove_redundant(sorted_rules)
    optimized = remove_shadowed(deduped)

    # Step 3 – AI prediction of suspicious/conflicting rules
    ai_flags = ai_model.predict_batch(optimized)

    result_rules = []
    for i, rule in enumerate(optimized):
        result_rules.append({**rule, 'ai_flag': ai_flags[i]})

    stats = {
        'original_count':  original_count,
        'optimized_count': len(result_rules),
        'reduction_pct':   round((1 - len(result_rules) / max(original_count, 1)) * 100, 1),
        'flagged_count':   sum(ai_flags),
    }

    return jsonify({'rules': result_rules, 'stats': stats})


# ── API: Search packet ───────────────────────────────────────────────────────
@app.route('/api/search', methods=['POST'])
def search():
    data   = request.get_json()
    rules  = data.get('rules', [])
    packet = data.get('packet', {})

    ip   = packet.get('ip', 0)
    port = packet.get('port', 0)

    matched = binary_search_packet(rules, ip, port)
    return jsonify({'matched': matched})


# ── API: Train AI model ──────────────────────────────────────────────────────
@app.route('/api/train', methods=['POST'])
def train():
    data = request.get_json()
    rules = data.get('rules', [])
    accuracy = ai_model.train(rules)
    return jsonify({'accuracy': round(accuracy * 100, 1), 'status': 'trained'})


# ── API: Upload CSV ──────────────────────────────────────────────────────────
@app.route('/api/upload', methods=['POST'])
def upload():
    import csv, io
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file'}), 400

    stream  = io.StringIO(file.stream.read().decode('utf-8'))
    reader  = csv.DictReader(stream)
    rules   = []
    for row in reader:
        try:
            rules.append({
                'start_ip': int(row['start_ip']),
                'end_ip':   int(row['end_ip']),
                'port':     int(row['port']),
                'action':   row['action'].strip().upper()
            })
        except Exception:
            pass
    return jsonify({'rules': rules, 'count': len(rules)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
