import json
import requests
import argparse
import time

'''
Descriptions of results:
    http://sharonkuo.me/dota2/matchdetails.html

'''

def read_file():
    with open('match_data.json', 'r') as file:
        d = json.load(file)
    print(len(d))
    with open('match_data2.json', 'r') as file:
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='API key', required=True)
    args = parser.parse_args()
    match_id = 5000009000
    invalid_ids = 0
    loops = 5000

    # get_match_data(args.key)

    set_up(loops, args.key, match_id, invalid_ids)

    # read_file()
'''
Random Error:
Traceback (most recent call last):
  File "dota_stats.py", line 140, in <module>
    set_up(loops, args.key, match_id, invalid_ids)
  File "dota_stats.py", line 27, in set_up
    result = get_match(key, match_id, count)
  File "dota_stats.py", line 59, in get_match
    match_data = data_request.json()
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/requests/models.py", line 897, in json
    return complexjson.loads(self.text, **kwargs)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/json/__init__.py", line 348, in loads
    return _default_decoder.decode(s)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

'''
