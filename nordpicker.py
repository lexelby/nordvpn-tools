#!/usr/bin/env python

import sys
import geopy
import requests
import json
from geopy.distance import vincenty as distance
from operator import itemgetter
from itertools import groupby

MY_LATITUDE = 42.4720476
MY_LONGITUDE = -71.7469334
MY_COUNTRY = "United States"
SERVER_LIST_URL = "https://api.nordvpn.com/server"


def get_servers():
    return requests.get(SERVER_LIST_URL).json()

def filter_by_country(servers, country):
    return [server for server in servers if server['country'] == country]

def filter_by_load(servers, max_load):
    return [server for server in servers if server['load'] <= max_load]

def tag_with_distance(servers, latitude, longitude):
    for server in servers:
        dist = distance((latitude, longitude),
                        (server['location']['lat'], server['location']['long']))
        server['distance'] = int(dist.miles)

def servers_by_distance(servers, latitude, longitude):
    tag_with_distance(servers, latitude, longitude)
    servers.sort(key=itemgetter('distance'))

    by_distance = groupby(servers, key=itemgetter('distance'))
    by_distance = [(distance, list(servers)) for distance, servers in by_distance]
    by_distance.sort()
    return by_distance

def short_name(server):
    name = server['domain']
    return name[:name.index('.')]

def print_by_distance(servers):
    for distance, servers in servers:
        print distance, " ".join(["%s:%d" % (short_name(server), server['load']) for server in servers])

def sort_by_distance_and_load(servers):
    def key(server):
        # break servers into bands of load 10% wide, sort by distance,
        # and finally sort by actual load
        return (server['load'] / 10, server['distance'], server['load'])

    servers.sort(key=key)

def print_server(server):
    print "%-5s: %s%% %d mi" % (short_name(server), server['load'], server['distance'])

def main():
    servers = get_servers()
    servers = filter_by_country(servers, MY_COUNTRY)
    tag_with_distance(servers, MY_LATITUDE, MY_LONGITUDE)
    sort_by_distance_and_load(servers)

    #for server in servers:
    #    print_server(server)

    print short_name(servers[0])

if __name__ == "__main__":
    sys.exit(main())
