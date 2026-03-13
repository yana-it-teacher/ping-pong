from pygame import *
import socket
import json
from threading import Thread
from launcher import ConnectWindow


win = ConnectWindow()
win.mainloop()

name = win.name
port = win.port
host = win.host

# ---ПУГАМЕ НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Ping-Pong")
mixer.init()
# ---СЕРВЕР ---
def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port)) # ---- Підключення до сервера
            buffer = ""
            game_state = {}
            my_id = int(client.recv(24).decode())
            client.sendall(name.encode())
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
font_score = font.Font("assets/fonts/Orbitron-Bold.ttf", 20)

# --- ЗОБРАЖЕННЯ ----
bg_img = image.load("assets/bg.png")
bg_img = transform.scale(bg_img, (WIDTH, HEIGHT))

paddle_img = image.load("assets/paddle.png")
paddle_img = transform.scale(paddle_img, (20, 130))

ball_img = image.load("assets/ball.png")
ball_img = transform.scale(ball_img, (30, 30))
# --- ЗВУКИ ---
sound_ball = mixer.Sound("assets/sounds/ball_hit.mp3")
sound_wall = mixer.Sound("assets/sounds/wall_hit.wav")
mixer.music.load("assets/sounds/game.mp3")
mixer.music.set_volume(0.2)
mixer.music.play(-1)
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
        
        if "names" in game_state:
            # json перетворює ключі-числа на рядки, тому використовуємо '0' та '1'
            name1_text = font_score.render(game_state['names']['0'], True, (3, 211, 252))
            name2_text = font_score.render(game_state['names']['1'], True, (3, 211, 252))
            
            # Малюємо ім'я першого гравця зліва
            screen.blit(name1_text, (200, 15))
            
            # Малюємо ім'я другого гравця справа (відступаємо від правого краю на ширину тексту)
            screen.blit(name2_text, (WIDTH - name2_text.get_width() - 200, 15))

        if game_state['sound_event']:
            if game_state['sound_event'] == 'wall_hit':
                # звук відбиття м'ячика від стін
                sound_wall.play()
                sound_wall.set_volume(0.2)
            if game_state['sound_event'] == 'platform_hit':
                # звук відбиття м'ячика від платформи
                sound_ball.play()
                sound_ball.set_volume(0.2)

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
