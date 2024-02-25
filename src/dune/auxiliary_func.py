def get_symbol(some_object, game):
    return game[type(some_object).__name__]
