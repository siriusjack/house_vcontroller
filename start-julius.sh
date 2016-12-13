#!/bin/bash
export ALSADEV="plughw:1,0"
julius -C camphor-house.jconf >/dev/null 2>&1 &
echo $!
sleep 3
