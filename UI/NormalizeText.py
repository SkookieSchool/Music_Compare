# Normalize text
def normalize_text(series):
    return (
        series.astype("string")
        .str.casefold()
        .str.replace(r"['\u2018\u2019]", "", regex=True)
        .str.replace(r"[\W_]+", "", regex=True)
    )