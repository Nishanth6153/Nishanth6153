from __future__ import annotations

import os
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance


USERNAME = "Nishanth6153"

ROOT = Path(__file__).resolve().parent
AVATAR_PATH = ROOT / "assets" / "avatar.jpg"
OUTPUT_PATH = ROOT / "assets" / "profile-card.png"

API_BASE = "https://api.github.com"
GRAPHQL_URL = "https://api.github.com/graphql"


# ============================================================
# PERSONAL INFORMATION
# ============================================================

PROFILE = {
    "name": "NISHANTH G",
    "field": "ARTIFICIAL INTELLIGENCE & DATA SCIENCE",
    "designation": "AI / DATA SCIENCE",
    "specialization": [
        "MACHINE LEARNING",
        "FULL STACK DEVELOPMENT",
        "DEVOPS",
    ],
    "systems": [
        "PYTHON / JAVA / REACT",
        "FASTAPI / SUPABASE / DOCKER",
    ],
    "status": [
        "SYSTEMS ENGINEERING",
        "SOFTWARE DEVELOPMENT",
        "DATA & INTELLIGENT SYSTEMS",
    ],
    "identifier": "NG-6153",
}


# ============================================================
# COLORS
# ============================================================

BG = "#050A0D"
PANEL = "#071116"
PANEL_2 = "#09151A"

CYAN = "#A8D8E1"
CYAN_BRIGHT = "#D2F4F8"
CYAN_DARK = "#4F8A95"
CYAN_DIM = "#6D9EA7"

GRID = "#0B242A"
BORDER = "#88AEB6"
TEXT = "#D4E4E7"
MUTED = "#76939A"


# ============================================================
# FONTS
# ============================================================

FONT_REGULAR_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD_PATH if bold else FONT_REGULAR_PATH

    if not Path(path).exists():
        return ImageFont.load_default()

    return ImageFont.truetype(path, size=size)


# ============================================================
# GITHUB API
# ============================================================

def github_headers() -> dict[str, str]:
    token = os.getenv("GITHUB_TOKEN", "").strip()

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def get_user() -> dict[str, Any]:
    url = f"{API_BASE}/users/{USERNAME}"

    response = requests.get(
        url,
        headers=github_headers(),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_repositories() -> list[dict[str, Any]]:
    repositories: list[dict[str, Any]] = []

    page = 1

    while True:
        response = requests.get(
            f"{API_BASE}/users/{USERNAME}/repos",
            headers=github_headers(),
            params={
                "per_page": 100,
                "page": page,
                "type": "owner",
            },
            timeout=30,
        )

        response.raise_for_status()

        batch = response.json()

        if not batch:
            break

        repositories.extend(batch)

        if len(batch) < 100:
            break

        page += 1

    return repositories


def get_contributions_last_year() -> int:
    token = os.getenv("GITHUB_TOKEN", "").strip()

    if not token:
        return 0

    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """

    response = requests.post(
        GRAPHQL_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "query": query,
            "variables": {
                "login": USERNAME
            },
        },
        timeout=30,
    )

    response.raise_for_status()

    payload = response.json()

    if payload.get("errors"):
        raise RuntimeError(payload["errors"])

    return int(
        payload["data"]["user"]["contributionsCollection"]
        ["contributionCalendar"]["totalContributions"]
    )


def calculate_account_age(created_at: str) -> str:
    created = datetime.fromisoformat(
        created_at.replace("Z", "+00:00")
    )

    now = datetime.now(timezone.utc)

    total_months = (
        (now.year - created.year) * 12
        + (now.month - created.month)
    )

    if now.day < created.day:
        total_months -= 1

    years = total_months // 12
    months = total_months % 12

    if years == 0:
        return f"{months}M"

    return f"{years}Y {months}M"


def collect_github_stats() -> dict[str, Any]:
    user = get_user()
    repositories = get_repositories()

    owned_non_forks = [
        repo
        for repo in repositories
        if not repo.get("fork", False)
    ]

    stars = sum(
        int(repo.get("stargazers_count", 0))
        for repo in owned_non_forks
    )

    contributions = get_contributions_last_year()

    return {
        "repos": int(user.get("public_repos", 0)),
        "followers": int(user.get("followers", 0)),
        "stars": stars,
        "contributions": contributions,
        "account_age": calculate_account_age(
            user["created_at"]
        ),
    }


# ============================================================
# ASCII PORTRAIT
# ============================================================

ASCII_CHARS = " .,:;irsXA253hMHGS#9B&@"


def make_ascii_portrait(
    image_path: Path,
    width: int = 82,
    height: int = 52,
) -> list[tuple[str, list[int]]]:

    image = Image.open(image_path).convert("RGB")

    # Crop to portrait ratio while keeping face centered.
    image = ImageOps.fit(
        image,
        (width, height * 2),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.48),
    )

    image = ImageEnhance.Contrast(image).enhance(1.25)
    image = ImageEnhance.Sharpness(image).enhance(1.4)

    grayscale = ImageOps.grayscale(image)

    # Compress vertically because terminal characters are taller
    # than they are wide.
    grayscale = grayscale.resize(
        (width, height),
        Image.Resampling.LANCZOS,
    )

    pixels = list(grayscale.getdata())

    rows: list[tuple[str, list[int]]] = []

    for y in range(height):
        chars: list[str] = []
        brightness_values: list[int] = []

        for x in range(width):
            value = pixels[y * width + x]

            index = int(
                value / 255 * (len(ASCII_CHARS) - 1)
            )

            chars.append(ASCII_CHARS[index])
            brightness_values.append(value)

        rows.append(
            (
                "".join(chars),
                brightness_values,
            )
        )

    return rows


# ============================================================
# DECORATIVE GRID
# ============================================================

def draw_background_grid(
    draw: ImageDraw.ImageDraw,
    width: int,
    height: int,
) -> None:

    spacing = 24

    for x in range(0, width, spacing):
        draw.line(
            [(x, 0), (x, height)],
            fill=GRID,
            width=1,
        )

    for y in range(0, height, spacing):
        draw.line(
            [(0, y), (width, y)],
            fill=GRID,
            width=1,
        )


# ============================================================
# TEXT HELPERS
# ============================================================

def draw_label(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
) -> None:

    draw.text(
        xy,
        text,
        font=font(20),
        fill=CYAN,
    )


def draw_value(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    size: int = 24,
) -> None:

    draw.text(
        xy,
        text,
        font=font(size, bold=True),
        fill=TEXT,
    )


# ============================================================
# ASCII PORTRAIT DRAWING
# ============================================================

def draw_ascii_portrait(
    draw: ImageDraw.ImageDraw,
    rows: list[tuple[str, list[int]]],
    x: int,
    y: int,
    char_size: int = 9,
) -> None:

    mono = font(char_size)

    # Approximate terminal character dimensions.
    bbox = draw.textbbox((0, 0), "@", font=mono)

    char_width = max(5, bbox[2] - bbox[0])
    char_height = max(8, bbox[3] - bbox[1] + 2)

    for row_index, (line, brightness) in enumerate(rows):

        yy = y + row_index * char_height

        for col_index, character in enumerate(line):

            if character == " ":
                continue

            xx = x + col_index * char_width

            value = brightness[col_index]

            # Bright pixels become brighter cyan.
            strength = 0.30 + (value / 255.0) * 0.70

            r = int(70 + 150 * strength)
            g = int(120 + 110 * strength)
            b = int(130 + 115 * strength)

            draw.text(
                (xx, yy),
                character,
                font=mono,
                fill=(r, g, b),
            )


# ============================================================
# CARD CREATION
# ============================================================

def create_card(stats: dict[str, Any]) -> None:

    WIDTH = 1400
    HEIGHT = 900

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        BG,
    )

    draw = ImageDraw.Draw(image)

    draw_background_grid(
        draw,
        WIDTH,
        HEIGHT,
    )

    # ========================================================
    # OUTER FRAME
    # ========================================================

    draw.rectangle(
        [28, 28, WIDTH - 28, HEIGHT - 28],
        outline=BORDER,
        width=2,
    )

    # Corner markers
    marker = 22

    corners = [
        (28, 28),
        (WIDTH - 28, 28),
        (28, HEIGHT - 28),
        (WIDTH - 28, HEIGHT - 28),
    ]

    for cx, cy in corners:

        draw.line(
            [(cx, cy), (cx + marker, cy)],
            fill=CYAN_BRIGHT,
            width=2,
        )

        draw.line(
            [(cx, cy), (cx, cy + marker)],
            fill=CYAN_BRIGHT,
            width=2,
        )

    # ========================================================
    # HEADER
    # ========================================================

    header_y = 48
    header_h = 68

    draw.rectangle(
        [52, header_y, WIDTH - 52, header_y + header_h],
        fill=PANEL,
        outline=BORDER,
        width=2,
    )

    draw.text(
        (74, 65),
        "NISHANTH // SYSTEM ID",
        font=font(27, bold=True),
        fill=CYAN_BRIGHT,
    )

    draw.text(
        (1010, 65),
        "SIGNAL: ONLINE",
        font=font(24),
        fill=CYAN,
    )

    # Battery indicator
    bx = 1240
    by = 64

    draw.rectangle(
        [bx, by, bx + 70, by + 28],
        outline=CYAN,
        width=2,
    )

    draw.rectangle(
        [bx + 70, by + 8, bx + 76, by + 20],
        fill=CYAN,
    )

    for i in range(4):
        draw.rectangle(
            [
                bx + 5 + i * 15,
                by + 5,
                bx + 16 + i * 15,
                by + 23,
            ],
            fill=CYAN,
        )

    # ========================================================
    # IDENTITY
    # ========================================================

    draw.text(
        (55, 140),
        "USER",
        font=font(19),
        fill=CYAN,
    )

    draw.text(
        (55, 172),
        PROFILE["name"],
        font=font(47, bold=True),
        fill=CYAN_BRIGHT,
    )

    draw.text(
        (55, 225),
        PROFILE["field"],
        font=font(21),
        fill=CYAN,
    )

    draw.text(
        (1130, 227),
        PROFILE["identifier"],
        font=font(20),
        fill=CYAN,
    )

    # ========================================================
    # MAIN PANELS
    # ========================================================

    left_x = 55
    right_x = 735

    top_y = 275
    bottom_y = 680

    # Left portrait panel
    draw.rectangle(
        [left_x, top_y, 680, bottom_y],
        fill=PANEL,
        outline=BORDER,
        width=2,
    )

    # Right information panel
    draw.rectangle(
        [right_x, top_y, WIDTH - 55, bottom_y],
        fill=PANEL,
        outline=BORDER,
        width=2,
    )

    # ========================================================
    # PORTRAIT
    # ========================================================

    ascii_rows = make_ascii_portrait(
        AVATAR_PATH,
        width=82,
        height=45,
    )

    draw_ascii_portrait(
        draw,
        ascii_rows,
        x=75,
        y=302,
        char_size=9,
    )

    # ========================================================
    # RIGHT INFORMATION
    # ========================================================

    x = right_x + 25
    y = top_y + 25

    draw_label(
        draw,
        (x, y),
        "DESIGNATION:",
    )

    draw_value(
        draw,
        (x, y + 28),
        PROFILE["designation"],
        size=23,
    )

    y += 88

    draw_label(
        draw,
        (x, y),
        "SPECIALIZATION:",
    )

    y += 30

    for item in PROFILE["specialization"]:

        draw.text(
            (x, y),
            item,
            font=font(20, bold=True),
            fill=TEXT,
        )

        y += 29

    y += 15

    draw_label(
        draw,
        (x, y),
        "PRIMARY SYSTEMS:",
    )

    y += 30

    for item in PROFILE["systems"]:

        draw.text(
            (x, y),
            item,
            font=font(20, bold=True),
            fill=TEXT,
        )

        y += 29

    y += 16

    draw_label(
        draw,
        (x, y),
        "PROFILE STATUS:",
    )

    y += 30

    for item in PROFILE["status"]:

        draw.text(
            (x, y),
            item,
            font=font(18, bold=True),
            fill=TEXT,
        )

        y += 27

    # ========================================================
    # LIVE GITHUB DATA PANEL
    # ========================================================

    stats_y = 700

    draw.rectangle(
        [55, stats_y, WIDTH - 55, 765],
        fill=PANEL_2,
        outline=BORDER,
        width=2,
    )

    live_text = (
        f"REPOS {stats['repos']:>4}     "
        f"STARS {stats['stars']:>4}     "
        f"FOLLOWERS {stats['followers']:>4}     "
        f"CONTRIBUTIONS/1Y {stats['contributions']:>4}"
    )

    draw.text(
        (78, stats_y + 19),
        live_text,
        font=font(18, bold=True),
        fill=CYAN_BRIGHT,
    )

    # ========================================================
    # AUTHORIZATION SECTION
    # ========================================================

    auth_y = 782

    draw.text(
        (58, auth_y),
        "AUTHORIZATION: GRANTED",
        font=font(19),
        fill=CYAN,
    )

    draw.text(
        (58, auth_y + 28),
        "DEVELOPER // AI // SOFTWARE SYSTEMS",
        font=font(16),
        fill=MUTED,
    )

    account_age_text = (
        f"GITHUB ACCOUNT AGE: {stats['account_age']}"
    )

    draw.text(
        (875, auth_y),
        account_age_text,
        font=font(16),
        fill=CYAN_DIM,
    )

    draw.text(
        (1120, auth_y + 28),
        "NG-6153",
        font=font(19, bold=True),
        fill=CYAN_BRIGHT,
    )

    # ========================================================
    # CRT SCANLINES
    # ========================================================

    overlay = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0),
    )

    overlay_draw = ImageDraw.Draw(overlay)

    for y in range(0, HEIGHT, 5):
        overlay_draw.line(
            [(0, y), (WIDTH, y)],
            fill=(130, 220, 230, 16),
            width=1,
        )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay,
    )

    # ========================================================
    # SAVE
    # ========================================================

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image.convert("RGB").save(
        OUTPUT_PATH,
        format="PNG",
        optimize=True,
    )

    print(f"Generated: {OUTPUT_PATH}")


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    if not AVATAR_PATH.exists():
        raise FileNotFoundError(
            f"Avatar not found: {AVATAR_PATH}"
        )

    print("Fetching GitHub statistics...")

    stats = collect_github_stats()

    print("GitHub statistics:")
    print(stats)

    print("Generating cyberpunk profile card...")

    create_card(stats)

    print("Done.")


if __name__ == "__main__":
    main()
