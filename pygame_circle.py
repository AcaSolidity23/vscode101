import pygame
pygame.init()

ourWindow = pygame.display.set_mode( [500, 500])
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ourWindow.fill((0, 0, 0))
    pygame.draw.circle(ourWindow, (0, 150,255), (100, 100), 50)
    pygame.display.flip()
pygame.quit()
