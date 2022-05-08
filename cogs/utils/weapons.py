boosts = {"💫": 5, "✨": 15, "⭐": 30, "🌟": 50}
enhancement_symbols = ["💫", "✨", "⭐", "🌟"]
base_damage = {
    "Fists": (40, 80, 5),
    "Alpha Blade": (100, 160, 20),
    "OP Weapon": (550, 800, 40),
    "🔮 OP Weapon": (5500, 8000, 50),
}

class WeaponInstance:

    def __init__(self, weapon_name: str):
        self.name = weapon_name
        self.enhancement = self.get_enhancement()
        self.boost = self.get_boost()
        self.clean_name = ""
        self.min_dmg = 0
        self.max_dmg = 0
        self.crit_chance = 0
        self.get_stats()

    # get enhancement
    def get_enhancement(self) -> str:

        if self.name[0] in enhancement_symbols:
            return self.name[0]
        return None

    # get boost
    def get_boost(self) -> int:
        if self.enhancement:
            return boosts[self.enhancement]
        return None

    def get_stats(self) -> None:

        if self.enhancement:

            try:
                self.clean_name = self.name.strip(self.name[0])[1:] # strip enhancement symbol
                self.base_min_dmg = base_damage[self.clean_name][0]
                self.base_max_dmg = base_damage[self.clean_name][1]
                self.base_crit_chance = base_damage[self.clean_name][2]
            except KeyError:
                self.base_min_dmg = 40
                self.base_max_dmg = 80
                self.base_crit_chance = 5

            # if boost is there
            # add boost to base damage
            if self.boost:
                self.min_dmg = int(self.base_min_dmg + (self.boost/100 * self.base_min_dmg))
                self.max_dmg = int(self.base_max_dmg + (self.boost/100) * self.base_max_dmg)
                self.crit_chance = int(self.base_crit_chance + (self.boost/100) * self.base_crit_chance)


        else:
            self.min_dmg = base_damage[self.name][0]
            self.max_dmg = base_damage[self.name][1]
            self.crit_chance = base_damage[self.name][2]

    # upgrade weapon and get stats
    def upgrade(self):

        # if weapon is already at max level
        if self.enhancement == "🌟":
            raise Exception("Weapon is already at max level.")

        if self.name[0] == "🔮":
            raise Exception("Unusuals cannot be upgraded.")

        # weapon does not have enhancement
        if self.name[0] not in enhancement_symbols:
            self.enhancement = "💫"
            self.name = f"{self.enhancement} {self.name}"
            self.boost = boosts[self.enhancement]
            self.get_stats()
            return self

        # weapon has tiers 1-3
        else:
            self.new_enhancement = enhancement_symbols[enhancement_symbols.index(self.enhancement) + 1]
            self.name = self.name.replace(self.enhancement, self.new_enhancement)
            self.enhancement = self.new_enhancement
            self.boost = boosts[self.enhancement]
            self.get_stats()
            return self

    def __str__(self) -> str:
        if self.boost:
            return f"Min: {self.min_dmg} (+{self.boost}%)\nMax: {self.max_dmg} (+{self.boost}%)\nCrit: {self.crit_chance}% (+{self.boost}%)"
        return f"Min: {self.min_dmg}\nMax: {self.max_dmg}\nCrit: {self.crit_chance}%"