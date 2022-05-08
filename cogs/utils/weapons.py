BASE_DAMAGES = {
    "Wooden Sword": (100, 200, 30),
    "Le sword": (9999, 9999, 100),
    "Alpha Blade": (300, 400, 45)
}

REFORGE_SYMBOLS = ['🌟', '🔮', '⚡']
REFORGE_NAMES = ["Ethereal", "Valorous", "Fabled"]

class WeaponInstance:

    def __init__(self, display_name: str):
        self.display = display_name
        self.get_stats(display_name)

    # damage calculations
    def get_stats(self, display_name: str) -> None:

        if display_name[0] in REFORGE_SYMBOLS:
            try:
                self.min_dmg = BASE_DAMAGES[self.strip_reforge(display_name)][0]
                self.max_dmg = BASE_DAMAGES[self.strip_reforge(display_name)][1]
                self.crit_chance = BASE_DAMAGES[self.strip_reforge(display_name)][2]
                self.base_min_dmg = BASE_DAMAGES[self.strip_reforge(display_name)][0]
                self.base_max_dmg = BASE_DAMAGES[self.strip_reforge(display_name)][1]
                self.base_crit_chance = BASE_DAMAGES[self.strip_reforge(display_name)][2]
            except KeyError:
                self.min_dmg = 100
                self.max_dmg = 200
                self.crit_chance = 10
                self.base_min_dmg = 100
                self.base_max_dmg = 200
                self.base_crit_chance = 10

        else:
            try:
                self.min_dmg = BASE_DAMAGES[display_name][0]
                self.max_dmg = BASE_DAMAGES[display_name][1]
                self.crit_chance = BASE_DAMAGES[display_name][2]
                self.base_min_dmg = BASE_DAMAGES[display_name][0]
                self.base_max_dmg = BASE_DAMAGES[display_name][1]
                self.base_crit_chance = BASE_DAMAGES[display_name][2]
            except KeyError:
                self.min_dmg = 100
                self.max_dmg = 200
                self.crit_chance = 10
                self.base_min_dmg = 100
                self.base_max_dmg = 200
                self.base_crit_chance = 10

        try:
            reforge = self.get_reforge(display_name)
            self.min_dmg = reforge.min_dmg
            self.max_dmg = reforge.max_dmg
            self.crit_chance = reforge.crit_chance
            self.name = reforge.name
            return self

        # No reforge found
        except AttributeError:
            self.name = display_name
            return self

    # Strip reforge symbol from name
    def strip_reforge(self, display_name: str) -> None:
        char = display_name[0]
        return display_name.strip(char)[1:]

    # Returns reforge name, and damages
    def get_reforge(self, display_name: str) -> None:

        """
        ✦ - Celestial (More Damage)
        """

        char = display_name[0]
        # ethereal reforge
        if char == '🌟':
            self.min_dmg += int((30/100) * self.min_dmg)
            self.max_dmg += int((30/100) * self.max_dmg)
            self.crit_chance += int((15/100) * self.crit_chance)
            self.name = f"{char} Ethereal {self.strip_reforge(display_name)}"
            return self

        elif char == "🔮":
            self.min_dmg += int((5/100) * self.min_dmg)
            self.max_dmg += int((5/100) * self.max_dmg)
            self.crit_chance += int((5/100) * self.crit_chance)
            self.name = f"{char} Fabled {self.strip_reforge(display_name)}"
            return self

        # VALOROUS REFORGE
        elif char == "⚡":
            self.min_dmg += int((10/100) * self.min_dmg)
            self.max_dmg += int((10/100) * self.max_dmg)
            self.crit_chance += int((30/100) * self.crit_chance)
            self.name = f"{char} Valorous {self.strip_reforge(display_name)}"
            return self

    @property
    def strip_name(self) -> str:
        return self.display.strip('⚡🔮🌟')[1:]