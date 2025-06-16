# Кто хочет стать миллионером? 🎮💰

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Полноценная реализация игры "Кто хочет стать миллионером" на Python с графическим интерфейсом. Идеальный проект для обучения Python и создания викторин.

## 🌟 Особенности

- 🎨 **Интерфейс** на Tkinter и минимум зависимостей
- 💡 **3 вида подсказок**: 50/50, Звонок другу, Помощь зала
- 📊 **Шкала выигрышей** с несгораемыми суммами
- 📝 **Множество вопросов** разного уровня сложности, в зависимости от несгораемой суммы
- 🔄 **Случайный порядок вопросов** при каждом запуске

## 🛠 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/rikovmike/Zerocoder-FinalProject.git
cd Zerocoder-FinalProject
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```


## 🚀 Запуск игры
```bash
python main.py
```

📂 Структура проекта
```text
millionaire-game/
├── questions.json   # База вопросов (1000+ вопросов)
├── config.json      # Настройки игры
├── main.py          # Точка входа
├── game_logic.py    # Логика игры
├── gui.py           # Графический интерфейс
```


## 💾 Формат вопросов

Файл questions.json содержит вопросы в формате:

```json
{
  "questions": {
    "easy": [
      {
        "question": "Текст вопроса",
        "answers": ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
        "correct": 0
      }
    ],
    "medium": [...],
    "hard": [...]
  }
}
```