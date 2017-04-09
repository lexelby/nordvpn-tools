#!/usr/bin/env python

import os
import sys
import tempfile
import requests
from zipfile import ZipFile
from glob import glob

CONFIG_URL = 'https://api.nordvpn.com/files/zipv2'


def read_until(stream, sentinel):
    data = ""

    for line in stream:
        if line.strip() == sentinel:
            break
        else:
            data += line

    return data

def short_name(name):
    name = os.path.basename(name)
    return name[:name.index('.')]

def process_remote(line):
    args = line.split(' ')[1:]

    return " ".join(args)

temp_dir = tempfile.mkdtemp()
response = requests.get(CONFIG_URL)

zip_path = '%s/config.zip' % temp_dir
configs_path = '%s/configs' % temp_dir
keys_path = sys.argv[1]

os.mkdir(configs_path)

with open(zip_path, 'w') as config_zip:
    config_zip.write(response.content)

with ZipFile(zip_path) as config_zip:
    config_zip.extractall(configs_path)

for config_path in glob('%s/us[0-9]*udp*' % configs_path):
    ca = ""
    tls_auth = ""
    with open(config_path) as config:
        host = short_name(config_path)

        for line in config:
            if line.startswith('remote'):
                with open('%s/%s.remote' % (keys_path, host), 'w') as remote_file:
                    remote_file.write(process_remote(line))
                break

        read_until(config, "<ca>")
        with open('%s/%s.ca' % (keys_path, host), 'w') as ca_file:
            ca_file.write(read_until(config, "</ca>"))

        read_until(config, "<tls-auth>")
        with open('%s/%s.tls_auth' % (keys_path, host), 'w') as tls_auth_file:
            tls_auth_file.write(read_until(config, "</tls-auth>"))
