import tkinter as tk
import webbrowser
from main import search_apis

# initialize main application window
window = tk.Tk()
window.title("Universal Music Bridge")
window.geometry("900x800")
window.configure(bg="#dff6ff")  # light blue

# app title label
title_label = tk.Label(
    window,
    text="Universal Music Bridge",
    font=("Segoe UI", 25),
    bg="#dff6ff", fg="#0077b6"
)
title_label.pack(pady=15)

# song input labels
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

# function to make the placeholder of the search bar have "Type an Artist..." in gray
# until user types in it
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

    song = song_entry.get()
    artist = artist_entry.get()

    apis = []

    if youtube_var.get():
        apis.append("youtube")
    if spotify_var.get():
        apis.append("spotify")
    if tidal_var.get():
        apis.append("tidal")

    if apis:
        results_label.config(text="Results:")

        query = song

        tidal_results, youtube_results, spotify_results = search_apis(
            query,
            ["songs"],
            apis
        )

        if youtube_var.get() and youtube_results:
            tk.Label(results_frame, text="YouTube Results:", bg="#dff6ff").pack()

            for result in youtube_results[0][:4]:
                    tk.Button(
                        results_frame,
                        text=result["title"] + " - " + result["artist"],
                        font=("Segoe UI", 12),
                        width=45,
                        bg="#caf0f8",
                        fg="#0077b6",
                        relief="groove",
                        command=lambda link=result["link"]: webbrowser.open(link)
                    ).pack(pady=5)

        if spotify_var.get() and spotify_results:
            tk.Label(results_frame, text="Spotify Results:", bg="#dff6ff", fg="#0077b6").pack()

            for result in spotify_results[0][:4]:
                tk.Button(
                    results_frame,
                    text=result["title"] + " - " + result["artist"],
                    width=45,
                    bg="#caf0f8",
                    fg="#0077b6",
                    relief="groove",
                    command=lambda link=result["link"]: webbrowser.open(link)
                ).pack(pady=5)

        if tidal_var.get() and tidal_results and isinstance(tidal_results[0], dict):
            tk.Label(results_frame, text="Tidal Result:", bg="#dff6ff").pack()

            result = tidal_results[0] if isinstance(tidal_results, list) else tidal_results

            tk.Button(
                results_frame,
                text=result["title"] + " - " + result.get("artist", "Unknown"),
                command=lambda link=result["link"]: webbrowser.open(link)
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