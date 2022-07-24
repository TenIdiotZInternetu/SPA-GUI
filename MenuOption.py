from abc import abstractclassmethod
import os, sys
import pygame
from pygame.sprite import DirtySprite

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class MenuOption(DirtySprite):
    def __init__(self, datafile, image):
        DirtySprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()

        self.assign_metadata(datafile)


    def assign_metadata(self, file):
        with open(file) as f:
            for line in f.readlines():
                if "[Title] " in line: self.title = line[7:-1]
                if "[Desc] " in line: self.description_file = line[7:-1]
                if "[Command] " in line: self.command = line[10:-1]
                if "[Author] " in line: self.author = line[9:]
