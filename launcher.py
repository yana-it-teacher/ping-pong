from customtkinter import *

# Встановлюємо темну тему
set_appearance_mode("dark")

class ConnectWindow(CTk):
    def __init__(self):
        super().__init__()

        self.name = None
        self.host = None
        self.port = None

        self.title('Ping Pong Launcher')
        self.geometry('800x600')

        # --- НАЛАШТУВАННЯ КОЛЬОРІВ ПІД ДИЗАЙН З КАРТИНКИ ---
        bg_color = "#0B0E27"        # Глибокий темно-синій фон
        cyan_accent = "#00FFFF"     # Яскраво-блакитний (для заголовка і рамок)
        btn_fill = "#15B5C8"        # Бірюзовий колір заливки кнопок
        btn_hover = "#1198A8"       # Трохи темніший бірюзовий при наведенні миші
        input_bg = "#060818"        # Дуже темний синій для полів введення
        text_white = "#FFFFFF"      # Білий колір тексту для кнопок

        # Задаємо колір фону самого вікна
        self.configure(fg_color=bg_color)

        # --- СТВОРЕННЯ ВІДЖЕТІВ ---
        
        # Заголовок у стилі логотипа
        CTkLabel(
            self, 
            text='CONNECT', 
            font=("Orbitron", 50, 'bold'), # Жирний масивний шрифт
            text_color=cyan_accent 
        ).pack(pady=(100, 20), padx=20)

        # Поле для імені
        self.name_entry = CTkEntry(
            self, 
            placeholder_text='Nickname', 
            height=45,
            width=300,
            font=('Orbitron', 14, 'bold'),
            fg_color=input_bg,            # Темно-синій фон поля
            border_color=cyan_accent,     # Яскраво-блакитна рамка
            text_color=text_white,        # Білий текст при введенні
            placeholder_text_color="gray"
        )
        self.name_entry.pack()

        # Поле для хоста
        self.host_entry = CTkEntry(
            self, 
            placeholder_text='Host', 
            height=45,
            width=300,
            font=('Orbitron', 14, 'bold'),
            fg_color=input_bg,
            border_color=cyan_accent,
            text_color=text_white,
            placeholder_text_color="gray"
        )
        self.host_entry.pack(pady=15)

        # Поле для порту
        self.port_entry = CTkEntry(
            self, 
            placeholder_text='Port', 
            height=45,
            width=300,
            font=('Orbitron', 14, 'bold'),
            fg_color=input_bg,
            border_color=cyan_accent,
            text_color=text_white,
            placeholder_text_color="gray"
        )
        self.port_entry.pack()

        # Кнопка в стилі "Грати" з картинки
        CTkButton(
            self, 
            text='Join', 
            command=self.open_game, 
            height=50,
            width=300,
            font=("Orbitron", 30, 'bold'),   # Великий білий текст
            fg_color=btn_fill,            # Бірюзова заливка
            border_width=2,               # Тонка яскрава рамка
            border_color=cyan_accent,     # Колір рамки
            text_color=text_white,        # Білий текст
            hover_color=btn_hover,        # Колір при наведенні
            corner_radius=10              # Закруглені кути, як на фото
        ).pack(pady=30)

    def open_game(self):
        self.name = self.name_entry.get()
        self.host = self.host_entry.get()
        
        # Перевірка, щоб програма не вилітала при неправильному порті
        try:
            self.port = int(self.port_entry.get())
        except ValueError:
            self.port = 0 
            print("Увага: Порт має бути числом!")
            
        self.destroy()
    