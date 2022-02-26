#Web Programming Exercise
#CMPSC 431W
#Author: Osheen Arya

#imports
from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

#app route to home page
#home page template is home.html
@app.route('/')
def index():
    return render_template('home.html')

#route to add patient page
#methods post and get used to input and retreive information
@app.route('/add', methods=['POST', 'GET'])

#function name takes input values from form on add.html page
def name():
    error = None
    if request.method == 'POST':
        #result is equal to the returned info from function valid_name
        result = valid_name(request.form['FirstName'], request.form['LastName'])
        #if result value obtained render template with result
        if result:
            return render_template('add.html', error=error, result=result)
        #if not out invalid input name
        else:
            error = 'invalid input name'
    #render template for add.html page
    return render_template('add.html', error=error)

#valid-name function takes inputs from form
#makes changes in database with SQL queries
#outputs all the rows in users in table
def valid_name(first_name, last_name):
    #connect to the database
    connection = sql.connect('database.db')
    #if table does not exist create table users with PID, First Name, Last Name of Pateints
    #primary key is created as pid and it is set to autoincrement
    connection.execute('CREATE TABLE IF NOT EXISTS users(pid integer primary key autoincrement, firstname TEXT, lastname TEXT);')
    #if table exists inserts new values from add.html form into table
    #strip funstion is used to account for any extra spaces before or after input
    connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name.strip(), last_name.strip()))
    connection.commit()
    #select everything from users table
    cursor = connection.execute('SELECT * FROM users;')
    #fetch all selected (to display on webpage)
    return cursor.fetchall()


#route to delete patient page
#methods post and get used to input and retreive information
@app.route('/delete', methods=['POST','GET'])

#function name takes input values from form on delete.html page
def dname():
    error = None
    #name values are taken from forn on delete patient page
    if request.method == 'POST':
        result = remove(request.form['FirstName'], request.form['LastName'])
        #render delete.html page with result
        if result:
            return render_template('delete.html', error=error, result=result)
        #if not valid input display invalid input name
        else:
            error = 'invalid input name'
    #Else statement created to display everything in database initially before removing the name
    else:
        #connect to database and selects everything from users that is present before patient has been deleted
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT * FROM users;')
        result=cursor.fetchall()
    return render_template('delete.html', error=error, result=result)
#function used to delete patient
#takes inout from html form in delete.html template
def remove(first_name, last_name):
    #connect to database
    connection = sql.connect('database.db')
    #query to delete pateit from users table
    connection.execute("DELETE FROM users WHERE firstname = '%s' AND lastname='%s'" % (first_name.strip(),last_name.strip()))
    connection.commit()
    #select all users after patient has been deleted
    #this allows for display of remaining patients in table after each patient is deleted 
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()


#run app
if __name__ == "__main__":
    app.run()


