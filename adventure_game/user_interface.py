import pygame
import adventure_game.config as cfg


class UserInterface:
    def __init__(self, target_display):
        self.container = pygame.sprite.RenderUpdates()
        self.background = pygame.Surface((cfg.UI_WIDTH, cfg.UI_HEIGHT))
        self.background.fill(cfg.GREEN)
        self.hearts = HeartContainers(self.container)
        self.container.clear(target_display, self.background)

    def update(self, player_life):
        self.container.update(player_life)

    def draw(self, target_display):
        return self.container.draw(target_display)


class HeartContainers(pygame.sprite.DirtySprite):
    """
    Handle the heart sprites in the. A full heart contains 2 heart units.
    """

    def __init__(self, container, max_hearts=3, heart_units=6):
        super().__init__(container)
        self.heart_image_size = (15, 15)
        self.full_heart_image = pygame.image.load(
            "assets/sprites/full_heart.png"
        ).convert()
        self.half_heart_image = pygame.image.load(
            "assets/sprites/half_heart.png"
        ).convert()
        self.empty_heart_image = pygame.image.load(
            "assets/sprites/empty_heart.png"
        ).convert()
        self.max_hearts = max_hearts
        self.heart_units = heart_units
        self.image = self.get_max_hearts_background_image()
        self.rect = self.image.get_rect()
        self.update(0)
        self.dirty = 1

    def get_max_hearts_background_image(self):
        height = self.heart_image_size[1]
        width = self.heart_image_size[0] * self.max_hearts
        surface = pygame.Surface((width, height))
        surface.fill(cfg.GREEN)
        return surface

    def update(self, player_life):
        if player_life != self.heart_units:
            self.heart_units = player_life
            self.image = self.get_max_hearts_background_image()

            full_hearts = self.heart_units // 2
            half_heart = self.heart_units % 2

            for heart_idx in range(self.max_hearts):
                if heart_idx < full_hearts:
                    self.image.blit(
                        self.full_heart_image, (self.heart_image_size[0] * heart_idx, 0)
                    )
                elif half_heart:
                    self.image.blit(
                        self.half_heart_image, (self.heart_image_size[0] * heart_idx, 0)
                    )
                    half_heart = 0
                else:
                    self.image.blit(
                        self.empty_heart_image,
                        (self.heart_image_size[0] * heart_idx, 0),
                    )

            self.dirty = 1