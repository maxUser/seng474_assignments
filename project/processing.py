import json

def read_file(filename):
    d = None
    with open(filename, 'r') as file:
        d = json.load(file)
    return d

def radiant_wins(data):
    win_count = 0
    loss_count = 0
    error_count = 0
    for match in data:
        try:
            if match['result']['radiant_win']:
                win_count += 1
            else:
                loss_count += 1
        except(KeyError) as e:
            error_count += 1
            pass


    print('Wins: {}'.format(win_count))
    print('Losses: {}'.format(loss_count))
    print('Errors: {}'.format(error_count))
    print('Total: {}'.format(win_count + loss_count + error_count))


def filter_by_gamemode(data, mode):
    return [match for match in data if match['result']['game_mode'] == mode]


def game_mode_stats(data):
    mode_stats = {
        0: {'name': 'Unknown', 'count': 0},
        1: {'name': 'All pick', 'count': 0},
        2: {'name': 'Captains mode', 'count': 0},
        3: {'name': 'Random draft', 'count': 0},
        4: {'name': 'Single draft', 'count': 0},
        5: {'name': 'All random', 'count': 0},
        6: {'name': 'Intro', 'count': 0},
        7: {'name': 'The Diretide', 'count': 0},
        8: {'name': 'Reverse captains mode', 'count': 0},
        9: {'name': 'Greeviling', 'count': 0},
        10: {'name': 'Tutorial', 'count': 0},
        11: {'name': 'Mid only', 'count': 0},
        12: {'name': 'Least played', 'count': 0},
        13: {'name': 'New player pool', 'count': 0},
        14: {'name': 'Compendium matchmaking', 'count': 0},
        15: {'name': 'Custom', 'count': 0},
        16: {'name': 'Captains draft', 'count': 0},
        17: {'name': 'Balanced draft', 'count': 0},
        18: {'name': 'Ability draft', 'count': 0},
        19: {'name': 'Event', 'count': 0},
        20: {'name': 'All random death match', 'count': 0},
        21: {'name': '1 vs. 1 solo mid', 'count': 0},
        22: {'name': 'Ranked all pick', 'count': 0},
        23: {'name': 'Ranked Roles', 'count': 0}
    }

    for match in data:
        # curr = mode_stats[match['result']['game_mode']]
        mode_stats[match['result']['game_mode']]['count'] += 1

    total = 0
    for stats in mode_stats.values():
        print('{}: {}'.format(stats['name'], stats['count']))
        total += stats['count']
    print('total {}'.format(total))


def highest_player_stat(data, stat):
    highest = 0
    mode = None

    for match in data:
        for player in match['result']['players']:
            if player[stat] > highest:
                highest = player[stat]
                mode = match['result']['game_mode']

    print('Most {} in a game: {}'.format(stat, highest))
    print('Game mode: {}'.format(mode))


def filter_by_hero(data, hero_id):
    return [match for match in data
            for player in match['result']['players'] if player['hero_id'] == hero_id]


def extract_duration_data(data):
    dur_data = {}

if __name__ == '__main__':
    data = read_file('all_data.json')
    # print(type(data[0]['result']['game_mode']))

    # radiant_wins(data)
    # captains_mode_data = filter_by_gamemode(data, 1)
    # radiant_wins(captains_mode_data)

    # game_mode_stats(data)

    # highest_player_stat(data, 'last_hits')

    some_hero = filter_by_hero(data, 0)
    print(len(some_hero))
