from flask_restful import Resource

from services.iplService import IplService


class Seasons(Resource):

    def __init__(self):
        self.service = IplService()

    def get(self):
        """ Get list of Seasons in years"""
        response = self.service.getIplSeasons()
        return response
