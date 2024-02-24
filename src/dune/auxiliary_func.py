def get_symbol(some_object, game):
    return game[type(some_object).__name__]


def return_object_from_field(cell, Class):
    return [object for object in cell if isinstance(object, Class)]


def add_to_field(field, obj):
    # if isinstance(obj, List):
    for element in obj:
        if element:
            field.field[element.row][element.column].append(element)
