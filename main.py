from tkinter import *
from pandas import *
import random
from pandas.errors import EmptyDataError

BACKGROUND_COLOR = "#B1DDC6"
CARD_SWAP=False
data_dict=[]
# ---------------------------- PANDA DATA----------------------------------- #
try:
    df=read_csv('data/words_to_learn.csv')
    if df.empty:
        raise EmptyDataError

except (FileNotFoundError, EmptyDataError):
    original_data=read_csv('data/french_words.csv')
    data_dict=original_data.to_dict(orient='records')
    foreign_language_title = original_data.columns[0]
    english_language_title = original_data.columns[1]
else:
    data_dict = df.to_dict(orient="records")
    foreign_language_title = df.columns[0]
    english_language_title = df.columns[1]





# -------------------------------- FUNCTIONS -------------------------------
def next_card():
    global random_word, CARD_SWAP, data_dict

    if len(data_dict) == 0:
        canvas.itemconfig(card_title, text="Finished!")
        canvas.itemconfig(card_word, text="No more cards!")
        return
    random_word = random.choice(data_dict)
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_title,text=foreign_language_title)
    canvas.itemconfig(card_word,text=random_word[foreign_language_title])
    CARD_SWAP=False


def swap(event):
    global CARD_SWAP
    global random_word
    CARD_SWAP=not CARD_SWAP
    if CARD_SWAP:
        canvas.itemconfig(card_image,image=card_back_img)
        canvas.itemconfig(card_title, text=english_language_title)
        canvas.itemconfig(card_word, text=random_word[english_language_title])
    else:
        canvas.itemconfig(card_image, image=card_front_img)
        canvas.itemconfig(card_title, text=foreign_language_title)
        canvas.itemconfig(card_word, text=random_word[foreign_language_title])


def is_known():
    global data_dict, random_word

    if random_word in data_dict:
        data_dict.remove(random_word)

    DataFrame(data_dict).to_csv("data/words_to_learn.csv", index=False)

    if len(data_dict) > 0:
        next_card()
    else:
        canvas.itemconfig(card_title, text="Congratulations!")
        canvas.itemconfig(card_word, text="You've learned all the words!", font=("Arial", 40, "bold"))
# ---------------------------- UI SETUP ------------------------------- #

window=Tk()
window.title("Flashy")
window.config(padx=50,pady=50,background=BACKGROUND_COLOR)


card_back_img=PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR,highlightthickness=0)
card_image=canvas.create_image(400,263,image=card_front_img)


card_title=canvas.create_text(400,150,text="Language",font=("Ariel",30,"italic"))
card_word=canvas.create_text(400,263,text="Word",font=("Ariel",60,"bold"))
canvas.grid(row=0,column=0,columnspan=2)
canvas.bind("<Button-1>", swap)



wrong_button_image=PhotoImage(file="images/wrong.png")
wrong_button=Button(image=wrong_button_image,highlightthickness=0,borderwidth=0,command=next_card)
wrong_button.grid(row=1,column=0)

right_button_image=PhotoImage(file="images/right.png")
right_button=Button(image=right_button_image,highlightthickness=0,borderwidth=0,command=is_known)
right_button.grid(row=1,column=1)

next_card()





window.mainloop()