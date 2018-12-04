import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="inventorysystemdb"
)
mycursor = mydb.cursor()

sqlFormula ="INSERT INTO logincredentials(UserName, Password) Values(%s,%s)"
password1 = ("Gwapo","gwapogiboy")

mycursor.execute(sqlFormula, password1)
mydb.commit()