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

    def Login():
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
            if matching == False:
                print("Username or password incorrect, please try again (error 1)")

Authentication.Login()

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


