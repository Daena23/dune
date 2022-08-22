from typing import Callable

import numpy as np


def update_position(
        game_map: np.ndarray,
        coordinates: np.ndarray,
        direction: np.ndarray,
        speed: float,
        direction_strategy: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray],
) -> None:

    current_block = coordinates.astype(np.int32)
    next_movement_block = game_map[current_block + direction]


