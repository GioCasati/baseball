from database.DB_connect import DBConnect
from model.team import Team


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT year
                   FROM teams
                   WHERE year >= 1980"""
        cursor.execute(query)
        res = []
        for row in cursor.fetchall():
            res.append(row['year'])
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllTeamsYear(year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT *
                   FROM teams
                   WHERE year = %s"""
        cursor.execute(query, (year,))
        res = []
        for row in cursor.fetchall():
            res.append(Team(**row))
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllEdgesYear(year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT p1.ID as u, p2.ID as v, p1.tot+p2.tot as weight
                    FROM (SELECT t.ID, sum(s.salary) as tot
                            FROM teams t , salaries s 
                            WHERE t.ID = s.teamID and t.`year` = s.year and t.`year` = %s
                            GROUP BY t.ID) p1,
                            (SELECT t.ID, sum(s.salary) as tot
                            FROM teams t , salaries s 
                            WHERE t.ID = s.teamID and t.`year` = s.year and t.`year` = %s
                            GROUP BY t.ID) p2
                    WHERE p1.ID<p2.ID"""

        cursor.execute(query, (year,year))
        res = []
        for row in cursor.fetchall():
            res.append(row)
        cursor.close()
        cnx.close()
        return res