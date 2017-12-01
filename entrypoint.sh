#!/bin/ash
set -e

# if command starts with an option, prepend walog
if [ "${1:0:1}" = '-' ]; then
	set -- walog "$@"
fi

echo "-> Preparing directory structure (mkdir/chown)"
mkdir -p /home/walog/.yowsup /messages
chown -R walog:walog /messages /home/walog
echo "-> Starting walog"
exec sudo -u walog "$@"
