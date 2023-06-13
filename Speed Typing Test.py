import string
from tkinter import *
from tkinter import messagebox
import random

TEST_TIME = 60
WPM_MODIFIER = 5
WORD_WINDOW_WIDTH = 50
FONT = 'Courier'

ALPHABET = list(string.ascii_letters)
ALPHABET.extend(["space", "apostrophe"])

#Initializes tkinter GUI and provides utility functions for the typing test
class App:
    def __init__(self):
        self.correct_total = 0
        self.error_total = 0
        self.previous_letter = ''
        self.prev_wrong = False
        with open('Random.txt') as data:
            words = data.read()
        word_list = words.splitlines()
        self.word_line = [random.choice(word_list) for i in range(500)]

        self.window = Tk()
        self.window.title('Speed Typing Test')

        self.frm = Frame(self.window)
        self.frm.grid()

        self.timer = StringVar(self.frm)
        self.time_text = Label(self.frm, textvariable=self.timer, font=(FONT, 30), fg='#141414', bg='#FFFFFF')
        self.time_text.grid(column=0, row=0, sticky='w')

        self.start_button = Button(self.frm, text="Start Challenge", command=lambda: self.countdown(TEST_TIME))
        self.start_button.grid(column=0, row=0, sticky='e')

        self.text = Text(self.frm,
                    {"bg": "#FFFFFF", "bd": 80, "fg": "#141414", "height": 2, "width": 30, "font": (FONT, 40),
                     "insertbackground": "#141414", "wrap": "word", "highlightthickness": 0})

        self.text.insert(INSERT, self.word_line)

        self.text.mark_set("insert", "%d.%d" % (1.0, 0.0))
        self.text.grid(column=0, row=3)
        self.text.tag_add("start", "1.0", END)
        self.text.tag_config("start", background="#565656", foreground="#565656")
        self.text.tag_add('cursor', INSERT)

        self.frm.bind_all("<Key>", self.key_press)


    # Event handler for keypress.  Compares the pressed key input with the current letter.  If they match, adds to the
    # total correct key press counter and allows the text widget cursor to advance as normal.  If they don't match, adds
    # to the error counter, moves the cursor back a space and into position for the user to try again- concurrently
    # highlights the incorrect letter to notify the user of the incorrect keystroke
    def key_press(self, event):
        self.text.yview(INSERT)
        current_letter = self.text.get(INSERT)
        if event.keysym in ALPHABET:
            if not self.prev_wrong:
                self.previous_letter = current_letter
            if event.char == current_letter:
                self.prev_wrong = False
                self.correct_total += 1
                self.text.delete(INSERT)
            else:
                self.prev_wrong = True
                self.error_total += 1
                self.text.delete('insert-1c')
                self.previous_letter = self.text.get('insert-1c')
                self.text.tag_add('cursor', 'insert', 'insert+1c')
                self.text.tag_config('cursor', background='#FBA92C')

        # Backspace is commonly impulsively pressed by users when they see that they have incorrectly typed the wrong letter.
        # This function effectively undoes the backspace in the text widget and highlights the next letter that needs
        # to be typed so the user can continue to work on correctly typing the current word
        elif event.keysym == "BackSpace":
            self.text.insert(INSERT, self.previous_letter)
            self.text.tag_add('cursor', 'insert', 'insert+1c')
            self.text.tag_config('cursor', background='#FBA92C')

    # Begins a countdown for the typing challenge.  When the time is up, the user's typing speed in words per minute
    # is calculated and displayed in a message box along with total errors
    def countdown(self, count):
        self.timer.set(f'Time remaining: {count}')
        self.text.focus()
        self.text.tag_config('start', foreground ='#FFFFFF')
        if count != 0:
            self.window.after(1000, self.countdown, count - 1)
            if count == 10:
                self.time_text.config(foreground='red')
            if count == 5:
                self.time_text.config(font=('Courier New', 30, 'bold'))
        else:
            average_speed = (self.correct_total/5) / (TEST_TIME/60)
            messagebox.showinfo(title='Challenge Complete!', message=f"Your typing speed was {int(average_speed)} "
                                                                     f"words per minute.\n"
                                                                     f"You made {self.error_total} errors.")


if __name__ == '__main__':
    app = App()
    app.window.mainloop()

