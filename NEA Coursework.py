#Computer science NEA main program
import pygame
import sqlite3


db = sqlite3.connect("Users.db")
cursor = db.cursor()

cursor.execute('''DROP TABLE users''')

cursor.execute('''CREATE TABLE users (id INT, username STRING, password STRING, security STRING, first_name STRING, last_name STRING, company_code STRING)''')

cursor.execute('''INSERT INTO users (id,username,password,security,first_name,last_name,company_code) VALUES (1,"rhianmack","1234","Storkey","Rhian","Mackintosh","ralphallen2019")''')
cursor.execute('''INSERT INTO users (id,username,password,security,first_name,last_name,company_code) VALUES (2,"milliel","1111","Lisney","Millie","Lisney","haysfeild2019")''')

class Authentication():
    #def __init__(self):

    def LogIn():
        matching = False
        while matching == False:
            L_username = input("Enter your username: ")
            L_password = input("Enter your password: ")
            cursor.execute('''SELECT * FROM users''')
            for row in cursor:
                if L_username == row[1]:
                    print("matching username")
                    cursor.execute('''SELECT password FROM users WHERE username = ?''', (L_username,))
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

    def SignUp():

        N_username = input("Enter a username: ")
        taken = True
        while taken:
            cursor.execute('''SELECT username FROM users''')
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
        N_code = input("(if applicable) Compnay code: ")
        if N_code == '':
            N_code = 'None'

        cursor.execute('''SELECT MAX(id) FROM users''')
        for row in cursor:
            last_id = row[0]
        last_id += 1

        cursor.execute('''INSERT INTO users (id,username,password,security,first_name,last_name,company_code) VALUES (?,?,?,?,?,?,?)''',(last_id,N_username,N_password,N_security,N_name,N_lastname,N_code))
        print("\nSign up complete you will now be taken to the log in page.\n")
        Authentication.LogIn()


Authentication.SignUp()

'''
#intial window
pygame.init()
screen_width = 500
screen_height = 500
window = pygame.display.set_mode((screen_width,screen_height))
window.fill((0,0,0))
pygame.display.set_caption("Project management")
pygame.display.update()

pygame.draw.rect(window,(255,255,255),(50,50,50,50))
pygame.display.update()

#def UpdateMove(move):

'''

def MainLoop():
    run = True
    while run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            quit()

        if key[pygame.K_UP]:
            move = (0,2)
            Update(move)


