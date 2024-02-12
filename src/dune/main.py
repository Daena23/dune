from field import Field
from game_initialization import initialize_game
from game_loop import update_bombs, update_explosions, update_field, update_loop, update_monsters, update_player, \
    update_portal, update_walls


def main():
    # initial parameters
    field = Field(size=9, p_walls=0.2)  # size - odd; p_wall - 0.1-0.3
    player, monster_list, bomb_list, explosion_list = initialize_game(field)
    player_won, player_lost = False, False
    step, postmortem_steps = 0, 0
    portal = None
    while not (player_lost or player_won) or postmortem_steps < 4:
        update_player(field, player, bomb_list)
        explosion_list = update_bombs(field, player, bomb_list)
        update_walls(field, bomb_list)
        update_monsters(field, player, monster_list, step)
        destroyed_objects = update_explosions(field, player, monster_list, bomb_list, explosion_list)
        portal = update_portal(field, player, portal, monster_list)
        if portal:
            print(portal.row, portal.column)
        update_field(field, player, monster_list, bomb_list, explosion_list, portal, player_won, destroyed_objects)
        player_lost, player_won, postmortem_steps = update_loop(player, player_lost, player_won, postmortem_steps)
        field.visualize()
        step += 1
    if player_won:
        print('you win ❤')
    if player_lost:
        print('you loose ❤')


if __name__ == '__main__':
    main()
