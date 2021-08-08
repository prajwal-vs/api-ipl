from flask_restful import Resource

from commons.json_utils import to_json
from constants.custom_field_error import HTTP_400_BAD_REQUEST
from services.iplService import IplService


class Metrics(Resource):

    def __init__(self):
        self.service = IplService()

    def get(self, season):
        """ Get Ipl Metrics Data """
        if season not in ['2017', '2016']:
            return to_json('Season should be either 2017 or 2016', is_error=True), HTTP_400_BAD_REQUEST
        response = self.service.getIplMetrics(season)
        return response
