import tkinter as tk

root = tk.Tk()

def create_square(parent, color, width, height):
    square = tk.Canvas(parent, width=width, height=height, bg=color)
    return square

def on_submit():
    entry = root.nametowidget("entry")
    input_text = entry.get()
    print(f"Submitted: {input_text}")

def main():
    # root = tk.Tk()
    root.title("Grey Squares App")

    # Calculate window size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width / 2)
    window_height = int(screen_height * 0.75)

    # Set window size and position
    root.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")
    root.configure(bg="white")
    root.resizable(False, False)

    square_width = 50
    square_height = 50
    num_squares = 6

    squares = []
    for _ in range(num_squares):
        square = create_square(root, "grey", square_width, square_height)
        squares.append(square)

    # Add text input and submit button
    entry = tk.Entry(root, font=("Arial", 16),  name="entry")
    entry.pack(pady=10, padx=10)

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(pady=10, padx=10)

    # Calculate total width of squares
    total_width = num_squares * (square_width + 5) - 5

    # Calculate horizontal center for squares
    horizontal_center = int((window_width - total_width) / 2)

    # Place squares horizontally centered
    for i, square in enumerate(squares):
        square.place(x=horizontal_center + i * (square_width + 5), y=100)  # Adjust y position as needed

    root.mainloop()

if __name__ == "__main__":
    main()
