import pygame
from control import Control
import config as cfg
from math import copysign


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame_dict = self._get_frame_dict()
        self.animation_dict = self._get_animation_dict()
        self.animation_key = 'idleRight'
        self.image = self.frame_dict[self.animation_key][0]
        self.rect = self.image.get_rect()
        self.rect.center = (cfg.DIS_WIDTH//2, cfg.DIS_HEIGHT//2)
        self.velX = 0
        self.velY = 0
        self.animation_counter = 0

    def _get_frame_dict(self):
        spriteSheet = pygame.image.load("./assets/sprites/player/dog.png").convert_alpha()
        sheetSize = spriteSheet.get_size()
        frame_dict = {}
        key_dict = {0: "down", 1: "right", 2: "up", 3: "left", 4: "idleDown",
                    5: "idleRight", 6: "idleRight2", 7: "sleep", 8: "run"}
        for iy in range(sheetSize[1]//cfg.SPRITE_SIZE):
            frames_x = []
            for ix in range(sheetSize[0]//cfg.SPRITE_SIZE):
                rect = pygame.Rect(ix*cfg.SPRITE_SIZE, iy*cfg.SPRITE_SIZE, cfg.SPRITE_SIZE, cfg.SPRITE_SIZE)
                frame = spriteSheet.subsurface(rect)
                frames_x.append(frame)
            frame_dict.update({key_dict[iy]: frames_x})
        return frame_dict

    def _get_animation_dict(self):
        animation_data = {
            "down": [10, 10, 10, 10],
            "right": [10, 10, 10, 10],
            "up": [10, 10, 10, 10],
            "left": [10, 10, 10, 10],
            "idleRight": [100, 5, 5, 100]
        }

        animation_dict = {}
        for key in animation_data:
            frames_duration = animation_data[key]
            frames_idx = []
            for idx, duration in enumerate(frames_duration):
                frames_idx.extend([idx for _ in range(duration)])
            animation_dict.update({key: frames_idx})

        return animation_dict

    def move(self, delta, control: Control):
        self.velX = 0
        self.velY = 0
        # self.animation_key = 'idleRight'
        if control.moving_up:
            self.velY = -cfg.VELOCITY
            self.animation_key = 'up'
            self.animation_counter += 1
        if control.moving_down:
            self.velY = cfg.VELOCITY
            self.animation_key = 'down'
            self.animation_counter += 1
        if control.moving_left:
            self.velX = -cfg.VELOCITY
            self.animation_key = 'left'
            self.animation_counter += 1
        if control.moving_right:
            self.velX = cfg.VELOCITY
            self.animation_key = 'right'
            self.animation_counter += 1

        if self.velX != 0 and self.velY != 0:
            if self.velX < 0:
                self.animation_key = 'left'
            else:
                self.animation_key = 'right'
            self.velX = copysign(0.7071 * self.velX, self.velX)
            self.velY = copysign(0.7071 * self.velY, self.velY)

        if self.animation_counter >= len(self.animation_dict[self.animation_key]):
            self.animation_counter = 0

        frame_idx = self.animation_dict[self.animation_key][self.animation_counter]
        self.image = self.frame_dict[self.animation_key][frame_idx]

        self.rect.x += int(delta * self.velX * cfg.FRAMERATE)
        self.rect.y += int(delta * self.velY * cfg.FRAMERATE)

    def update(self, delta, control: Control):
        self.move(delta, control)
