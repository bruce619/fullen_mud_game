
class GamePlayVisuals:

    def __int__(self):
        pass

    def game_play(self):

        """ method to print out the game play """
        with open('../resources/gameplay.txt', 'r') as f:
            game = f.read()
        return game


class MonsterVisual:
    """
    This class retrieves any form of text visuals
    REF: https://www.asciiart.eu/
    """

    def __int__(self):
        pass

    def alrog_demon(self):
        """ method to print out the alrog demon """
        with open('../resources/monsters/alrog_demon.txt', 'r') as f:
            d = f.read()
        return d

    def bazog_demon(self):
        """ method to print out the bazog demon """
        with open('../resources/monsters/bazog_demon.txt', 'r') as f:
            d = f.read()
        return d

    def fire_dragon(self):
        """ method to print out the fire dragon """
        with open('../resources/monsters/fire_dragon.txt', 'r') as f:
            d = f.read()
        return d

    def gorr(self):
        """ method to print out the gorr"""
        with open('../resources/monsters/gorr.txt', 'r') as f:
            d = f.read()
        return d

    def harpy_demon(self):
        """ method to print out the harpy demon"""
        with open('../resources/monsters/harpy_demon.txt', 'r') as f:
            d = f.read()
        return d

    def snakes(self):
        """ method to print out the snakes """
        with open('../resources/monsters/snakes.txt', 'r') as f:
            d = f.read()
        return d

    def sorcerers(self):
        """ method to print out the sorcerers"""
        with open('../resources/monsters/sorcerers.txt', 'r') as f:
            d = f.read()
        return d

    def torturers(self):
        """ method to print out the torturers"""
        with open('../resources/monsters/torturers.txt', 'r') as f:
            d = f.read()
        return d


class LocationVisuals:

    """
    This class contains visuals for all locations
    REF: https://www.asciiart.eu/
    """

    def __int__(self):
        pass

    def paraiso(self):
        """ method to print out the cross location"""
        with open('../resources/locations/golden_gates.txt', 'r') as f:
            d = f.read()
        return d

    def cross_location(self):
        """ method to print out the cross location"""
        with open('../resources/locations/cross_roads.txt', 'r') as f:
            d = f.read()
        return d

    def damned_valley(self):
        """ method to print out the damned valley"""
        with open('../resources/locations/damned_valley.txt', 'r') as f:
            d = f.read()
        return d

    def dark_dungeon(self):
        """ method to print out the dark dungeon"""
        with open('../resources/locations/dark_dugeon.txt', 'r') as f:
            d = f.read()
        return d

    def demon_cave(self):
        """ method to print out the demon cave"""
        with open('../resources/locations/demon_cave.txt', 'r') as f:
            d = f.read()
        return d

    def golden_gates(self):
        """ method to print out the golden gate"""
        with open('../resources/locations/golden_gates.txt', 'r') as f:
            d = f.read()
        return d

    def gorr_fortress(self):
        """ method to print out the gorr fortress"""
        with open('../resources/locations/gorr_fortress.txt', 'r') as f:
            d = f.read()
        return d

    def inferno_shop(self):
        """ method to print out the inferno shop"""
        with open('../resources/locations/inferno_shop.txt', 'r') as f:
            d = f.read()
        return d

    def snake_island(self):
        """ method to print out the snake island"""
        with open('../resources/locations/inferno_shop.txt', 'r') as f:
            d = f.read()
        return d

    def terra_city_market(self):
        """ method to print out the terra city market"""
        with open('../resources/locations/terra_city_market.txt', 'r') as f:
            d = f.read()
        return d

    def terra_nova(self):
        """ method to print out the terra nova"""
        with open('../resources/locations/terra_nova.txt', 'r') as f:
            d = f.read()
        return d

    def torture_liar(self):
        """ method to print out the torturer liar"""
        with open('../resources/locations/torture_liar.txt', 'r') as f:
            d = f.read()
        return d


class OrbVisuals:

    """
    This class contain the visuals of orbs
    REF: https://www.asciiart.eu/
    """

    def __int__(self):
        pass

    def conecementor(self):
        """ method to print out the conecementor orb"""
        with open('../resources/orbs/conecemento.txt', 'r') as f:
            d = f.read()
        return d

    def poder(self):
        """ method to print out the poder orb"""
        with open('../resources/orbs/poder.txt', 'r') as f:
            d = f.read()
        return d

    def vida(self):
        """ method to print out the vida orb"""
        with open('../resources/orbs/vida.txt', 'r') as f:
            d = f.read()
        return d


class WeaponVisuals:

    """
        This visual contains weapons
    """

    def __int__(self):
        pass

    def axe(self):
        """ method to print out the  orb"""
        with open('../resources/weapons/axe.txt', 'r') as f:
            d = f.read()
        return d

    def armour(self):
        """ method to print out the  armour"""
        with open('../resources/weapons/armour.txt', 'r') as f:
            d = f.read()
        return d

    def blade(self):
        """ method to print out the blade"""
        with open('../resources/weapons/blade.txt', 'r') as f:
            d = f.read()
        return d

    def magic_whip(self):
        """ method to print out the magic whip"""
        with open('../resources/weapons/magic_whip.txt', 'r') as f:
            d = f.read()
        return d

    def sonic_beam(self):
        """ method to print out the sonic beam"""
        with open('../resources/weapons/sonc_beam.txt', 'r') as f:
            d = f.read()
        return d

    def spear(self):
        """ method to print out the spear"""
        with open('../resources/weapons/spear.txt', 'r') as f:
            d = f.read()
        return d

    def list_of_weapon_visuials(self):
        arr = [self.axe(), self.spear(), self.armour(), self.sonic_beam(), self.blade(), self.magic_whip()]
        return arr


class InventoryVisuals:

    def __int__(self):
        pass

    def barbarian_boots(self):
        """ method to print out the barbarian boots"""
        with open('../resources/inventories/barbarian_boots.txt', 'r') as f:
            d = f.read()
        return d

    def braies(self):
        """ method to print out the braies"""
        with open('../resources/inventories/braies.txt', 'r') as f:
            d = f.read()
        return d

    def breastplates(self):
        """ method to print out the breastplates"""
        with open('../resources/inventories/breastplate.txt', 'r') as f:
            d = f.read()
        return d

    def cotte(self):
        """ method to print out the cotte"""
        with open('../resources/inventories/cotte.txt', 'r') as f:
            d = f.read()
        return d

    def drawers(self):
        """ method to print out the drawers"""
        with open('../resources/inventories/drawers.txt', 'r') as f:
            d = f.read()
        return d

    def helmet(self):
        """ method to print out the helmet"""
        with open('../resources/inventories/helmet.txt', 'r') as f:
            d = f.read()
        return d

    def leather(self):
        """ method to print out the helmet"""
        with open('../resources/inventories/leather.txt', 'r') as f:
            d = f.read()
        return d

    def map(self):
        """ method to print out the map"""
        with open('../resources/inventories/map.txt', 'r') as f:
            d = f.read()
        return d

    def spell_cast(self):
        """ method to print out the spell cast"""
        with open('../resources/inventories/spell_cast.txt', 'r') as f:
            d = f.read()
        return d

    def surcoat(self):
        """ method to print out the map"""
        with open('../resources/inventories/surcoat.txt', 'r') as f:
            d = f.read()
        return d

    def potions(self):
        """ method to print out potions"""
        with open('../resources/inventories/potion.txt', 'r') as f:
            d = f.read()
        return d

    def list_of_inventories(self):
        arr = [self.helmet(), self.potions(), self.barbarian_boots(), self.breastplates(), self.surcoat(),
               self.leather(), self.map(), self.braies(), self.drawers(), self.cotte(), self.spell_cast()]
        return arr