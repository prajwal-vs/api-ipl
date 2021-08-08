from os import environ


class DBQUERIES(object):
    def __init__(self):
        pass

    # Env Variables
    POSTGRES_SCHEMA = environ.get('POSTGRES_SCHEMA')
    MATCHES_TABLE = environ.get('MATCHES_TABLE')
    DELIVERIES_TABLE = environ.get('DELIVERIES_TABLE')

    # DB Query
    SELECT_CLAUSE_KEY = """SELECT """
    FROM = " FROM "
    WHERE_CLAUSE_KEY = """ WHERE """
    IN_OPERATOR = " IN "
    AND_OPERATOR = " AND "
    ORDER_BY_CLAUSE_KEY = """ ORDER BY """
    GROUP_BY_CLAUSE_KEY = """ GROUP BY """
    DESC = """ DESC """
    LIMIT = """ LIMIT """
    DISTINCT_CLAUSE_KEY = """ DISTINCT """
    WHEN = """ WHEN """


class Const:
    def __init__(self):
        pass

    SEASONS = {
        "2017",
        "2016",
        "2015",
        "2014",
        "2013",
        "2012",
        "2011",
        "2010",
        "2009",
        "2008"
    }
