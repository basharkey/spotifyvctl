#!/usr/bin/env python3
# Modified version of Marcin's script adding command line arguments

# Original author: Marcin Kocur
# Attribution license: https://creativecommons.org/licenses/by/4.0/
# Source: https://wiki.archlinux.org/title/Spotify#Global_media_hotkeys 

import subprocess
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('mode', type=str, help="raise/lower")
parser.add_argument('percent', type=int, help="percentage to raise/lower volume by")
args = parser.parse_args()

x=0
y=0
env = os.environ
env['LANG'] = 'en_US'
app = '"spotify"'
pactl = subprocess.check_output(['pactl', 'list', 'sink-inputs'], env=env).decode().strip().split()
if app in pactl:
    for e in pactl:
        x += 1
        if e == app:
            break
    for i in pactl[0 : x -1 ]:
        y += 1
        if i == 'Sink' and pactl[y] == 'Input' and '#' in pactl[y + 1]:
            sink_id = pactl[y+1]
        if i == 'Volume:' and '%' in pactl[y + 3]:
            volume = pactl[y + 3]
    sink_id = sink_id[1: ]
    volume = volume[ : -1 ]
    if args.mode == 'raise' and int(volume) < 100:
        subprocess.run(['pactl', 'set-sink-input-volume', sink_id, '+' + str(args.percent) + '%'])
    elif args.mode == 'lower' and int(volume) > 0:
        subprocess.run(['pactl', 'set-sink-input-volume', sink_id, '-' + str(args.percent) + '%'])
