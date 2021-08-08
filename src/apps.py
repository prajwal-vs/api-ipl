#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Flask base application declaration and URL configuration."""

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from resources.iplSeasons import Seasons
from resources.iplStats import Statistics
from resources.iplMetrics import Metrics

app = Flask(__name__)
CORS(app)
api = Api(app)


# http://server/api/v1/ipl/seasons
api.add_resource(Seasons, '/api/v1/ipl/seasons')

# http://server/api/v1/ipl/statistics/<string:season>
api.add_resource(Statistics, '/api/v1/ipl/statistics/<string:season>')

# http://server/api/v1/ipl/metrics/<string:season>
api.add_resource(Metrics, '/api/v1/ipl/metrics/<string:season>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
