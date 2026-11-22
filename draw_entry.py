#!/usr/bin/env python3
"""Draw "The Daily Globe" — Saturday 21 November 2026 front page.

One image, 1024x1024, drawn from scratch with PIL: a newspaper front
page summing up the six verified stories of 21 November 2026 plus a
three-item footer strip. No network, no external assets, fully
deterministic (same bytes on every run).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# ---- palette ---------------------------------------------------------
PAPER = (247, 242, 230)      # warm newsprint cream
CARD = (255, 253, 244)       # slightly lighter card fill
INK = (28, 28, 28)           # near-black headline ink
BODY = (74, 74, 68)          # grey body text
NAVY = (24, 39, 66)          # masthead + accents
CRIMSON = (176, 42, 48)      # kicker red
GOLD = (227, 168, 28)        # masthead day + star
TEAL = (20, 101, 95)         # climate/markets accent
ORANGE = (217, 122, 30)      # explosion / flame
HAIR = (201, 194, 174)       # hairline rules
MUTED = (102, 102, 96)       # credit line

# ---- fonts -----------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, fnt_path, start_size, max_width, max_lines, min_size=24):
    """Shrink the font until the wrapped text fits in max_lines lines."""
    size = start_size
    while size > min_size:
        fnt = font(fnt_path, size)
        lines = wrap_text(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 2
    fnt = font(fnt_path, min_size)
    return fnt, wrap_text(draw, text, fnt, max_width)


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines top-down; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---- little pictures -------------------------------------------------
def starburst(draw, cx, cy, outer, inner, spikes, fill):
    pts = []
    for i in range(spikes * 2):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def five_star(draw, cx, cy, radius, fill, outline, width=3):
    pts = []
    for i in range(10):
        r = radius if i % 2 == 0 else radius * 0.42
        a = math.pi * i / 5 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill, outline=outline, width=width)
    return pts


def flame(draw, cx, base_y, w, h, outer, inner):
    """A simple flame: outer teardrop, inner smaller teardrop."""
    top = base_y - h
    draw.polygon([
        (cx, top),
        (cx + w * 0.42, base_y - h * 0.55),
        (cx + w * 0.30, base_y - h * 0.30),
        (cx + w * 0.48, base_y),
        (cx - w * 0.48, base_y),
        (cx - w * 0.30, base_y - h * 0.30),
        (cx - w * 0.42, base_y - h * 0.55),
    ], fill=outer)
    draw.polygon([
        (cx, base_y - h * 0.62),
        (cx + w * 0.22, base_y - h * 0.28),
        (cx + w * 0.26, base_y),
        (cx - w * 0.26, base_y),
        (cx - w * 0.22, base_y - h * 0.28),
    ], fill=inner)


def globe(draw, cx, cy, r, colour):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=colour, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=colour, width=2)
    draw.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
             180, 360, fill=colour, width=2)
    # clock hands on the globe face
    draw.line([cx, cy, cx, cy - r * 0.55], fill=CRIMSON, width=4)
    draw.line([cx, cy, cx + r * 0.45, cy + r * 0.25], fill=INK, width=4)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)


def chart_down(draw, x, y, w, h):
    """Three descending bars and a down-right arrow."""
    bars = [0.95, 0.62, 0.34]
    bw = w // 4
    for i, frac in enumerate(bars):
        bh = int(h * frac)
        bx = x + i * (bw + 6)
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=CRIMSON)
    draw.line([x - 4, y + 6, x + w + 8, y + h - 2], fill=INK, width=5)
    ax, ay = x + w + 8, y + h - 2
    draw.polygon([(ax, ay), (ax - 16, ay - 2), (ax - 2, ay - 16)], fill=INK)


def speech_bubbles(draw, x, y, w, h):
    """Two overlapping rounded speech bubbles, gold behind, navy front."""
    draw.rounded_rectangle([x, y, x + w * 0.62, y + h * 0.62],
                           radius=12, fill=GOLD)
    draw.polygon([(x + 10, y + h * 0.62), (x + 26, y + h * 0.62),
                  (x + 12, y + h * 0.85)], fill=GOLD)
    draw.rounded_rectangle([x + w * 0.34, y + h * 0.30,
                            x + w, y + h],
                           radius=12, fill=NAVY)
    draw.polygon([(x + w * 0.78, y + h), (x + w * 0.92, y + h),
                  (x + w * 0.88, y + h * 1.22)], fill=NAVY)


# ---- the page --------------------------------------------------------
def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([10, 10, 1013, 1013], outline=INK, width=3)

    # ---- masthead ----------------------------------------------------
    d.rectangle([16, 16, 1008, 104], fill=NAVY)
    d.text((30, 30), "THE DAILY GLOBE", font=font(SERIF_B, 54), fill=(255, 255, 255))
    day = font(SANS_B, 28)
    d.text((994, 26), "SATURDAY", font=day, fill=GOLD, anchor="ra")
    d.text((994, 60), "21 NOVEMBER 2026", font=day, fill=(255, 255, 255), anchor="ra")
    d.rectangle([16, 108, 1008, 112], fill=CRIMSON)

    # ---- lead story --------------------------------------------------
    lx, lead_top, lead_bot = 20, 122, 292
    d.rectangle([lx, lead_top, lx + 8, lead_bot], fill=CRIMSON)
    d.text((44, 126), "WAR IN THE GULF  ·  BAHRAIN",
           font=font(SANS_B, 19), fill=CRIMSON)
    d.text((42, 148), "IRAN HITS US BASES", font=font(SERIF_B, 54), fill=INK)
    lead_body = ("Iran's Revolutionary Guards say they fired missiles and "
                 "drones at US positions at two bases in Bahrain. Bahrain "
                 "says a civilian site was hit, a fire broke out, no one hurt.")
    body_f = font(SERIF, 21)
    lines = wrap_text(d, lead_body, body_f, 700)
    draw_text_block(d, 44, 216, lines, body_f, BODY, 25)
    # explosion icon, right of the lead
    starburst(d, 895, 208, 64, 36, 12, ORANGE)
    d.ellipse([895 - 23, 208 - 23, 895 + 23, 208 + 23], fill=(242, 183, 5))

    # ---- 2 x 2 grid --------------------------------------------------
    cards = [
        # (x, y, accent, kicker, headline, body, icon)
        (16, 302, NAVY, "CRIME  ·  MEXICO",
         "“EL CHAPO ISIDRO” CAUGHT",
         "FBI Top 10 cartel boss Fausto Isidro Meza Flores seized in "
         "Sinaloa; 11 dead in the backlash.",
         "star"),
        (519, 302, TEAL, "WAR  ·  UKRAINE",
         "MISSILE HITS ZELENSKYY’S HOMETOWN",
         "A Russian strike on Kryvyi Rih kills 2 and wounds 60 in a "
         "double-tap attack.",
         "flame"),
        (16, 510, CRIMSON, "CLIMATE  ·  ANTALYA",
         "COP31: NO DEAL, OVERTIME",
         "UN climate talks run past their deadline with no deal. The "
         "draft drops fossil fuels — and a $120bn aid target.",
         "globe"),
        (519, 510, TEAL, "MARKETS  ·  NEW YORK",
         "NASDAQ −5.3%, S&P IN CORRECTION",
         "Wall Street’s worst week since March 2020: Nasdaq wipes out "
         "its gains for the year; Nvidia falls 14% in a day.",
         "chart"),
    ]
    card_w, card_h = 489, 198
    for (cx, cy, accent, kicker, headline, body, icon) in cards:
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=CARD,
                    outline=HAIR, width=1)
        d.rectangle([cx, cy, cx + 8, cy + card_h], fill=accent)
        tx = cx + 24
        d.text((tx, cy + 12), kicker, font=font(SANS_B, 17), fill=CRIMSON)
        head_f, head_lines = fit_lines(d, headline, SERIF_B, 38, 330, 2,
                                       min_size=20)
        head_end = draw_text_block(d, tx, cy + 36, head_lines, head_f, INK, 40)
        body_f2 = font(SERIF, 16)
        blines = wrap_text(d, body, body_f2, 330)
        body_y = max(cy + 122, head_end + 6)
        room = (cy + card_h - 10 - body_y) // 21
        blines = blines[:max(1, room)]
        draw_text_block(d, tx, body_y, blines, body_f2, BODY, 21)
        ix, iy = cx + card_w - 88, cy + card_h // 2
        if icon == "star":
            five_star(d, ix + 30, iy, 42, GOLD, NAVY, 3)
            d.ellipse([ix + 20, iy - 10, ix + 40, iy + 10], fill=NAVY)
        elif icon == "flame":
            d.rectangle([ix - 6, iy + 6, ix + 14, iy + 52], fill=(138, 138, 138))
            d.rectangle([ix + 20, iy - 6, ix + 40, iy + 52], fill=(138, 138, 138))
            d.rectangle([ix + 46, iy + 14, ix + 66, iy + 52], fill=(138, 138, 138))
            flame(d, ix + 33, iy + 8, 64, 52, ORANGE, (194, 46, 46))
        elif icon == "globe":
            globe(d, ix + 30, iy, 40, TEAL)
        elif icon == "chart":
            chart_down(d, ix - 8, iy - 26, 84, 52)

    # ---- story six: full-width band ----------------------------------
    bx, band_top, band_bot = 20, 720, 840
    d.rectangle([bx, band_top, bx + 8, band_bot], fill=NAVY)
    d.text((44, band_top + 8), "DIPLOMACY  ·  SHENZHEN",
           font=font(SANS_B, 19), fill=CRIMSON)
    d.text((42, band_top + 32), "“FRIEND” vs “KILLER”",
           font=font(SERIF_B, 40), fill=INK)
    band_body = ("Trump defends calling Putin “my friend” after Shenzhen. "
                 "Zelenskyy answers on CNN: “For us, he is an enemy, and "
                 "of course, for us, he is a killer.”")
    band_f = font(SERIF, 19)
    blines = wrap_text(d, band_body, band_f, 780)
    draw_text_block(d, 44, band_top + 84, blines, band_f, BODY, 24)
    speech_bubbles(d, 896, band_top + 30, 84, 56)

    # ---- footer strip ------------------------------------------------
    d.line([16, 852, 1008, 852], fill=HAIR, width=1)
    foot = [
        (24, "SCIENCE",
         "Wolbachia mosquitoes cut dengue by ~69% in a Brazil trial of "
         "5,700 children."),
        (356, "PERU",
         "Magnitude 6.7 quake shakes the Andes; felt in Lima, no deaths "
         "reported."),
        (688, "MARKETS",
         "Anthropic slides 8.5% to $88.91, a day after its $2 trillion "
         "debut."),
    ]
    foot_f = font(SERIF, 16)
    for (fx, label, text) in foot:
        d.text((fx, 862), label, font=font(SANS_B, 16), fill=CRIMSON)
        flines = wrap_text(d, text, foot_f, 300)
        draw_text_block(d, fx, 886, flines, foot_f, BODY, 21)

    # ---- credit line -------------------------------------------------
    d.line([16, 958, 1008, 958], fill=HAIR, width=1)
    credit = ("THE DAILY GLOBE  ·  SATURDAY 21 NOVEMBER 2026  ·  "
              "Sources: Reuters, AP, CNN, Xinhua, Cboe")
    d.text((512, 972), credit, font=font(SANS, 14), fill=MUTED, anchor="ma")

    return img


def main():
    page = draw_page()
    page.save(OUT, format="PNG")
    print("wrote", OUT, page.size)


if __name__ == "__main__":
    main()
