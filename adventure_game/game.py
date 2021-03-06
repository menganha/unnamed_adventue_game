import sys
from typing import List

import pygame

import adventure_game.config as cfg
import adventure_game.utilities as utils
from adventure_game.control import Control
from adventure_game.enemy_group import EnemyGroup
from adventure_game.player import Player
from adventure_game.user_interface import UserInterface
from adventure_game.world import World
from adventure_game.scene_director import SceneDirector


class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Untitled Adventure Game")
        self.screen = pygame.display.set_mode((cfg.DIS_WIDTH * cfg.SCALE, cfg.DIS_HEIGHT * cfg.SCALE))
        self.display = pygame.Surface((cfg.DIS_WIDTH, cfg.DIS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./assets/font/PressStart2P.ttf", 8)
        self.exit = False
        self.control = Control()
        self.player = Player()
        self.world = World()
        self.ui = UserInterface(self.display, self.font)
        self.enemies = EnemyGroup(self.world.map_data_file)
        self.director = SceneDirector(self.player, self.world, self.enemies)
        self.delta = 0

    def game_loop(self):
        while not self.exit:
            self.delta = self.clock.tick(cfg.FRAMERATE) / 1000
            self.delta = 1 / cfg.FRAMERATE

            if self.director.under_control():
                self.director.update(self.delta)
            else:
                self._process_input()
                self._update_objects()
            self._render_to_screen()

        pygame.quit()
        sys.exit(0)

    def _process_input(self):
        self.control.fetch_input()
        self.exit = self.control.close_window

    def _update_objects(self):
        self.ui.update(self.player.life)
        self.player.update(self.delta, self.control, self.world.solid_objects, self.enemies)
        self.enemies.update(self.delta, self.world.solid_objects, self.player.position)

    def _render_to_screen(self):
        world_rect = self.world.draw(self.display)
        ui_rects = self.ui.draw(self.display)
        self.player.sprite_group.draw(self.display)
        self.enemies.sprite_group.draw(self.display)
        self._debug_blit()
        pygame.transform.scale(self.display, (cfg.DIS_WIDTH * cfg.SCALE, cfg.DIS_HEIGHT * cfg.SCALE), self.screen)

        updated_rectangles = self._scale_rects(world_rect, *ui_rects)
        pygame.display.update(updated_rectangles)

    @staticmethod
    def _scale_rects(*list_of_rects: pygame.Rect) -> List[pygame.Rect]:
        scaled_rectangles = []
        scaled_rectangles.extend(utils.scale_rect(rect) for rect in list_of_rects)
        return scaled_rectangles

    def _debug_blit(self):
        """
        Blits things that are only used for testing purposes
        """
        self.display.blit(self.player.sword.image, self.player.sword.current_rect)
        self.display.blit(self.player.hitbox.image, self.player.hitbox.rect)
