import copy

def simplify_fraction(numer, denumer):
    a = numer
    b = denumer
    while b:
        a, b = b, a % b
    numer, denumer = int(numer/a), int(denumer/a)
    return (numer, denumer)


def calculate_spoilage_proportion(c1, c2):
    c1_sum = sum(c1)
    c2_sum = sum(c2)
    p2 = min(c2)
    idx = c2.index(p2)
    p1 = c1[idx]
    # Populate a set of potential 'w's and their corresponding values
    w_lookup = {}
    for p2_idx in range(0, p2 + 1):
        p1_idx_end = min(p1 + 1, int(p2_idx * p1/p2) + 1)
        for p1_idx in range(1, p1_idx_end):
            nom = p1 * p2_idx
            denom = p2 * p1_idx
            if nom / denom > 1:
                this_w = nom/denom # simplify_fraction(p1 * p2_idx, p2 * p1_idx)
                if this_w not in w_lookup:
                    w_lookup[this_w] = {}
                w_lookup[this_w][(nom, denom)] = (p1_idx, p2_idx)

    c1_rem = c1
    c2_rem = c2
    del c1_rem[idx]
    del c2_rem[idx]
    for product_idx in range(len(c1_rem)):
        w_mutual = {}
        p1 = c1_rem[product_idx]
        p2 = c2_rem[product_idx]
        for p2_idx in range(0, p2 + 1):
            p1_idx_end = min(p1 + 1, int(p2_idx * p1/p2) + 1)
            for p1_idx in range(1, p1_idx_end):
                nom = p1 * p2_idx
                denom = p2 * p1_idx
                key = nom / denom
                if key > 1 and key in w_lookup:
                    w_mutual[key] = w_lookup[key]
                    for element in w_mutual[key]:
                        old_p1_idx = w_mutual[key][element][0]
                        old_p2_idx = w_mutual[key][element][1]
                        w_mutual[key][element] = (p1_idx + old_p1_idx, p2_idx + old_p2_idx)
        w_lookup = w_mutual
    possible_ws = copy.deepcopy(w_lookup)
    for w in w_lookup:
        for element in w_lookup[w]:
            if w != (w_lookup[w][element][0] / c1_sum) / (w_lookup[w][element][1] / c2_sum):
                if len(possible_ws[w]) == 1:
                    del possible_ws[w]
                else:
                    del possible_ws[w][element]

            else:
                this_w = simplify_fraction(element[0], element[1])
                print("{}/{}".format(this_w[0], this_w[1]))
        
    print(len(possible_ws))
    print(possible_ws)
    

def calculate_spoilage_proportion2(c1, c2):
    w_lookup = {}
    w_paths = {}
    w_common = None
    for idx in range(len(c1)):
        w_lookup[idx] = set()
        w_paths[idx] = {}
        p1 = c1[idx]
        p2 = c2[idx]
        for p2_idx in range(0, p2+1):
            # check min p1_idx:
            # (p2_idx / p2) / (p1_idx / p1) > 1
            p1_idx_end = min(p1+1, int(p2_idx * p1/p2) + 1)
            for p1_idx in range(1, p1_idx_end):
                # fraction: (p2_idx / p2) / (p1_idx / p1) = (p1 * p2_idx) / (p2 * p1_idx)
                nom = p1 * p2_idx
                denom = p2 * p1_idx
                if nom / denom > 1:
                    this_w = simplify_fraction(p1 * p2_idx, p2 * p1_idx)
                    w_lookup[idx].add(this_w)
                    w_paths[idx][this_w] = (p1_idx, p2_idx)
        # Initialise w_common
        if w_common == None:
            w_common = w_lookup[idx]
        # No solution
        elif len(w_common) == 0:
                return
        # Only keep mutual w elements in set
        else:
            w_common = w_common & w_lookup[idx]
    # Check overall inverted w
    for w in w_common:
        p1_idx_sum = 0
        p2_idx_sum = 0
        for idx in range(len(c1)):
            p1_idx_sum += w_paths[idx][w][0]
            p2_idx_sum += w_paths[idx][w][1]
        # fraction: (p1_idx_sum / p1_sum) / (p2_idx_sum / p2_sum) = (p2_sum * p1_idx_sum) / (p1_sum * p2_idx_sum)
        this_w = simplify_fraction(sum(c2) * p1_idx_sum, sum(c1) * p2_idx_sum)
        if w == this_w:
            print("{}/{}".format(w[0], w[1]))


c1 = [5248, 1312, 2624, 5760, 3936]
c2 = [640, 1888, 3776, 3776, 5664]
# c1 = [10, 8, 6]
# c2 = [2, 9, 9]
# calculate_spoilage_proportion(c1, c2)

import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()
calculate_spoilage_proportion(c1, c2)
pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
