#!/bin/sh
for arg in "$@"; do
    if [ "$arg" = '-verifyroms' ]; then
        exec /usr/games/mame "$@"
    fi
done
exec /usr/games/mame "$@" -gameio joy
