import random

from dataclasses import dataclass

def flatten(xss):
    return [x for xs in xss for x in xs]

@dataclass
class Allelen:
    a: int
    ap: int
    b: int
    bp: int
    c: int
    cp: int

    def get_pools(self):
        return [
            [True] * x + [False] * xp for x, xp in [(self.a, self.ap), (self.b, self.bp), (self.c, self.cp)]
        ]

@dataclass
class Fisch:
    gene: list[int]

    def get_length(self):
        return sum([
            sum(self.gene[0]) + 10,
            sum(self.gene[1]) + 6,
            sum(self.gene[2]) + 2
        ])

class FischPool:
    def __init__(self, kill_slice=slice(0, 6), allelen=Allelen(12, 12, 12, 12, 12, 12)):
        self.allelen = allelen
        self.kill_slice = kill_slice
    
    def make_fisch_and_evolve(self):
        fische = []

        pools = self.allelen.get_pools()

        def pull_pool(pool):
            e = random.choice(pool)
            pool.remove(e)
            return int(e)

        for i in range(12):
            gene = tuple((pull_pool(p), pull_pool(p)) for p in pools)
            fische.append(Fisch(gene))
        
        fische = sorted(fische, key=lambda x: x.get_length())

        print("GENE")

        for f in fische:
            print(f.get_length(), f.gene)
        
        print("avg length:", sum(map(Fisch.get_length, fische)) / len(fische))

        print(self.allelen)
        
        survivors = fische[self.kill_slice]

        assert len(survivors) == 6, "slice didnt result in 6 remaining fisch"

        gene_items = [[] for _ in range(3)]

        for s in survivors:
            for i in range(3):
                gene_items[i] += s.gene[i]

        self.allelen = Allelen(
            gene_items[0].count(1) * 2,
            gene_items[0].count(0) * 2,
            gene_items[1].count(1) * 2,
            gene_items[1].count(0) * 2,
            gene_items[2].count(1) * 2,
            gene_items[2].count(0) * 2,
        )

        return fische, Allelen(
            gene_items[0].count(1),
            gene_items[0].count(0),
            gene_items[1].count(1),
            gene_items[1].count(0),
            gene_items[2].count(1),
            gene_items[2].count(0),
        )

    
if __name__ == "__main__":
    p = FischPool()
    p.make_fisch_and_evolve()
    p.make_fisch_and_evolve()
    p.make_fisch_and_evolve()
    p.make_fisch_and_evolve()
    p.make_fisch_and_evolve()
