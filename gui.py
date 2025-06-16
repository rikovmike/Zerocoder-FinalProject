# gui.py
import os
import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk

class GameGUI:
    def __init__(self, root, game_logic):
        self.root = root
        self.game = game_logic
        
        # Настройки окна
        self.root.title("Кто хочет стать миллионером")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Шрифты
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.question_font = font.Font(family="Helvetica", size=18)
        self.answer_font = font.Font(family="Helvetica", size=14)
        self.prize_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Элементы интерфейса
        self.bg_image = None
        self.bg_photo = None
        self.answer_buttons = []
        self.prize_labels = []
        
        self.create_main_menu()

    def create_main_menu(self):
        """Создание главного меню"""
        self.clear_window()
        
        # Фоновое изображение
        if os.path.exists("images/main_bg.jpg"):
            self.bg_image = Image.open("images/main_bg.jpg").resize((1000, 700), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            tk.Label(self.root, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
        
        # Заголовок и кнопки
        tk.Label(self.root, text="Кто хочет стать миллионером",
                font=self.title_font, bg="black", fg="gold").pack(pady=50)
        
        tk.Button(self.root, text="Играть", font=self.question_font,
                 command=self.start_game, bg="gold", fg="black",
                 width=20, height=2).pack(pady=20)
        
        tk.Button(self.root, text="Выход", font=self.question_font,
                 command=self.root.quit, bg="red", fg="white",
                 width=20, height=2).pack(pady=20)
        


    def start_game(self):
        """Начало новой игры"""
        self.game.reset_game()
        self.show_question()



    def show_question(self):
        """Отображение текущего вопроса"""

        self.clear_window()
        question = self.game.get_current_question()

        # Настройка grid
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Левая панель (вопросы)
        left_frame = tk.Frame(self.root, bg="black")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Правая панель (призы)
        right_frame = tk.Frame(self.root, bg="black")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Вопрос
        tk.Label(left_frame, text=question["question"],
                font=self.question_font, bg="black", fg="white",
                wraplength=600, justify=tk.CENTER).grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Ответы
        answers_frame = tk.Frame(left_frame, bg="black")
        answers_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=10)

        # Настройка пропорций сетки
        answers_frame.grid_rowconfigure(0, weight=1)  # Первая строка
        answers_frame.grid_rowconfigure(1, weight=1)  # Вторая строка
        answers_frame.grid_columnconfigure(0, weight=1)  # Первая колонка
        answers_frame.grid_columnconfigure(1, weight=1)  # Вторая колонка

        self.answer_buttons = []
        for i, answer in enumerate(question["answers"]):
            btn = tk.Button(answers_frame, text=answer, font=self.answer_font,
                           command=lambda idx=i: self.check_answer(idx),
                           bg="navy", fg="white", height=2, wraplength=300)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            self.answer_buttons.append(btn)

        hints_frame = tk.Frame(left_frame, bg="black")
        hints_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        tk.Button(hints_frame, text="50/50", font=self.answer_font,
                  command=self.use_fifty_fifty, bg="darkgreen" if not self.game.used_hints["50_50"] else "gray" , fg="white",
                  state=tk.NORMAL if not self.game.used_hints["50_50"] else tk.DISABLED
                  ).pack(side=tk.LEFT, padx=10, expand=True)

        tk.Button(hints_frame, text="Звонок другу", font=self.answer_font,
                  command=self.use_call_friend, bg="darkgreen" if not self.game.used_hints["call_friend"] else "gray" , fg="white",
                  state=tk.NORMAL if not self.game.used_hints["call_friend"] else tk.DISABLED
                  ).pack(side=tk.LEFT, padx=10, expand=True)

        tk.Button(hints_frame, text="Помощь зала", font=self.answer_font,
                  command=self.use_audience_help, bg="darkgreen" if not self.game.used_hints["audience_help"] else "gray" , fg="white",
                  state=tk.NORMAL if not self.game.used_hints["audience_help"] else tk.DISABLED
                  ).pack(side=tk.LEFT, padx=10, expand=True)
        
        # Шкала призов
        self.create_prize_scale(right_frame)

    def create_prize_scale(self, parent):
        """Создание шкалы призов"""
        tk.Label(parent, text="Шкала выигрышей", font=self.answer_font,
                bg="black", fg="gold").grid(row=0, column=0, sticky="ew", pady=10)
        
        levels_frame = tk.Frame(parent, bg="black")
        levels_frame.grid(row=1, column=0, sticky="nsew")
        
        self.prize_labels = []
        for i, prize in enumerate(reversed(self.game.prize_levels)):
            pos = len(self.game.prize_levels) - self.game.current_question_index - 1
            bg = "gold" if i == pos else "darkgreen" if i > pos else "navy"
            fg = "black" if bg == "gold" else "white"
            
            text = f"{prize} ₽ {'(несгораемая)' if i in [len(self.game.prize_levels)-idx-1 for idx in self.game.safe_levels] else ''}"
            
            label = tk.Label(levels_frame, text=text, font=self.prize_font,
                            bg=bg, fg=fg, width=18)
            label.grid(row=i, column=0, sticky="nsew", padx=5, pady=1)
            self.prize_labels.append(label)

    def check_answer(self, answer_index):
        """Обработка ответа игрока"""
        if self.game.check_answer(answer_index):

            if self.game.current_question_index >= len(self.game.prize_levels):
                self.show_win_screen()
            else:
                self.show_question()
        else:

            self.show_lose_screen()

    def show_lose_screen(self):
        """Экран проигрыша"""
        self.clear_window()

        # Определяем последнюю несгораемую сумму
        prize = 0
        for level in reversed(range(self.game.current_question_index)):
            if level in self.game.safe_levels:
                prize = self.game.prize_levels[level]
                break

        message = f"К сожалению, это неправильный ответ.\n\nВаш выигрыш: {prize} ₽\n\nХотите сыграть ещё раз?"
        message_label = tk.Label(self.root, text=message,
                                 font=self.question_font, bg="black", fg="gold",
                                 wraplength=600)
        message_label.pack(pady=100)



        # Кнопки
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Играть снова", font=self.answer_font,
                  command=self.start_game, bg="gold", fg="black",
                  width=15, height=2).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Выход", font=self.answer_font,
                  command=self.root.quit, bg="red", fg="white",
                  width=15, height=2).pack(side=tk.LEFT, padx=10)

    def show_win_screen(self):
        """Экран победы"""
        self.clear_window()

        message = "Поздравляем! Вы выиграли 1,000,000 ₽!\n\nХотите сыграть ещё раз?"
        message_label = tk.Label(self.root, text=message,
                                 font=self.question_font, bg="black", fg="gold",
                                 wraplength=600)
        message_label.pack(pady=100)



        # Кнопки
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Играть снова", font=self.answer_font,
                  command=self.start_game, bg="gold", fg="black",
                  width=15, height=2).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Выход", font=self.answer_font,
                  command=self.root.quit, bg="red", fg="white",
                  width=15, height=2).pack(side=tk.LEFT, padx=10)

    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def use_fifty_fifty(self):
        """Обработка подсказки 50/50"""

        to_remove = self.game.get_fifty_fifty_options()
        for idx in to_remove:
            self.answer_buttons[idx].config(state=tk.DISABLED, bg="gray")

    def use_call_friend(self):
        """Обработка подсказки 'Звонок другу'"""

        answer_idx = self.game.get_call_friend_answer()
        if answer_idx is not None:
            answer = self.game.get_current_question()["answers"][answer_idx]
            messagebox.showinfo("Звонок другу", f"Друг думает, что правильный ответ: {answer}")

    def use_audience_help(self):
        """Обработка подсказки 'Помощь зала'"""

        percentages = self.game.get_audience_help()
        if percentages:
            help_window = tk.Toplevel(self.root)
            help_window.title("Помощь зала")
            help_window.geometry("400x300")

            for i, (answer, percent) in enumerate(zip(self.game.get_current_question()["answers"], percentages)):
                frame = tk.Frame(help_window)
                frame.pack(fill=tk.X, padx=10, pady=5)

                tk.Label(frame, text=answer, width=20, anchor=tk.W).pack(side=tk.LEFT)

                canvas = tk.Canvas(frame, height=20, width=200, bg="white")
                canvas.pack(side=tk.LEFT)
                canvas.create_rectangle(0, 0, 2 * percent, 20, fill="blue")

                tk.Label(frame, text=f"{percent}%").pack(side=tk.LEFT, padx=5)