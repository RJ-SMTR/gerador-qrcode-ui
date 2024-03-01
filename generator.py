from pathlib import Path
import random
from sys import argv
from typing import List, Union

import jinja2
import qrcode
from tqdm import tqdm


CHARSET: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
LENGTH: int = 4
OUTPUT_DIR: Path = Path("output")
URL_TEMPLATE: jinja2.Template = jinja2.Template(
    "https://mobilidade.rio/{{ code }}")

def generate_url(code: str) -> str:
    return URL_TEMPLATE.render(code=code)


def generate_qr(code: str) -> str:
    img = qrcode.make(generate_url(code))
    img.save(OUTPUT_DIR / f"{code}.png")

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python3 generator.py <list of codes separated by commas>")
        exit(1)

    codes_list = argv[1].split(',')

    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir()

    for code in tqdm(codes_list):
        generate_qr(code)

    print(f"Generated {len(codes_list)} codes")
    print(f"Output directory: {OUTPUT_DIR}")
