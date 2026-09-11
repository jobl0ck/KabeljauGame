import random

from dataclasses import dataclass

from fpdf import FPDF, Align
from fpdf.svg import SVGObject
from fpdf.drawing import Transform

from kabeljaugame import fisch_graphics


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
    
    def as_array(self):
        return [self.a, self.ap, self.b, self.bp, self.c, self.cp]

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
        
        avg = sum(map(Fisch.get_length, fische)) / len(fische)

        print("avg length:", avg)
        print("percent:", avg/21*100)

        #print(self.allelen)
        
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

        new_allelen = Allelen(
            gene_items[0].count(1),
            gene_items[0].count(0),
            gene_items[1].count(1),
            gene_items[1].count(0),
            gene_items[2].count(1),
            gene_items[2].count(0),
        )

        print(new_allelen)

        return fische, new_allelen, survivors
    
def main():
    # pdf needs page with tables 1a, 1b, 2a, 2b and fische from both runs
    pdf = FPDF()

    for kill_slice, text, table_letter in [
            (slice(0, 6), "großer Individuen", "a"),
            (slice(3, 9), "mittelgroßer Individuen", "b")
        ]:

        p = FischPool(kill_slice)

        all_fische = []
        all_allelen = []

        fische, allele, _ = p.make_fisch_and_evolve()
        all_fische.append(fische)
        all_allelen.append(allele)
        pre_1_raw_svgs = fisch_graphics.make_many_fische(fische)
        fische, allele, _ = p.make_fisch_and_evolve()
        all_fische.append(fische)
        all_allelen.append(allele)
        fische, allele, _ = p.make_fisch_and_evolve()
        all_fische.append(fische)
        all_allelen.append(allele)
        fische, allele, survivors = p.make_fisch_and_evolve()
        all_fische.append(fische)
        all_allelen.append(allele)
        post_4_raw_svgs = fisch_graphics.make_many_fische(survivors)

        # try generating some fische

        pdf.add_page()

        pdf.set_font("Times", size=12)

        pdf.cell(pdf.w, 10, f"Fische vor Fang 1 {text}", align=Align.C, center=True)

        for i, s in enumerate(pre_1_raw_svgs):
            svg = SVGObject(s)

            width, height, paths = svg.transform_to_page_viewport(pdf, align_viewbox=False)

            paths.transform = paths.transform @ Transform.translation(
                -width / 2, -height / 2
            ).scale(0.5, 0.5).translate(pdf.w / 2 - (width * 0.6) + (width * 0.6) * (i % 3), 20 + (height * 0.6 * ((i // 3) + 0.5)))

            pdf.draw_path(paths)
        
        offset = height*0.6*4+20

        pdf.ln(offset)

        pdf.cell(pdf.w, 10, f"Fische nach Fang 4 {text}", align=Align.C, center=True)

        for i, s in enumerate(post_4_raw_svgs):
            svg = SVGObject(s)

            width, height, paths = svg.transform_to_page_viewport(pdf, align_viewbox=False)

            paths.transform = paths.transform @ Transform.translation(
                -width / 2, -height / 2
            ).scale(0.5, 0.5).translate(pdf.w / 2 - (width * 0.6) + (width * 0.6) * (i % 3), offset + 20 + (height * 0.6 * ((i // 3) + 0.5)))

            pdf.draw_path(paths)
        
        # now the tables ..

        pdf.add_page()

        pdf.cell(text=f"Tab. 1{table_letter}")

        pdf.ln()

        with pdf.table() as table:

            # header
            row = table.row()
            row.cell()
            for i in range(4):
                row.cell(f"{i+1}. Fang")

            # the fische
            for ri in range(12):
                row = table.row()
                row.cell(f"Fisch {ri+1}")
                for gen in all_fische:
                    row.cell(f"{gen[ri].get_length()}")
            
            # averages
            row = table.row()
            row.cell("Mittelwert der LE")
            for gen in all_fische:
                avg = sum(map(Fisch.get_length, gen)) / len(gen)
                row.cell(f"{avg:.2f}")
            
            # percentages

            first_gen_avg = sum(map(Fisch.get_length, all_fische[0])) / len(all_fische[0])

            row = table.row()
            row.cell("Prozent LE der Ausgangspopulation", align=Align.L)
            for gen in all_fische:
                avg = sum(map(Fisch.get_length, gen)) / len(gen)
                row.cell(f"{avg/first_gen_avg*100:.2f}%")

        pdf.ln()

        pdf.cell(text=f"Tab. 2{table_letter}")

        pdf.ln()

        with pdf.table() as table:
            row = table.row()
            row.cell()
            row.cell("LE")
            for i in range(4):
                row.cell(f"{i+1}. Fang")
            
            for ri in range(6):
                row = table.row()
                
                if ri % 2 == 0:
                    row.cell(f"Gen {["A", "B", "C"][ri//2]}", rowspan=2)
                
                row.cell(f"{["Blau", "Schwarz", "Rot", "Gelb", "Lila", "Orange"][ri]} = {6-ri}", align=Align.R)

                for gen in all_allelen:
                    row.cell(f"{gen.as_array()[ri]}")

        # now generate graphs
        # for fisch le use min max avg
        # for allelen just raw values plotted or smth.
        #   use split colored graph for each gene maybe

    pdf.output("out.pdf")