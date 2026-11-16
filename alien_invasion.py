import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from stats import GameStats
from time import sleep
from button import Button
from HUD import HUD

class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.settings.dynamic_settings()  
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_width, self.settings.screen_height))
        self.stats = GameStats(self)
        self.HUD = HUD(self)
        self.clock = pygame.time.Clock()

        self.arsenal = Arsenal(self)
        self.ship = Ship(self, self.arsenal)
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()

        self.play_button = Button(self, 'START')
        self.game_active = False
        
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.lasersound)
        self.laser_sound.set_volume(0.7)
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

    def run_game(self):
        while True:
            self._check_events()
            self.screen.fill((230, 230, 230))
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self.check_game_status()


        if self.alien_fleet.check_fleet_bottom():
            self.check_game_status()

        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound .fadeout(500)
            self.stats.update(collisions)
            self.HUD.update_scores()


        if self.alien_fleet.check_destroy():
            self.reset_level()
            self.settings.increase_diff()
            self.stats.update_level()

    def check_game_status(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.reset_level()
            sleep(0.5)
        else:
            self.game_active = False


        print(self.stats.ships_left)


    def reset_level(self):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self):
        self.settings.dynamic_settings()
        self.stats.reset_stats()
        self.HUD.update_scores()
        self.reset_level()
        self.ship.center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)
         
    def _update_screen(self):
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        self.arsenal.draw_arsenal()
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_scores()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
               self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_button_clicked()

    def check_button_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
                if self.ship.fire():
                    self.laser_sound.play()
                    self.laser_sound.fadeout(250)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_q:
            self.running = False
            self.stats.save_scores()
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
