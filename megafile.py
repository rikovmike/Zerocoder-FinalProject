import json
import random
import os
import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import winsound


class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Кто хочет стать миллионером")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)


        # Инициализация игровых переменных
        self.current_question_index = 0
        self.score = 0
        self.used_hints = {
            "50_50": False,
            "call_friend": False,
            "audience_help": False
        }

        self.sounds = {
            "correct": "sounds/correct.wav",
            "wrong": "sounds/wrong.wav",
            "win": "sounds/win.wav",
            "lose": "sounds/lose.wav",
            "hint": "sounds/hint.wav",
            "music": "sounds/music.wav"
        }

        # Шкала выигрышей
        self.prize_levels = [
            500, 1000, 2000, 5000, 10000,  # Несгораемая сумма 5,000
            20000, 40000, 80000, 160000, 250000,  # Несгораемая сумма 250,000
            500000, 1000000
        ]
        self.safe_levels = [4, 9]  # Индексы несгораемых сумм

        # Загрузка вопросов
        self.load_questions()

        # Настройка шрифтов
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.question_font = font.Font(family="Helvetica", size=18)
        self.answer_font = font.Font(family="Helvetica", size=14)
        self.prize_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Создание интерфейса
        self.create_main_menu()

        # Загрузка звуков
        self.load_sounds()




    def load_questions(self):
        """Загрузка вопросов из JSON файла"""
        try:
            with open('questions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.questions = data["questions"]
                # Перемешиваем вопросы, но сохраняем порядок сложности
                for level in self.questions:
                    random.shuffle(self.questions[level])
        except FileNotFoundError:
            # Пример вопросов по умолчанию
            self.questions = {
                "easy": [
                    {
                        "question": "Какая планета известна как Красная планета?",
                        "answers": ["Венера", "Марс", "Юпитер", "Сатурн"],
                        "correct": 1
                    },
                    # ... другие вопросы ...
                ],
                "medium": [
                    # ... вопросы средней сложности ...
                ],
                "hard": [
                    # ... сложные вопросы ...
                ]
            }
            self.save_sample_questions()

    def save_sample_questions(self):
        """Сохранение примеров вопросов в JSON файл"""
        data = {
            "questions": {
                "easy": [
                    {
                        "question": "Какая планета известна как Красная планета?",
                        "answers": ["Венера", "Марс", "Юпитер", "Сатурн"],
                        "correct": 1
                    },
                    {
                        "question": "Какой газ наиболее распространен в атмосфере Земли?",
                        "answers": ["Кислород", "Азот", "Углекислый газ", "Водород"],
                        "correct": 1
                    }
                ],
                "medium": [
                    {
                        "question": "Кто написал роман 'Преступление и наказание'?",
                        "answers": ["Лев Толстой", "Федор Достоевский", "Антон Чехов", "Иван Тургенев"],
                        "correct": 1
                    }
                ],
                "hard": [
                    {
                        "question": "Какой химический элемент обозначается символом 'Au'?",
                        "answers": ["Серебро", "Алюминий", "Золото", "Аргон"],
                        "correct": 2
                    }
                ]
            }
        }
        with open('questions.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_sounds(self):
        """Инициализация звуков"""

        # Проверка существования звуковых файлов
        for sound in self.sounds.values():
            if not os.path.exists(sound):
                print(f"Предупреждение: звуковой файл {sound} не найден")

    def play_sound(self, sound_name):
        """Воспроизведение звука"""
        if not self.config.get("sounds", True):
            return

        if sound_name in self.sounds:
            try:
                winsound.PlaySound(self.sounds[sound_name], winsound.SND_ASYNC)
            except Exception as e:
                print(f"Ошибка воспроизведения звука {sound_name}: {e}")
        else:
            print(f"Звук {sound_name} не доступен")

    def create_main_menu(self):
        """Создание главного меню"""
        self.clear_window()

        # Фоновое изображение
        self.bg_image = Image.open("images/main_bg.jpg") if os.path.exists("images/main_bg.jpg") else None
        if self.bg_image:
            self.bg_image = self.bg_image.resize((1000, 700), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Заголовок
        title_label = tk.Label(self.root, text="Кто хочет стать миллионером",
                               font=self.title_font, bg="black", fg="gold")
        title_label.pack(pady=50)

        # Кнопка "Играть"
        play_btn = tk.Button(self.root, text="Играть", font=self.question_font,
                             command=self.start_game, bg="gold", fg="black",
                             width=20, height=2)
        play_btn.pack(pady=20)

        # Кнопка "Выход"
        exit_btn = tk.Button(self.root, text="Выход", font=self.question_font,
                             command=self.root.quit, bg="red", fg="white",
                             width=20, height=2)
        exit_btn.pack(pady=20)

        # Воспроизведение фоновой музыки
        if self.config["music"]:
            self.play_sound("music")

    def start_game(self):
        """Начало новой игры"""
        self.current_question_index = 0
        self.score = 0
        self.used_hints = {
            "50_50": False,
            "call_friend": False,
            "audience_help": False
        }
        self.show_question()

    def show_question(self):
        """Отображение текущего вопроса с использованием grid layout"""
        self.clear_window()

        # Определяем уровень сложности
        level = "easy" if self.current_question_index < 5 else "medium" if self.current_question_index < 10 else "hard"

        # Получаем текущий вопрос
        question_data = self.questions[level][self.current_question_index % len(self.questions[level])]
        self.current_question = question_data["question"]
        self.current_answers = question_data["answers"]
        self.correct_answer = question_data["correct"]

        # Настройка grid
        self.root.grid_columnconfigure(0, weight=2)  # 2/3 для основной панели
        self.root.grid_columnconfigure(1, weight=1)  # 1/3 для шкалы призов
        self.root.grid_rowconfigure(0, weight=1)

        # Основная панель (левая)
        left_frame = tk.Frame(self.root, bg="black")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Шкала призов (правая)
        right_frame = tk.Frame(self.root, bg="black")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Настройка grid для левой панели
        left_frame.grid_rowconfigure(0, weight=1)  # Вопрос
        left_frame.grid_rowconfigure(1, weight=3)  # Ответы
        left_frame.grid_rowconfigure(2, weight=1)  # Подсказки
        left_frame.grid_columnconfigure(0, weight=1)

        # Вопрос
        question_label = tk.Label(left_frame, text=self.current_question,
                                  font=self.question_font, bg="black", fg="white",
                                  wraplength=600, justify=tk.CENTER)
        question_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Ответы
        answers_frame = tk.Frame(left_frame, bg="black")
        answers_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=10)

        # Настройка grid для ответов
        for i in range(2):
            answers_frame.grid_rowconfigure(i, weight=1)
            answers_frame.grid_columnconfigure(i, weight=1)

        self.answer_buttons = []
        for i, answer in enumerate(self.current_answers):
            btn = tk.Button(answers_frame, text=answer, font=self.answer_font,
                            command=lambda idx=i: self.check_answer(idx),
                            bg="navy", fg="white", height=2, wraplength=300)
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")
            self.answer_buttons.append(btn)

        # Подсказки
        hints_frame = tk.Frame(left_frame, bg="black")
        hints_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        # Создаем кнопки подсказок с правильными названиями методов
        hint_buttons = [
            ("50_50", "50/50", self.use_fifty_fifty),
            ("call_friend", "Звонок другу", self.use_call_friend),
            ("audience_help", "Помощь зала", self.use_audience_help)
        ]

        for hint, text, command in hint_buttons:
            btn = tk.Button(hints_frame, text=text, font=self.answer_font,
                            command=command,
                            bg="darkgreen", fg="white",
                            state=tk.NORMAL if not self.used_hints[hint] else tk.DISABLED)
            btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        # Шкала призов (правая панель)
        self.create_prize_scale(right_frame)

    def create_prize_scale(self, parent):
        """Создание шкалы призов с использованием grid"""
        parent.grid_rowconfigure(0, weight=0)  # Заголовок
        parent.grid_rowconfigure(1, weight=1)  # Уровни призов

        # Заголовок
        tk.Label(parent, text="Шкала выигрышей", font=self.answer_font,
                 bg="black", fg="gold").grid(row=0, column=0, sticky="ew", pady=10)

        # Фрейм для уровней призов
        levels_frame = tk.Frame(parent, bg="black")
        levels_frame.grid(row=1, column=0, sticky="nsew")

        # Распределяем пространство равномерно
        levels_count = len(self.prize_levels)
        for i in range(levels_count):
            levels_frame.grid_rowconfigure(i, weight=1)
        levels_frame.grid_columnconfigure(0, weight=1)

        self.prize_labels = []
        for i, prize in enumerate(reversed(self.prize_levels)):
            # Определяем цвет
            pos = len(self.prize_levels) - self.current_question_index - 1
            if i == pos:
                bg, fg = "gold", "black"  # Текущий уровень
            elif i > pos:
                bg, fg = "darkgreen", "white"  # Пройденные уровни
            else:
                bg, fg = "navy", "white"  # Будущие уровни

            # Несгораемые суммы
            text = f"{prize} ₽ {'(несгораемая)' if i in [len(self.prize_levels) - idx - 1 for idx in self.safe_levels] else ''}"

            label = tk.Label(levels_frame, text=text, font=self.prize_font,
                             bg=bg, fg=fg, width=18)
            label.grid(row=i, column=0, sticky="nsew", padx=5, pady=1)
            self.prize_labels.append(label)

    def check_answer(self, answer_index):
        """Проверка выбранного ответа"""
        if answer_index == self.correct_answer:
            # Правильный ответ
            self.play_sound("correct")
            self.score = self.prize_levels[self.current_question_index]
            self.current_question_index += 1

            if self.current_question_index >= len(self.prize_levels):
                # Игрок ответил на все вопросы
                self.show_win_screen()
            else:
                # Сразу переходим к следующему вопросу
                self.show_question()
        else:
            # Неправильный ответ
            self.play_sound("wrong")
            self.show_lose_screen()

    def show_next_question_screen(self):
        """Показ экрана перехода к следующему вопросу"""
        self.clear_window()

        # Проверяем, достигли ли мы несгораемой суммы
        is_safe_level = (self.current_question_index - 1) in self.safe_levels

        # Сообщение
        message = f"Правильно! Ваш текущий выигрыш: {self.score} ₽"
        if is_safe_level:
            message += "\n\nВы достигли несгораемой суммы!"

        message_label = tk.Label(self.root, text=message, font=self.question_font,
                                 bg="black", fg="gold", wraplength=600)
        message_label.pack(pady=100)

        # Кнопка продолжения
        next_btn = tk.Button(self.root, text="Следующий вопрос", font=self.answer_font,
                             command=self.show_question, bg="gold", fg="black",
                             width=20, height=2)
        next_btn.pack(pady=20)

        # Шкала выигрышей
        self.create_prize_scale(self.root)

    def show_win_screen(self):
        """Показ экрана победы"""
        self.clear_window()

        message = f"Поздравляем! Вы выиграли 1,000,000 ₽!\n\nХотите сыграть еще раз?"
        message_label = tk.Label(self.root, text=message, font=self.question_font,
                                 bg="black", fg="gold", wraplength=600)
        message_label.pack(pady=100)

        self.play_sound("win")

        # Кнопки
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=20)

        play_again_btn = tk.Button(btn_frame, text="Играть снова", font=self.answer_font,
                                   command=self.start_game, bg="gold", fg="black",
                                   width=15, height=2)
        play_again_btn.pack(side=tk.LEFT, padx=10)

        exit_btn = tk.Button(btn_frame, text="Выход", font=self.answer_font,
                             command=self.root.quit, bg="red", fg="white",
                             width=15, height=2)
        exit_btn.pack(side=tk.LEFT, padx=10)

    def show_lose_screen(self):
        """Показ экрана проигрыша"""
        self.clear_window()

        # Определяем выигрыш (последняя несгораемая сумма)
        prize = 0
        for level in reversed(range(self.current_question_index)):
            if level in self.safe_levels:
                prize = self.prize_levels[level]
                break

        message = f"К сожалению, это неправильный ответ.\n\nВаш выигрыш: {prize} ₽\n\nХотите сыграть еще раз?"
        message_label = tk.Label(self.root, text=message, font=self.question_font,
                                 bg="black", fg="gold", wraplength=600)
        message_label.pack(pady=100)

        self.play_sound("lose")

        # Кнопки
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=20)

        play_again_btn = tk.Button(btn_frame, text="Играть снова", font=self.answer_font,
                                   command=self.start_game, bg="gold", fg="black",
                                   width=15, height=2)
        play_again_btn.pack(side=tk.LEFT, padx=10)

        exit_btn = tk.Button(btn_frame, text="Выход", font=self.answer_font,
                             command=self.root.quit, bg="red", fg="white",
                             width=15, height=2)
        exit_btn.pack(side=tk.LEFT, padx=10)

    def use_fifty_fifty(self):
        """Использование подсказки 50/50"""
        self.play_sound("hint")
        self.used_hints["50_50"] = True

        # Находим два неверных ответа (кроме правильного)
        wrong_answers = [i for i in range(4) if i != self.correct_answer]
        to_remove = random.sample(wrong_answers, 2)

        # Отключаем выбранные неверные ответы
        for idx in to_remove:
            self.answer_buttons[idx].config(state=tk.DISABLED, bg="gray")

    def use_call_friend(self):
        """Использование подсказки 'Звонок другу'"""
        self.play_sound("hint")
        self.used_hints["call_friend"] = True

        # 80% шанс на правильный ответ
        if random.random() < 0.8:
            answer = self.current_answers[self.correct_answer]
            message = f"Друг думает, что правильный ответ: {answer}"
        else:
            # Выбираем случайный ответ (может быть правильным)
            idx = random.randint(0, 3)
            answer = self.current_answers[idx]
            message = f"Друг думает, что правильный ответ: {answer}"

        # Показываем сообщение
        messagebox.showinfo("Звонок другу", message)

    def use_audience_help(self):
        """Использование подсказки 'Помощь зала'"""
        self.play_sound("hint")
        self.used_hints["audience_help"] = True

        # Создаем окно с результатами голосования
        help_window = tk.Toplevel(self.root)
        help_window.title("Помощь зала")
        help_window.geometry("400x300")
        help_window.resizable(False, False)

        # Генерируем псевдослучайные проценты с уклоном к правильному ответу
        percentages = [random.randint(5, 30) for _ in range(4)]
        percentages[self.correct_answer] += random.randint(30, 60)
        total = sum(percentages)
        percentages = [int(p * 100 / total) for p in percentages]

        # Корректируем, чтобы сумма была 100%
        diff = 100 - sum(percentages)
        if diff != 0:
            percentages[self.correct_answer] += diff

        # Отображаем гистограмму
        for i, (answer, percent) in enumerate(zip(self.current_answers, percentages)):
            frame = tk.Frame(help_window)
            frame.pack(fill=tk.X, padx=10, pady=5)

            label = tk.Label(frame, text=answer, width=20, anchor=tk.W)
            label.pack(side=tk.LEFT)

            canvas = tk.Canvas(frame, height=20, width=200, bg="white")
            canvas.pack(side=tk.LEFT)

            width = 2 * percent
            canvas.create_rectangle(0, 0, width, 20, fill="blue")

            percent_label = tk.Label(frame, text=f"{percent}%")
            percent_label.pack(side=tk.LEFT, padx=5)

    def clear_window(self):
        """Очистка окна от всех виджетов"""
        for widget in self.root.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    game = MillionaireGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()