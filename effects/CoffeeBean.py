#!/usr/bin/python3
import sys
import random
# non std modules
import pygame
from pygame import gfxdraw
import noise


class CoffeeDraw(object):
    """draws nice colored lines on surface"""


    class Bean(object):
        """represents one colored line"""

        def __init__(self, surface, beans, parameter_dict):
            """
            (pygame.Surface) surface - surface to draw on
            (list) beans - list of beans to remove self when velocity is 0
            (dict) parameter_dict - dictionary of parameters
            """
            self.surface = surface
            self.beans = beans
            self.__dict__.update(parameter_dict)
            self.x = None
            self.y = None
            self.x_off = None
            self.y_off = None
            self.vel = 3 # or option vel
            self.accel = -0.003 # or option accel
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()
            self.color = pygame.Color(0, 0, 0, 0)

        def draw(self):
            """draw line"""
            if self.vel < 0 :
                # remove self
                self.beans.remove(self)
            # original 0.0007
            self.x_off += 0.0007
            self.y_off += 0.0007
            self.vel += self.accel
            self.x += noise.pnoise1(self.x_off, octaves=8) * self.vel - self.vel / 2
            self.y += noise.pnoise1(self.y_off, octaves=8) * self.vel - self.vel / 2
            # set color
            h = abs(noise.pnoise1((self.x_off + self.y_off) / 2)) * 360
            self.color.hsva = (h, 100, 100, 4)
            pygame.gfxdraw.pixel(self.surface, int(self.x) % self.width, int(self.y) % self.height, self.color)


    def __init__(self, surface):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.surface = surface
        # initialize
        self.beans = []
        self.framecount = 1

    def update(self):
        """update every frame"""
        self.framecount += 1
        x_off = self.framecount * 0.0003
        y_off = x_off + 20
        x = noise.pnoise1(x_off, octaves=8) * self.surface.get_width()
        y = noise.pnoise1(y_off, octaves=8) * self.surface.get_height()
        # every 8th frame a new bean
        if self.framecount % 4 == 0:
            self.beans.append(self.Bean(self.surface, self.beans, {
                "x" : x,
                "y" : y,
                "x_off" : x_off,
                "y_off" : y_off}))
        for bean in self.beans:
            bean.draw()

def main():
    try:
        fps = 50
        surface = pygame.display.set_mode((320, 200))
        pygame.init()
        effects = [
            CoffeeDraw(surface),
            ]
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit(0)
            if pause is not True:
                #surface.fill((0, 0, 0, 255))
                for effect in effects:
                    effect.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__" :
    main()
