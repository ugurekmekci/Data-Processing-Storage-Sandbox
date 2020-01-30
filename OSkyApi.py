import requests as rq

def row(api_endpoint):
    '''This func takes APIurl adn goes to listen endpoint of OpenSky API .
    flattens the nested information inside of a json documents.
    It is possible to add country filter'''
    resp = rq.get(api_endpoint)
    if resp.status_code != 200:
        # something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    for i in resp:
        data = resp.json()
        #print (data)
        return(data)


data = row('https://opensky-network.org/api/states/all')
time = data['time']

keys = ['icao24',
              'callsign',
              'origin_country',
              'time_position',
              'last_contact',
              'longitude',
              'latitude',
              'baro_altitude',
              'on_ground',
              'velocity',
              'true_track',
              'vertical_rate',
              'sensors',
              'geo_altitude',
              'squawk',
              'spi',
              'position_source',
              'time']

for i in data['states']:
    i.append(time)
    converted=dict(zip(keys, i))
    #foo = i[2:]
    if converted['origin_country'] == 'Turkey':
        print(converted)
    else:
        pass





