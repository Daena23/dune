from field import Field
from game_initialization import initialize_game
from game_loop import update_field, update_loop, update_portal, update_bombs, update_player, \
    update_monsters, update_explosions
# TODO насколько нужно deepcopy empty field/ symbols


def main():
    # initial parameters
    field = Field(size=9, p_walls=0.2)  # size - odd; p_wall - 0.1-0.3
    player, monsters_list, bombs_list, portal, explosions_list, new_bomb = initialize_game(field)
    portal_exists = False
    player_won = False
    player_lost = False
    postmortem_steps = 0
    step = 0

    while not (player_lost or player_won) or postmortem_steps < 4:
        # todo проблема ходит бомбой в бомбу, - радномные бомбы; бомба выше игрока; можно отгородиться от монстра; своевременное удаление бомбы - двойной вхрыв
        update_player(field, player, bombs_list, postmortem_steps)
        explosions_list = update_bombs(field, player, bombs_list)
        update_explosions(player, explosions_list)
        print('bomb list', bombs_list)
        for bomb in bombs_list:
            print('bomb.timer', bomb.timer)
        update_monsters(field, player, monsters_list, step)
        portal_exists = update_portal(field, monsters_list, portal_exists, portal)
        update_field(field, player, monsters_list, bombs_list, explosions_list, portal, portal_exists, player_won)
        player_lost, player_won, postmortem_steps = update_loop(player, monsters_list, portal, player_lost, postmortem_steps)
        field.visualize()
        step += 1
    if player_won:
        print('you win ❤')
    if player_lost:
        print('you loose ❤')


if __name__ == '__main__':
    main()
