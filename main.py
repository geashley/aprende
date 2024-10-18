from tkinter import *
import random
import pandas


BACKGROUND_COLOR = "#B1DDC6"

try:
    data_csv = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    # Creating new flashcards
    data = pandas.read_csv("data/500_spanish_words.csv")
    data_list = data.to_dict(orient="records")
else:
    data_list = data_csv.to_dict(orient="records")


def new_flashcard():
    random_card = random.choice(data_list)
    flashcard.itemconfig(card_image, image=front)
    flashcard.itemconfig(language, text="Spanish", fill="black")
    flashcard.itemconfig(spanish_word, text=random_card["spanish"], fill="black")
    flashcard.after(3000, flip_card, random_card)


def flip_card(card):
    flashcard.itemconfig(card_image, image=back)
    flashcard.itemconfig(language, text="English", fill="white")
    english_word = card["english"]
    flashcard.itemconfig(spanish_word, text=english_word, fill="white")


def discard_card():
    current_word = flashcard.itemcget(spanish_word, "text")
    for word in data_list:
        if word["spanish"] == current_word or word["english"] == current_word:
            data_list.remove(word)
    new_data = pandas.DataFrame(data_list)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    new_flashcard()

# Creating UI
window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flashcard = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
front = PhotoImage(file="images/card_front.png")
back = PhotoImage(file="images/card_back.png")
card_image = flashcard.create_image(400, 263, image=front)
language = flashcard.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
flashcard.grid(column=0, row=0, columnspan=2)
spanish_word = flashcard.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

right_img = PhotoImage(file="images/right.png")
right = Button(image=right_img, highlightthickness=0, command=discard_card)
right.grid(column=1, row=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong = Button(image=wrong_img, highlightthickness=0, command=new_flashcard)
wrong.grid(column=0, row=1)
new_flashcard()
window.mainloop()

