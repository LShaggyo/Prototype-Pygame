import pygame
import random
from classes.player import Player
from classes.coin import Coin
from classes.platform import Platform

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Prototipo Pygame")
icon = pygame.image.load('assets/imgs/icon.png')
pygame.display.set_icon(icon)

# Cargar y escalar la imagen de fondo
background = pygame.image.load('assets/imgs/akatsuki.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Inicializar jugador, plataformas y grupo de monedas
def create_sprites():
    player = Player()
    coins = pygame.sprite.Group()
    for _ in range(5):
        coin = Coin()
        coins.add(coin)

    platforms = pygame.sprite.Group()
    ground = Platform(0, screen_height - 40, screen_width, 40)  # Suelo
    platform1 = Platform(100, 500, 200, 20)
    platform2 = Platform(400, 400, 200, 20)
    platform3 = Platform(150, 300, 200, 20)
    platform4 = Platform(500, 200, 200, 20)
    platform5 = Platform(250, 100, 200, 20)

    platforms.add(ground, platform1, platform2, platform3, platform4, platform5)
    player.set_platforms(platforms)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(coins)
    all_sprites.add(platforms)

    return player, coins, all_sprites

player, coins, all_sprites = create_sprites()

# Contador de monedas recogidas
coins_collected = 0
font = pygame.font.Font(None, 36)

# Bucle principal del juego
running = True
won = False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and won:
                player, coins, all_sprites = create_sprites()
                coins_collected = 0
                won = False

    keys = pygame.key.get_pressed()
    if not won:
        player.move(keys)  # Mover el jugador basado en las teclas presionadas

        # Verificar colisiones con plataformas
        player.handle_vertical_collisions()

        # Verificar colisiones entre el jugador y las monedas
        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        coins_collected += len(collected_coins)

        if coins_collected == 5:
            won = True

        # Actualizar todos los sprites
        all_sprites.update()

    # Dibujar todo en la pantalla
    screen.blit(background, (0, 0))  # Dibujar el fondo primero
    all_sprites.draw(screen)

    # Mostrar el contador de monedas recogidas
    text = font.render(f"Monedas recogidas: {coins_collected}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Mostrar el mensaje de ganar
    if won:
        win_text = font.render("¡Ganaste! Presiona R para reiniciar", True, (255, 255, 255))
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - win_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

# Salir de Pygame
pygame.quit()
