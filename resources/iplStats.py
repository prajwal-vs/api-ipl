from flask_restful import Resource

from commons.json_utils import to_json
from constants.constants import Const
from constants.custom_field_error import HTTP_400_BAD_REQUEST
from services.iplService import IplService


class Statistics(Resource):

    def __init__(self):
        self.service = IplService()

    def get(self, season):
        """ Get Ipl Statistics"""
        if season not in Const.SEASONS:
            return to_json('Season should be either of these values: ' + ', '.join(Const.SEASONS), is_error=True), HTTP_400_BAD_REQUEST

        response = self.service.getIplStats(season)
        return response
