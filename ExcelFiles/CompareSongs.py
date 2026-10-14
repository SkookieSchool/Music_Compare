from pathlib import Path

import pandas as pd
from rapidfuzz import process, fuzz

from Consistents.SimilarityThresholds import TITLE_THRESHOLD, ARTIST_THRESHOLD
from ExcelFiles.PrepareSheet import prepare_sheet


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