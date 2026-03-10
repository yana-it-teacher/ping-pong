from pygame import *
import socket
import json
from threading import Thread

# ---ПУГАМЕ НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Ping-Pong")
# ---СЕРВЕР ---
def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('localhost', 8080)) # ---- Підключення до сервера
            buffer = ""
            game_state = {}
            my_id = int(client.recv(24).decode())
            return my_id, game_state, buffer, client
        except:
            pass


def receive():
    global buffer, game_state, game_over
    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data
            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
        except:
            game_state["winner"] = -1
            break
font_dir = "assets/fonts/Orbitron-Regular.ttf"
# --- ШРИФТИ ---
font_win = font.Font(font_dir, 72)
font_main = font.Font(font_dir, 36)
font_score = font.Font("assets/fonts/Orbitron-Bold.ttf", 30)

# --- ЗОБРАЖЕННЯ ----
bg_img = image.load("assets/bg.png")
bg_img = transform.scale(bg_img, (WIDTH, HEIGHT))

paddle_img = image.load("assets/paddle.png")
paddle_img = transform.scale(paddle_img, (20, 130))

ball_img = image.load("assets/ball.png")
ball_img = transform.scale(ball_img, (30, 30))
# --- ЗВУКИ ---

# --- ГРА ---
game_over = False
winner = None
you_winner = None
my_id, game_state, buffer, client = connect_to_server()
Thread(target=receive, daemon=True).start()
ball_angle = 0
while True:
    for e in event.get():
        if e.type == QUIT:
            exit()

    if "countdown" in game_state and game_state["countdown"] > 0:
        screen.fill((0, 0, 0))
        countdown_text = font.Font(font_dir, 72).render(str(game_state["countdown"]), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 30))
        display.update()
        continue  # Не малюємо гру до завершення відліку

    if "winner" in game_state and game_state["winner"] is not None:
        screen.fill((20, 20, 20))

        if you_winner is None:  # Встановлюємо тільки один раз
            if game_state["winner"] == my_id:
                you_winner = True
            else:
                you_winner = False

        if you_winner:
            text = "You Win!"
        else:
            text = "You Lose!"

        win_text = font_win.render(text, True, (255, 215, 0))
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)

        text = font_win.render('K - restart', True, (255, 215, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(text, text_rect)

        display.update()
        continue  # Блокує гру після перемоги

    if game_state:
        screen.blit(bg_img, (0, 0))
        screen.blit(paddle_img, (20, game_state['paddles']['0']))
        screen.blit(paddle_img, (WIDTH - 40, game_state['paddles']['1']))
        ball_angle = (ball_angle + 5) % 360
        ball_rot = transform.rotate(ball_img, ball_angle)

        ball_rect = ball_rot.get_rect(center=(game_state['ball']['x'],
                                            game_state['ball']['y']))
        screen.blit(ball_rot, ball_rect)
        score_text = font_score.render(
            f"{game_state['scores'][0]} : {game_state['scores'][1]}",
            True,
            (0,255,255)
        )
        screen.blit(score_text, (WIDTH // 2 -25, 20))
        
        
        if game_state['sound_event']:
            if game_state['sound_event'] == 'wall_hit':
                # звук відбиття м'ячика від стін
                pass
            if game_state['sound_event'] == 'platform_hit':
                # звук відбиття м'ячика від платформи
                pass

    else:
        wating_text = font_main.render(f"Download...", True, (255, 255, 255))
        screen.blit(wating_text, (WIDTH // 2 - 25, 20))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_w]:
        client.send(b"UP")
    elif keys[K_s]:
        client.send(b"DOWN")
