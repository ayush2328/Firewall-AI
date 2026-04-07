# search.py – Binary Search O(log n)
# Find the first matching firewall rule for a given IP + port

def binary_search_packet(rules, ip: int, port: int):
    """
    Rules must be sorted by start_ip.
    Returns the first matching rule dict, or None.
    """
    lo, hi = 0, len(rules) - 1
    candidate = None

    while lo <= hi:
        mid  = (lo + hi) // 2
        rule = rules[mid]

        if rule['start_ip'] <= ip <= rule['end_ip'] and rule['port'] == port:
            candidate = rule
            hi = mid - 1          # keep searching left for earlier match
        elif rule['start_ip'] > ip:
            hi = mid - 1
        else:
            lo = mid + 1

    return candidate
