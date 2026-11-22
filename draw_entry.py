#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page, from scratch.

One 1024x1024 PNG, deterministic: same input -> same bytes every run.
No network, no external assets; every glyph and shape is drawn here.
Layout: masthead, one lead story, four cards in two rows, one wide
strip, and a three-item footer. News verified 21 Nov 2026 from
Reuters, AP, CNN, Xinhua, Cboe and the Associated Press.
"""
import math
import os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
CARD = (255, 253, 246)
INK = (22, 22, 22)
GREY = (74, 74, 74)
NAVY = (20, 36, 62)
RED = (176, 42, 42)
RULE = (201, 194, 174)
ORANGE = (214, 110, 30)
TEAL = (18, 110, 105)
GOLD = (232, 178, 40)


def _font_dir():
    """Locate the Liberation fonts instead of assuming one path."""
    for cand in (
        "/usr/share/fonts/truetype/liberation/",
        "/usr/share/fonts/liberation/",
    ):
        if os.path.exists(cand + "LiberationSerif-Bold.ttf"):
            return cand
    raise FileNotFoundError(
        "Liberation fonts not found; checked "
        "/usr/share/fonts/truetype/liberation/ and "
        "/usr/share/fonts/liberation/"
    )


FONT_DIR = _font_dir()
SERIF = FONT_DIR + "LiberationSerif-Bold.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"
SANS_B = FONT_DIR + "LiberationSans-Bold.ttf"


@lru_cache(maxsize=None)
def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading):
    """Draw wrapped text; return y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, box, bar_color):
    """A white story card with a coloured left bar and hairline border."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=1)
    draw.rectangle([x0, y0, x0 + 6, y1], fill=bar_color)


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 16)
    draw.text((x, y), text, font=f, fill=color)
    return y + 22


# ---------------------------------------------------------------- icons
def icon_burst(draw, cx, cy, r):
    """Starburst explosion: alternating long/short spikes."""
    pts = []
    for i in range(24):
        ang = math.radians(i * 15)
        rad = r if i % 2 == 0 else int(r * 0.45)
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=ORANGE)
    draw.ellipse([cx - r // 3, cy - r // 3, cx + r // 3, cy + r // 3],
                 fill=GOLD)


def icon_badge(draw, cx, cy, r):
    """Five-point sheriff-style star badge."""
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else int(r * 0.45)
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=GOLD, outline=INK)
    draw.ellipse([cx - r // 4, cy - r // 4, cx + r // 4, cy + r // 4],
                 fill=NAVY)


def icon_flame(draw, x, y, s):
    """A flame over three rooftop blocks."""
    for i, h in enumerate((30, 48, 36)):
        bx = x + i * (s // 3)
        draw.rectangle([bx, y + s - h, bx + s // 4, y + s], fill=(120, 120, 120))
    fx, fy = x + s // 2, y + int(s * 0.30)
    draw.polygon([(fx - 18, fy + 26), (fx - 23, fy - 6), (fx - 9, fy + 5),
                  (fx, fy - 26), (fx + 11, fy - 3), (fx + 20, fy - 10),
                  (fx + 18, fy + 26)], fill=ORANGE)
    draw.polygon([(fx - 9, fy + 23), (fx - 4, fy), (fx + 3, fy + 10),
                  (fx + 9, fy - 5), (fx + 9, fy + 23)], fill=GOLD)


def icon_globe_clock(draw, cx, cy, r):
    """Globe outline with clock hands: talks running over time."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=4)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=TEAL, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=TEAL, width=2)
    draw.line([cx, cy, cx, cy - int(0.6 * r)], fill=RED, width=4)
    draw.line([cx, cy, cx + int(0.5 * r), cy + int(0.3 * r)], fill=INK, width=4)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def icon_falling_bars(draw, x, y, s):
    """Three descending bars with a down-trend arrow."""
    tops = (0.10, 0.28, 0.46)
    for i, t in enumerate(tops):
        bx = x + 8 + i * (s // 3)
        top = y + int(s * t)
        bot = y + int(s * (t + 0.26))
        draw.rectangle([bx, top, bx + 16, bot], fill=RED)
    draw.line([x + 4, y + 8, x + s - 6, y + s - 10], fill=INK, width=3)
    draw.polygon([(x + s - 6, y + s - 10), (x + s - 22, y + s - 12),
                  (x + s - 8, y + s - 24)], fill=INK)


def icon_quotes(draw, x, y, s):
    """Two speech bubbles, one amber, one navy."""
    # left bubble
    draw.rounded_rectangle([x, y + 8, x + int(s * 0.52), y + int(s * 0.62)],
                           radius=10, fill=GOLD, outline=INK, width=2)
    draw.polygon([(x + 14, y + int(s * 0.62)), (x + 26, y + int(s * 0.62)),
                  (x + 12, y + int(s * 0.82))], fill=GOLD)
    # right bubble
    draw.rounded_rectangle([x + int(s * 0.42), y + int(s * 0.30),
                            x + s, y + int(s * 0.92)],
                           radius=10, fill=NAVY, outline=INK, width=2)
    draw.polygon([(x + int(s * 0.72), y + int(s * 0.92)),
                  (x + int(s * 0.84), y + int(s * 0.92)),
                  (x + int(s * 0.86), y + s)], fill=NAVY)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # masthead
    d.rectangle([14, 14, W - 15, 106], fill=NAVY)
    d.text((30, 26), "THE DAILY GLOBE", font=font(SERIF, 52), fill=(248, 244, 232))
    d.text((W - 30, 34), "SATURDAY", font=font(SANS_B, 26),
           fill=GOLD, anchor="ra")
    d.text((W - 30, 66), "21 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=(248, 244, 232), anchor="ra")
    d.line([14, 112, W - 15, 112], fill=RED, width=4)

    # ---- lead: Iran strikes US bases in Bahrain
    card(d, (14, 122, W - 15, 300), RED)
    y = kicker(d, 34, 136, "WAR IN THE GULF  ·  BAHRAIN")
    d.text((34, y), "IRAN HITS US BASES", font=font(SERIF, 46), fill=INK)
    y += 56
    text_block(d, 34, y,
               "Iran's Revolutionary Guards say they fired missiles and "
               "drones at US positions at two bases in Bahrain. Bahrain "
               "says a civilian site was hit, a fire broke out, no one hurt.",
               font(SANS, 19), GREY, 660, 25)
    icon_burst(d, 906, 212, 56)

    # ---- row 2: Mexico | Ukraine
    card(d, (14, 312, 502, 516), NAVY)
    y = kicker(d, 34, 326, "CRIME  ·  MEXICO")
    d.text((34, y), "\u201cEL CHAPO ISIDRO\u201d\nCAUGHT", font=font(SERIF, 33), fill=INK)
    y += 82
    text_block(d, 34, y,
               "FBI Top 10 cartel boss Fausto Isidro Meza Flores seized "
               "in Sinaloa. Gun battles after the arrest leave 11 dead.",
               font(SANS, 17), GREY, 330, 23)
    icon_badge(d, 442, 462, 42)

    card(d, (522, 312, W - 15, 516), TEAL)
    y = kicker(d, 542, 326, "WAR  ·  UKRAINE")
    d.text((542, y), "MISSILE HITS\nZELENSKYY\u2019S HOMETOWN", font=font(SERIF, 33), fill=INK)
    y += 82
    text_block(d, 542, y,
               "A Russian ballistic strike on Kryvyi Rih kills 2 — a boy "
               "of 7 and a woman of 20 — and wounds 60 in a double-tap hit.",
               font(SANS, 17), GREY, 330, 23)
    icon_flame(d, 908, 420, 84)

    # ---- row 3: COP31 | Markets
    card(d, (14, 528, 502, 732), ORANGE)
    y = kicker(d, 34, 542, "CLIMATE  ·  ANTALYA")
    d.text((34, y), "COP31: NO DEAL,\nOVERTIME", font=font(SERIF, 33), fill=INK)
    y += 82
    text_block(d, 34, y,
               "UN climate talks run past their deadline with no deal. "
               "The draft drops fossil fuels — and a $120bn aid target.",
               font(SANS, 17), GREY, 330, 23)
    icon_globe_clock(d, 442, 678, 44)

    card(d, (522, 528, W - 15, 732), TEAL)
    y = kicker(d, 542, 542, "MARKETS  ·  NEW YORK")
    d.text((542, y), "NASDAQ \u22125.3%,\nS&P IN CORRECTION", font=font(SERIF, 33), fill=INK)
    y += 82
    text_block(d, 542, y,
               "Wall Street\u2019s worst week since March 2020: Nasdaq wipes "
               "out its gains for the year; Nvidia falls 14% in a day.",
               font(SANS, 17), GREY, 330, 23)
    icon_falling_bars(d, 908, 636, 84)

    # ---- strip: "friend" vs "killer"
    card(d, (14, 744, W - 15, 866), NAVY)
    y = kicker(d, 34, 758, "DIPLOMACY  ·  SHENZHEN")
    d.text((34, y), "\u201cFRIEND\u201d vs \u201cKILLER\u201d", font=font(SERIF, 32), fill=INK)
    y += 44
    text_block(d, 34, y,
               "Trump defends calling Putin \u201cmy friend\u201d after "
               "Shenzhen. Zelenskyy answers on CNN: \u201cFor us, he is "
               "an enemy, and of course, for us, he is a killer.\u201d",
               font(SANS, 18), GREY, 700, 24)
    icon_quotes(d, 900, 772, 80)

    # ---- footer: three short items
    d.line([14, 884, W - 15, 884], fill=RULE, width=2)
    foot = [
        ("SCIENCE", "Wolbachia mosquitoes cut dengue by ~69% in a Brazil "
                    "trial of 5,700 children."),
        ("PERU", "Magnitude 6.7 quake shakes the Andes; felt in Lima, "
                 "no deaths reported."),
        ("MARKETS", "Anthropic slides 8.5% to $88.91, a day after its "
                    "$2 trillion debut."),
    ]
    fx = 30
    for tag, txt in foot:
        d.text((fx, 898), tag, font=font(SANS_B, 15), fill=RED)
        text_block(d, fx, 920, txt, font(SANS, 15), GREY, 300, 20)
        fx += 332
    d.line([14, 982, W - 15, 982], fill=RULE, width=1)
    d.text((W // 2, 990), "THE DAILY GLOBE  ·  SATURDAY 21 NOVEMBER 2026  ·  "
           "Sources: Reuters, AP, CNN, Xinhua, Cboe",
           font=font(SANS, 13), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    build().save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")
