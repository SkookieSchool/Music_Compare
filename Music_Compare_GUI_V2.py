# Program Created by Eliza Boulay
# October 2026
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from Consistents.AppColors import THEMES
from ExcelFiles.BrowseInput import browse_input
from ExcelFiles.BrowseOutput import browse_output
from UI.ApplyTheme import apply_theme
from UI.HandleHelpClick import handle_help_click
from UI.ResourcePath import resource_path
from UI.RunComparison import run_comparison
from UI.SetTheme import set_theme

# Create the application window
root = tk.Tk()
root.title("Music List Comparison")
root.geometry("800x500")
root.minsize(800, 500)

# Style the application widgets
style = ttk.Style(root)
style.theme_use("clam")

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

mode_frame = tk.Frame(top_row)
mode_frame.pack(side="right", anchor="e", padx=(10, 10))

tk.Button(
    mode_frame,
    text="Light",
    command=lambda: set_theme(
        "light", root, style, mode_frame, help_frame, help_button, help_label
    ),
    relief="flat",
    borderwidth=0,
    cursor="hand2"
).pack(side="left", padx=2)
tk.Button(
    mode_frame,
    text="Dark",
    command=lambda: set_theme(
        "dark", root, style, mode_frame, help_frame, help_button, help_label
    ),
    relief="flat",
    borderwidth=0,
    cursor="hand2"
).pack(side="left", padx=2)

# Help Icon
help_image = tk.PhotoImage(file=resource_path("sealquestionmark.png"))

help_image = help_image.subsample(10, 10)

# Create a frame for the help button
help_frame = tk.Frame(
    top_row,
    bg=THEMES["light"]["background"]
)
help_frame.pack(side="right", anchor="e")

# Display the picture as a button
help_button = tk.Button(
    help_frame,
    image=help_image,
    command=lambda: handle_help_click(root),
    bg=THEMES["light"]["background"],
    activebackground=THEMES["light"]["background"],
    relief="flat",
    borderwidth=0,
    cursor="hand2"
)

help_button.pack(anchor="center")

# Label underneath the help button
help_label = tk.Label(
    help_frame,
    text="Click here for help",
    bg=THEMES["light"]["background"],
    fg=THEMES["light"]["text"],
    font=("Arial", 10),
    cursor="hand2"
)
help_label.pack(anchor="center")
help_label.bind("<Button-1>", lambda event: handle_help_click(root))

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
    command=lambda: browse_input(file1_var, root)
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
    command=lambda: browse_input(file2_var, root)
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
    command=lambda: browse_output(output_var, root)
).pack(side="left", padx=(10, 0))

# Compare button
compare_button = ttk.Button(
    main_frame,
    text="Compare Songs",
    style="Pink.TButton",
    command=lambda: run_comparison(
        file1_var,
        file2_var,
        output_var,
        root,
        compare_button,
        status_var
    )
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
apply_theme(
    "light",
    root,
    style,
    mode_frame,
    help_frame,
    help_button,
    help_label
)
root.mainloop()