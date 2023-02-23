import pygame


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        self.health_bar = pygame.image.load('./data/ui/health_bar.png').convert_alpha()

        self.coin = pygame.image.load('./data/coins/gold/0.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))

        self.font = pygame.font.Font('./data/ui/ARCADEPI.TTF', 30)

    def show_health(self, current, full):
        health_bar_rect = pygame.Rect((54, 39), (152 * (current / full), 4))

        self.display_surface.blit(self.health_bar, (20, 10))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_coins(self, amount):
        coin_amount_surface = self.font.render(str(amount), False, '#33323d')
        coin_amount_rect = coin_amount_surface.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))

        self.display_surface.blit(self.coin, self.coin_rect)
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)
