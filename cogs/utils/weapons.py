import random
import math

new_boosts = {"<:uncommon:992507268715262002>": 5, "<:epic:992507250595877005>": 15, "<:legendary:992505206308884611>": 30}
rarities = ["<:common:992507237413167145>", "<:uncommon:992507268715262002>", "<:epic:992507250595877005>", "<:legendary:992505206308884611>",  "<:mythic:992527133744304250>"]
base_damage = {
    "Fists": (50, 100, 5),
    "<:mythic:992527133744304250> Fists": (999999*1.25, 999999*1.25, 100),
    "<:uncommon:992507268715262002> Eclipse": (int(65*1.25), int(90*1.25), 10),
    "<:uncommon:992507268715262002> Crescent Scythe": (int(75*1.25), int(110*1.25), 15),
    "<:epic:992507250595877005> Terra Scepter": (int(90*1.25), int(125*1.25), 20),
    "<:special:992527447327252532> Armageddon": (99999, 99999, 100),
}

class WeaponInstance:

    def __init__(self, name: str):

        self.name = name
        self.rarity = self.name.split(" ")[0]
        self.min_dmg = 0
        self.min_dmg = 0
        self.max_dmg = 0
        self.crit_chance = 0
        self.base_min_dmg = 0
        self.base_max_dmg = 0
        self.base_crit_chance = 0
        self.get_stats()

    def get_tier(self) -> int:

        try:
            return rarities.index(self.rarity) + 1
        except ValueError:
            return 10

    def get_stats(self) -> None:

        self.clean_name = self.name.replace(self.rarity, " ").replace("  ", "")  # strip rarity symbol

        # Cycle through keys and rarities, match rarity and clean name
        for key in base_damage:
            for rarity in rarities:
                # if rarity + clean name match the key, take the base stats of that dict entry
                if f"{rarity} {self.clean_name}" == key:
                    self.base_name = f"{rarity} {self.clean_name}"
                    self.base_rarity = rarity
                    self.base_min_dmg = base_damage[key][0]
                    self.base_max_dmg = base_damage[key][1]
                    self.base_crit_chance = base_damage[key][2]
                    self.base = True
                    break

        try:              
            
            # Check to see if a boost should be given, if yes, it should be 1 or above (n > 0)
            if rarities.index(self.rarity) - rarities.index(self.base_rarity) > 0:
                self.boost = new_boosts[self.rarity]
    
                self.min_dmg = round(int(self.base_min_dmg + (self.boost / 100 * self.base_min_dmg)), 0)
                self.max_dmg = round(int(self.base_max_dmg + (self.boost / 100) * self.base_max_dmg), -1)
                self.crit_chance = round(int(self.base_crit_chance + (self.boost / 100) * self.base_crit_chance), 0)
    
            # else, no boost, base stats will be given
            else:
                self.min_dmg = self.base_min_dmg
                self.max_dmg = self.base_max_dmg
                self.crit_chance = self.base_crit_chance
                self.boost = None
        except:
            # raise
            self.min_dmg = 40
            self.max_dmg = 80
            self.crit_chance = 5
            self.boost = None

    # Get new stats, used for the upgrade function
    def get_new_stats(self):

        self.min_dmg = round(int(self.base_min_dmg + (self.boost / 100 * self.base_min_dmg)), 0)
        self.max_dmg = round(int(self.base_max_dmg + (self.boost / 100) * self.base_max_dmg), 0)
        self.crit_chance = round(int(self.base_crit_chance + (self.boost / 100) * self.base_crit_chance), 0)
        return

    def upgrade(self):

        tier = self.get_tier()

        # Uncommon to Epic
        if tier == 2:
            self.boost = new_boosts["<:epic:992507250595877005>"]
            self.name = self.name.replace(self.rarity, "<:epic:992507250595877005>")
            self.get_new_stats()
            return self

        # Epic to Legendary
        if tier == 3:
            self.boost = new_boosts["<:legendary:992505206308884611>"]
            self.name = self.name.replace(self.rarity, "<:legendary:992505206308884611>")
            self.get_new_stats()
            return self

        if tier >= 4:
            raise Exception("Could not upgrade. Weapon is at max level already!")


    def __repr__(self) -> str:
        return f"Min: {self.min_dmg}\nMax: {self.max_dmg}\nCrit: {self.crit_chance}%"