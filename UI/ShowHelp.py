from tkinter import ttk
import tkinter as tk
help_window = None


# Display the How to Use window
def show_help(root):
    global help_window
    colors = root.app_theme

    # If the help window is already open, bring it to the front
    if help_window is not None and help_window.winfo_exists():
        help_window.lift()
        help_window.focus_force()
        return

    # Create a separate help window
    help_window = tk.Toplevel(root)
    help_window.title("How to Use")
    help_window.geometry("600x500")
    help_window.configure(bg=colors["background"])

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
        bg=colors["entry"],
        fg=colors["text"],
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
        "Dark mode was added by Nikki Gardiner, along with modifying the program to be easier to expand and maintain. \n"
        "If you have any questions, please contact Eliza Boulay and it will be forwarded to me. \n"
    )

    # Prevent editing the instructions
    instructions.config(state="disabled")

# Easter Egg!
help_click_times = []