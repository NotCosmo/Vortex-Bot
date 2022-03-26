BASE_DAMAGES = {
    "Dawn": (200, 400),
    "Le sword": (9999, 9999),
}

REFORGE_SYMBOLS = ['✦', '✪']

class WeaponInstance:

    def __init__(self, display_name: str):

        self.get_stats(display_name)

    # damage calculations
    def get_stats(self, display_name: str) -> None:

        if display_name[0] in REFORGE_SYMBOLS:
            try:
                self.min_dmg = BASE_DAMAGES[self.strip_reforge(display_name)][0]
                self.max_dmg = BASE_DAMAGES[self.strip_reforge(display_name)][1]
            except KeyError:
                self.min_dmg = 100
                self.max_dmg = 200

        else:
            try:
                self.min_dmg = BASE_DAMAGES[display_name][0]
                self.max_dmg = BASE_DAMAGES[display_name][1]
            except KeyError:
                self.min_dmg = 100
                self.max_dmg = 200

        try:
            reforge = self.get_reforge(display_name)
            self.min_dmg = reforge.min_dmg
            self.max_dmg = reforge.max_dmg
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

        # Celestial (More Damage)
        if char == '✦':

            # complex calculations for advanced weapons go here
            self.min_dmg *= 2
            self.max_dmg *= 2
            self.name = f"✦ Celestial {self.strip_reforge(display_name)}"
            return self

        if char == '✪':
            # complex calculations for advanced weapons go here
            self.min_dmg *= 5
            self.max_dmg *= 5
            self.name = f"✪ Godly {self.strip_reforge(display_name)}"
            return self