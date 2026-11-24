from pathlib import Path
class Settings:
    def __init__(self):
        self.name = "Alien Invasion"
        self.screen_width = 1200
        self.screen_height = 800   
        self.FPS = 60
        self.bg_file = Path.cwd()/'Assets'/'images'/'Starbasesnow.png'
        self.diff_scale = 1.1
        self.scores_file = Path.cwd()/'Assets'/'file'/'scores.json'

        self.ship = Path.cwd()/'Assets'/'images'/'ship2(no bg).png'
        self.ship_width =40
        self.ship_height = 60   
        self.bullet = Path.cwd()/'Assets'/'images'/'laserBlast.png'
        self.lasersound = Path.cwd()/'Assets'/'sound'/'laser.mp3'
        self.impact_sound = Path.cwd()/'Assets'/'sound'/'impactSound.mp3'

        

        self.alien = Path.cwd()/'Assets'/'images'/'enemy_4.png'
        self.alien_width = 40
        self.alien_height = 40
        self.fleet_direction = 1

        self.button_width = 200
        self.button_height = 50
        self.button_color = (0,135,50)

        self.text_color = (255,255,255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd()/'Assets'/'Fonts'/'Silkscreen'/'Silkscreen-Bold.ttf'



    def dynamic_settings(self):
        self.ship_speed = 5
        self.ship_start_amount = 3
        self.bullet_speed = 15
        self.bullet_amount = 15
        self.single_fire_bullet_amount = 5
        self.fleet_speed = 3
        self.fleet_drop = 40
        self.bullet_width = 25
        self.bullet_height = 80
        self.alien_points = 50
        self.spread_cooldown = 5000
        self.spread_x_speed = 3.0
        self.spread_max_shots = 5
        self.armored_alien_health = 3
        self.weak_alien_health = 1


    def increase_diff(self):
        self.ship_speed *= self.diff_scale
        self.bullet_speed *= self.diff_scale
        self.fleet_speed *= self.diff_scale
        self.armored_alien_health *= self.diff_scale