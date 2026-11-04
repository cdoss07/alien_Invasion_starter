import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_width, self.settings.ship_height))
        self.rect = self.image.get_rect()
        self.center_ship()
        self.moving_right = False
        self.moving_left = False
        self.arsenal = arsenal

    def center_ship(self):
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)

    def update(self):
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed
        self.rect.x = self.x

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)

    def fire(self) -> None:
        return self.arsenal.fire_bullet()

    def check_collisions(self, other_group):
        if pygame.sprite.spritecollideany(self, other_group):
            self.center_ship()
            return True
        return False