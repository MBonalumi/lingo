import tkinter as tk

# dataset

def define_dataset(path:str=None):
    global dataset

    if path is None:
        path = "vocabolari/from_vocabolario_60k/words6.csv"
    dataset = pd.read_csv(path, names=['w'])

def reset_true_word(new_true_word=None):
    if new_true_word is None:
        new_true_word = dataset.sample(1).iloc[0,0].upper()
    else:
        new_true_word = new_true_word.upper()
    
    global true_word
    true_word = new_true_word
    print("true:", true_word)
    return true_word

def set_info_text(text:str):
    info_text.set(text)
    root.update()
    return

def score(word):
    score = [0]*len(word)
    todo = list(range(len(word)))

    for i in range(len(word)):
        if word[i] == true_word[i]:
            score[i] = 2
            todo.remove(i)

    true_word_remaining = [true_word[i] for i in todo] if todo else []

    for i in todo:
        if word[i] in true_word_remaining:
            score[i] = 1
            true_word_remaining.remove(word[i])

    return score

def on_submit(word=None):
    if word is None:
        input_text = str(entry.get()).upper()
    else:
        input_text = word.upper()
    
    global guesses
    guesses.append(input_text)

    print(f"Submitted: {input_text}")
    entry.delete(0, tk.END)
    #controlla l'input
    # info.config(text="Try again")

    len = input_text.__len__()
    ok = len==num_squares

    if not ok:
        info_text.set(f"Riprova! Inserisci una parola di {num_squares} lettere")
        return -2
    
    wscore = score(input_text)

    #TODO: controlla se la parola esiste nel dataset
    if input_text not in dataset.values:
        info_text.set("La parola non è valida! ")# la risposta era " + true_word)
        wscore = [3]*num_squares
        write(input_text, wscore)
        # end_state()
        return wscore

    if wscore == [2]*num_squares:
        info_text.set("Hai vinto!")
        write(input_text, wscore)
        end_state()
        return wscore

    write(input_text, wscore)
    info_text.set("Go on!") 

    global incremental_y, tries, max_tries

    if tries >= max_tries:
        info_text.set(f"Hai perso! la parola era {true_word}")
        end_state()
        return -1
        
    tries += 1

    incremental_y += 60
    entry.focus_set()

    global display_word
    new_display_word = ""
    for i in range(num_squares):
        if wscore[i] == 2:
            new_display_word += input_text[i]
        else:
            new_display_word += display_word[i]

    display_word = new_display_word
    write(display_word, score(display_word))

    return wscore

def write(text, wscore):
    # background_colors = ["#1156f1", "#f4af0f", "#01c02e", "#fa3a4a"]    # blue, yellow, green, red -> Lingo
    background_colors = ["#787c7e", "#f4af0f", "#01c02e", "#fa3a4a"]    # wordle_gray, yellow, green, red
    for i, char in enumerate(text):
        square_text = tk.Label( root, text=char, font=("Arial", 16, 'bold'),
                                fg="white", bg=background_colors[wscore[i]], width=4, height=2,
                                name=f"square_text_{tries}_{i}")
        square_text.place(x=horizontal_center + i * (square_width + 5), y=incremental_y)  # Adjust y position as needed
    root.update()

def end_state():
    global state
    state = "ko"

    with open("var/logs.txt", "a") as f:
        f.write(f"{true_word}-{','.join(guesses)}\n")

    entry.config(state="disabled")
    submit_button.config(state="disabled")
    root.unbind('<Return>')
    reset_button.config(state="normal")
    root.bind('<r>', lambda event: reset())  # Bind Return key event to submit button

def reset(new_true_word=None):
    reset_true_word(new_true_word)

    reset_button.config(state="disabled")
    root.unbind('<r>')

    global incremental_y, tries, display_word, true_word

    # get button by name
    for i in range(tries):
        for j in range(num_squares):
            square_text = root.nametowidget(f"square_text_{i+1}_{j}")
            square_text.destroy()

    incremental_y = 100
    tries = 1

    entry.config(state="normal")
    submit_button.config(state="normal")
    info_text.set(f"Inserisci una parola di {num_squares} lettere" )
    root.bind('<Return>', lambda event: on_submit())  # Bind Return key event to submit button

    display_word = true_word[0] + " "*(num_squares-1)
    print(display_word)
    write(display_word, score(display_word))

    global guesses, state
    guesses = [display_word]
    state = "playing"

    return true_word[0]

########################
#####    AI play   #####
########################
from filter_word import filter_word
from compute_entropy import compute_entropy
import pandas as pd
import numpy as np
def next_guess(guess, feedback, filter_w, words, scores):
    filter_w.filter(guess, feedback)
    _filtered_words = filter_w.apply(words)
    set_info_text(f"AI è indecisa tra {len(_filtered_words)} parole.")

    if len(_filtered_words) == 1:
        set_info_text(f"AI conosce la riposta!")
        print('The word is: ', _filtered_words.iloc[0])
        return _filtered_words.iloc[0]
    
    _entropies = compute_entropy(words, _filtered_words, scores)
    _mask = _entropies == _entropies.max()
    print("Try this:")
    print(words[_mask])

    return words[_mask].sample(1).iloc[0]

#TODO: AI might cache all the initial choices
#      i.e., <guess> to make when true_word starts wiht 'A', when with 'B', ...
#      in a dictionary, with keys the starting letter, e.g. { A:"INTERO", S:"PERITA", ... }
def ai_play():
    if(state == "ko"):
        reset()
    
    set_info_text("AI sta pensando...")

    words = dataset['w']
    candidate_answers = dataset['w']
    #TODO: make this and the loading of the dataset coherent
    scores = np.load("var/scores6.npy", allow_pickle=True)

    filter_w = filter_word(num_squares)
    for g in guesses:
        feedback = np.array( score(g) )
        filter_w.filter(g, feedback)

    if len(guesses)==1:
        from utils import best_initial_guesses
        guess = best_initial_guesses[guesses[0][0]]
    else:
        guess = next_guess(guesses[-1], feedback, filter_w, words, scores)

    feedback = np.array( on_submit(guess) )
    while (feedback!=2).any()  and  tries <= max_tries:
        guess = next_guess(guess, feedback, filter_w, words, scores)
        feedback = np.array( on_submit(guess) )
        #force tk to update

def ai_hint():
    if(state == "ko"):
        set_info_text("Resetta per far giocare AI")
        return
    set_info_text("AI sta pensando...")

    if len(guesses)==1:
        from utils import best_initial_guesses
        guess = best_initial_guesses[guesses[0][0]]
        entry.delete(0, tk.END)
        entry.insert(0, guess)
        set_info_text(f"AI consiglia, come prima mossa con iniziale {display_word[0]}:")
        return

    # use global variable <guesses>
    words = dataset['w']
    #TODO: make this and the loading of the dataset coherent
    scores = np.load("var/scores6.npy", allow_pickle=True)

    filter_w = filter_word(num_squares)

    for g in guesses:
        feedback = np.array( score(g) )
        filter_w.filter(g, feedback)

    _filtered_words = filter_w.apply(words)
    if len(_filtered_words) == 1:
        set_info_text(f"AI conosce la riposta!")
        entry.delete(0, tk.END)
        entry.insert(0, _filtered_words.iloc[0])
        return
    
    set_info_text(f"AI è indecisa tra {len(_filtered_words)} parole.")
    
    _entropies = compute_entropy(words, _filtered_words, scores)
    _mask = _entropies == _entropies.max()
    #prefer filtered_words to other words

    _filtered_words_optimal = words[np.array([wi for wi in _filtered_words.index.to_numpy() if _mask[wi]])]

    if len(_filtered_words_optimal) > 0:
        print("AI ci prova, e gioca una di queste: ", _filtered_words_optimal.tolist())
        guess = np.random.choice(_filtered_words_optimal)
    else:
        guess = words[_mask].sample(1).iloc[0]
    entry.delete(0, tk.END)
    entry.insert(0, guess)

    info_text.set("AI consiglia:")
    return


def ai_play_x_times(x=1):
    text = str(entry.get())
    text = text[:-1]
    #check if text is a valid number
    try:
        amt = int(text)
    except:
        amt = x
    
    if amt<1: amt=1

    set_info_text(f"AI giocherà {amt} volte")
    from time import sleep
    sleep(2)

    for _ in range(amt):
        ai_play()


########################
#####     main     #####
########################
# def reset_with_word():
#     #TODO: open a new popup window with a multiselector of words from the dataset, and a confirm button
#     #      the confirm button should call reset with the selected word
# import tkinter as tk
from tkinter import messagebox

def open_popup():
    popup = tk.Toplevel()
    popup.title("Word Selector")
    popup.configure(bg="white")
    popup.resizable(False, False)
    popup.geometry("300x500")
    
    words_frame = tk.Frame(popup, bg="white")
    words_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create a Listbox to display the words from the dataset
    listbox = tk.Listbox(words_frame, selectmode=tk.SINGLE, width=30, height=20, font=("Arial", 12), bg="white")
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    #align words to the center of the listbox
    listbox.config(justify=tk.CENTER)

    scrollbar = tk.Scrollbar(words_frame)
    scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH) 
    listbox.config(yscrollcommand = scrollbar.set) 
    scrollbar.config(command = listbox.yview) 

    # Add words from the dataset to the Listbox
    dataset = pd.read_csv("vocabolari/from_vocabolario_60k/words6.csv")
    words = dataset.iloc[:, 0].tolist()
    for word in words:
        listbox.insert(tk.END, word)

    # Create a Confirm button
    def confirm_selection():
        selected_words = [listbox.get(idx) for idx in listbox.curselection()]
        if not selected_words:
            messagebox.showerror("No Selection", "You must select a word to continue.")
            return
        messagebox.showinfo("Selected Words", f"You have selected: {selected_words}")
        popup.destroy()
        reset(selected_words[0])

    confirm_button = tk.Button(popup, text="Confirm", command=confirm_selection)
    confirm_button.pack(side=tk.BOTTOM, pady=10, padx=10)

def update():
    # l.config(text=str(random.random()))
    root.after(1000, update)

def main():
    global root, entry, info_text, submit_button, reset_button,\
            horizontal_center, square_width, num_squares, incremental_y,\
            tries, max_tries, display_word,\
            guesses,\
            state
    
    define_dataset()

    reset_true_word()

    root = tk.Tk()
    root.title("Lingo")

    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=False)
    file_menu.add_command(label="New Game", command=reset)
    file_menu.add_command(label="New Game with Custom Word", command=open_popup)
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File",menu=file_menu,underline=0)
    game_menu = tk.Menu(menubar, tearoff=False)
    game_menu.add_command(label="Let AI play", command=ai_play)
    game_menu.add_command(label="get AI hint", command=ai_hint)
    menubar.add_cascade(label="Game",menu=game_menu,underline=0)

    root.bind('<F10>', lambda event: ai_hint())
    root.bind('<F9>', lambda event: ai_play())
    root.bind('<~>', lambda event: ai_play_x_times(x=2))

    # Calculate window size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width / 5 * 2)
    window_height = int(screen_height * 0.75)

    # Set window size and position
    root.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")
    root.configure(bg="white")
    root.resizable(False, False)

    square_width = 60
    square_height = 60
    num_squares = 6
    incremental_y = 100
    tries = 1
    max_tries = 5

    total_width = num_squares * (square_width + 5) - 5
    horizontal_center = int((window_width - total_width) / 2)


    display_word = true_word[0] + " "*(num_squares-1)
    print(display_word)
    write(display_word, score(display_word))
    
    # Add text input and submit button
    entry = tk.Entry(root, font=("Arial", 16, 'bold'), width=10, name="entry")
    entry_w = entry.winfo_screenmmwidth()
    entry.pack(pady=10, padx=10)
    entry.focus_set()
    #size = 10+154+10 = 174

    submit_button = tk.Button(root, text="Submit", command=on_submit, width=10, name="submit")
    submit_button.pack(pady=10, padx=10)
    root.bind('<Return>', lambda event: on_submit())  # Bind Return key event to submit button
    # submit_button.bind("<Enter>", lambda event: on_submit())  # Bind Return key event to submit button
    #size = 10+100+10 = 120
    #totsize = 174+120 = 294

    entry.place(x=horizontal_center, y=window_height-100)
    submit_button.place(x=horizontal_center  + 200, y=window_height-100)

    info_text = tk.StringVar()
    info_text.set(f"Inserisci una parola di {num_squares} lettere" )
    info = tk.Label(root, textvariable=info_text, font=("Arial", 14), bg="white").place(x=horizontal_center, y=window_height-150)

    reset_button = tk.Button(root, text="Reset", command=reset, state="disabled", width=10, name="reset")
    reset_button.pack(pady=10, padx=10)
    reset_button.place(x=horizontal_center+200, y=window_height-50)

    guesses = [display_word]

    state = "playing"

    root.after(1000, update)
    root.mainloop()

import pandas as pd
if __name__ == "__main__":
    # global dataset
    # dataset = pd.read_csv("vocabolari/from_vocabolario_60k/words6.csv")
    # true_word = dataset.sample(1).iloc[0,0].upper()
    main()
