#черновой вариант
import pygame

pygame.init
w = pygame.display.set_mode((500, 500))
pygame.display.set_caption('игра фром саня')

igrok = pygame.image.load('player.png')
backGround = pygame.image.load('background.jpg')

x = 50
y = 50
speed = 5

clock = pygame.time.Clock()
run = True
while(run):
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= speed
    elif keys[pygame.K_RIGHT]:
        x += speed
    elif keys[pygame.K_UP]:
        y -= speed
    elif keys[pygame.K_DOWN]:
        y += speed

    w.blit(backGround, (0, 0))
    w.blit(igrok, (x, y))
    pygame.display.update()

pygame.quit()