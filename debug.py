import datetime

from object.connectMysql import ConnetMysql

def char_split():
    a = ";"
    print(a.split(";"))

def char_strip():
    a = "  fwe  "
    print(a.strip())

def db_search():
    db = ConnetMysql()
    status = db.search("select status from book where ISBN = '1' and number = 1")
    print(status)
    print(len(status))

def test_digit():
    print("".isdigit())

def comp_date():
    now_date = datetime.datetime.today()
    yes_date = datetime.datetime.strptime("2019-12-15", "%Y-%m-%d")
    print((now_date - yes_date).days)

def add_days():
    now_date = datetime.datetime.today()
    tom_date = now_date + datetime.timedelta(days=1)
    print(tom_date.strftime("%Y-%m-%d"))

if __name__ == '__main__':
    comp_date()