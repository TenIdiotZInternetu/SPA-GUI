import pygame
import os, sys, pathlib
import platform
import time, math

import MainMenu

# Pripnutie adresy súboru ku koreňovej adrese projektu
currentdir = os.path.dirname(os.path.realpath(__file__)) 
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

if platform.system() == "Linux":
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV'      , '/dev/fb0')
    os.putenv('SDL_MOUSEDRV'   , 'TSLIB')

# Inicializácia driverov
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

ROOTDIR = pathlib.Path(__file__).parent


class App():
    def __init__(self):
        self.SCREEN_WIDTH = 800     	     # šírka obrazovky
        self.SCREEN_HEIGHT = 480             # výška obrazovky
        self.FPS = 60
        self.CLOCK = pygame.time.Clock()     # objekt časovača

        # inicializácia okna s rozmermi obrazovky
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.rect = self.SCREEN.get_rect()

        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.KEYDOWN])


    def launch_app(self):
        with open(str(ROOTDIR/"loading_check.txt")) as l_check:
            if l_check.readline() == "1":
                l_check.seek(0)
                l_check.write("0")
                self.loading_screen()
                
        MainMenu.MainMenu()


    def loading_screen(self):
        t = time.time()
        image = pygame.image.load(str(ROOTDIR/"Assets"/"load_screen.png")).convert()
        font = pygame.font.Font(str(ROOTDIR/"Assets"/"FootlightMTLight.ttf"), 42)

        while 1:
            self.CLOCK.tick(10)
            time_left = 20 - (time.time() - t)

            if time_left % 1 < 0.1:
                text = font.render("Please, wait " + str(math.floor(time_left)) + " more seconds", True, (255, 255, 255))
                text_rect = text.get_rect(center = self.rect.center)

                self.SCREEN.blit(image, (0, 0))
                self.SCREEN.blit(text, text_rect)
                pygame.display.update()

            if time_left < 0: return
        
    

# Globálne premenné
APP = App()
ROOTDIR = pathlib.Path(__file__).parent # Koreňová adresa aplikácie

if __name__ == "__main__":
    APP.launch_app()