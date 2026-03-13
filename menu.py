import pygame
import sys
import subprocess
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/start_menu.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

clock = pygame.time.Clock()

# кольори
BG = (10, 15, 40)
BUTTON = (30, 180, 200)
BUTTON_HOVER = (60, 220, 240)
TEXT = (255, 255, 255)

font_title = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 70)
font_button = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 40)


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, mouse_pos):

        hover = self.rect.collidepoint(mouse_pos)

        base_color = (30, 180, 200)
        glow_color = (0, 255, 255)

        if hover:
            base_color = (60, 220, 240)

        # основна кнопка
        pygame.draw.rect(screen, base_color, self.rect, border_radius=12)

        # неонове світіння
        for i in range(3):
            glow_rect = self.rect.inflate(i*6, i*6)
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(
                s,
                (*glow_color, 80 - i*16),
                s.get_rect(),
                width=5,
                border_radius=14
            )
            screen.blit(s, glow_rect)

        # текст
        text_surface = font_button.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Shape:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])

        self.size = random.randint(10, 30)
        self.type = random.choice(["circle", "square", "triangle"])

        self.color = random.choice([
            (30, 2, 156),
            (110, 81, 245),
            (76, 38, 252)
        ])

    def update(self):

        self.x += self.vx
        self.y += self.vy

        if self.x < 0 or self.x > WIDTH:
            self.vx *= -1

        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -1

    def draw(self):

        if self.type == "circle":
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

        elif self.type == "square":
            rect = pygame.Rect(self.x, self.y, self.size, self.size)
            pygame.draw.rect(screen, self.color, rect, border_radius=4)

        elif self.type == "triangle":
            points = [
                (self.x, self.y),
                (self.x + self.size, self.y),
                (self.x + self.size//2, self.y - self.size)
            ]
            pygame.draw.polygon(screen, self.color, points)

play_button = Button("Play", WIDTH//2 - 150, 250, 300, 60)
settings_button = Button("Setting", WIDTH//2 - 150, 350, 300, 60)
exit_button = Button("Exit", WIDTH//2 - 150, 450, 300, 60)
bg_img = pygame.image.load("assets/bg.png")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
shapes = [Shape() for _ in range(40)]

while True:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if play_button.clicked(mouse_pos):
                subprocess.Popen(["python", "client.py"])
                pygame.quit()
                sys.exit()

            if settings_button.clicked(mouse_pos):
                print("Відкрити налаштування")

            if exit_button.clicked(mouse_pos):
                pygame.quit()
                sys.exit()

    screen.fill(BG)
    for shape in shapes:
        shape.update()
        shape.draw()

    # заголовок
    title_text = "PING PONG"
    title_color = (0, 220, 255)
    glow_color = (0, 255, 255)

    title = font_title.render(title_text, True, title_color)
    title_rect = title.get_rect(center=(WIDTH//2, 150))

    # неонове світіння
    for i in range(5):
        glow = font_title.render(title_text, True, glow_color)
        glow_rect = glow.get_rect(center=(WIDTH//2, 150))
        glow_rect.inflate_ip(i*6, i*6)

        glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        glow_surf.blit(glow, (0,0))
        glow_surf.set_alpha(40 - i*7)

        screen.blit(glow_surf, glow_rect)

    # основний текст
    screen.blit(title, title_rect)

    # кнопки
    play_button.draw(mouse_pos)
    settings_button.draw(mouse_pos)
    exit_button.draw(mouse_pos)

    pygame.display.update()
    clock.tick(60)