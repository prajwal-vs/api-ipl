import logging
from commons.json_utils import to_json
from constants.constants import DBQUERIES
from constants.custom_field_error import HTTP_200_OK
from DataAccessLayer import DatabaseService

logger = logging.getLogger()


class IplService:
    """Ipl Service"""

    def __init__(self):
        self.service = DatabaseService()

    def getIplSeasons(self):
        try:
            """Query to get the list of IPL Seasons"""
            query = f"""{DBQUERIES.SELECT_CLAUSE_KEY} {DBQUERIES.DISTINCT_CLAUSE_KEY} season {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.ORDER_BY_CLAUSE_KEY} season {DBQUERIES.DESC}"""
            response = self.service.select_many(query)
            if response and 'error' in response:
                return to_json(response, is_error=True)
            return to_json({'seasons': [season[0] for season in response]})

        except Exception as e:
            logger.error(e)
            return to_json(e, is_error=True), Const.HTTP_200_OK

    def getIplStats(self, season):
        try:
            """Query to get the Ipl statistics for a given season"""
            query = f"""{DBQUERIES.SELECT_CLAUSE_KEY}
            array({DBQUERIES.SELECT_CLAUSE_KEY} winner {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' group by winner order by count(winner) desc limit 4)as top_four_winner,
            ({DBQUERIES.SELECT_CLAUSE_KEY} toss_winner {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' group by toss_winner order by count(toss_winner) desc limit 1)as most_tosses_won,
            ({DBQUERIES.SELECT_CLAUSE_KEY} player_of_match {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' group by player_of_match  order by count(player_of_match) desc limit 1) as player_of_match,
            ({DBQUERIES.SELECT_CLAUSE_KEY} winner {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' group by winner order by count(winner) desc limit 1)as won_max_matches,
            ({DBQUERIES.SELECT_CLAUSE_KEY} venue {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' group  by venue ,winner order by count(venue) desc limit 1) as max_hosted_venue_top_team,
            ({DBQUERIES.SELECT_CLAUSE_KEY} venue {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' group  by venue order by count(venue) desc limit 1) as max_hosted_venue,
            ({DBQUERIES.SELECT_CLAUSE_KEY} winner {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' order by win_by_runs desc limit 1) as highest_margin_run,
            ({DBQUERIES.SELECT_CLAUSE_KEY} count(id) {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' and toss_decision ='bat') as decide_to_bat,
            ({DBQUERIES.SELECT_CLAUSE_KEY} count(id) {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}') as total_matches,
            ({DBQUERIES.SELECT_CLAUSE_KEY} count(id) {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' and toss_winner=winner) as won_toss_and_match,
            ({DBQUERIES.SELECT_CLAUSE_KEY} winner {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}' order by win_by_wickets desc limit 1) as highest_margin_wickets
            """
            response = self.service.select_many(query)
            if response and 'error' in response:
                return to_json(response, is_error=True)
            response_data = {
                'top_4_teams': response[0][0],
                'most_tosses_won': response[0][1],
                'won_max_player_of match': response[0][2],
                'won_max_matches': response[0][3],
                'max_hosted_venue_top_team': response[0][4],
                'max_hosted_venue': response[0][5],
                'highest_margin_run': response[0][6],
                'per_team_won_toss': (response[0][7] * 100) // response[0][8],
                'won_toss_and_match': response[0][9],
                'highest_margin_wickets': response[0][10]
            }
            return response_data

        except Exception as e:
            logger.error(e)
            return to_json(e, is_error=True), HTTP_200_OK

    def getIplMetrics(self, season):
        try:
            """Query to get the Ipl metrics for a given season"""
            query = f"""{DBQUERIES.SELECT_CLAUSE_KEY}
            ({DBQUERIES.SELECT_CLAUSE_KEY} jsonb_build_object('batsman', batsman ,'total_runs',sum(batsman_runs) )as batting_stats  {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.DELIVERIES_TABLE}  
            {DBQUERIES.WHERE_CLAUSE_KEY} match_id in ({DBQUERIES.SELECT_CLAUSE_KEY} id {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}')
            group  by batsman order  by sum(batsman_runs) desc limit 1),
            ({DBQUERIES.SELECT_CLAUSE_KEY} jsonb_build_object('bowler', bowler ,'total_wickets',count(dismissal_kind)) as bowling_stats{DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.DELIVERIES_TABLE}  
            {DBQUERIES.WHERE_CLAUSE_KEY} match_id in ({DBQUERIES.SELECT_CLAUSE_KEY} id {DBQUERIES.FROM} {DBQUERIES.POSTGRES_SCHEMA}.{DBQUERIES.MATCHES_TABLE} {DBQUERIES.WHERE_CLAUSE_KEY} season ='{season}') and dismissal_kind  in ('caught','bowled','lbw', 'caught and bowled')
            group  by bowler order  by count(dismissal_kind) desc limit 1)
            """
            response = self.service.select_many(query)
            if response and 'error' in response:
                return to_json(response, is_error=True)
            response_data = {
                'batting_stats': response[0][0],
                'bowling_stats': response[0][1],
            }
            return response_data

        except Exception as e:
            logger.error(e)
            return to_json(e, is_error=True), HTTP_200_OK
