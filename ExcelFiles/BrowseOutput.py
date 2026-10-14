from tkinter import filedialog

# Browse for the output location
def browse_output(variable, parent):
    filename = filedialog.asksaveasfilename(
        title="Save comparison results",
        defaultextension=".xlsx",
        initialfile="unique_songs.xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        parent=parent
    )

    if filename:
        variable.set(filename)

help_window = None