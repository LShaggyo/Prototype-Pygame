import pygame

# Clase Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('assets/imgs/itachi.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (70, 70))  # Imagen original del jugador
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False
        self.used_double_jump = False  # Estado para controlar el doble salto
        self.speed = 3  # Velocidad de movimiento del jugador
        self.jump_power = -12  # Potencia de salto del jugador
        self.gravity = 0.6  # Gravedad
        self.shrunk = False  # Estado para controlar si el jugador está encogido

    def update(self):
        # Aplicar movimiento horizontal
        self.rect.x += self.change_x
        
        # Verificar colisiones horizontales
        self.handle_horizontal_collisions()

        # Aplicar gravedad
        if not self.on_ground:
            self.change_y += self.gravity
        
        # Aplicar movimiento vertical
        self.rect.y += self.change_y

        # Verificar colisiones verticales
        self.handle_vertical_collisions()

        # Limitar el movimiento del jugador dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:  # Ancho de la pantalla
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:  # Alto de la pantalla
            self.rect.bottom = 600

    def handle_horizontal_collisions(self):
        collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in collisions:
            if self.change_x > 0:  # Moviendo a la derecha
                self.rect.right = platform.rect.left
            elif self.change_x < 0:  # Moviendo a la izquierda
                self.rect.left = platform.rect.right

    def handle_vertical_collisions(self):
        self.on_ground = False
        collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in collisions:
            if self.change_y > 0:  # Cayendo
                self.rect.bottom = platform.rect.top
                self.change_y = 0
                self.on_ground = True
                self.used_double_jump = False  # Reiniciar el estado del doble salto
            elif self.change_y < 0:  # Saltando
                self.rect.top = platform.rect.bottom
                self.change_y = 0

    def move(self, keys):
        self.change_x = 0

        if keys[pygame.K_LEFT]:
            self.change_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.change_x = self.speed
        if keys[pygame.K_UP] and self.on_ground:
            self.change_y = self.jump_power  # Salto
        if keys[pygame.K_SPACE] and not self.on_ground and not self.used_double_jump:
            self.change_y = self.jump_power  # Doble salto
            self.used_double_jump = True  # Marcar que el doble salto se ha usado
        if keys[pygame.K_DOWN] and not self.shrunk:
            self.shrink()
        elif not keys[pygame.K_DOWN] and self.shrunk:
            self.unshrink()

    def shrink(self):
        self.image = pygame.transform.scale(self.original_image, (35, 35))  # Reducir la imagen a la mitad
        self.rect = self.image.get_rect(center=self.rect.center)
        self.shrunk = True

    def unshrink(self):
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.rect.center)
        self.shrunk = False

    def set_platforms(self, platforms):
        self.platforms = platforms
