#!/bin/bash

set -ex

readonly SCRIPT_DIR="$( cd -P "$( dirname "$(readlink -f "${BASH_SOURCE[0]}")" )" >/dev/null 2>&1 && pwd )"
python3 ${SCRIPT_DIR}/../src/wishlist/update.py
