from tkinter import filedialog

# Browse for an input Excel file
def browse_input(variable, parent):
    filename = filedialog.askopenfilename(
        title="Select an Excel file",
        filetypes=[
            ("Excel files", "*.xlsx *.xls *.xlsm"),
            ("All files", "*.*")
        ],
        parent=parent
    )

    if filename:
        variable.set(filename)