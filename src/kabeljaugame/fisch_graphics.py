COLORS = [
    "#3C70AE",
    "#000000",
    "#E5262E",
    "#FFE500",
    "#9B3D8F",
    "#F39217",
]

ORIGS = [
    "#ff0000",
    "#ff0001",
    "#ff0002",
    "#ff0003",
    "#ff0004",
    "#ff0005",
]

def flatten(xss):
    return [x for xs in xss for x in xs]

def make_many_fische(fische):
    return [
        make_fisch(fisch) for fisch in fische
    ]

def make_fisch(fisch, out_name="out.svg"):
    gene = flatten(fisch.gene)

    with open("kabeljau.svg") as f:
        data = f.read()

    for i, c in enumerate(ORIGS):
        new_c = COLORS[(i//2)*2 + 1 - gene[i]]

        #print(new_c, gene[i])

        data = data.replace(c, new_c)
    
    return data
        