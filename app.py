import tkinter as tk

# dataset

def pick_word():
    return "moneta".upper()

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

def on_submit():
    input_text = str(entry.get()).upper()
    print(f"Submitted: {input_text}")
    entry.delete(0, tk.END)
    #controlla l'input
    # info.config(text="Try again")

    len = input_text.__len__()
    ok = len==num_squares

    if not ok:
        info_text.set(f"Riprova! Inserisci una parola di {num_squares} lettere")
        return
    
    #TODO: controlla se la parola esiste nel dataset
    if input_text not in dataset.values:
        info_text.set("La parola non è valida! la risposta era " + true_word)
        write(input_text, [3]*num_squares)
        end_state()
        return

    wscore = score(input_text)
    write(input_text, wscore)

    if wscore == [2]*num_squares:
        info_text.set("Hai vinto!")
        end_state()
        return

    global incremental_y, tries, max_tries

    if tries >= max_tries:
        info_text.set(f"Hai perso! la parola era {true_word}")
        end_state()
        return
        
    tries += 1

    incremental_y += 60
    info_text.set("Go on!") 
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

def write(text, wscore):
    background_colors = ["#1156f1", "#f4af0f", "#01c02e", "#fa3a4a"]    # blue, yellow, green, red
    for i, char in enumerate(text):
        square_text = tk.Label( root, text=char, font=("Arial", 16, 'bold'),
                                fg="white", bg=background_colors[wscore[i]], width=4, height=2,
                                name=f"square_text_{tries}_{i}")
        square_text.place(x=horizontal_center + i * (square_width + 5), y=incremental_y)  # Adjust y position as needed

def end_state():
    entry.config(state="disabled")
    submit_button.config(state="disabled")
    root.unbind('<Return>')
    reset_button.config(state="normal")
    root.bind('<r>', lambda event: reset())  # Bind Return key event to submit button

def reset():
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

    true_word = dataset.sample(1).iloc[0,0].upper()
    print("true:", true_word)

    display_word = true_word[0] + " "*(num_squares-1)
    print(display_word)
    write(display_word, score(display_word))

def main():
    global root, entry, info_text, submit_button, reset_button,\
            horizontal_center, square_width, num_squares, incremental_y,\
            tries, max_tries, display_word

    root = tk.Tk()
    root.title("Lingo")

    # Calculate window size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width / 2)
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

    root.mainloop()

import pandas as pd
if __name__ == "__main__":
    global true_word, dataset
    dataset = pd.read_csv("vocabolari/words6.csv")
    true_word = dataset.sample(1).iloc[0,0].upper()
    print("true:", true_word)
    main()
