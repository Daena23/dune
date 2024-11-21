from typing import List

from any_object import AnyObject, LivingObject, NonLivingObject


class Game:
    def __init__(self, player):
        # Living objects
        self.player = player
        self.monsters = []
        # Non-living objects
        self.inter_walls = []
        self.bound_walls = []
        self.breakable_walls = []
        self.non_breakable_walls = []
        self.portal = None
        self.bombs = []
        self.explosions = []
        # Coordinates
        self.penetrable_cell_coord: List[List[int]] = []

    @property
    def living_objects(self) -> List[LivingObject]:
        return [self.player] + self.monsters

    @property
    def non_living_objects(self) -> List[NonLivingObject]:
        non_living_objects = self.non_breakable_walls + self.breakable_walls + self.bombs + self.explosions
        if self.portal:
            non_living_objects += [self.portal]
        return non_living_objects

    @property
    def objects(self) -> List[AnyObject]:
        return self.living_objects + self.non_living_objects
