# optimizer.py – DAA Module
# Algorithms: Merge Sort O(n log n) + Greedy O(n)

# ── Merge Sort ───────────────────────────────────────────────────────────────
def merge_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr

    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid],  key=key)
    right = merge_sort(arr[mid:],  key=key)
    return _merge(left, right, key)


def _merge(left, right, key):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ── Greedy: Remove exact duplicates ─────────────────────────────────────────
def remove_redundant(rules):
    seen    = set()
    cleaned = []
    for r in rules:
        key = (r['start_ip'], r['end_ip'], r['port'], r['action'])
        if key not in seen:
            seen.add(key)
            cleaned.append(r)
    return cleaned


# ── Greedy: Remove shadowed rules ────────────────────────────────────────────
# A rule B is shadowed by rule A if A's IP range fully covers B's range
# and both share the same port, but have opposite actions.
def remove_shadowed(rules):
    result = []
    for i, candidate in enumerate(rules):
        shadowed = False
        for j, dominant in enumerate(rules):
            if i == j:
                continue
            if (dominant['start_ip'] <= candidate['start_ip'] and
                    dominant['end_ip'] >= candidate['end_ip'] and
                    dominant['port']     == candidate['port'] and
                    dominant['action']   != candidate['action'] and
                    j < i):
                shadowed = True
                break
        if not shadowed:
            result.append(candidate)
    return result
