#!/usr/bin/env python
# coding: utf-8

# In[4]:


import json
import tkinter
from tkinter import *
import random

# Load questions and answer choices from json file
with open('./data.json', encoding="utf8") as f:
    data = json.load(f)

# Convert the dictionary into lists of questions and answers_choice 
questions = [v for v in data[0].values()]
answers_choice = [v for v in data[1].values()]
answers = [2, 1, 1, 3, 0, 3, 1, 3, 0, 3,   # Questions 1-10
           1, 1, 3, 1, 2, 2, 3, 0, 3, 3,   # Questions 11-20
           1, 1, 3, 1, 2, 2, 3, 0, 3, 3]   # Questions 21-30


user_answer = []
indexes = []
timer_label = None
time_remaining = 20  # seconds
timer_running = False  # Flag to track if the timer is running

def gen():
    global indexes
    while len(indexes) < 10:
        x = random.randint(0, 29)
        if x in indexes:
            continue
        else:
            indexes.append(x)

def showresult(score):
    lblQuestion.destroy()
    btn1.destroy()
    btn2.destroy()
    btn3.destroy()
    btn4.destroy()
    timer_label.destroy()
    labelimage = Label(
        root,
        background="#ffffff",
        border=0,
    )
    labelimage.pack(pady=(50, 30))
    labelresulttext = Label(
        root,
        font=("Consolas", 20),
        background="#99B7FF",
    )
    labelresulttext.pack()
    if score >= 90:
        img = PhotoImage(file="great.png")
        labelimage.configure(image=img)
        labelimage.image = img
        lblFeedback.config(text="")
        labelresulttext.configure(text=f"You Are Excellent !!\nYour Score: {score}")
    elif score >= 60 and score < 90:
        img = PhotoImage(file="ok.png")
        labelimage.configure(image=img)
        labelimage.image = img
        lblFeedback.config(text="")
        labelresulttext.configure(text=f"You Can Be Better !!\nYour Score: {score}")
    else:
        img = PhotoImage(file="bad.png")
        labelimage.configure(image=img)
        labelimage.image = img
        lblFeedback.destroy()
        labelresulttext.configure(text=f"You Should Work Hard !!\nYour Score: {score}")

def calc():
    global indexes, user_answer, answers
    x = 0
    score = 0
    for i in indexes:
        if user_answer[x] == answers[i]:
            score += 10
        x += 1
    showresult(score)

ques = 0
def selected(value):
    global user_answer, ques, time_remaining, timer_running
    global lblQuestion, btn1, btn2, btn3, btn4, lblFeedback
    user_answer.append(value)
    
    # Check if the answer is correct and display feedback
    if value == -1:
        lblFeedback.config(text="Not Attempted", fg="#FA4C06")
    elif value == answers[indexes[ques]]:
        lblFeedback.config(text="Correct!", fg="#008000")
    else:
        lblFeedback.config(text="Incorrect!", fg="#FF0000")
    
    lblFeedback.pack()
    
    # After a short delay, move to the next question
    ques += 1
    timer_running = False  # Stop the timer
    root.after(1500, show_next_question)  # 1.5 second delay

def show_next_question():
    global ques, time_remaining, timer_running
    if ques < 10:
        lblQuestion.config(text=questions[indexes[ques]])
        btn1['text'] = answers_choice[indexes[ques]][0]
        btn2['text'] = answers_choice[indexes[ques]][1]
        btn3['text'] = answers_choice[indexes[ques]][2]
        btn4['text'] = answers_choice[indexes[ques]][3]
        lblFeedback.config(text="")  # Clear feedback for the next question
        # Reset and start the timer
        time_remaining = 20
        timer_running = True
        update_timer()
    else:
        calc()

def update_timer():
    global time_remaining, timer_label, timer_running
    if timer_running:
        if time_remaining > 0:
            time_remaining -= 1
            timer_label.config(text=f"Time remaining: {time_remaining} seconds")
            timer_label.after(1000, update_timer)
        else:
            # Time is up, proceed to the next question
            selected(-1)  # Passing -1 to indicate time up

def startquiz():
    global lblQuestion, btn1, btn2, btn3, btn4, lblFeedback, timer_label
    lblQuestion = Label(
        root,
        text=questions[indexes[0]],
        font=("Consolas", 16),
        width=500,
        justify="center",
        wraplength=400,
        background="#99B7FF",
    )
    lblQuestion.pack(pady=(100, 30))

    btn1 = Button(
        root,
        text=answers_choice[indexes[0]][0],
        font=("Times", 12),
        bg="#000000",
        fg="#ffffff",
        width=25,
        justify="center",
        wraplength=170,
        command=lambda: selected(0),
    )
    btn1.pack(pady=10)

    btn2 = Button(
        root,
        text=answers_choice[indexes[0]][1],
        font=("Times", 12),
        bg="#000000",
        fg="#ffffff",
        width=25,
        justify="center",
        wraplength=170,
        command=lambda: selected(1),
    )
    btn2.pack(pady=20)

    btn3 = Button(
        root,
        text=answers_choice[indexes[0]][2],
        font=("Times", 12),
        bg="#000000",
        fg="#ffffff",
        width=25,
        justify="center",
        wraplength=170,
        command=lambda: selected(2),
    )
    btn3.pack(pady=10)

    btn4 = Button(
        root,
        text=answers_choice[indexes[0]][3],
        font=("Times", 12),
        bg="#000000",
        fg="#ffffff",
        width=25,
        justify="center",
        wraplength=170,
        command=lambda: selected(3),
    )
    btn4.pack(pady=10)

    lblFeedback = Label(
        root,
        text="",
        font=("Consolas", 14),
        background="#99B7FF",
    )
    lblFeedback.pack(pady=10)
    
    timer_label = Label(
        root,
        text="",
        font=("Consolas", 14),
        background="#99B7FF",
    )
    timer_label.pack(pady=10)
    
    # Delay the start of the timer to give the GUI time to render
    root.after(100, lambda: update_timer())

    # Start the timer for the first question
    global time_remaining, timer_running
    time_remaining = 20
    timer_running = True

def startIspressed():
    labelimage.destroy()
    labeltext.destroy()
    lblInstruction.destroy()
    lblRules.destroy()
    btnStart.destroy()
    gen()
    startquiz()

root = tkinter.Tk()
root.title("QuizMaster")
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
w = 700
h = 600
x=int(ws/2 - w/2)
y=int(hs/2 - h/2)
data = str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y)
root.geometry(data)
# root.geometry("700x600")
root.config(background="#99B7FF")
root.resizable(0, 0)

img1 = PhotoImage(file="transparentGradHat.png")

labelimage = Label(
    root,
    image=img1,
    background="#99B7FF"
)
labelimage.pack(pady=(40, 0))

labeltext = Label(
    root,
    text="Welcome to the QuizMaster !!!",
    font=("Comic sans MS", 24, "bold"),
    background="#99B7FF",
)
labeltext.pack(pady=(0, 50))

img2 = PhotoImage(file="Frame.png")

btnStart = Button(
    root,
    image=img2,
    relief=FLAT,
    border=0,
    command=startIspressed,
)
btnStart.pack()

lblInstruction = Label(
    root,
    text="Read The Rules And\nClick Start Once You Are ready",
    background="#99B7FF",
    font=("Consolas", 14),
    justify="center",
)
lblInstruction.pack(pady=(10, 100))

lblRules = Label(
    root,
    text="This quiz contains random 10 questions from set of 30 questions\nYou will get 20 seconds to solve a question\nOnce you select a button that will be a final choice\nhence think before you select",
    width=100,
    font=("Times", 14),
    background="#000080",
    foreground="#FACA2F",
)
lblRules.pack()

root.mainloop()




