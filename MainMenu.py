from abc import abstractclassmethod
import os, sys
import pygame
import subprocess
from pygame.sprite import DirtySprite

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Startup import APP, ROOTDIR
from MenuOption import MenuOption


class MainMenu(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        
        self.options_folder = ROOTDIR/"Options"
        self.options = []
        self.cur_option = None
        self.cur_option_i = 0

        self.visible_options = []
        self.thumbnails = []
        self.option_frame = pygame.image.load(str(ROOTDIR/"Assets"/"frame.png")).convert_alpha()

        self.cycle = 0

        self.running = True

        self.load_options()
        self.update_thumbnails()
        self.main_loop()


    def load_options(self):
        for file in os.listdir(str(self.options_folder)):
            datafile = str(self.options_folder/file/"data.txt")
            image = str(self.options_folder/file/"image.png")

            mo = MenuOption(datafile, image)
            self.options.append(mo)

        self.cur_option = self.options[0]


    def main_loop(self):
        while self.running:
            APP.CLOCK.tick(30)
            self.event_loop()
            pygame.display.update()
            self.cycle += 1


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: 
                    self.cur_option_i = (self.cur_option_i - 1) % len(self.options)
                    self.cur_option = self.options[self.cur_option_i]
                    self.update_thumbnails()

                if event.key == pygame.K_DOWN: 
                    self.cur_option_i = (self.cur_option_i + 1) % len(self.options)
                    self.cur_option = self.options[self.cur_option_i]
                    self.update_thumbnails()

                if event.key == pygame.K_RETURN: 
                    pygame.display.quit()
                    subprocess.call(self.cur_option.command, shell=True)
                    pygame.quit()

                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()


    def update_thumbnails(self):
        self.thumbnails = []
        self.update_rects = []
        self.visible_options = []

        bg = pygame.image.load(str(ROOTDIR/"Assets"/"bg.png")).convert_alpha()
        APP.SCREEN.blit(bg, (0,0))

        for i in range(-2, 5):
            if i == 0:
                self.thumbnails.append(pygame.transform.scale(self.cur_option.image, (160, 90)))
                self.visible_options.append(self.cur_option)
                continue

            opt_i = (self.cur_option_i + i) % len(self.options)

            self.thumbnails.append(pygame.transform.scale(self.options[opt_i].image, (80, 45)))
            self.visible_options.append(self.options[opt_i])

        pos = [[69, 14], [89, 74], [181, 145], [89, 261],
               [69, 321], [29, 381], [-31, 441]]
        self.update_rects = []

        for i in range(7):
            self.update_rects.append(APP.SCREEN.blit(self.thumbnails[i], pos[i]))

            if i != 2: self.draw_text(self.visible_options[i], pos[i])

        self.draw_cur_option()


    def draw_text(self, option, pos):
        font = pygame.font.Font(str(ROOTDIR/"Assets"/"AAbsoluteEmpire-EaXpg.ttf"), 14)
        image = font.render(option.title, False, (217, 217, 217))
        pos[0] += 100
        pos[1] += 16

        APP.SCREEN.blit(image, pos)


    def draw_cur_option(self):
        font = pygame.font.Font(str(ROOTDIR/"Assets"/"AAbsoluteEmpire-EaXpg.ttf"), 44)
        image = font.render(self.cur_option.title, False, (255, 255, 255))
        APP.SCREEN.blit(image, (359, 154))

        font = pygame.font.Font(str(ROOTDIR/"Assets"/"FootlightMTLight.ttf"), 24)
        image = font.render("By:   " + self.cur_option.author, False, (255, 255, 255))
        APP.SCREEN.blit(image, (388, 228))

        APP.SCREEN.blit(self.option_frame, (179, 143))
