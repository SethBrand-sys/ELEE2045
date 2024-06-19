
import pygame

pygame.init()
window = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
running = True


Vs = 5 #Voltage source initial
R = 2000 #Resistence in Ohms
q_t = 0 #Initial Q
I = 0 #Initial Current
C = 1  # 1 mFarad
dt = 0 

window.fill("black")
start = pygame.time.get_ticks()
current = start
previous = 0
font = pygame.font.Font('freesansbold.ttf', 32)


# I is dq(t)/dt



while running:
    window.fill("black")
    barHeight = 5 + (30 * q_t)
    position = pygame.Vector2(window.get_width() / 2 - 50, (window.get_height() / 2 - barHeight) + 200)
    bar = pygame.draw.rect(window, 'red',pygame.Rect(position, (100, barHeight)))
    
    
    

    text1 = font.render(f"Vc: {Vs}", True, (255,255,255))
    textspace1 = text1.get_rect()

    text2 = font.render(f"Charge: {q_t:.2f}", True, (255,255,255))
    textspace2 = text2.get_rect()
    textspace2.centery = int(textspace1.centery) + 30

    text3 = font.render(f"dt: {dt}", True, (255,255,255))
    textspace3 = text3.get_rect()
    textspace3.centery = int(textspace2.centery) + 30
    
    previous = current
    current = pygame.time.get_ticks()
    dt = current - previous
    clock.tick(60) / 1000


    I = (Vs - q_t / C)/R
    q_t = q_t + I * dt
    window.blit(text1, textspace1)
    window.blit(text2, textspace2)
    window.blit(text3, textspace3)


    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if keys[pygame.K_c]:
        Vs = 5
    else:
        Vs = 0
        

    
    
    pygame.display.update()
    
pygame.quit()