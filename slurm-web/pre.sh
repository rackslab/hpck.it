#!/bin/bash

#PRESCRIPT_DEPS@distributions:el8 module:nodejs:18
#PRESCRIPT_DEPS@distributions:el9 module:nodejs:18
#PRESCRIPT_DEPS npm
#PRESCRIPT_TARBALLS node_modules

npm --prefix frontend --cache /tmp ci
mv frontend/node_modules .
