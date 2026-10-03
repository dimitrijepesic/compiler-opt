import csv, sys
def validate(input_csv, dump_csv):
    """Independent check: uses ONLY the original input (half-open [lower, upper)) and the dumped offsets."""
    src = {}
    with open(input_csv) as f:
        for row in csv.DictReader(f):
            src[int(row["id"])] = (int(row["lower"]), int(row["upper"]), int(row["size"]))
    off, reported = {}, None
    with open(dump_csv) as f:
        for line in f:
            if line.startswith("#makespan"): reported = int(line.strip().split(",")[1]); continue
            if line.startswith("id,"): continue
            i, b, d, s, o = map(int, line.strip().split(","))
            off[i] = o
    problems = []
    if set(off) != set(src): problems.append(f"id sets differ: {len(set(src) - set(off))} missing, {len(set(off) - set(src))} extra")
    items = sorted((src[i][0], src[i][1], off[i], off[i] + src[i][2], i) for i in src if i in off)
    n = len(items)
    for a in range(n):
        la, ua, oa, ea, ia = items[a]
        for b in range(a + 1, n):
            lb, ub, ob, eb, ib = items[b]
            if lb >= ua: break
            if ub > la and oa < eb and ob < ea and ea > oa and eb > ob:
                problems.append(f"overlap {ia} {ib}")
                if len(problems) > 5: break
        if len(problems) > 5: break
    makespan = max(e for _, _, _, e, _ in items) if items else 0
    return {"buffers": n, "makespan": makespan, "reported": reported, "valid": not problems, "problems": problems[:5]}
if __name__ == "__main__":
    print(validate(sys.argv[1], sys.argv[2]))
