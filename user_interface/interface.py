import tkinter as tk

window = tk.Tk()
window.title("Universal Music Bridge")
window.geometry("900x800")
window.configure(bg="#dff6ff")  # light blue

# title
title_label = tk.Label(
    window,
    text="Universal Music Bridge",
    font=("Segoe UI", 25),
    bg="#dff6ff", fg="#0077b6"
)
title_label.pack(pady=15)

# song search input labels
song_label = tk.Label(
    window,
    text="Song Name",
    font=("Segoe UI", 20),
    bg="#dff6ff", fg="#0077b6"
)
song_label.pack(pady=5)

# function to make the placeholder of the search bar have "Type a Song..." in gray
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

artist_label = tk.Label(
    window,
    text="Artist Name",
    font=("Segoe UI", 20),
    bg="#dff6ff", fg="#0077b6"
)
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

# checkboxes to filter which platform to be used
filter_label = tk.Label(
    window,
    text="Choose platforms: ",
    font=("Segoe UI", 16),
    bg="#dff6ff", fg="#0077b6"
)
filter_label.pack(pady=10)

checkbox_frame = tk.Frame(window, bg="#dff6ff")
checkbox_frame.pack(pady=5)

youtube_var = tk.BooleanVar()
spotify_var = tk.BooleanVar()
tidal_var = tk.BooleanVar()

youtube_checkbox = tk.Checkbutton(
    checkbox_frame,
    text="YouTube Music",
    variable=youtube_var,
    font=("Segoe UI", 12),
    bg="#dff6ff",
    activebackground="#dff6ff"
)
youtube_checkbox.pack(side="left", padx=15)

spotify_checkbox = tk.Checkbutton(
    checkbox_frame,
    text="Spotify ",
    variable=spotify_var,
    font=("Segoe UI", 12),
    bg="#dff6ff",
    activebackground="#dff6ff"
)
spotify_checkbox.pack(side="left", padx=15)

tidal_checkbox = tk.Checkbutton(
    checkbox_frame,
    text="Tidal ",
    variable=tidal_var,
    font=("Segoe UI", 12),
    bg="#dff6ff",
    activebackground="#dff6ff"
)
tidal_checkbox.pack(side="left", padx=15)

# search function

def search():
    for widget in results_frame.winfo_children():
        widget.destroy()

    selected = []

    if youtube_var.get():
        selected.append("YouTube Music")
    if spotify_var.get():
        selected.append("Spotify")
    if tidal_var.get():
        selected.append("Tidal")

    if selected:
        results_label.config(text="Results:")

        for platform in selected:
            tk.Label(
                results_frame,
                text=platform + " result will appear here",
                font=("Segoe UI", 12),
                width=40,
                relief="groove",
                bg="#dff6ff", fg="#0077b6",
                pady=8
            ).pack(pady=5)
    else:
        results_label.config(text="No platform selected")


search_button = tk.Button(
    window,
    text="Search",
    font=("Segoe UI", 12, "bold"),
    bg="#90e0ef",
    fg="black",
    relief="flat",
    padx=10,
    pady=5,
    command=search
)
search_button.pack(pady=20)

results_label = tk.Label(
    window,
    text="Results will appear here",
    font=("Segoe UI", 12),
    fg="gray",
    bg="#dff6ff"
)
results_label.pack(pady=10)

# result container
results_frame = tk.Frame(window, bg="#dff6ff")
results_frame.pack(pady=20)


window.mainloop()