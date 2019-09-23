#Computer science NEA main program

import sqlite3
import os


db = sqlite3.connect("Companies.db")
cursor = db.cursor()

#cursor.execute('''DROP TABLE companies''')
#cursor.execute('''DROP TABLE ras2019''')
#cursor.execute('''DROP TABLE hgs2019''')

cursor.execute('''CREATE TABLE IF NOT EXISTS companies (id INT, name STRING, code STRING, no_users INT, no_admin INT, admin_code STRING)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS ras2019 (id INT, username STRING, password STRING, security STRING, first_name STRING, last_name STRING, level INT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS hgs2019 (id INT, username STRING, password STRING, security STRING, first_name STRING, last_name STRING, level INT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS projects (project_id INT, company_name STRING, users STRING)''')


cursor.execute('''INSERT INTO companies (id,name,code,no_users,no_admin,admin_code) VALUES (1,"Ralph Allen School","ras2019",1,2,1111)''')
cursor.execute('''INSERT INTO companies (id,name,code,no_users,no_admin,admin_code) VALUES (2,"Haysfield Girls School","hgs2019",1,3,1111)''')

cursor.execute('''INSERT INTO ras2019 (id,username,password,security,first_name,last_name,level) VALUES (1,"rhianmack","1234","Storkey","Rhian","Mackintosh",1)''')
cursor.execute('''INSERT INTO hgs2019 (id,username,password,security,first_name,last_name,level) VALUES (2,"milliel","1111","Lisney","Millie","Lisney",2)''')



def Menu():
    code = input("Enter company code or press '#' to register a company: ")

    a = False
    while not a:
        if code == '#':
            Register()
            a = True
        else:
            cursor.execute('''SELECT code FROM companies''')
            for row in cursor:
                if row[0] == code:
                    a = True
                    choice = input("log in (any key) sign up (1): ")
                    if choice == '1':
                        SignUp(code)
                    else:
                        LogIn(code)
            if not a:
                code = input("Company code not recognised, please try again: ")





def LogIn(code):
    matching = False
    while matching == False:
        L_username = input("Enter your username: ")
        L_password = input("Enter your password: ")
        cursor.execute('''SELECT * FROM '''+ code)
        for row in cursor:
            if L_username == row[1]:
                print("matching username")
                cursor.execute('''SELECT password FROM '''+code+''' WHERE username = ?''', (L_username,))
                for row1 in cursor:
                    if L_password == str(row1[0]):
                        print("matching password")
                        matching = True
                        break
                    else:
                        print("wrong password")
                pass
            else:
                pass
        if not matching:
            print("Username or password incorrect, please try again (error 1)")

def SignUp(code):

    N_username = input("Enter a username: ")
    taken = True
    while taken:
        cursor.execute('''SELECT username FROM '''+code)
        for row in cursor:
            if row[0] == N_username:
                taken = True
                N_username = input("Username taken please try again: ")
                break
            else:
                taken = False
    matching = False
    while not matching:
        N_password = input("Enter your password: ")
        N_pass = input("Enter password again: ")
        if N_password == N_pass:
            matching = True
        else:
            print("Passwords do not match please try again: ")

    print("\nPlease enter your details: ")
    N_name = input("First name: ")
    N_lastname = input("Last name: ")
    N_security = input("Mothers maiden name: ")
    N_level = input("(if applicable) Enter admin code: ")
    if N_level == "code":
        N_level = 1
    else:
        N_level = 2

    cursor.execute('''SELECT MAX(id) FROM '''+code)
    for row in cursor:
        last_id = row[0]
    last_id += 1

    cursor.execute('''INSERT INTO '''+code+''' (id,username,password,security,first_name,last_name,level) VALUES (?,?,?,?,?,?)''',(last_id,N_username,N_password,N_security,N_name,N_lastname,N_level))
    print("\nSign up complete you will now be taken to the log in page.\n")
    LogIn()


def Register():
    name = input("Enter full company name: ")

    admin_code = os.urandom(5)

    code = input("Enter a company code: ")

    cursor.execute('''SELECT MAX(id) FROM companies''')
    for row in cursor:
        last_id = row[0]
    last_id += 1

    cursor.execute('''INSERT INTO companies (id, name, code, no_users, admin_code) VALUES (?,?,?,?,?)''',(last_id,name,code,0,admin_code))

    print("Company registered, you will now be take to sign up your first user")
    SignUp(code)





Menu()