import tkinter as tk
import webbrowser
from main import search_apis
from PIL import Image, ImageTk
import requests
from io import BytesIO


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
# style for small labels
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
    "width": 35,
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

# album search input labels

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
song_entry.insert(0, "Type a song...")
song_entry.pack(pady=5)

song_entry.bind("<FocusIn>", clear_placeholder)
song_entry.bind("<FocusOut>", add_placeholder)

album_label = tk.Label(
    window,
    text="Album Name",
    **LABEL_STYLE
)
album_label.pack(pady=5)

def clear_album_placeholder(event):
    if album_entry.get() == "Type an album...":
        album_entry.delete(0, tk.END)
        album_entry.config(fg="black")

def add_album_placeholder(event):
    if album_entry.get() == "":
        album_entry.insert(0, "Type an album...")
        album_entry.config(fg="gray")

album_entry = tk.Entry(window, width=50, fg="gray")
album_entry.insert(0, "Type an album...")
album_entry.pack(pady=5)

album_entry.bind("<FocusIn>", clear_album_placeholder)
album_entry.bind("<FocusOut>", add_album_placeholder)

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
artist_entry.insert(0, "Type an artist...")
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
    result_card = tk.Frame(parent, bg=APP_BG)
    result_card.pack(pady=5, anchor='n')

    HoverButton(
        result_card,
        text=text,
        command=lambda: webbrowser.open(link),
        **RESULT_BUTTON_STYLE
    ).pack(side="left", padx=5)

    HoverButton(
        result_card,
        text="Copy Link",
        command=lambda: copy_link(link),
        **BUTTON_STYLE
    ).pack(side="left", padx=5)

def copy_link(link):
    window.clipboard_clear()
    window.clipboard_append(link)
    window.update()
    results_label.config(text="Link copied to clipboard!")


def create_album_art(parent, image_url):
    try:
        response = requests.get(image_url)
        img_data = response.content

        img = Image.open(BytesIO(img_data))
        img = img.resize((120, 120))  # adjust size here

        photo = ImageTk.PhotoImage(img)

        label = tk.Label(parent, image=photo, bg=APP_BG)
        label.image = photo
        label.pack(pady=5, anchor='n')

    except:
        pass


def search():
    # Clear existing results
    for widget in results_frame.winfo_children():
        widget.destroy()

    song = song_entry.get().replace("Type a song...", "").strip()
    artist = artist_entry.get().replace("Type an artist...", "").strip()
    album = album_entry.get().replace("Type an album...", "").strip()

    search_types = []

    if album:
        search_types = ["albums"]
        query = f"{album} {artist}".strip()
    elif song:
        search_types = ["songs"]
        query = f"{song} {artist}".strip()
    elif artist:
        search_types = ["artists"]
        query = artist
    else:
        results_label.config(text="Please enter a song, album, or artist.")
        return

    # Determine APIS
    apis = []
    if youtube_var.get(): apis.append("youtube")
    if spotify_var.get(): apis.append("spotify")
    if tidal_var.get(): apis.append("tidal")

    if not apis:
        results_label.config(text="No platform selected")
        return

    results_label.config(text="Results:")

    # Call API through main function
    tidal_results, youtube_results, spotify_results = search_apis(query, search_types, apis)

    for widget in results_frame.winfo_children():
        widget.destroy()

    column_tray = tk.Frame(results_frame, bg=APP_BG)
    column_tray.pack(pady=10, expand=True)

    # Youtube column (if selected)
    if youtube_var.get():
        yt_col = tk.Frame(column_tray, bg=APP_BG, padx=10)
        yt_col.pack(side="left", fill="y", anchor="n")

        tk.Label(yt_col, text="YouTube Music", **RESULT_SECTION_STYLE).pack(pady=10)

        if youtube_results and youtube_results[0]:
            for result in youtube_results[0][:4]:
                if result.get("thumbnail"):
                    create_album_art(yt_col, result["thumbnail"][0]["url"])

                create_result_button(yt_col, f"{result.get('title')} - {result.get('artist')}", result["link"])
        else:
            tk.Label(yt_col, text="No results found", **RESULTS_LABEL_STYLE).pack()

    # Spotify column (if selected)
    if spotify_var.get():
        sp_col = tk.Frame(column_tray, bg=APP_BG, padx=10)
        sp_col.pack(side="left", fill="y", anchor="n")

        tk.Label(sp_col, text="Spotify", **RESULT_SECTION_STYLE).pack(pady=10)

        if spotify_results and spotify_results[0]:
            for result in spotify_results[0][:4]:
                if result.get("thumbnail"):
                    create_album_art(sp_col, result["thumbnail"][0]["url"])

                create_result_button(sp_col, f"{result['title']} - {result['artist']}", result["link"])
        else:
            tk.Label(sp_col, text="No results found", **RESULTS_LABEL_STYLE).pack()

    # Tidal Column (if selected)
    if tidal_var.get():
        td_col = tk.Frame(column_tray, bg=APP_BG, padx=10)
        td_col.pack(side="left", fill="y", anchor="n")

        tk.Label(td_col, text="Tidal", **RESULT_SECTION_STYLE).pack(pady=10)

        if tidal_results and tidal_results[0]:
            # Normalize Tidal data (handling list vs single dict)
            res_list = tidal_results[0] if isinstance(tidal_results[0], list) else [tidal_results[0]]
            for result in res_list[:4]:
                if result.get("thumbnail"):
                    # Use your fixed URL logic here
                    thumb = result["thumbnail"][0]["url"] if isinstance(result["thumbnail"], list) else result[
                        "thumbnail"]
                    create_album_art(td_col, thumb)

                create_result_button(td_col, f"{result['title']} - {result.get('artist', 'Unknown')}", result["link"])
        else:
            tk.Label(td_col, text="No results found", **RESULTS_LABEL_STYLE).pack()

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
    **RESULTS_LABEL_STYLE
)
results_label.pack(pady=10)

# Scrollable results container
container = tk.Frame(window, bg=APP_BG)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container, bg=APP_BG, highlightthickness=0)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
results_frame = tk.Frame(canvas, bg=APP_BG)

result_window = canvas.create_window((0, 0), window=results_frame, anchor="nw")

results_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Ensure results remain centered
def center_results(event):
    canvas_width = event.width
    canvas.itemconfig(result_window, width=canvas_width)

canvas.bind("<Configure>", center_results)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

window.mainloop()
