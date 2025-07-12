#!/bin/bash

mkdir -p sync/voltron
curl -o sync/voltron/choosy_voltron.txt https://raw.githubusercontent.com/48klocs/dim-wish-list-sources/master/choosy_voltron.txt
curl -o sync/voltron/voltron.txt https://raw.githubusercontent.com/48klocs/dim-wish-list-sources/master/voltron.txt
curl -o sync/voltron/LICENSE https://raw.githubusercontent.com/48klocs/dim-wish-list-sources/master/LICENSE
python3 wishlist/select.py sync/voltron/voltron.txt wishlist/voltron_subset.txt