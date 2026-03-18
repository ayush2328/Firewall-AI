# ai_model.py – AI/ML Module (Decision Tree)
import random

try:
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class FirewallAIModel:
    def __init__(self):
        self.model   = None
        self.trained = False

    # ── Training ─────────────────────────────────────────────────────────────
    def train(self, rules):
        """
        Train on a list of rule dicts.
        Label = 1 (redundant/suspicious) if DENY rule is completely inside an
        ALLOW range with the same port (heuristic labelling for demo).
        """
        if not rules or not SKLEARN_AVAILABLE:
            self.trained = False
            return 0.0

        X, y = [], []
        for i, r in enumerate(rules):
            feat  = [r['start_ip'], r['end_ip'], r['port'],
                     1 if r['action'] == 'DENY' else 0]
            label = 0
            # heuristic: flag if another rule shadows this one
            for j, other in enumerate(rules):
                if i != j and (other['start_ip'] <= r['start_ip'] and
                               other['end_ip']   >= r['end_ip'] and
                               other['port']      == r['port'] and
                               other['action']    != r['action']):
                    label = 1
                    break
            X.append(feat)
            y.append(label)

        if len(set(y)) < 2:
            # can't split with one class; just fit anyway
            self.model = DecisionTreeClassifier(max_depth=4)
            self.model.fit(X, y)
            self.trained = True
            return 1.0

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        self.model = DecisionTreeClassifier(max_depth=4)
        self.model.fit(X_train, y_train)
        self.trained = True

        preds = self.model.predict(X_test)
        return accuracy_score(y_test, preds)

    # ── Prediction ───────────────────────────────────────────────────────────
    def predict_batch(self, rules):
        """
        Returns list of 0/1 flags for each rule.
        Falls back to heuristic if model not trained or sklearn unavailable.
        """
        if self.trained and SKLEARN_AVAILABLE and self.model:
            X = [[r['start_ip'], r['end_ip'], r['port'],
                  1 if r['action'] == 'DENY' else 0]
                 for r in rules]
            return [int(p) for p in self.model.predict(X)]
        else:
            return self._heuristic_flags(rules)

    def _heuristic_flags(self, rules):
        flags = []
        for i, r in enumerate(rules):
            flag = 0
            for j, other in enumerate(rules):
                if i != j and (other['start_ip'] <= r['start_ip'] and
                               other['end_ip']   >= r['end_ip'] and
                               other['port']      == r['port'] and
                               other['action']    != r['action']):
                    flag = 1
                    break
            flags.append(flag)
        return flags
