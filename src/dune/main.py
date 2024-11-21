from game_initialization import initialize_game
from game_loop import (
    create_monsters_from_portal,
    update_bombs,
    update_explosions,
    update_field,
    update_loop,
    remove_objects,
    check_if_player_won,
    visualize,
)


def main():
    # Initial parameters
    field, game = initialize_game()
    player_won, player_lost = False, False
    step, steps_after_game_ends = 0, 0
    while not (player_lost or player_won) or steps_after_game_ends < 4:
        if game.portal.is_under_explosion:
            create_monsters_from_portal(game)
        update_bombs(field, game)
        for liv_obj in game.living_objects:
            liv_obj.make_move(field, game, step, player_won, player_lost)
        if not player_won:
            player_won = check_if_player_won(game, player_won)
        update_explosions(field, game)
        update_field(field, game)
        player_won, player_lost, steps_after_game_ends = update_loop(game, player_won, player_lost, steps_after_game_ends)
        visualize(field, game)
        remove_objects(field, game)
        step += 1
    if player_won:
        print('you won ❤')
    elif player_lost:
        print('you loose ❤')


if __name__ == '__main__':
    main()
