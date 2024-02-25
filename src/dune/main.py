from game_initialization import create_new_monsters, initialize_game
from game_loop import update_bombs, update_explosions, update_field, update_loop, \
    update_object_state, update_portal, visualize


def main():
    # initial parameters
    field, game = initialize_game()
    player_won, player_lost = False, False
    step, postmortem_steps = 0, 0
    while not (player_lost or player_won) or postmortem_steps < 4:
        create_new_monsters(game)
        update_bombs(field, game)
        for liv_obj in game.get_living_objects():
            liv_obj.make_move(field, game, step, player_won, player_lost)
        player_won = update_portal(game, player_won, player_lost)
        update_explosions(field, game)
        update_field(field, game)  # put objects
        player_won, player_lost, postmortem_steps = update_loop(game, player_won, player_lost, postmortem_steps)
        visualize(field, game)
        update_object_state(field, game)  # remove destroyed objects
        step += 1
    if player_won:
        print('you win ❤')
    if player_lost:
        print('you loose ❤')


if __name__ == '__main__':
    main()
