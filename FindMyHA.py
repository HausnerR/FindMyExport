#!/usr/bin/python3
import os, sys, time, json, datetime, urllib.request, urllib.error;

itemsFilePath = '/Users/jakub/Library/Caches/com.apple.findmy.fmipcore/Items.data'

homeAssistantApiUrl = 'https://xxxx/api/'
homeAssistantApiToken = 'xxxx'


def make_ha_request(api_node, payload):
    req = urllib.request.Request(homeAssistantApiUrl + api_node, data=json.dumps(payload).encode('utf-8'))
    req.add_header('Authorization', 'Bearer ' + homeAssistantApiToken)
    req.add_header('Content-Type', 'application/json')

    try:
        res = urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(datetime.datetime.now(), 'ERROR', e)
    else:
        print(datetime.datetime.now(), 'OK', payload)


while True:
    try:
        os.system('open --hide --background /System/Applications/FindMy.app')
    except:
        print(datetime.datetime.now(), 'ERROR Can\'t open FindMy.app!')

    time.sleep(30)

    try:
        f = open(itemsFilePath, 'r')
        j = json.load(f)
        f.close()
    except:
        print(datetime.datetime.now(), 'ERROR Can\'t read items file!')
    else:
        make_ha_request('states/sensor.findmyha_last_update', {
            'state': str(datetime.datetime.now().replace(microsecond=0)),
            'attributes': { 'friendly_name': 'FindMyHA last update', 'device_class': 'date' }
        })

        for item in j:
            make_ha_request('services/device_tracker/see', {
                'dev_id': item['name'].lower(),
                'gps': [ item['location']['latitude'], item['location']['longitude'] ],
                'gps_accuracy': item['location']['horizontalAccuracy'],
                'battery': round(item['batteryStatus'] * 100)
            })

            make_ha_request('states/sensor.' + item['name'].lower() + '_last_seen', {
                'state': str(datetime.datetime.fromtimestamp(round(item['location']['timeStamp'] / 1000))),
                'attributes': {
                    'friendly_name': item['name'] + ' last seen',
                    'device_class': 'date'
                }
            })

    sys.stdout.flush()
    sys.stderr.flush()
