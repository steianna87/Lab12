from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountry():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct gr.Country 
                    from go_retailers gr
                     order by gr.Country  desc"""

        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getRetailer_by_country(country):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select *
                    from go_retailers gr 
                    where gr.Country = %s"""

        cursor.execute(query, (country, ))

        result = []
        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        cnx.close()
        return result

    @classmethod
    def getSpigolo(cls, r1, r2, year, retailerMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select gds2.Retailer_code as r1 , gds.Retailer_code as r2, gds2.`Date` , gds.`Date`, count(distinct gds2.Product_number) as n
                    from go_daily_sales gds, go_daily_sales gds2  
                    where gds2.Retailer_code = %s  and gds.Retailer_code = %s and gds2.Product_number = gds.Product_number 
                    and year (gds.`Date`) = %s and year (gds2.`Date`) = year (gds.`Date`)
                    group by gds2.Retailer_code , gds.Retailer_code"""

        cursor.execute(query, (r1, r2, year))

        result = []
        for row in cursor:
            r1 = retailerMap[row["r1"]]
            r2 = retailerMap[row["r2"]]
            peso = row["n"]
            result.append(Connessione(r1, r2, peso))


        cursor.close()
        cnx.close()
        return result
