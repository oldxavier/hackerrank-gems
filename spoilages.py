def simplify_fraction(numer, denumer):
    a = numer
    b = denumer
    while b:
        a, b = b, a % b
    numer, denumer = int(numer/a), int(denumer/a)
    return (numer, denumer)


def luxury_humpers(c1, c2):
    c1_sum = sum(c1)
    c2_sum = sum(c2)
    p1 = c1[0]
    p2 = c2[0]
    # Populate a set of potential 'w's and their corresponding values
    w_lookup = {}
    for i2 in range(1, p2 + 1):
        for i1 in range(1, p1 + 1):
            nom = p1 * i2
            denom = p2 * i1
            if nom / denom > 1:
                this_w = nom/denom
                if this_w not in w_lookup:
                    w_lookup[this_w] = {}
                w_lookup[this_w][(nom, denom)] = [(i1, i2)]
    # Loop through the other products and only keep the 'w's that are mutual
    c1_rem = c1
    c2_rem = c2
    del c1_rem[0]
    del c2_rem[0]
    for product_idx in range(len(c1_rem)):
        w_mutual = {}
        p1 = c1_rem[product_idx]
        p2 = c2_rem[product_idx]
        for i2 in range(1, p2 + 1):
            for i1 in range(1, p1 + 1):
                nom = p1 * i2
                denom = p2 * i1
                key = nom / denom
                if key > 1 and key in w_lookup:
                    if key not in w_mutual:
                        w_mutual[key] = {}
                    for element in w_lookup[key]:
                        for pair in w_lookup[key][element]:
                            i1_old = pair[0]
                            i2_old = pair[1]
                            if element not in w_mutual[key]:
                                w_mutual[key][element] = [(i1 + i1_old, i2 + i2_old)]
                            else:
                                w_mutual[key][element].append((i1 + i1_old, i2 + i2_old))
        w_lookup = w_mutual
    # Find w by overall spoilage
    for w in w_lookup:
        for element in w_lookup[w]:
            for pair in w_lookup[w][element]:
                overall_nom = pair[0] * c2_sum
                overall_denom = pair[1] * c1_sum
                if w == overall_nom / overall_denom:
                    this_w = simplify_fraction(overall_nom, overall_denom)
                    if this_w[1] == 1:
                        print("{}".format(this_w[0]))
                    else:
                        print("{}/{}".format(this_w[0], this_w[1]))
                    return

n = int(input())
c1 = [int(x) for x in input().split()]
c2 = [int(x) for x in input().split()]

luxury_humpers(c1, c2)
