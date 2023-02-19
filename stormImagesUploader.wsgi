#!/usr/bin/python3
import sys
sys.path.insert(0, '/var/www/web/')

activate_this = '/var/www/web/StormImagesUploader/env/bin/activate'
with open(activate_this) as file:
    exec(file.read(), dict(__file__=activate_this))

from main import app
