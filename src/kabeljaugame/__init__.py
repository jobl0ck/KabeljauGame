import random

class GenePool:
    __pool: list[int]

    def __init__(self, gene_a_count: int, gene_b_count: int):
        """
        Note:   gene_a is the one without prime and gene b is with prime
                gene_a is treated as 1 and gene b as zero
        """

        self.__pool = [1] * gene_a_count + [0] * gene_b_count
    
    def __pull_item(self):
        chosen = random.choice(self.__pool)
        self.__pool.remove(chosen)
        return chosen

    def pull_gene(self):
        if len(self.__pool) == 0:
            raise ValueError("Pool is empty")
        return (self.__pull_item(), self.__pull_item())

class TripleGenePool:
    pool_a: GenePool
    pool_b: GenePool
    pool_c: GenePool

    generateable_amount: int

    def __init__(self, cnt_a, cnt_ap, cnt_b, cnt_bp, cnt_c, cnt_cp):
        assert cnt_a + cnt_ap == cnt_b + cnt_bp and cnt_a + cnt_ap == cnt_c + cnt_cp, "pools have to be of the same size"
        assert (cnt_a + cnt_ap) % 2 == 0, "sum of n and np has to be even"
        
        self.pool_a = GenePool(cnt_a, cnt_ap)
        self.pool_b = GenePool(cnt_b, cnt_bp)
        self.pool_c = GenePool(cnt_c, cnt_cp)

        self.generateable_amount = (cnt_a + cnt_ap) // 2
    
    def generate_fish(self):
        return Fish(
            self.pool_a.pull_gene(),
            self.pool_b.pull_gene(),
            self.pool_c.pull_gene()
        )
    
    def generate_all_fish(self):
        return list(self.generate_fish() for _ in range(self.generateable_amount))

class Fish:
    gene_a: tuple[int, int]
    gene_b: tuple[int, int]
    gene_c: tuple[int, int]

    const_a: int = 10
    const_b: int = 6
    const_c: int = 2

    def __init__(self, a, b, c):
        self.gene_a = a
        self.gene_b = b
        self.gene_c = c
    
    def get_length(self):
        return sum(sum(a) + b for a, b in zip(
            [self.gene_a, self.gene_b, self.gene_c],
            [self.const_a, self.const_b, self.const_c]))
    
    def __str__(self):
        return f"Fish with length {self.get_length()} {self.gene_a} {self.gene_b} {self.gene_c}"
    

def fish_to_new_pool(fish: list[Fish]):
    gene_a_items = []
    gene_b_items = []
    gene_c_items = []

    for f in fish:
        gene_a_items += f.gene_a
        gene_b_items += f.gene_b
        gene_c_items += f.gene_c
    
    pool = TripleGenePool(
        gene_a_items.count(1) * 2,
        gene_a_items.count(0) * 2,
        gene_b_items.count(1) * 2,
        gene_b_items.count(0) * 2,
        gene_c_items.count(1) * 2,
        gene_c_items.count(0) * 2,
    )

    print("new values: {0}, {1}, {2}, {3}, {4}, {5}".format(gene_a_items.count(1) * 2,
                    gene_a_items.count(0) * 2,
                    gene_b_items.count(1) * 2,
                    gene_b_items.count(0) * 2,
                    gene_c_items.count(1) * 2,
                    gene_c_items.count(0) * 2,)
                )

    return pool

def main() -> None:
    pool = TripleGenePool(12, 12, 12, 12, 12, 12)

    for i in range(4):
        print(f"generation {i}")
        fish = pool.generate_all_fish()

        fish = sorted(fish, key=lambda x: x.get_length())

        for f in fish:
            print(f)
        
        print("avg length:", sum(map(Fish.get_length, fish)) / len(fish))
        
        if i == 3:
            break

        fish = fish[:6]
        
        pool = fish_to_new_pool(fish)
