#Computer science NEA main program
import pygame

#intial window
pygame.init()
screen_width = 500
screen_height = 500
window = pygame.display.set_mode((screen_width,screen_height))
window.fill((0,0,0))
pygame.display.set_caption("Evolution Simulator")
pygame.display.update()

pygame.draw.rect(window,(255,255,255),(50,50,50,50))
pygame.display.update()

#def UpdateMove(move):


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

MainLoop()