import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import time
import threading
import pygame
import struct
import random
import os

    
accx = 0
accy = 0
accz = 0
button = 0
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 25)
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("The Sky is Falling")

textst = font.render(f"Connecting to M5 Stick...", True, (255,255,255))
textsstpace = textst.get_rect()
textsstpace.centery = window.get_height() / 2
textsstpace.centerx = window.get_width() / 2
window.blit(textst, textsstpace)
pygame.display.update()

running = True


a = struct.Struct("<fffhh")


def async_thread():
    print("I'm a new thread")

    async def run():
        scanner = BleakScanner()
        devices = await scanner.discover(5,return_adv=True)
        print(devices)
        def notification_callback(sender,payload):
            global accx,accy,accz, button
            accx, accy, accz, batt, button = a.unpack(payload)
            print(accx, accy, button)
            

        async with BleakClient("E8:9F:6D:09:2B:FA") as client:

            await client.start_notify("b0bb55cf-e0f0-4b05-8bca-c6a5835c7a02", notification_callback)
            while running:
                await asyncio.sleep(1)
            
    asyncio.run(run())

t1 = threading.Thread(target = async_thread)

def pygameThread():
    
    async def run():
        await asyncio.sleep(1)
        running = True
        
        posx = window.get_width() / 2
        posy = window.get_height() / 2
        
        start = pygame.time.get_ticks()
        current = start
        previous = 0
        dt = 0
       
        clock = pygame.time.Clock()
        vx = 0
        vy = 0
        font = pygame.font.Font('freesansbold.ttf', 17)

       
           
        
        class Ship(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.image = pygame.Surface([30,30])
                self.image.fill('orange')
                self.rect = self.image.get_rect()
                self.rect.centerx = posx
                self.rect.centery = posy
                self.speedx = vx
                self.speedy = vy
                self.shot1 = 0
                self.last_square = 0
                self.score = 0
                self.dead = False
                self.bullets = pygame.sprite.Group()
                self.squaresGroup = pygame.sprite.Group()
                

            def update(self):
                self.speedx = vx
                self.speedy = vy
                self.rect.centerx += self.speedx
                self.rect.centery += self.speedy
                if self.rect.centerx < 0 or self.rect.centerx > 640:
                    self.rect.centerx = window.get_width() / 2
                if self.rect.centery < 0 or self.rect.centery > 480:
                    self.rect.centery = window.get_height() / 2
                
                    
                
            def shoot(self):
                current = pygame.time.get_ticks()
                if (current - self.shot1) > 250:    
                    self.shot1 = current
                    bullet = Bullet()
                    self.bullets.add(bullet)
                    self.bullets.update()
                    self.bullets.draw(window)
                    
                    

            def spawnSquares(self):
                current = pygame.time.get_ticks()
                if (current - self.last_square) > 250:    
                    self.last_square = current
                    square = Squares()
                    self.squaresGroup.add(square)
                    self.squaresGroup.update()
                    self.squaresGroup.draw(window)
                    
                
                   
            def draw(self):
                
                window.blit(self.image, self.rect)
                
                

        class Bullet(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.image = pygame.Surface([5,5])
                self.image.fill("green")
                self.rect = self.image.get_rect()
                self.rect.centerx = ship.rect.centerx
                self.rect.centery = ship.rect.top

            def update(self):
                self.rect.centery -= 1
                if self.rect.top > window.get_height():
                    self.kill()

           


            def draw(self):
                window.blit(self.image, self.rect)
                
        
        class Squares(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.image = pygame.image.load('lab-1-SethBrand-sys/lab4/meteor.png')
                self.image = pygame.transform.scale(self.image, (30,30))
                self.rect = self.image.get_rect()
                self.rect.centerx = random.randint(0,window.get_width())
                self.rect.centery = -3

            def update(self):
                self.rect.centery += 1
                
                
                
            def draw(self):
                window.blit(pygame.image.load('meteor.png'), self.rect)
        
                


        ship = Ship()
        
        collisions = pygame.sprite.groupcollide(ship.bullets, ship.squaresGroup, True, True)
        hit = pygame.sprite.spritecollide(ship, ship.squaresGroup, True)
        while running:
            
            clock.tick(60)
            previous = current
            current = pygame.time.get_ticks()
            dt = current - previous
            window.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            collisions = pygame.sprite.groupcollide(ship.bullets, ship.squaresGroup, True, True)
            if collisions:
                ship.score += 10
            hit = pygame.sprite.spritecollide(ship, ship.squaresGroup, True)
            if hit:
                ship.dead = True
                ship.kill()
                
            text = font.render(f"Avoid the meteors by moving or by shooting them", True, (255,255,255))
            textspace = text.get_rect()
            window.blit(text, textspace)
            text2 = font.render(f"Score: {ship.score}", True, (255,255,255))
            textspace2 = text2.get_rect()
            textspace2.centery += 40
            window.blit(text2, textspace2)
            
            posx = ship.rect.centerx
            posy = ship.rect.centery
            vx = float(-accx / 5 * dt)
            vy = float(accy / 5 * dt)

            
            ship.bullets.update()
            ship.bullets.draw(window)
            ship.spawnSquares()
            ship.squaresGroup.update()
            ship.squaresGroup.draw(window)
            ship.update()
            ship.draw()
            if button == 1:
                ship.shoot()
            
            while ship.dead == True:
                window.fill('black')
                text3 = font.render(f"Game Over", True, (255,255,255))
                textspace3 = text3.get_rect()
                textspace3.centery = window.get_height() / 2
                textspace3.centerx = window.get_width() / 2
                window.blit(text3, textspace3)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        ship.dead = False
            
            

                

            pygame.display.flip()
            pygame.display.update()
        
        
            
        pygame.quit()
        
    asyncio.run(run())

t2 = threading.Thread(target = pygameThread)

t1.start()
wait = True
while wait == True:
    time.sleep(0.1)
    if accx != 0 and accy != 0 and accz != 0:
        wait = False
while wait == False:
    time.sleep(0.1)
    window.fill('black')
    text = font.render(f"Press M5 Button to begin", True, (255,255,255))
    textspace = text.get_rect()
    textspace.centery = window.get_height() / 2
    textspace.centerx = window.get_width() / 2
    window.blit(text, textspace)
    pygame.display.update()
    if button == 1:
        wait = True
t2.start()
if running == False:
    t1.join()
    t2.join()