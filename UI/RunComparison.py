# Run the comparison
from pathlib import Path
from tkinter import messagebox

from ExcelFiles.CompareSongs import compare_songs


def run_comparison(file1_var, file2_var, output_var, root, compare_button, status_var):
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