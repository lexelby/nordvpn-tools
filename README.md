# Tools for NordVPN

NordVPN has a ton of servers, and they seem to fluctuate in how loaded they are over time.  I wanted to write a script that picked a close-ish server with reasonable load.

These are raw and totally customized to my use case, but hopefully they'll at least provide a starting point for others.

## `nordpicker.py`

Pulls the list of NordVPN servers, calculates the distance to each, and picks a close-ish one with low load.

The search algorithm could probably use some improvement.

## `nordextract.py`

Downloads config.zip, extracts it, and processes each config file.  It pulls out the server IP/port, CA key file, and tls-auth key file and saves them into individual files in the directory specified by the first command-line argument.

The idea is that you can strip out those options from the config file and pass them on the command-line, allowing you to select a server by name.

