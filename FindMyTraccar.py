#!/usr/bin/python3

import os, functools, time, json, datetime, urllib.request, urllib.parse, urllib.error;

itemsFilePath = '/Users/jakub/Library/Caches/com.apple.findmy.fmipcore/Items.data'
traccarApiUrl = 'http://xxxx:5055/'


print = functools.partial(print, flush=True)

while True:
    try:
        print(datetime.datetime.now(), 'Opening FindMy App...')
        os.system('open --hide --background /System/Applications/FindMy.app')
    except:
        print(datetime.datetime.now(), 'ERROR Can\'t open FindMy.app!')

    time.sleep(30)

    try:
        print(datetime.datetime.now(), 'Opening FindMy App items file...')
        f = open(itemsFilePath, 'r')
        j = json.load(f)
        f.close()
    except:
        print(datetime.datetime.now(), 'ERROR Can\'t read items file!')
    else:
        for item in j:
            payload = {
                'id': 'findmy_' + item['name'].lower(),
                'lat': item['location']['latitude'],
                'lon': item['location']['longitude'],
                'accuracy': item['location']['horizontalAccuracy'],
                'batteryLevel': round(item['batteryStatus'] * 100),
                'lastFindMyUpdate': str(datetime.datetime.fromtimestamp(round(item['location']['timeStamp'] / 1000), tz=datetime.timezone.utc))
            }

            req = urllib.request.Request(traccarApiUrl + '?' + urllib.parse.urlencode(payload))

            try:
                res = urllib.request.urlopen(req, timeout=5)
            except Exception as e:
                print(datetime.datetime.now(), 'ERROR', e)
            else:
                print(datetime.datetime.now(), 'OK', payload)
