# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep the player on the screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def shoot(self):
        # Create a bullet instance at the player's position
        bullet = Bullet(self.rect.right, self.rect.centery)
        bullets.add(bullet)
        all_sprites.add(bullet)

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Define the bullet object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'bullet'
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load("bullet.png ").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.speed = 10

    # Move the bullet based on its speed
    # Remove the bullet when it passes the right edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


# Define the Boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.surf = pygame.image.load("boss.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH - self.surf.get_width() // 2,
                random.randint(
                    self.surf.get_height() // 2, SCREEN_HEIGHT - self.surf.get_height() // 2
                ),
            )
        )
        self.horizontal_speed = random.randint(3, 7)
        self.vertical_speed = random.randint(3, 7)
        self.direction_x = 1
        self.direction_y = 1
        self.health = 10  # Initialize boss health

    def update(self):
        self.rect.move_ip(self.horizontal_speed * self.direction_x, self.vertical_speed * self.direction_y)
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.direction_y *= -1
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


def render_text_with_outline(text, font, text_color, outline_color, outline_width):
    base = font.render(text, True, text_color)
    outline = font.render(text, True, outline_color)

    outline_rect = outline.get_rect()
    base_rect = base.get_rect()

    final_image = pygame.Surface((outline_rect.width + outline_width * 2, outline_rect.height + outline_width * 2),
                                 pygame.SRCALPHA)

    positions = [
        (outline_width, 0), (outline_width, outline_width * 2),
        (0, outline_width), (outline_width * 2, outline_width),
        (0, 0), (0, outline_width * 2),
        (outline_width * 2, 0), (outline_width * 2, outline_width * 2)
    ]

    for pos in positions:
        final_image.blit(outline, pos)

    final_image.blit(base, (outline_width, outline_width))
    return final_image


def start_menu(screen):
    menu_running = True
    font = pygame.font.Font(None, 74)
    title_text = "Saving 'Merica"
    instruction_text = "Press SPACE to Start"

    text_color = (0, 0, 0)
    outline_color = (255, 255, 255)
    outline_width = 2

    title_image = render_text_with_outline(title_text, font, text_color, outline_color, outline_width)
    instruction_image = render_text_with_outline(instruction_text, font, text_color, outline_color, outline_width)

    # Load the background image
    background = pygame.image.load("start_background.jpg").convert()

    while menu_running:
        screen.blit(background, (0, 0))  # Draw the background image
        screen.blit(title_image, (SCREEN_WIDTH // 2 - title_image.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(instruction_image, (SCREEN_WIDTH // 2 - instruction_image.get_width() // 2, SCREEN_HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == K_SPACE:
                    menu_running = False
            elif event.type == QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(30)


def show_end_screen(screen, message, background_image):
    font = pygame.font.Font(None, 74)
    text_color = (255, 255, 255)
    outline_color = (0, 0, 0)
    outline_width = 2

    text_image = render_text_with_outline(message, font, text_color, outline_color, outline_width)

    background = pygame.image.load(background_image).convert()

    screen.blit(background, (0, 0))
    screen.blit(text_image,
                (SCREEN_WIDTH // 2 - text_image.get_width() // 2, SCREEN_HEIGHT // 2 - text_image.get_height() // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == QUIT:
                waiting = False
                pygame.quit()
                exit()

# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup the clock
clock = pygame.time.Clock()

# Load and play background music
pygame.mixer.music.load("Fortunate Son.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")
exposion_sound = pygame.mixer.Sound("exposion.mp3")

# Display the start menu
start_menu(screen)

# Create custom events for adding enemies and clouds
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create sprite groups
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Instantiate player and boss
player = Player()
boss = None

# Add player to all_sprites group
all_sprites.add(player)

# Main game loop
running = True
start_time = pygame.time.get_ticks()  # Track start time

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                player.shoot()
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= 10000 and boss is None:  # Spawn boss after 10 seconds
        boss = Boss()
        all_sprites.add(boss)

    enemies.update()
    clouds.update()
    bullets.update()
    if boss:
        boss.update()

    for bullet in bullets:
        enemies_hit = pygame.sprite.spritecollide(bullet, enemies, True)
        if enemies_hit:
            bullet.kill()
            collision_sound.play()

    if boss:
        boss_hit = pygame.sprite.spritecollide(boss, bullets, True)
        if boss_hit:
            boss.health -= 1  # Decrease boss health
            if boss.health <= 0:
                boss.kill()  # Remove boss from the game if health reaches 0
                exposion_sound.play()
                show_end_screen(screen, "You saved America", "background_image.jpg")
                running = False

    screen.fill((169, 169, 169))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Draw health bar only if boss exists
    health_bar_length = 200  # Length of the health bar
    health_bar_height = 20  # Height of the health bar
    if boss:
        health_bar_fill = (boss.health / 5) * health_bar_length  # Calculate filled portion of the health bar
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, health_bar_length, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 10, health_bar_fill, health_bar_height))

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        show_end_screen(screen, "You were defeated", "lose_background.jpg")
        running = False

    if boss and pygame.sprite.spritecollideany(player, [boss]):
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        show_end_screen(screen, "You were defeated", "lose_background.jpg")
        running = False

    screen.blit(player.surf, player.rect)
    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()