# main.py
import tkinter as tk
from game_logic import GameLogic
from gui import GameGUI

def main():
    root = tk.Tk()
    game_logic = GameLogic()
    game_gui = GameGUI(root, game_logic)
    root.mainloop()

if __name__ == "__main__":
    main()
