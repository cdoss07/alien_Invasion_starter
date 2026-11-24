import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    def __init__(self, fleet: 'AlienFleet', x: float, y: float, alien_type: str = 'weak') -> None:
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings
        self.alien_type = alien_type

        self.image = pygame.image.load(self.settings.alien)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_width, self.settings.alien_height))

        if self.alien_type == 'armored':
            self.health = self.settings.armored_alien_health
            self.color_red()
        else:
            self.health = self.settings.weak_alien_health



        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = float(self.rect.y)
        self.x =float(self.rect.x)

    def color_red(self):
        red_alien = self.image.copy()
        red_alien.fill((255, 60, 60, 255), special_flags = pygame.BLEND_RGBA_MULT)
        self.image = red_alien

    def update(self) -> None:
        temp_speed = self.settings.fleet_speed

        #if self.check_edges():
            #self.settings.fleet_direction *= -1
            #self.y += self.settings.fleet_drop

        self.x += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        return (self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)

    def draw_alien(self) -> None:
        self.screen.blit(self.image, self.rect)