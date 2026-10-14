# Music Compare

Music Compare is a desktop application made for WQRI that compares two music
spreadsheets and creates a list of songs that are not shared between them.

Original programming by Eliza Boulay.

Dark mode & modifying the program to be easier to expand and maintain by Nikki Gardiner.

## Features

- Compare two Excel workbooks.
- Match songs using normalized titles and artists with fuzzy matching.
- Ignore capitalization, spaces, punctuation, and common apostrophe
  differences during matching.
- Save unmatched songs to a new `.xlsx` workbook.
- Choose between light, dark, and dark high-contrast themes.
- Use the built-in help window for usage instructions.

## Requirements

- Python 3
- A graphical desktop environment with Tk available
- The packages listed in `requirements.txt`

Tkinter and `pathlib` are provided by Python/the operating system and are not
installed through pip. On some Linux distributions, Tkinter must be installed
separately.

## Installation

Create and activate a virtual environment, then install the project
dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS, use:

```bash
source .venv/bin/activate
```

## Running the application

From the project directory, run:

```bash
python Music_Compare_GUI_V2.py
```

The application opens a window where you can:

1. Select the first Excel file.
2. Select the second Excel file.
3. Choose an output filename, or keep the default
   `unique_songs.xlsx` in your home directory.
4. Click **Compare Songs**.

The two input files must be different. The output file must use the `.xlsx`
extension and must not overwrite either input file.

## Input spreadsheet format

Each workbook should contain columns named:

```text
title
artist
```

Column names are matched case-insensitively and surrounding whitespace is
ignored. Supported input formats include `.xlsx`, `.xlsm`, and `.xls`.

Rows without a title or artist are ignored. Duplicate songs within each input
file are removed before comparison.

## Matching and output

The comparison uses fuzzy matching so small spelling differences can still
match. A song is considered shared only when both its title and artist meet
the configured similarity thresholds in
`Consistents/SimilarityThresholds.py`.

The generated workbook contains:

| Column | Description |
| --- | --- |
| `Title` | Original song title |
| `Artist` | Original artist name |
| `File` | Input file where the unmatched song was found |

Review the output manually when titles or artist names are very similar.
Fuzzy matching is intended to reduce duplicate work, but it is not a
replacement for verifying the results.

## Themes and help

Use the theme controls at the top of the application to switch between:

- **Light**: the default pink theme.
- **Dark**: a dark background with muted pink controls.

## Project structure

```text
Music_Compare_GUI_V2.py       Main Tkinter application
ExcelFiles/                   Spreadsheet selection and comparison logic
UI/                           GUI helpers, themes, assets, and help content
Consistents/                  Shared colors and similarity thresholds
requirements.txt              Python package dependencies
```

## Troubleshooting

### `ModuleNotFoundError`

Make sure the virtual environment is active and reinstall the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Tkinter is unavailable on Linux

Install the Tk package supplied by your distribution, then run the
application again. On Debian/Ubuntu:

```bash
sudo apt install python3-tk
```

### The comparison reports a missing column

Rename the spreadsheet columns to `title` and `artist`, then try again.

## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).
