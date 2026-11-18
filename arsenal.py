import pygame
from bullet import Bullet
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class Arsenal:
    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

        self.fire_mode = 1
        self.spread_shots_remaining = self.settings.spread_max_shots
        self.cooldown = False
        self.cooldown_start_time = 0

    def set_fire_mode(self, mode: int):
        if mode in (1, 3):
            self.fire_mode = mode

    def remove_bullet_off_screen(self):
        for bullet in self.arsenal.copy():
            if (bullet.rect.bottom <= 0 or bullet.rect.right < 0 or bullet.rect.left > self.settings.screen_width):
                self.arsenal.remove(bullet)

    def fire_bullet(self):
        current_time = pygame.time.get_ticks()
        if self.fire_mode == 3:
            if not self.cooldown and self.spread_shots_remaining > 0:
                if len(self.arsenal) + 3 <= self.settings.bullet_amount:
                    for x_vel in (-self.settings.spread_x_speed, 0.0, self.settings.spread_x_speed):
                        new_bullet = Bullet(self.game, self.game.ship, x_speed = x_vel)
                        self.arsenal.add(new_bullet)

                    self.spread_shots_remaining -= 1

                    if self.spread_shots_remaining == 0:
                        self.cooldown = True
                        self.cooldown_start_time = current_time

                    return True
            else:
                remaining_time = max(0.0, (self.settings.spread_cooldown - (current_time - self.cooldown_start_time)) / 1000.0)

        if len(self.arsenal) < self.settings.single_fire_bullet_amount:
            new_bullet = Bullet(self.game, self.game.ship, x_speed = 0.0)
            self.arsenal.add(new_bullet)
            return True
        return False

    def update_arsenal(self) -> None:
        self.arsenal.update()
        self.remove_bullet_off_screen()

        if self.cooldown:
            time_used = pygame.time.get_ticks() - self.cooldown_start_time
            if time_used >= self.settings.spread_cooldown:
                self.cooldown = False
                self.spread_shots_remaining = self.settings.spread_max_shots

    def draw_arsenal(self) -> None:
        for bullet in self.arsenal:
            bullet.draw_bullet()
