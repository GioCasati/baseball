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
        query = """SELECT p1.ID as u, p2.ID as v, p1.totSalary+p2.totSalary as weight
                    FROM
                        (select t.teamCode, t.ID, sum(s.salary) as totSalary
                        from salaries s, teams t, appearances a
                        where s.`year` = t.`year` and t.`year` = a.`year` 
                        and a.`year` = %s
                        and t.ID = a.teamID 
                        and s.playerID = a.playerID 
                        group by t.teamCode) p1,
                        (select t.teamCode, t.ID, sum(s.salary) as totSalary
                        from salaries s, teams t, appearances a
                        where s.`year` = t.`year` and t.`year` = a.`year` 
                        and a.`year` = %s
                        and t.ID = a.teamID 
                        and s.playerID = a.playerID 
                        group by t.teamCode) p2
                    WHERE p1.ID<p2.ID"""

        cursor.execute(query, (year,year))
        res = []
        for row in cursor.fetchall():
            res.append(row)
        cursor.close()
        cnx.close()
        return res