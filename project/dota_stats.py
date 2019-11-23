'''
DO NOT USE THIS FILE.
DEPRECATED.
To get more data use:
    scrape_database.py
'''
import json
import requests
import argparse
import time

'''
Descriptions of results:
    http://sharonkuo.me/dota2/matchdetails.html

API calls/things you should know:
    https://dev.dota2.com/showthread.php?t=58317

'''

def get_player_profile(key, steam_id):
    # steam_id = steamID64
    data_request = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?steamids={}&key={}'.format(steam_id, key))
    print(data_request.text)

def get_heroes(key, id):
    data_request = requests.get('http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1/?key={}'.format(key))
    hero_dict = data_request.json()
    for hero in hero_dict['result']['heroes']:
        if hero['id'] == id:
            print(hero['name'])


def read_file(filename):
    with open(filename, 'r') as file:
        d = json.load(file)
    print(len(d))

def set_up(n, key, match_id, invalid_ids):
    '''
    Use this function to fill the file.
    The file must already contain 1 dictionary.
    This function:
        * runs get_match n times.
        * appends ']' to close the list
    '''
    count = 1
    for i in range(n):
        result = get_match(key, match_id, count)
        count += 1
        time.sleep(1)
        match_id += 1
        if result == 1:
            invalid_ids += 1


    with open('match_data3.json', 'a') as file:
        file.write(']')

    with open('match_data3.json', 'r') as file:
        d = json.load(file)


    print('{} matches loaded'.format(len(d)))
    print('{} invalid match IDs'.format(invalid_ids))

def get_match(key, match_id, count):
    '''
    This function appends a comma followed
    by a match dictionary to the json file
    '''

    data_request = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?match_id={}&key={}'.format(match_id, key))
    '''
    data_request is a requests.model.Response object. See link for its methods:
    https://github.com/psf/requests/blob/master/requests/models.py#L587
    '''
    print('Response {}: {}'.format(count, data_request))
    # match_data = json.loads(data_request.text)

    match_data = data_request.json()

    '''
    Check if match ID returns a match
    '''
    if 'error' in match_data['result'].keys():
        print('{}: match_id does not exist'.format(match_id))
        return 1
    else:
        with open('match_data3.json', 'a') as file:
            file.write(', ')
            json.dump(match_data, file, indent=4, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='API key', required=True)
    args = parser.parse_args()
    match_id = 5000009000
    invalid_ids = 0
    loops = 5000
    hero_id = 1
    steam_id = '76561198044089924'
    filename = 'all_data_the_remix.json'

    # get_match_data(args.key)

    # set_up(loops, args.key, match_id, invalid_ids)

    read_file(filename)

    #get_heroes(args.key, hero_id)

    # get_player_profile(args.key, steam_id)
