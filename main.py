from tkinter import *
import random

word_banks = {
    'Normal': ["apple", "banana", "keyboard"],
    'Hard': ["binary search", "linked list", "cloud storage"],
    'Nightmare': ["Practice makes perfect", "Accuracy is more import than speed"]
}

difficulty = ""
word = ""
current_round = 0
total_rounds = 0
score = 0
countdown_after_id = None  # 用來取消倒數計時

def normalize_text(s):
    """去除多餘空格並忽略大小寫"""
    return " ".join(s.strip().split()).lower()

def random_word():
    global word
    if difficulty:
        word = random.choice(word_banks[difficulty])
        test.config(text=word)
        entryword.delete(0, END)
        result_label.config(text="")

def Normal():
    global difficulty
    difficulty = 'Normal'
    Time.config(text="")
    random_word()

def Hard():
    global difficulty
    difficulty = 'Hard'
    Time.config(text="")
    random_word()

def Nightmare():
    global difficulty
    difficulty = 'Nightmare'
    Time.config(text="")
    random_word()

def Timer():
    global current_round, total_rounds, score
    if not difficulty:
        Time.config(text="請先選難度")
        return

    try:
        total_rounds = int(entryround.get())
    except:
        Time.config(text="請輸入數字")
        return

    current_round = 1
    score = 0
    final_score_label.config(text="")
    run_round(current_round)

def run_round(r):
    global current_round, countdown_after_id
    if r > total_rounds:
        test.config(text="遊戲結束")
        Time.config(text="")
        final_score_label.config(text=f"Final Score: {score}/{total_rounds} ({score/total_rounds*100:.0f}%)")
        return

    current_round = r
    random_word()
    t = 10 if difficulty in ["Normal", "Hard"] else 15
    t = float(t)

    def countdown(sec):
        global countdown_after_id
        if sec < 0:
            run_round(current_round + 1)
            return
        Time.config(text=f"{sec:.1f}")
        countdown_after_id = root.after(100, countdown, sec - 0.1)

    countdown(t)

def check_input(event=None):
    global score, current_round, countdown_after_id
    user_input = entryword.get()
    if normalize_text(user_input) == normalize_text(word):
        result_label.config(text="✅ 正確", fg="green")
        score += 1
        # 正確立即取消目前倒數，進入下一輪
        if countdown_after_id is not None:
            root.after_cancel(countdown_after_id)
            countdown_after_id = None
        run_round(current_round + 1)
    else:
        result_label.config(text="❌ 錯誤", fg="red")

root = Tk()
root.title("打字遊戲")
root.geometry("800x700")

Label(root, text="Speed Typing Game", font=("Arial", 18)).pack(pady=10)

# Rounds
round_frame = Frame(root)
round_frame.pack(pady=10)
Label(round_frame, text="Rounds:", font=("Arial", 14)).pack(side="left")
entryround = Entry(round_frame, font=("Arial", 14))
entryround.pack(side="left")

# 難度按鈕
button_frame = Frame(root)
button_frame.pack(pady=10)
Button(button_frame, text="Normal", font=("Arial", 14), command=Normal).pack(side="left", padx=10)
Button(button_frame, text="Hard", font=("Arial", 14), command=Hard).pack(side="left", padx=10)
Button(button_frame, text="Nightmare", font=("Arial", 14), command=Nightmare).pack(side="left", padx=10)

# Start Game
Button(root, text="Start Game", font=("Arial", 14), command=Timer).pack(pady=10)

# 顯示單字
test = Label(root, text="", font=("Arial", 16))
test.pack(pady=20)

# 倒數時間
Time = Label(root, text="", font=("Arial", 16))
Time.pack()

# 使用者輸入單字
entryword = Entry(root, font=("Arial", 16))
entryword.pack(pady=10)
entryword.bind("<Return>", check_input)  # 按 Enter 檢查輸入

# 顯示結果（正確或錯誤）
result_label = Label(root, text="", font=("Arial", 16))
result_label.pack(pady=10)

# 顯示最後分數
final_score_label = Label(root, text="", font=("Arial", 16))
final_score_label.pack(pady=20)

root.mainloop()
