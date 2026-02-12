import asyncio
import subprocess
from googletrans import Translator
from pynput import mouse
import tkinter as tk
from tkinter import scrolledtext
import os
import shutil


def get_clipboard():
    try:
        if os.environ.get('XDG_SESSION_TYPE') == 'wayland':
            return subprocess.check_output(["wl-paste"], text=True, timeout=1).strip()
        return subprocess.check_output(["xclip", "-selection", "clipboard", "-o"], text=True, timeout=1).strip()
    except Exception as e:
        return f"Ошибка: {e}"

def check_clipboard_utility():
    try:
        if os.environ.get('XDG_SESSION_TYPE') == 'wayland':
            return shutil.which("wl-paste")
        return shutil.which("xclip")
    except Exception as e:
        return f"Ошибка: {e}"
    
def show_translated_text(text: str):
    m = mouse.Controller()
    # position[0] - это X, position[1] - это Y
    x, y = m.position
    
    root = tk.Tk()
    root.title("Перевод")

    # Сначала X, потом Y. Добавляем +10 пикселей, чтобы курсор не "давил" на окно
    root.geometry(f"+{x+10}+{y+10}")
   
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    text_area.insert(tk.INSERT, text)
    text_area.pack()

    root.bind_all("<Escape>", lambda e: root.destroy())    
    # root.bind("", lambda e: root.destroy())
    root.mainloop()

async def translate(text: str):
    translator = Translator()
    translation = await translator.translate(text, dest='ru')
    return translation.text

if __name__ == "__main__":
    check_clipboard_utility()
    result = asyncio.run(translate(get_clipboard()))
    show_translated_text(result)
        

