import numpy as np
from copy import deepcopy
from collections import OrderedDict

class CookedFood:
    '''
    Cooked food struct
    '''
    def __init__(self, **kwargs):
        self.name        = kwargs.get("name", "Questionable Food")
        self.bonus       = kwargs.get("bonus", 0)
        self.hp          = kwargs.get("hp", 1)
        self.stacks      = kwargs.get("stacks", 0)
        self.buff        = kwargs.get("buff", "")
        self.weight      = kwargs.get("weight", 1)
        self.chance      = kwargs.get("chance", 1.0)
        self.time        = kwargs.get("time", 10.0)
        self.ingredients = kwargs.get("ingredients", [])

class Food:
    '''
    Recipe emulator
    '''
    def __init__(self, ingredients, recipes, **kwargs):
        self.ingredients = ingredients
        self.recipes = OrderedDict(sorted(recipes.items(), key=lambda x:int(x[0])))
        self.type = self.allTypes()
        self.validIngredients = self.allIngredients()

        self.spoonlevel  = kwargs.get("spoon", 0)
        self.playerlevel = kwargs.get("level", 1)
        self.update_levels( self.playerlevel, self.spoonlevel )

    def update_levels(self, player, spoon):
        self.spoonlevel  = spoon
        self.playerlevel = player
        self.level = spoon*3 + player

    def cook(self, inglist, **kwargs):
        # Ingredient list should be max 5 min 1
        verbose = kwargs.get("verbose", False)
        nIng    = len(inglist)
        scale   = {k:0 for k in self.type}
        weight  = 0
        buffs   = []
        for ing in inglist:
            if ing not in self.validIngredients:
                raise NameError(f'{ing} not valid')
            for k in self.type:
                scale[k] += self.ingredients[ing][k] * self.ingredients[ing]['size']
            if self.ingredients[ing]["buff"] != "":
                buffs.append(self.ingredients[ing]["buff"])
                if(len(set(buffs))>1):
                    for k in self.type:
                        scale[k] -= self.ingredients[ing][k] * self.ingredients[ing]['size']
            weight += self.ingredients[ing]['size']
        uniqueBuffs = set(buffs)
        # Find the first valid recipe with the above ingredients
        totalWeight = sum([v for k,v in scale.items()])
        if verbose:
            print(f'{scale} => {totalWeight}')
        recipe = 'Questionable Food'
        tags   = {k:v for k,v in scale.items() if v>0}
        hp     = 1
        for uid,rec in self.recipes.items():
            if len(uniqueBuffs) > 1:
                break
            # Check enough ingredients exist
            if False in [bool(v) for (k,v) in scale.items() if k in rec["Ingredients"]]:
                continue
            validWeight = sum([v for (k,v) in scale.items() if k in rec["Ingredients"]])
            if validWeight >= (totalWeight - validWeight):
                recipe = rec["Name"]
                tags = {k:scale[k] for k in rec["Ingredients"]}
                hp = rec["HP"]
                break

        # With the recipe selected, lets calculate the bonus
        lvlBonus = np.floor( self.level/30 - 1 )
        tagBonus = min([v for k,v in tags.items()])
        bonus    = lvlBonus + tagBonus
        hp       = (bonus+1)*hp
        stacks   = (bonus*2 + 1)
        buff     = buffs[0] if len(buffs)>0 else ""
        cooktime = 4**(0.95+0.05*weight)
        if verbose:
            print(f'{recipe}')
            print(f'>> Bonus: {lvlBonus} + {tagBonus} = {bonus}')
            print(f'>> HP: {hp}')
            print(f'>> Stacks: {stacks}')
            print(f'>> Buff: {buff}')

        retVal = CookedFood(name=recipe, bonus=bonus, hp=hp, stacks=stacks, 
                            buff=buff, ingredients=inglist)
        return retVal



    def allIngredients(self):
        ilist = [k for (k,v) in self.ingredients.items()]
        return ilist

    def allTypes(self):
        return ['fruit', 'vegetable', 'grain', 'dairy', 'egg', 'meat', 'beast',
                'poultry', 'fish', 'monster', 'spice', 'sweetener', 'preservative']
