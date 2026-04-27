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

# defining themes
APP_BG = "#0f0f0e"
CARD_BG = "#1e1e1e"
TEXT_MAIN = "#ffffff"
ACCENT = "#27B98E"
BUTTON_HOVER = "#48cae4"
ENTRY_BG = "#2b2b2b"

# initialize main application window
window = tk.Tk()
window.title("Universal Music Bridge")
window.geometry("1920x1800")

# main app background
window.configure(bg=APP_BG)

# style for title
TITLE_STYLE = {
    "bg": APP_BG,
    "fg": ACCENT,
    "font": ("Segoe UI", 25, "bold")
}

# style for standard labels
LABEL_STYLE = {
    "bg": APP_BG,
    "fg": ACCENT,
    "font": ("Segoe UI", 20)
}
# style for small labels
SMALL_LABEL_STYLE = {
    "bg": APP_BG,
    "fg": ACCENT,
    "font": ("Segoe UI", 16)
}

# style for buttons
BUTTON_STYLE = {
    "bg": "#198062",
    "hover_bg": ACCENT,
    "fg": "white",
    "font": ("Segoe UI", 12, "bold"),
    "relief": "flat",
    "padx": 10,
    "pady": 5
}

# style for result buttons
RESULT_BUTTON_STYLE = {
    "bg": "#333333",
    "hover_bg": "#444444",
    "fg": ACCENT,
    "font": ("Segoe UI", 12),
    "width": 35,
    "relief": "flat"
}
# style for check box
CHECKBOX_STYLE = {
    "font": ("Segoe UI", 12),
    "bg": APP_BG,
    "fg": ACCENT,
    "activebackground": APP_BG,
    "activeforeground": ACCENT,
    "selectcolor": "#000000"
}

RESULTS_LABEL_STYLE = {
    "font": ("Segoe UI", 14, "bold"),
    "bg": CARD_BG,
    "fg": ACCENT,
}

RESULT_SECTION_STYLE = {
    "bg": CARD_BG,
    "fg": ACCENT,
    "font": ("Segoe UI", 14, "bold")
}

# app title label
title_label = tk.Label(
    window,
    text="Universal Music Bridge",
    **TITLE_STYLE
)
title_label.pack(pady=15)

tk.Label(window, text="Search Category", **SMALL_LABEL_STYLE).pack(pady=(10, 0))

# Variable to hold the dropdown choice
search_category = tk.StringVar(window)
search_category.set("Song")

# Dropdown Menu
dropdown = tk.OptionMenu(window, search_category, "Song", "Album", "Artist", "Compilation", "Single")
dropdown.config(
    bg=ENTRY_BG,
    fg=TEXT_MAIN,
    activebackground=ACCENT,
    activeforeground="white",
    highlightthickness=0,
    relief="flat",
    font=("Segoe UI", 11),
    width=15
)
dropdown["menu"].config(bg=ENTRY_BG, fg=TEXT_MAIN, font=("Segoe UI", 11))
dropdown.pack(pady=10)

query_entry = tk.Entry(
    window,
    width=55,
    bg=ENTRY_BG,
    fg="gray",
    insertbackground=ACCENT,
    relief="flat",
    font=("Segoe UI", 12)
)
query_entry.insert(0, "Enter search term...")
query_entry.pack(pady=10, ipady=3)

# Enter single entry for query
def on_focus_in(e):
    if query_entry.get() == "Enter search term...":
        query_entry.delete(0, tk.END)
        query_entry.config(fg="white")

def on_focus_out(e):
    if query_entry.get() == "":
        query_entry.insert(0, "Enter search term...")
        query_entry.config(fg="gray")

query_entry.bind("<FocusIn>", on_focus_in)
query_entry.bind("<FocusOut>", on_focus_out)

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
    result_card = tk.Frame(parent, bg=CARD_BG)
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
    results_label.config(text="Link copied!", fg=ACCENT)


def create_album_art(parent, image_url):
    try:
        response = requests.get(image_url)
        img_data = response.content

        img = Image.open(BytesIO(img_data))
        img = img.resize((120, 120))  # adjust size here

        photo = ImageTk.PhotoImage(img)

        label = tk.Label(parent, image=photo, bg=CARD_BG)
        label.image = photo
        label.pack(pady=5, anchor='n')

    except:
        pass


def search():
    # Clear existing results
    for widget in results_frame.winfo_children():
        widget.destroy()

    user_query = query_entry.get().replace("Enter search term...", "").strip()
    category = search_category.get()

    if not user_query:
        results_label.config(text="Please enter something to search for.", fg="red")
        return

    category_map = {
        "Song": ["songs"],
        "Album": ["albums"],
        "Artist": ["artists"],
        "Compilation": ["compilations"],
        "Single": ["singles"]
    }

    search_types = category_map.get(category)

    apis = []
    if youtube_var.get(): apis.append("youtube")
    if spotify_var.get(): apis.append("spotify")
    if tidal_var.get(): apis.append("tidal")

    if not apis:
        results_label.config(text="No platform selected", fg="red")
        return

    results_label.config(text=f"Searching {category}s for '{user_query}'...", fg=ACCENT)
    window.update()

    # Call API through main function
    tidal_results, youtube_results, spotify_results = search_apis(user_query, search_types, apis)

    for widget in results_frame.winfo_children():
        widget.destroy()

    # Centered column tray
    column_tray = tk.Frame(results_frame, bg=APP_BG)
    column_tray.pack(pady=10, expand=True)

    # Youtube column (if selected)
    if youtube_var.get():
        yt_col = tk.Frame(column_tray, bg=CARD_BG, padx=15)
        yt_col.pack(side="left", fill="y", anchor="n", padx=15)

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
        sp_col = tk.Frame(column_tray, bg=CARD_BG, padx=15)
        sp_col.pack(side="left", fill="y", anchor="n", padx=15)

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
        td_col = tk.Frame(column_tray, bg=CARD_BG, padx=15)
        td_col.pack(side="left", fill="y", anchor="n", padx=15)

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
    bg=APP_BG,
    fg="gray",
    font=("Segoe UI", 10, "italic")
)
results_label.pack(pady=5)

# Scrollable results container
container = tk.Frame(window, bg=APP_BG)
container.pack(fill="both", expand=True, padx=20, pady=20)

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
