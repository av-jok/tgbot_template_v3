import pymysql
from app.config import conf


def query_select(query):
    try:
        db = pymysql.connect(host=conf.db.host,

                             user=conf.db.user,
                             password=conf.db.password,
                             database=conf.db.database,
                             cursorclass=pymysql.cursors.DictCursor
                             )
        db.autocommit(True)
        try:

            with db.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        finally:
            db.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)
    return rows


def query_insert(query):
    try:
        db = pymysql.connect(host=conf.db.host,

                             user=conf.db.user,
                             password=conf.db.password,
                             database=conf.db.database,
                             cursorclass=pymysql.cursors.DictCursor
                             )
        db.autocommit(True)
        try:
            with db.cursor() as cursor:
                cursor.execute(query)
                db.commit()
        except Exception as ex:
            print(ex)
        finally:
            db.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)
