#!/bin/sh
set -eu
exec "$(dirname -- "$0")/OmniView.app/Contents/MacOS/launch" "$@"
