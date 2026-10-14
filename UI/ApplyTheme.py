from Consistents.AppColors import THEMES

def apply_theme(
    theme_name,
    root,
    style,
    mode_frame,
    help_frame,
    help_button,
    help_label
):
    colors = THEMES[theme_name]
    root.app_theme = colors
    root.configure(bg=colors["background"])

    style.configure("Pink.TFrame", background=colors["background"])
    style.configure(
        "Pink.TLabel",
        background=colors["background"],
        foreground=colors["text"],
        font=("Arial", 10)
    )
    style.configure(
        "Heading.TLabel",
        background=colors["background"],
        foreground=colors["text"],
        font=("Arial", 20, "bold")
    )
    style.configure(
        "Pink.TEntry",
        fieldbackground=colors["entry"],
        foreground=colors["text"],
        insertcolor=colors["text"],
        padding=6
    )
    style.configure(
        "Pink.TButton",
        background=colors["button"],
        foreground=colors["text"],
        font=("Arial", 10, "bold"),
        padding=(12, 7),
        borderwidth=0
    )
    style.map(
        "Pink.TButton",
        background=[
            ("active", colors["button_active"]),
            ("pressed", colors["button_active"]),
            ("disabled", colors["button"])
        ],
        foreground=[
            ("disabled", colors["disabled"])
        ]
    )

    mode_frame.configure(bg=colors["background"])
    for mode_button in mode_frame.winfo_children():
        mode_button.configure(
            bg=colors["button"],
            fg=colors["text"],
            activebackground=colors["button_active"],
            activeforeground=colors["text"]
        )

    help_frame.configure(bg=colors["background"])
    help_button.configure(
        bg=colors["background"],
        activebackground=colors["background"]
    )
    help_label.configure(
        bg=colors["background"],
        fg=colors["text"]
    )