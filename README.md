# 🛡 FirewallAI — Rule Optimization System
### DAA + AI/ML + Cloud-Ready Flask Backend

---

## 📦 Project Structure

```
firewall-ai/
├── backend/
│   ├── app.py          ← Flask entry point + all API routes
│   ├── optimizer.py    ← DAA: Merge Sort + Greedy (O(n log n) + O(n))
│   ├── search.py       ← DAA: Binary Search O(log n)
│   └── ai_model.py     ← ML: Decision Tree Classifier
├── frontend/
│   └── templates/
│       ├── index.html     ← Landing page
│       └── dashboard.html ← Full interactive dashboard
├── data/
│   └── rules_dataset.csv  ← Sample training data
└── requirements.txt
```

---

## 🚀 Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Flask server
cd backend
python app.py

# 3. Open browser
http://localhost:5000
```

---

## 🔗 API Endpoints

| Method | Route          | Description                        |
|--------|----------------|------------------------------------|
| POST   | /api/optimize  | Sort + Greedy optimize + AI flag   |
| POST   | /api/search    | Binary search for a packet         |
| POST   | /api/train     | Train AI model on rules            |
| POST   | /api/upload    | Upload CSV of rules                |

---

## 📊 Algorithm Complexity

| Step              | Algorithm      | Complexity   |
|-------------------|----------------|--------------|
| Sorting           | Merge Sort     | O(n log n)   |
| Redundancy Removal| Greedy         | O(n)         |
| Packet Matching   | Binary Search  | O(log n)     |
| AI Prediction     | Decision Tree  | O(1)/rule    |

---

## 🎓 Viva Points

- **DAA**: Merge Sort for ordering, Greedy for rule removal, Binary Search for fast lookups
- **AI**: Decision Tree detects shadowed/conflicting rules automatically
- **Cloud**: REST API architecture → deploy on AWS/Firebase/Heroku unchanged
- **Improvement**: Linear O(n) packet scan → O(log n) via Binary Search

---

## 📥 CSV Format

```
start_ip,end_ip,port,action
10,100,80,ALLOW
20,40,80,DENY
50,60,443,ALLOW
```
