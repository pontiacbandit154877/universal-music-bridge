import tkinter as tk

window = tk.Tk()
window.title("Universal Music Bridge")
window.geometry("900x800")

# title
title_label = tk.Label(window, text="Universal Music Bridge", font=("Segoe UI", 25))
title_label.pack(pady=15)

# song search input labels
song_label = tk.Label(window, text="Song Name", font=("Segoe UI", 20))
song_label.pack(pady=5)

# function to make the placeholder of the search bar have "Type a Song..." in grey
# until user types in it

def clear_placeholder(event):
    if song_entry.get() == "Type a song...":
        song_entry.delete(0, tk.END)
        song_entry.config(fg="black")

def add_placeholder(event):
    if song_entry.get() == "":
        song_entry.insert(0, "Type a song...")
        song_entry.config(fg="gray")

song_entry = tk.Entry(window, width=50, fg="gray")
song_entry.insert(0,"Type a song...")
song_entry.pack(pady=5)

song_entry.bind("<FocusIn>", clear_placeholder)
song_entry.bind("<FocusOut>", add_placeholder)


# artist search input labels

artist_label = tk.Label(window, text="Artist Name", font=("Segoe UI", 20))
artist_label.pack(pady=5)

def clear_artist_placeholder(event):
    if artist_entry.get() == "Type an artist...":
        artist_entry.delete(0, tk.END)
        artist_entry.config(fg="black")

def add_artist_placeholder(event):
    if artist_entry.get() == "":
        artist_entry.insert(0, "Type an artist...")
        artist_entry.config(fg="gray")

artist_entry = tk.Entry(window, width=50, fg="gray")
artist_entry.insert(0,"Type an artist...")
artist_entry.pack(pady=5)

artist_entry.bind("<FocusIn>", clear_artist_placeholder)
artist_entry.bind("<FocusOut>", add_artist_placeholder)

window.mainloop()