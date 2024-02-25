from typing import List

from any_object import AnyObject, LivingObject, NonLivingObject


class Game:
    def __init__(self, player):
        # living objects
        self.player = player
        self.monsters = []
        # non_living objects
        self.inter_walls = []
        self.bound_walls = []
        self.breakable_walls = []
        self.non_breakable_walls = []
        self.portal = None
        self.bombs = []
        self.explosions = []
        # coord lists
        self.penetrable_cell_coord: List[List[int]] = []
        self.create_new_monsters = False

    def get_living_objects(self) -> List[LivingObject]:
        return [self.player] + self.monsters

    def get_non_living_objects(self) -> List[NonLivingObject]:
        sum_lst = self.non_breakable_walls + self.breakable_walls + self.bombs + self.explosions
        return sum_lst + [self.portal] if self.portal else sum_lst

    def get_objects(self) -> List[AnyObject]:
        lst = []
        lst.extend(self.get_living_objects())
        lst.extend(self.get_non_living_objects())
        return lst
