from tkinter import *
import random
import time

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
countdown_after_id = None

start_time = 0
end_time = 0


def normalize_text(s):
    return " ".join(s.strip().split()).lower()


# ✨ 單字淡入動畫
def fade_in_text(text):
    colors = ["#bbbbbb", "#888888", "#555555", "#222222", "#000000"]

    def step(i):
        if i < len(colors):
            test.config(text=text, fg=colors[i])
            root.after(60, step, i + 1)

    step(0)


def random_word():
    global word
    if difficulty:
        word = random.choice(word_banks[difficulty])
        fade_in_text(word)
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
    global current_round, total_rounds, score, start_time

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

    start_time = time.time()  # 記錄開始時間

    run_round(current_round)


def run_round(r):
    global current_round, countdown_after_id, end_time

    if r > total_rounds:
        end_time = time.time()

        elapsed = end_time - start_time
        wpm = (score / elapsed) * 60

        test.config(text="🎉 Game Over")

        show_result_animation(score, total_rounds, wpm)
        Time.config(text="")
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

        # ⏱ 顏色動畫
        if sec < 3:
            Time.config(fg="red")
        elif sec < 6:
            Time.config(fg="orange")
        else:
            Time.config(fg="black")

        Time.config(text=f"{sec:.1f}")

        countdown_after_id = root.after(100, countdown, sec - 0.1)

    countdown(t)


def check_input(event=None):
    global score, current_round, countdown_after_id

    user_input = entryword.get()

    if normalize_text(user_input) == normalize_text(word):

        result_label.config(text="✅ Correct!", fg="green")
        score += 1

        if countdown_after_id is not None:
            root.after_cancel(countdown_after_id)

        run_round(current_round + 1)

    else:
        result_label.config(text="❌ Wrong", fg="red")


# 🎉 結算動畫
def show_result_animation(score, total, wpm):

    text = f"Final Score: {score}/{total}\nWPM: {wpm:.1f}"

    size = 10

    def grow():
        nonlocal size
        if size < 28:
            final_score_label.config(text=text, font=("Arial", size))
            size += 1
            root.after(30, grow)

    grow()


root = Tk()
root.title("Speed Typing Game")
root.geometry("800x700")
root.configure(bg="#f0f0f0")

Label(root, text="Speed Typing Game", font=("Arial", 22, "bold")).pack(pady=10)

round_frame = Frame(root, bg="#f0f0f0")
round_frame.pack(pady=10)

Label(round_frame, text="Rounds:", font=("Arial", 14)).pack(side="left")

entryround = Entry(round_frame, font=("Arial", 14))
entryround.pack(side="left")

button_frame = Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

Button(button_frame, text="Normal", font=("Arial", 14), command=Normal).pack(side="left", padx=10)
Button(button_frame, text="Hard", font=("Arial", 14), command=Hard).pack(side="left", padx=10)
Button(button_frame, text="Nightmare", font=("Arial", 14), command=Nightmare).pack(side="left", padx=10)

Button(root, text="Start Game", font=("Arial", 14), command=Timer).pack(pady=10)

test = Label(root, text="", font=("Arial", 22))
test.pack(pady=20)

Time = Label(root, text="", font=("Arial", 20))
Time.pack()

entryword = Entry(root, font=("Arial", 16))
entryword.pack(pady=10)
entryword.bind("<Return>", check_input)

result_label = Label(root, text="", font=("Arial", 16))
result_label.pack(pady=10)

final_score_label = Label(root, text="", font=("Arial", 16))
final_score_label.pack(pady=20)

root.mainloop()