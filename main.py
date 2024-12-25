#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup


def fetch_published_doc_content(doc_url: str) -> str:
    print(f"Fetching doc content from: {doc_url}")
    response = requests.get(doc_url)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch published document data. "
            f"HTTP status code: {response.status_code}. "
            f"Check the link and its publishing settings."
        )

    return response.text


def parse_doc_table(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    table_data = []

    all_tables = soup.find_all("table")
    if not all_tables:
        print("No <table> elements found in the published doc HTML.")
        return table_data

    target_table = all_tables[0]
    rows = target_table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        x_str = cols[0].get_text(strip=True)
        char_str = cols[1].get_text(strip=True)
        y_str = cols[2].get_text(strip=True)

        try:
            x_val = int(x_str)
            y_val = int(y_str)
        except ValueError:
            continue

        table_data.append((x_val, y_val, char_str))

    return table_data


def build_and_print_grid(coordinate_data):
    if not coordinate_data:
        print("No coordinate data to display or parse.")
        return

    max_x = max(x for x, _, _ in coordinate_data)
    max_y = max(y for _, y, _ in coordinate_data)

    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y, ch in coordinate_data:
        grid[y][x] = ch

    for row in reversed(grid):
        print("".join(row))


def print_grid_from_published_doc(doc_url: str):
    html_content = fetch_published_doc_content(doc_url)
    table_data = parse_doc_table(html_content)

    if table_data:
        print("\nExtracted Data (x, y, char):")
        for data_row in table_data:
            print(data_row)

        print("\nResulting Grid:\n")
    else:
        print("No valid (x, y, char) data found in the published doc.\n")

    build_and_print_grid(table_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <PublishedGoogleDocURL>")
        sys.exit(1)

    doc_url = sys.argv[1]
    print_grid_from_published_doc(doc_url)
