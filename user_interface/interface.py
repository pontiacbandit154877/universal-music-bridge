import tkinter as tk
import webbrowser
from main import search_apis

# class to change button color when you hover
class HoverButton(tk.Button):
    def __init__(self, master=None, hover_bg=None, **kwargs):
        self.default_bg = kwargs.get('bg', 'SystemButtonFace')
        self.hover_bg = hover_bg if hover_bg else self.default_bg

        super().__init__(master, **kwargs)

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(bg=self.hover_bg)

    def on_leave(self, event):
        self.config(bg=self.default_bg)


# initialize main application window
window = tk.Tk()
window.title("Universal Music Bridge")
window.geometry("900x800")

# defining themes

# main app background
APP_BG = "#dff6ff"
APP_FG = "#0077b6"
window.configure(bg=APP_BG)

# style for title
TITLE_STYLE = {
    "bg": APP_BG,
    "fg": APP_FG,
    "font": ("Segoe UI", 25)
}

# style for standard labels
LABEL_STYLE = {
    "bg": APP_BG,
    "fg": APP_FG,
    "font": ("Segoe UI", 20)
}
#style for small labels
SMALL_LABEL_STYLE = {
    "bg": APP_BG,
    "fg": APP_FG,
    "font": ("Segoe UI", 16)
}

# style for buttons
BUTTON_STYLE = {
    "bg": "#90e0ef",
    "hover_bg": "#ade8f4",
    "fg": "black",
    "font": ("Segoe UI", 12, "bold"),
    "relief": "flat",
    "padx": 10,
    "pady": 5
}

# style for result buttons
RESULT_BUTTON_STYLE = {
    "bg": "#caf0f8",
    "hover_bg": "#e0fbfc",
    "fg": "#0077b6",
    "font": ("Segoe UI", 12),
    "width": 45,
    "relief": "groove"
}
# style for check box
CHECKBOX_STYLE = {
    "font": ("Segoe UI", 12),
    "bg": APP_BG,
    "activebackground": APP_BG
}

RESULTS_LABEL_STYLE = {
    "font": ("Segoe UI", 12),
    "fg": "gray",
    "bg": APP_BG
}

RESULT_SECTION_STYLE = {
    "bg": APP_BG,
    "fg": APP_FG,
    "font": ("Segoe UI", 12, "bold")
}

# app title label
title_label = tk.Label(
    window,
    text="Universal Music Bridge",
    **TITLE_STYLE
)
title_label.pack(pady=15)

# song input labels
song_label = tk.Label(
    window,
    text="Song Name",
    **LABEL_STYLE,
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
    **LABEL_STYLE
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
    **SMALL_LABEL_STYLE
)
filter_label.pack(pady=10)

checkbox_frame = tk.Frame(window, bg=APP_BG)
checkbox_frame.pack(pady=5)

youtube_var = tk.BooleanVar()
spotify_var = tk.BooleanVar()
tidal_var = tk.BooleanVar()

youtube_checkbox = tk.Checkbutton(
    checkbox_frame,
    text="Youtube Music",
    variable=youtube_var,
    **CHECKBOX_STYLE
)
youtube_checkbox.pack(side="left", padx=15)

spotify_checkbox = tk.Checkbutton(
    checkbox_frame,
    text="Spotify",
    variable=spotify_var,
    **CHECKBOX_STYLE
)
spotify_checkbox.pack(side="left", padx=15)

tidal_checkbox = tk.Checkbutton(
    checkbox_frame,
    text="Tidal",
    variable=tidal_var,
    **CHECKBOX_STYLE
)
tidal_checkbox.pack(side="left", padx=15)

# search function

def create_result_button(parent, text, link):
    HoverButton(
        parent,
        text=text,
        command=lambda: webbrowser.open(link),
        **RESULT_BUTTON_STYLE
    ).pack(pady=5)

def search():
    for widget in results_frame.winfo_children():
        widget.destroy()

    song = song_entry.get()
    artist = artist_entry.get()

    if song == "Type a song...":
        song = ""
    if artist == "Type an artist...":
        artist = ""

    query = f"{song} {artist}".strip()

    if not query:
        results_label.config(text="Please enter a song or artist.")
        return

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
            tk.Label(results_frame, text="YouTube Results:", **RESULT_SECTION_STYLE).pack()

            for result in youtube_results[0][:4]:
                create_result_button(
                    results_frame,
                    result["title"] + " - " + result["artist"],
                    result["link"]
                )

        if spotify_var.get() and spotify_results:
            tk.Label(results_frame, text="Spotify Results:", **RESULT_SECTION_STYLE).pack()

            for result in spotify_results[0][:4]:
                create_result_button(
                    results_frame,
                    result["title"] + " - " + result["artist"],
                    result["link"]
                )

        if tidal_var.get() and tidal_results and isinstance(tidal_results[0], dict):
            tk.Label(results_frame, text="Tidal Results:", **RESULT_SECTION_STYLE).pack()

            result = tidal_results[0] if isinstance(tidal_results, list) else tidal_results

            create_result_button(
                results_frame,
                result["title"] + " - " + result.get("artist", "Unknown"),
                result["link"]
            )

    else:
        results_label.config(text="No platform selected")


search_button = HoverButton(
    window,
    text="Search",
    command=search,
    **BUTTON_STYLE
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
results_frame = tk.Frame(window, bg=APP_BG)
results_frame.pack(pady=20)



window.mainloop()