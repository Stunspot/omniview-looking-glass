#!/bin/sh
cd -- "$(dirname -- "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
  python3 ./host.py
else
  printf '%s\n' 'Install Python 3.10 or newer, then open this file again.'
  read -r reply
fi
