import json


def read_file(filename):
    '''Read in json data file'''
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)

    return data


def radiant_wins(data):
    '''Given dataset, determine radiant win statistics'''
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
    '''Given dataset, filter on game mode'''
    return [match for match in data if match['result']['game_mode'] == mode]


def game_mode_stats(data):
    '''Game mode distribution'''
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
    '''Calculate the maximum player stat'''
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
    '''Filter out matches where selected hero did not appear'''
    return [match for match in data
            for player in match['result']['players']
            if player['hero_id'] == hero_id]


def extract_duration_data(data):
    '''Extract data based on game duration.

       Match duration is stored in secondsso we define the categories as the
       following:
        early      --> 0-19 mins  (0-1199 sec)
        mid        --> 20-39 mins (1200-2399 sec)
        late       --> 40-59 mins (2400-3599 sec)
        ultra-late --> 60+ mins   (3600+ sec)
    '''
    early = []
    mid = []
    late = []
    ultra_late = []

    for match in data:
        if match['result']['duration'] <= 1199:
            early.append(match)
        elif match['result']['duration'] <= 2399:
            mid.append(match)
        elif match['result']['duration'] <= 3599:
            late.append(match)
        else:
            ultra_late.append(match)

    # check the output
    print('Early matches: {}'.format(len(early)))
    print('Mid matches: {}'.format(len(mid)))
    print('Late matches: {}'.format(len(late)))
    print('Ultra Late matches: {}'.format(len(ultra_late)))

    return early, mid, late, ultra_late


def did_hero_win_match(match, hero_id):
    '''Take a hero and a match and determine victory

       Here, player_slot tells us which team the player is on.  0-4 is Radiant,
       128-132 is Dire.
    '''
    player_slot = None
    for player in match['result']['players']:
        if player['hero_id'] == hero_id:
            player_slot = player['player_slot']

    if player_slot == None:
        print('hero {} not in match {}'.format(hero_id, match['result']['match_id']))

    try:
        if player_slot <= 4:
            return match['result']['radiant_win']
        else:
            return not match['result']['radiant_win']
    except:
        print('Match_id: {}, does not have \'radiant_win\''.format(match['result']['match_id']))
        pass


def get_win_percent(total_matches, wins):
    '''Calculate win percentage'''
    return (float(wins) / float(total_matches)) * 100


def filter_bad_data(data):
    '''Filter out data with no win condition'''
    return [match for match in data if 'radiant_win' in match['result'].keys()]


if __name__ == '__main__':
    # Collect data
    raw_data = read_file('all_data_the_remix.json')

    # Filter out bad data
    data = filter_bad_data(raw_data)

    # Check game mode distribution
    # game_mode_stats(data)

    # Calculate hero win percentage based on match duration
    selected_hero = 42
    hero_data = filter_by_hero(data, selected_hero)
    print('Total matches for hero: {}'.format(len(hero_data)))

    early, mid, late, ultra_late = extract_duration_data(hero_data)

    early_wins = [match for match in early if did_hero_win_match(match, selected_hero)]
    mid_wins = [match for match in mid if did_hero_win_match(match, selected_hero)]
    late_wins = [match for match in late if did_hero_win_match(match, selected_hero)]
    ultra_late_wins = [match for match in ultra_late if did_hero_win_match(match, selected_hero)]

    print('Early win percent: {}%'.format(get_win_percent(len(early), len(early_wins))))
    print('Mid win percent: {}%'.format(get_win_percent(len(mid), len(mid_wins))))
    print('Late win percent: {}%'.format(get_win_percent(len(late), len(late_wins))))
    print('Ultra Late win percent: {}%'.format(get_win_percent(len(ultra_late), len(ultra_late_wins))))
