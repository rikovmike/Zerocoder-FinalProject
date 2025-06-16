# game_logic.py
import json
import random
import os
from datetime import datetime


class GameLogic:
    def __init__(self):

        # Используем текущее время в микросекундах для seed
        random.seed(datetime.now().microsecond)
        self.shuffled_questions = {
            "easy": [],
            "medium": [],
            "hard": []
        }

        self.current_question_index = 0
        self.score = 0
        self.used_hints = {
            "50_50": False,
            "call_friend": False,
            "audience_help": False
        }


        self.prize_levels = [
            500, 1000, 2000, 5000, 10000,
            20000, 40000, 80000, 160000, 250000,
            500000, 1000000
        ]
        self.safe_levels = [4, 9]
        

        self.load_questions()


        self.current_sound = None  # Для хранения текущего воспроизводимого звука


    def load_questions(self):
        """Загрузка вопросов из JSON файла"""
        try:
            """Загрузка и перемешивание вопросов при каждом запуске"""
            with open('questions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                questions = data["questions"]

                # Перемешиваем вопросы для каждого уровня сложности
                for level in questions:
                    questions_list = questions[level].copy()
                    random.shuffle(questions_list)
                    self.shuffled_questions[level] = questions_list

        except FileNotFoundError:
            self.questions = {
                "easy": [
                    {
                        "question": "Какая планета известна как Красная планета?",
                        "answers": ["Венера", "Марс", "Юпитер", "Сатурн"],
                        "correct": 1
                    },
                    # ... другие вопросы ...
                ],
                # ... другие уровни ...
            }
            self.save_sample_questions()

    def save_sample_questions(self):
        """Сохранение примеров вопросов"""
        data = {"questions": self.questions}
        with open('questions.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)



    def get_current_question(self):
        """Получение текущего вопроса"""
        level = "easy" if self.current_question_index < 5 else "medium" if self.current_question_index < 10 else "hard"

        question_data = self.shuffled_questions[level][
            self.current_question_index % len(self.shuffled_questions[level])
        ]
        return question_data

    def check_answer(self, answer_index):
        """Проверка ответа игрока"""
        question = self.get_current_question()
        if answer_index == question["correct"]:
            self.score = self.prize_levels[self.current_question_index]
            self.current_question_index += 1
            return True
        return False
    def get_fifty_fifty_options(self):
        """Возвращает индексы двух неверных ответов для подсказки 50/50"""
        if self.used_hints["50_50"]:
            return []
        self.used_hints["50_50"] = True
        question = self.get_current_question()
        wrong_answers = [i for i in range(4) if i != question["correct"]]
        return random.sample(wrong_answers, 2)

    def get_call_friend_answer(self):
        """Возвращает ответ для подсказки 'Звонок другу'"""
        if self.used_hints["call_friend"]:
            return None
        self.used_hints["call_friend"] = True
        question = self.get_current_question()
        if random.random() < 0.8:
            return question["correct"]
        return random.randint(0, 3)

    def get_audience_help(self):
        """Возвращает проценты для подсказки 'Помощь зала'"""
        if self.used_hints["audience_help"]:
            return None
        self.used_hints["audience_help"] = True
        question = self.get_current_question()
        percentages = [random.randint(5, 30) for _ in range(4)]
        percentages[question["correct"]] += random.randint(30, 60)
        total = sum(percentages)
        return [int(p * 100 / total) for p in percentages]

    def reset_game(self):
        """Сброс состояния игры"""
        self.current_question_index = 0
        self.score = 0
        self.used_hints = {
            "50_50": False,
            "call_friend": False,
            "audience_help": False
        }

        for level in self.shuffled_questions:
            random.shuffle(self.shuffled_questions[level])
