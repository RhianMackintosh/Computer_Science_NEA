import mysql.connector
import random
import datetime
from flask import Flask, render_template, request, flash, redirect, url_for,  make_response

def ValidateNewUserLogIn(PossibleUser,PasswordProvided):
    if PossibleUser == "admin" and PasswordProvided == "password":
        return PossibleUser

    Results = SQLExecute("""Select Password FROM NEADatabase2.tblusers Where UserName = %s""", (PossibleUser, ),'r')
    print('Results from SQL', end = " ")
    for item in Results:
        print(item)
        if item == (PasswordProvided, ):
            return PossibleUser
    return "# " + PossibleUser + " unknown."

def InvalidCredential(PossibleUser,Code):

    Results = SQLExecute("""Select SessionID FROM NEADatabase2.tblusers Where UserName = %s""", (PossibleUser, ),'r')
    print('Results from SQL [SessionID]', end = " ")
    for x in Results:
        print(x)
        if x == (Code, ):
            return False
    return True

def Authenticated(PossibleUser,PasswordProvided):

    Results = SQLExecute("""Select Password FROM NEADatabase2.tblusers Where UserName = %s""", (PossibleUser, ),'r')
    print('Results from SQL')
    for x in Results:
        print(x)
        if x == (PasswordProvided, ):
            return PossibleUser
    return "# " + PossibleUser + " unknown."

def AuthenticatedRenderTemplate(Webpage, Username):
    # Generate SessionTokenCode
    SessionTokenCode = SecureString(8, 65, 91)
    # Modify SQL Database with Session and Expiry Date/Time
    SQLExecute("UPDATE NEADatabase2.tblusers SET SessionID = %s, SessionExpire = %s Where UserName = %s",
             (SessionTokenCode, datetime.datetime.now() + datetime.timedelta(0, 60 * 10), Username),'u')

    # Set up Webpage to reply to User with including Cookies for future authenticated use
    res = make_response(render_template(Webpage, title=Username))
    res.set_cookie('ID', SessionTokenCode, max_age=60 * 10)
    res.set_cookie('User', Username, max_age=60 * 10)
    return res

def SecureString(Number, Low, High, Omit=[]):
#Omit is a list of Ascii codes to be omitted from the String like ' or "
    if Number > 1 :
        #Use Recursion to generate the previous character list then concatenate a new one
        return SecureString(Number - 1, Low, High, Omit) + chr(RandomNumber(Low,High,Omit))
    else :
        # At the bottom of the Recursion so return a single character
        return chr(RandomNumber(Low,High,Omit))

def RandomNumber(Low, High, Omit=[]) :
    #Set PossibleNumberValid Flag to False to force loop to execute
    PossibleNumberValid = False
    while not PossibleNumberValid :
        #Select an integer number that is >= Low, but < High
        SelectNumber = random.randrange(Low, High)
        #Assume the number is valid and adjust flag
        PossibleNumberValid = True
        #Loop through the Omit Array, should the SelectNumber be in the list set the flag to False
        for EachNumber in Omit:
            if EachNumber == SelectNumber:
                PossibleNumberValid = False
    return SelectNumber

print("Test")
for x in range(1, 6):
    print(SecureString(50,33,127,(34,67)))

def SQLExecute(SQLCommand, SQLAddress, type):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="PenygelliSQL2!",
    )
    print('SQL Execute start', end = " ")
    print(SQLCommand, end = " ")
    print(SQLAddress)
    # TheCursor is linked to the Database
    TheCursor = db.cursor()
    #TheDatabase.commit()
    if type == 'r':
        Results = TheCursor.fetchall()
        TheCursor.execute(SQLCommand, SQLAddress)
        print('Done')
        return Results
    else:
        if SQLAddress == "":
            TheCursor.execute(SQLCommand)
        else:
            TheCursor.execute(SQLCommand, SQLAddress)
        print(TheCursor.rowcount, "record(s) affected")
    db.commit()
    db.close()
'''
def SQLUpdate(SQLCommand, SQLAddress):
    TheDatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Apple",
        database="testdatabase",
    )
    TheCursor = TheDatabase.cursor()
    print(SQLAddress, end = " ")
    print(SQLCommand, end = " ")
    if SQLAddress == "" :
        TheCursor.execute(SQLCommand)
    else:
        TheCursor.execute(SQLCommand, SQLAddress)
    TheDatabase.commit()
    print(TheCursor.rowcount, "record(s) affected")

    return TheCursor.rowcount'''
