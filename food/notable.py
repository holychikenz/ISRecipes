from Food import *
import numpy as np
import json
import argparse

# Set max ingredients
def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--elvl", default=150, type=int)
    parser.add_argument("--threshold", default=0, type=int)
    return parser.parse_args()

def main():
    args = getargs()
    with open("foods.json") as jj:
        ingredients = json.load(jj)
    with open("recipes.json") as jj:
        recipes = json.load(jj)
    chef = Food(ingredients, recipes, level=args.elvl)

    print( f'Max depth: {len(chef.allIngredients())}')
    print( chef.allIngredients() )
    #exclude = ['raw tuna', 'raw trout', 'raw shark' ]
    exclude = []
    deepsearch(chef, exclude=exclude, threshold=args.threshold)

def deepsearch(chef, **kwargs):
    # try 3 deep
    exclude = kwargs.get("exclude", [])
    threshold = kwargs.get("threshold", 0)
    ilist = [x for x in chef.allIngredients() if x not in exclude]
    print(ilist)
    depth = len(ilist)
    print(depth)
    count = 0
    bhp = besthp(20)
    ehp = bestehp(20)
    gather = beststack(20, 'gathering')
    sh = beststack(20, 'superheated')
    fish = beststack(20, 'fishing')
    spider = beststack(20, 'nimble')
    for a in range(depth):
        aname = ilist[a]
        for b in range(a, depth):
            bname = ilist[b]
            for c in range(b, depth):
                cname = ilist[c]
                for d in range(c, depth):
                    dname = ilist[d]
                    for e in range(d, depth):
                        ename = ilist[e]
                        x = chef.cook([aname, bname, cname, dname, ename])
                        if x.modchance < threshold/100:
                            continue
                        count += 1
                        bhp.append(x)
                        ehp.append(x)
                        gather.append(x)
                        sh.append(x)
                        fish.append(x)
                        spider.append(x)
                        #print(f'{x.name} +{x.bonus}')
    print('Raw HP :>')
    print(bhp.csvresults())
    print('DShp :>')
    print(ehp.csvresults())
    print('Nimble :>')
    print(spider.csvresults())
    print('Gathering :>')
    print(gather.csvresults())
    print('Superheated :>')
    print(sh.csvresults())
    print('Fishing :>')
    print(fish.csvresults())
    print(f'{count} iterations')

class besthp:
    def __init__(self, depth):
        self.depth = depth
        self.hplist = np.zeros(depth)
        self.cflist = [None for x in range(depth)]

    def append(self, cf):
        hp = cf.hp
        spots = np.where(hp > self.hplist)[0]
        if len(spots) > 0:
            self.hplist[spots[0]] = hp
            self.cflist[spots[0]] = cf

    def csvresults(self):
        s = ''
        for cf in self.cflist:
            s += f'{cf.hp} {cf.ingredients}\n'
        return s

class bestehp:
    def __init__(self, depth):
        self.depth = depth
        self.hplist = np.zeros(depth)
        self.cflist = [None for x in range(depth)]

    def append(self, cf):
        hp   = cf.hp
        dshp = np.floor(2*cf.stacks) if cf.buff == "demon skin" else 0
        thp  = hp+dshp
        spots = np.where(thp > self.hplist)[0]
        if len(spots) > 0:
            self.hplist[spots[0]] = thp
            self.cflist[spots[0]] = cf

    def csvresults(self):
        s = ''
        for cf in self.cflist:
            s += f'{cf.hp} {cf.stacks} {cf.stacks*2+cf.hp} {cf.ingredients} {cf.buff}\n'
        return s

class beststack:
    def __init__(self, depth, buff):
        self.depth = depth
        self.buff = buff
        self.stacklist = np.zeros(depth)
        self.cflist = [None for x in range(depth)]

    def append(self, cf):
        if cf.buff == self.buff:
            stacks = cf.stacks
            spots = np.where(stacks > self.stacklist)[0]
            if len(spots) > 0:
                self.stacklist[spots[0]] = stacks
                self.cflist[spots[0]] = cf

    def csvresults(self):
        s = ''
        for cf in self.cflist:
            s += f'{cf.hp} {cf.stacks} {cf.stacks*2+cf.hp} {cf.ingredients} {cf.buff}\n'
        return s

if __name__ == '__main__':
    main()
