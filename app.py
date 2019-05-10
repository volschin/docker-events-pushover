# Copyright 2018 Socialmetrix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import docker
from pushover import init, Client
import os
import sys
import time
import signal

event_filters = ["create","update","destroy","die","kill","pause","unpause","start","stop"]
ignore_names = []
ignore_label = "docker-events.ignore"

BUILD_VERSION=os.getenv('BUILD_VERSION')
APP_NAME = 'Docker Events Pushover (v{})'.format(BUILD_VERSION)

def get_config(env_key, optional=False):
    value = os.getenv(env_key)
    if not value and not optional:
        print('Environment variable {} is missing. Can\'t continue'.format(env_key))
        sys.exit(1)
    return value


def watch_and_notify_events(client):
    global event_filters

    event_filters = {"event": event_filters}

    for event in client.events(filters=event_filters, decode=True):
#        print(event)
        container_id = event['Actor']['ID'][:12]
        attributes = event['Actor']['Attributes']
        when = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(event['time']))
        event['status'] = event['status']+'d'

        x = 'no'

        try:
            x = event['Actor']['Attributes']['docker-events.ignore']
        except KeyError:
            pass

        if x != 'no':
#            print('docker-events.ignore specified')
            continue
		
#       print('docker-events.ignore NOT specified')
			
        if attributes['name'] in ignore_names:
            continue

        message = "The container {} ({}) {} at {}" \
                .format(attributes['name'],
                        attributes['image'],
                        event['status'],
                        when)
        send_message(message)


def send_message(message):
    client = Client(po_key, api_token=po_token)
    client.send_message(message,title="Docker Event")
##    global pb_key
##    pb = Pushbullet(pb_key)
##    pb.push_note("Docker Event", message)
    pass


def exit_handler(_signo, _stack_frame):
    send_message('{} received SIGTERM on {}. Goodbye!'.format(APP_NAME, host))
    sys.exit(0)


def host_server(client):
    return client.info()['Name']


if __name__ == '__main__':
##    pb_key = get_config("PB_API_KEY")
    po_token = get_config("PUSHOVER_TOKEN")
    po_key = get_config("PUSHOVER_KEY")

    events_string = get_config("EVENTS", True)
    if events_string:
        event_filters = events_string.split(',')

    ignore_strings = get_config("IGNORE_NAMES", True)
    if ignore_strings:
        ignore_names = ignore_strings.split(',')

    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)

    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    host = host_server(client)

#    message = '{} reporting for duty on {}'.format(APP_NAME, host)
#    send_message(message)

    watch_and_notify_events(client)

    pass
