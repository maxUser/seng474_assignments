import json
import requests
import argparse
import time


'''
"match_id":5119839943,
"match_seq_num":4296002164,
"start_time":1574193575,
"lobby_type":0,
"radiant_team_id":0,
"dire_team_id":0,
"players":[

'''
def get_match(key):
    id = 36992584
    data_request = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?match_id={}&key={}'.format(id, key))
    '''
    data_request is a requests.model.Response object. See link for its methods:
    https://github.com/psf/requests/blob/master/requests/models.py#L587
    '''
    print('Response: {}'.format(data_request))
    # match_data = json.loads(data_request.text)
    match_data = data_request.json()
    print(match_data)


def get_match_data(key):
    match_data = {}
    most_recent_match = 0
    unique_match_ids = set()
    first_loop = True

    while len(unique_match_ids) < 2000:
        data_requests = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?start_at_match_id={}&key={}'.format(most_recent_match, key))
        print('Response: {}'.format(data_requests))
        time.sleep(1)
        if first_loop:
            first_loop = False
            match_data = json.loads(data_requests.text)
            match_ids = [matches['match_id'] for matches in match_data['result']['matches']]
            most_recent_match = match_ids[-1]
            most_recent_match -= 1

        else:
            temp_data = json.loads(data_requests.text)
            match_data['result']['matches'] = match_data['result']['matches'] + temp_data['result']['matches']

        for match in match_data['result']['matches']:
            unique_match_ids.add(match['match_id'])
        print(len(unique_match_ids))

    print('Data len: {}'.format(len(match_data['result']['matches'])))
    print('Set len: {}'.format(len(unique_match_ids)))


    import sys
    sys.exit(0)


    print('most recent match id: {}'.format(most_recent))

    most_recent += 1
    print('updated most recent match id: {}'.format(most_recent))

    data_requests_2 = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?start_at_match_id={}&key={}'.format(most_recent, key))
    print('RESPONSE: {}'.format(data_requests_2))
    match_data_2 = json.loads(data_requests_2.text)
    match_ids_2 = [matches['match_id'] for matches in match_data_2['result']['matches']]

    count = 0
    for id in match_ids:
        if id in match_ids_2:
            print('common ID: {}'.format(id))
            count += 1

    if count > 0:
        print('Some matching ids: {}'.format(count))
    else:
        print('no matching')


    # with open('match_data.json', 'w') as file:
    #     json.dump(match_data, file, indent=4, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='API key', required=True)
    args = parser.parse_args()

    # get_match_data(args.key)
    get_match(args.key)
