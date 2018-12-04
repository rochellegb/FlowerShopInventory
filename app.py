from flask import Flask, render_template, request, redirect, url_for, flash, session , escape

import pymysql

app = Flask(__name__)
app.secret_key = "super secret key"
@app.route('/')
def login():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return render_template('login.html')
@app.route('/home', methods =['POST'])
def home():
    return render_template('index.html')
@app.route('/log', methods = ['POST'])
def log():

        try:
            username_form = request.form['username']
            password_form = request.form['password']
            if username_form == "" and password_form == "":
              print('Please fill out the fields')
            else:

                if request.method == 'POST':
                        mydb = pymysql.connect(user='root', password='root', host='localhost', database='inventorysystemdb')
                        mycursor = mydb.cursor()

                        if 'username' in session:
                            return redirect(url_for('index'))
                        if request.method == 'POST':
                            mycursor.execute("SELECT COUNT(1) FROM logincredentials WHERE UserName = %s;", [username_form])
                            if mycursor.fetchone()[0]:
                                mycursor.execute("SELECT Password FROM logincredentials WHERE Password = %s;", [password_form])
                                for row in mycursor.fetchall():
                                    if password_form == row[0]:
                                        session['username'] = request.form['username']
                                        mydb.commit()
                                        mycursor.close()
                                        print('Login Successfully')
                                        return render_template('index.html')
                                    else:
                                        print('Either Username or Password is Incorrect')
                                        return redirect(url_for('login'))
                                else:
                                    print('Either Username or Password is Incorrect')
                                    return redirect(url_for('login'))
                            else:
                                print('Either Username or Password is Incorrect')
                                return redirect(url_for('login'))
        except Exception as e:
                    print(e)
                    return render_template('login.html')

@app.route('/logout', methods = ['GET'])
def logout():
    if request.method == 'GET':
      session.clear()
      return render_template('login.html')

@app.route('/insert', methods = ['POST'])
def insert():


        try:
            prodname = request.form['addname']
            prodprice = request.form['addprice']
            prodquant = request.form['addquantity']

            if prodname == "" and prodprice == "" and prodquant == "":
                  print('Please fill out the fields')
                  return redirect(url_for('index'))
            else:
                    if request.method == 'POST':

                        mydb = pymysql.connect(user ='root', password= 'root', host = 'localhost',database="inventorysystemdb")

                        mycursor = mydb.cursor()

                        mycursor.execute("INSERT INTO flowerinventory(product_name, price ,quantity) Values(%s,%s,%s)", (prodname, prodprice, prodquant))
                        mydb.commit()
                        mycursor.close()
                        mydb.close()
                        print(prodname + ', ' + prodprice + ', ' + prodquant + ', Successfully saved!' )
                        return render_template('index.html')
        except Exception as e:
            print(e)
            return render_template('index.html')
@app.route('/searchall', methods =['POST'])
def searchall():
    try:
        if request.method == 'POST':
            mydb = pymysql.connect(user='root', password='root', host='localhost', database='inventorysystemdb')
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM flowerinventory")
            data = mycursor.fetchall()
            return render_template('index.html', products=data)
    except Exception as e:
        print(e)
        return render_template('index.html')
@app.route('/search', methods =['POST'])
def search():

    try:
        prodname = request.form['searchprod']
        if prodname == "":
            print('Please fill out the fields')
            return render_template('index.html')
        else:
            if request.method == 'POST':
                mydb = pymysql.connect(user='root', password='root', host='localhost', database='inventorysystemdb')
                mycursor = mydb.cursor()
                if request.method == 'POST':
                    mycursor.execute("SELECT COUNT(1) FROM flowerinventory WHERE product_name = %s;", [prodname])
                    if mycursor.fetchone()[0]:
                        mycursor.execute("SELECT * FROM flowerinventory WHERE product_name = %s;", [prodname])
                        prod = mycursor.fetchall()
                        print(prodname + ' Found!')
                        return render_template('index.html', prodnames=prod)
                    else:
                        print('There no such product as' + prodname)
                    return render_template('index.html')
                else:
                    print('There no such product as' + prodname)
                    return render_template('index.html')
            else:
                return render_template('index.html')
            return render_template('index.html')
    except Exception as e:
        print(e)
        return render_template('index.html')
@app.route('/delete', methods =['POST'])
def delete():
    try:
        namee = request.form['prodsname']
        if namee == "":
            print('please fill out the field')
            return render_template('index.html')
        else:
            if request.method == 'POST':
                mydb = pymysql.connect(user='root', password='root', host='localhost', database='inventorysystemdb')
                mycursor = mydb.cursor()
                if request.method == 'POST':
                    mycursor.execute("SELECT COUNT(1) FROM flowerinventory WHERE product_name = %s;", [namee])
                    if mycursor.fetchone()[0]:
                        mycursor.execute("DELETE FROM flowerinventory WHERE product_name = %s;", [namee])
                        mydb.commit()
                        mycursor.close()
                        mydb.close()
                        print('Successfully Deleted!')
                        return render_template('index.html')
                    else:
                        print('Product' + request.form['prodsname'] + ' is not on the List')
        return render_template('index.html')
    except Exception as e:
        print(e)
        return render_template('index.html')

if __name__ == "__main__":
 app.run(debug=True)