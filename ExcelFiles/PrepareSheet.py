from UI.NormalizeText import normalize_text

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