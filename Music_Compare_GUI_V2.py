# Program Created by Eliza Boulay
# October 2026
import pandas as pd
import tkinter as tk
import sys
import time
import winsound
from tkinter import filedialog, messagebox, ttk
from rapidfuzz import process, fuzz
from pathlib import Path

# Similarity thresholds
TITLE_THRESHOLD = 90
ARTIST_THRESHOLD = 90

# Application colors
BACKGROUND_COLOR = "#FCE4EC"
BUTTON_COLOR = "#F8BBD0"
BUTTON_ACTIVE_COLOR = "#F48FB1"
TEXT_COLOR = "#4A2633"
ENTRY_COLOR = "#FFF8FA"

# Normalize text
def normalize_text(series):
    return (
        series.astype("string")
        .str.casefold()
        .str.replace(r"['\u2018\u2019]", "", regex=True)
        .str.replace(r"[\W_]+", "", regex=True)
    )


# Prepare songs from an Excel file
def prepare_sheet(df, filename):
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.casefold()
    )

    result = df[["title", "artist"]].copy()
    result.columns = ["Original Title", "Original Artist"]

    result["title_key"] = normalize_text(result["Original Title"])
    result["artist_key"] = normalize_text(result["Original Artist"])
    result["file"] = filename

    result = result.dropna(subset=["title_key", "artist_key"])
    result = result[
        (result["title_key"] != "") &
        (result["artist_key"] != "")
    ]

    result = result.drop_duplicates(
        subset=["title_key", "artist_key"]
    )

    return result.reset_index(drop=True)

# Compare the two Excel files
def compare_songs(file1, file2):
    sheet1 = pd.read_excel(file1)
    sheet2 = pd.read_excel(file2)

    songs1 = prepare_sheet(sheet1, file1)
    songs2 = prepare_sheet(sheet2, file2)

    songs2_keys = [
        f"{row['title_key']} {row['artist_key']}"
        for _, row in songs2.iterrows()
    ]

    matched_song2 = set()
    unique_rows = []

    for _, song1 in songs1.iterrows():
        search_key = (
            f"{song1['title_key']} {song1['artist_key']}"
        )

        candidates = process.extract(
            search_key,
            songs2_keys,
            scorer=fuzz.ratio,
            limit=10,
            score_cutoff=70
        )

        best_match = None
        best_score = -1

        for _, _, j in candidates:
            if j in matched_song2:
                continue

            song2 = songs2.iloc[j]

            title_score = fuzz.ratio(
                song1["title_key"],
                song2["title_key"]
            )

            artist_score = fuzz.ratio(
                song1["artist_key"],
                song2["artist_key"]
            )

            if (
                title_score >= TITLE_THRESHOLD
                and artist_score >= ARTIST_THRESHOLD
            ):
                score = (title_score + artist_score) / 2

                if score > best_score:
                    best_score = score
                    best_match = j

        if best_match is not None:
            matched_song2.add(best_match)
        else:
            unique_rows.append({
                "Title": song1["Original Title"],
                "Artist": song1["Original Artist"],
                "File": Path(file1).name
            })

    # Add unmatched songs from the second file
    for j, song2 in songs2.iterrows():
        if j not in matched_song2:
            unique_rows.append({
                "Title": song2["Original Title"],
                "Artist": song2["Original Artist"],
                "File": Path(file2).name
            })

    unique_songs = pd.DataFrame(
        unique_rows,
        columns=["Title", "Artist", "File"]
    )

    unique_songs = unique_songs.drop_duplicates(
        subset=["Title", "Artist", "File"]
    )

    unique_songs = unique_songs.sort_values(
        by=["Title", "Artist"]
    ).reset_index(drop=True)

    return unique_songs


# Browse for an input Excel file
def browse_input(variable):
    filename = filedialog.askopenfilename(
        title="Select an Excel file",
        filetypes=[
            ("Excel files", "*.xlsx *.xls *.xlsm"),
            ("All files", "*.*")
        ],
        parent=root
    )

    if filename:
        variable.set(filename)


# Browse for the output location
def browse_output():
    filename = filedialog.asksaveasfilename(
        title="Save comparison results",
        defaultextension=".xlsx",
        initialfile="unique_songs.xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        parent=root
    )

    if filename:
        output_var.set(filename)

help_window = None

# Display the How to Use window
def show_help():
    global help_window

    # If the help window is already open, bring it to the front
    if help_window is not None and help_window.winfo_exists():
        help_window.lift()
        help_window.focus_force()
        return

    # Create a separate help window
    help_window = tk.Toplevel(root)
    help_window.title("How to Use")
    help_window.geometry("600x500")
    help_window.configure(bg=BACKGROUND_COLOR)

    # Handle closing the help window
    def close_help():
        global help_window
        help_window.destroy()
        help_window = None

    help_window.protocol("WM_DELETE_WINDOW", close_help)

    # Frame inside the help window
    help_frame = ttk.Frame(
        help_window,
        padding=15,
        style="Pink.TFrame"
    )
    help_frame.pack(fill="both", expand=True)

    # Help window heading
    ttk.Label(
        help_frame,
        text="Music Comparison Information",
        style="Heading.TLabel",
        wraplength=550
    ).pack(anchor="w", pady=(0, 12))

    ttk.Label(
        help_frame,
        text="Refer to the information below for usage and questions.",
        style="Pink.TLabel",
        wraplength=550
    ).pack(anchor="w", pady=(0, 12))

    # Scrollable instructions area
    text_frame = ttk.Frame(
        help_frame,
        style="Pink.TFrame"
    )
    text_frame.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        text_frame,
        orient="vertical"
    )
    scrollbar.pack(side="right", fill="y")

    instructions = tk.Text(
        text_frame,
        wrap="word",
        font=("Arial", 10),
        bg=ENTRY_COLOR,
        fg=TEXT_COLOR,
        relief="flat",
        padx=12,
        pady=12,
        spacing1=3,
        spacing3=5,
        yscrollcommand=scrollbar.set,
        cursor="arrow",
        borderwidth=0
    )
    instructions.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=instructions.yview)

    instructions.tag_configure(
        "heading",
        font=("Arial", 11, "bold"),
        spacing1=8,
        spacing3=4
    )

    instructions.insert(
        "end",
        "1. Prepare your Excel files\n",
        "heading"
    )
    instructions.insert(
        "end",
        "Hit the Browse button and select the Excel files you want to compare. \n"
        "These files should be the RadioMusic.com Excel file and the same genre master list provided in the drive. \n"
        "You will need to remove the top rows from the RadioMusic.com Excel File. \n"
        "The top rows should read title and artist instead of the buying information. \n\n"
    )

    instructions.insert(
        "end",
        "2. Choose where to save the results\n",
        "heading"
    )
    instructions.insert(
        "end",
        "The output field shows where the results will be saved. \n"
        "You can keep the suggested location or click Browse to choose a different folder and filename. \n"
        "The results are saved as an Excel .xlsx file.\n\n"
    )

    instructions.insert(
        "end",
        "3. Compare the songs\n",
        "heading"
    )
    instructions.insert(
        "end",
        "Click Compare Songs and wait for the comparison to finish. \n"
        "A message will tell you how many unique songs were found and where the results were saved.\n\n"
    )

    instructions.insert(
        "end",
        "4. Understand the results/output\n",
        "heading"
    )
    instructions.insert(
        "end",
        "Open the resulting Excel file. It contains three columns:\n"
        "Title: The title of the song \n"
        "Artist: The artist of the song \n"
        "File: the file where the song originates from"
        "\n\n"
    )

    instructions.insert(
        "end",
        "5. Tip and notes\n",
        "heading"
    )
    instructions.insert(
        "end",
        "Small spelling differences may still match.\n"
        "Capitalization, spaces, and punctuation are ignored during matching.\n"
        "Check the output if song titles or artist names are very similar. \n"
        "The matching library I used is not exact. It filters out spelling mistakes, "
        "but you still must manually look through the output file to ensure no songs are missed. \n\n"
    )
    instructions.insert(
        "end",
        "Credits!\n",
        "heading"
    )
    instructions.insert(
        "end",
        "Programmed originally by Eliza Boulay. I hope you find it useful! \n"
        "If you have any questions, email me at elizabeth.boulay0@gmail.com \n"
    )

    # Prevent editing the instructions
    instructions.config(state="disabled")

# Easter Egg!
help_click_times = []

def handle_help_click(event=None):
    global help_click_times

    current_time = time.monotonic()

    help_click_times = [
        click_time for click_time in help_click_times
        if current_time - click_time <= 1.0
    ]

    help_click_times.append(current_time)

    if len(help_click_times) >= 3:
        sound_path = Path(resource_path("Seal_Noises_fixed.wav"))

        try:
            winsound.PlaySound(
                str(sound_path),
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )
        except RuntimeError as error:
            messagebox.showerror(
                "Sound Error",
                f"Could not play the custom WAV:\n\n{error}",
                parent=root
            )
        help_click_times = []
    show_help()

# Run the comparison
def run_comparison():
    file1 = file1_var.get().strip()
    file2 = file2_var.get().strip()
    output_file = output_var.get().strip()

    if not file1 or not file2:
        messagebox.showwarning(
            "Missing files",
            "Please select both Excel files.",
            parent=root
        )
        return

    if not output_file:
        messagebox.showwarning(
            "Missing output location",
            "Please choose where to save the results.",
            parent=root
        )
        return

    if not output_file.lower().endswith(".xlsx"):
        messagebox.showwarning(
            "Invalid output file",
            "The output filename must end in .xlsx.",
            parent=root
        )
        return

    if Path(file1).resolve() == Path(file2).resolve():
        messagebox.showwarning(
            "Same input file",
            "Please select two different Excel files.",
            parent=root
        )
        return

    if (
        Path(output_file).resolve() == Path(file1).resolve()
        or Path(output_file).resolve() == Path(file2).resolve()
    ):
        messagebox.showwarning(
            "Invalid output location",
            "Choose a new output file, not one of the input files.",
            parent=root
        )
        return

    compare_button.config(state="disabled")
    status_var.set("Comparing songs...")
    root.update_idletasks()

    try:
        unique_songs = compare_songs(file1, file2)
        unique_songs.to_excel(output_file, index=False)

        status_var.set("Comparison complete!")

        messagebox.showinfo(
            "Success",
            f"Comparison complete!\n\n"
            f"Unique songs found: {len(unique_songs)}\n\n"
            f"Results saved to:\n{output_file}",
            parent=root
        )

    except KeyError as error:
        status_var.set("Comparison failed.")

        messagebox.showerror(
            "Missing column",
            "Both Excel files must contain columns "
            "named 'title' and 'artist'.\n\n"
            f"Details: {error}",
            parent=root
        )

    except Exception as error:
        status_var.set("Comparison failed.")

        messagebox.showerror(
            "Error",
            "The comparison could not be completed :( \n\n"
            f"Details: {error}",
            parent=root
        )

    finally:
        compare_button.config(state="normal")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = Path(__file__).resolve().parent

    return str(Path(base_path) / relative_path)

# Create the application window
root = tk.Tk()
root.title("Music List Comparison")
root.geometry("800x500")
root.minsize(800, 500)
root.configure(bg=BACKGROUND_COLOR)

# Style the application widgets
style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Pink.TFrame",
    background=BACKGROUND_COLOR
)

style.configure(
    "Pink.TLabel",
    background=BACKGROUND_COLOR,
    foreground=TEXT_COLOR,
    font=("Arial", 10)
)

style.configure(
    "Heading.TLabel",
    background=BACKGROUND_COLOR,
    foreground=TEXT_COLOR,
    font=("Arial", 20, "bold")
)

style.configure(
    "Pink.TEntry",
    fieldbackground=ENTRY_COLOR,
    foreground=TEXT_COLOR,
    padding=6
)

style.configure(
    "Pink.TButton",
    background=BUTTON_COLOR,
    foreground=TEXT_COLOR,
    font=("Arial", 10, "bold"),
    padding=(12, 7),
    borderwidth=0
)

style.map(
    "Pink.TButton",
    background=[
        ("active", BUTTON_ACTIVE_COLOR),
        ("pressed", BUTTON_ACTIVE_COLOR),
        ("disabled", "#E8C7D2")
    ],
    foreground=[
        ("disabled", "#8C7A80")
    ]
)

# Main layout
main_frame = ttk.Frame(
    root,
    padding=25,
    style="Pink.TFrame"
)
main_frame.pack(fill="both", expand=True)

# Title and How to Use button
top_row = ttk.Frame(
    main_frame,
    style="Pink.TFrame"
)
top_row.pack(fill="x", pady=(0, 8))

heading = ttk.Label(
    top_row,
    text="Music List Comparison",
    style="Heading.TLabel"
)
heading.pack(side="left", anchor="w")

# Help Icon
help_image = tk.PhotoImage(
    file=resource_path("seal question mark.png")
)

help_image = help_image.subsample(10, 10)

# Create a frame for the help button
help_frame = tk.Frame(
    top_row,
    bg=BACKGROUND_COLOR
)
help_frame.pack(side="right", anchor="e")

# Display the picture as a button
help_button = tk.Button(
    help_frame,
    image=help_image,
    command=handle_help_click,
    bg=BACKGROUND_COLOR,
    activebackground=BACKGROUND_COLOR,
    relief="flat",
    borderwidth=0,
    cursor="hand2"
)

help_button.pack(anchor="center")

# Label underneath the help button
help_label = tk.Label(
    help_frame,
    text="Click here for help",
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    font=("Arial", 10),
    cursor="hand2"
)
help_label.pack(anchor="center")
help_label.bind("<Button-1>", handle_help_click)

description = ttk.Label(
    main_frame,
    text="Select two Excel files to find songs that are not in common.",
    style="Pink.TLabel"
)
description.pack(anchor="w", pady=(0, 22))

# First input file
file1_var = tk.StringVar()

ttk.Label(
    main_frame,
    text="First file to compare:",
    style="Pink.TLabel"
).pack(anchor="w")

row1 = ttk.Frame(main_frame, style="Pink.TFrame")
row1.pack(fill="x", pady=(5, 15))

ttk.Entry(
    row1,
    textvariable=file1_var,
    style="Pink.TEntry"
).pack(side="left", fill="x", expand=True)

ttk.Button(
    row1,
    text="Browse...",
    style="Pink.TButton",
    command=lambda: browse_input(file1_var)
).pack(side="left", padx=(10, 0))

# Second input file
file2_var = tk.StringVar()

ttk.Label(
    main_frame,
    text="Second file to compare:",
    style="Pink.TLabel"
).pack(anchor="w")

row2 = ttk.Frame(main_frame, style="Pink.TFrame")
row2.pack(fill="x", pady=(5, 15))

ttk.Entry(
    row2,
    textvariable=file2_var,
    style="Pink.TEntry"
).pack(side="left", fill="x", expand=True)

ttk.Button(
    row2,
    text="Browse...",
    style="Pink.TButton",
    command=lambda: browse_input(file2_var)
).pack(side="left", padx=(10, 0))

# Output file
output_var = tk.StringVar(
    value=str(Path.home() / "unique_songs.xlsx")
)

ttk.Label(
    main_frame,
    text="Save results as:",
    style="Pink.TLabel"
).pack(anchor="w")

row3 = ttk.Frame(main_frame, style="Pink.TFrame")
row3.pack(fill="x", pady=(5, 20))

ttk.Entry(
    row3,
    textvariable=output_var,
    style="Pink.TEntry"
).pack(side="left", fill="x", expand=True)

ttk.Button(
    row3,
    text="Browse...",
    style="Pink.TButton",
    command=browse_output
).pack(side="left", padx=(10, 0))

# Compare button
compare_button = ttk.Button(
    main_frame,
    text="Compare Songs",
    style="Pink.TButton",
    command=run_comparison
)
compare_button.pack(anchor="w", pady=(0, 15))

# Status message at the bottom
status_var = tk.StringVar(value="Ready.")

ttk.Label(
    main_frame,
    textvariable=status_var,
    style="Pink.TLabel"
).pack(anchor="w", pady=(0, 5))

# Start the application
root.mainloop()