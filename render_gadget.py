#!/usr/bin/env python3
"""Draw the-catalogue-photo-of-an-2-20261121-0341 entry: a clean studio
catalogue photograph of an impossible gadget — the YesterKettle, a kettle
that pours yesterday's tea. Pillow only, no network, no randomness:
running this script twice writes byte-identical PNGs.

The gadget: a brushed-steel kettle with a clock dial on its belly. Its
spout points up and to the left; below it sits a full cup, and the tea
stream flows UPWARD out of the cup and back into the spout — yesterday's
tea, served today. Plain studio background, soft floor shadow, spec
callouts with leader lines, and a price tag.
"""
import math

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
BG = (246, 245, 241)
INK = (22, 22, 22)
MUTED = (96, 96, 96)
ACCENT = (163, 24, 44)
TEA = (176, 110, 32)
STEEL = (196, 200, 205)
STEEL_DARK = (148, 153, 160)
STEEL_LIGHT = (226, 229, 232)
SHADOW = (208, 206, 198)
FAINT_LINE = (190, 188, 180)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def serif_b(size):
    return load("LiberationSerif-Bold.ttf", size)


def serif(size):
    return load("LiberationSerif-Regular.ttf", size)


def serif_i(size):
    return load("LiberationSerif-Italic.ttf", size)


def sans_b(size):
    return load("LiberationSans-Bold.ttf", size)


def sans(size):
    return load("LiberationSans-Regular.ttf", size)


img = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)
pen = ImageDraw.Draw(img)

# ---------------- soft floor shadow ----------------
pen.ellipse([272, 800, 752, 862], fill=SHADOW)
pen.ellipse([322, 812, 702, 850], fill=(219, 217, 209))

# ---------------- header ----------------
pen.text((512, 44), "THE IMPOSSIBLE CATALOGUE", font=sans_b(24),
         fill=MUTED, anchor="ma")
pen.text((512, 84), "YESTERKETTLE\u2122", font=serif_b(84),
         fill=INK, anchor="ma")
pen.text((512, 172), "It pours yesterday's tea. Today.",
         font=serif_i(26), fill=MUTED, anchor="ma")
pen.line([(332, 218), (692, 218)], fill=FAINT_LINE, width=2)

# ---------------- kettle ----------------
# Body: tapered steel body, wider at the base.
pen.polygon([(392, 810), (632, 810), (606, 400), (418, 400)],
            fill=STEEL, outline=STEEL_DARK)
# Highlight stripe down the left of the body.
pen.polygon([(430, 798), (462, 798), (448, 412), (424, 412)],
            fill=STEEL_LIGHT)
# Base band.
pen.polygon([(392, 810), (632, 810), (628, 778), (396, 778)],
            fill=STEEL_DARK)
# Lid: shallow dome + knob.
pen.pieslice([432, 330, 592, 420], start=180, end=360, fill=STEEL_DARK)
pen.ellipse([488, 322, 536, 352], fill=INK)
pen.ellipse([500, 312, 524, 330], fill=STEEL_LIGHT)
# Spout: rises from the body's left side, tip pointing up-left.
pen.polygon([(414, 470), (392, 396), (296, 322), (272, 330),
             (330, 408), (372, 470)], fill=STEEL, outline=STEEL_DARK)
pen.polygon([(296, 322), (272, 330), (288, 346), (306, 338)],
            fill=STEEL_DARK)
# Handle: thick arc on the right side.
pen.arc([596, 420, 700, 620], start=270, end=90, fill=INK, width=22)
pen.arc([606, 430, 690, 610], start=270, end=90, fill=STEEL_DARK,
        width=8)

# Clock dial on the kettle's belly: "yesterday" o'clock.
pen.ellipse([442, 480, 582, 620], fill=(250, 249, 244),
            outline=INK, width=4)
for hour in range(12):
    a = math.radians(hour * 30 - 90)
    x0 = 512 + 58 * math.cos(a)
    y0 = 550 + 58 * math.sin(a)
    x1 = 512 + 64 * math.cos(a)
    y1 = 550 + 64 * math.sin(a)
    pen.line([(x0, y0), (x1, y1)], fill=INK, width=3)
# Hands point to 9 and 12 — nine o'clock, yesterday.
pen.line([(512, 550), (512, 498)], fill=INK, width=5)
pen.line([(512, 550), (468, 550)], fill=INK, width=5)
pen.ellipse([506, 544, 518, 556], fill=ACCENT)
pen.text((512, 578), "YESTERDAY", font=sans_b(13), fill=ACCENT,
         anchor="ma")

# ---------------- the impossible part: tea flows UP ----------------
# Cup sitting on the floor, left of the kettle, under the spout tip.
pen.polygon([(212, 800), (332, 800), (320, 726), (224, 726)],
            fill=(250, 249, 244), outline=INK, width=3)
pen.ellipse([212, 716, 332, 742], fill=TEA, outline=INK, width=3)
pen.arc([320, 736, 362, 786], start=270, end=90, fill=INK, width=6)
# Saucer.
pen.ellipse([188, 796, 356, 820], fill=(232, 230, 224), outline=INK,
            width=2)
# Rising stream: a wavy ribbon of tea from the cup up into the spout.
pts = []
for i in range(41):
    t = i / 40
    y = 726 - t * 386
    x = 272 + 10 * math.sin(t * math.pi * 3.5)
    pts.append((x, y))
pen.line(pts, fill=TEA, width=9, joint="curve")
# Droplets climbing the stream (they rise, not fall).
for t, r in [(0.18, 5), (0.42, 6), (0.66, 5), (0.86, 6)]:
    y = 726 - t * 386
    x = 272 + 10 * math.sin(t * math.pi * 3.5)
    pen.ellipse([x - r, y - r, x + r, y + r], fill=TEA)
# Small upward arrow beside the stream.
pen.text((212, 470), "\u2191", font=sans_b(34), fill=TEA, anchor="ma")

# ---------------- price tag (top right) ----------------
tag = Image.new("RGBA", (220, 110), (0, 0, 0, 0))
td = ImageDraw.Draw(tag)
td.rounded_rectangle([4, 8, 216, 102], radius=10, fill=(255, 255, 255),
                     outline=INK, width=3)
td.ellipse([14, 44, 34, 64], fill=BG, outline=INK, width=3)
td.text((128, 26), "$299", font=serif_b(46), fill=ACCENT, anchor="ma")
td.text((128, 74), "TIMELESS EDITION", font=sans_b(14), fill=MUTED,
        anchor="ma")
tag = tag.rotate(-8, expand=True, resample=Image.BICUBIC)
img.paste(tag, (742, 250), tag)

# ---------------- spec callouts ----------------
def callout(x, y, text, target, side):
    """Text label with a leader line to a point on the product."""
    pen.text((x, y), text, font=sans_b(19), fill=INK,
             anchor="ma" if side == "c" else ("ra" if side == "r" else "la"))
    # leader dot at the target, line from label edge to target
    pen.ellipse([target[0] - 4, target[1] - 4, target[0] + 4,
                 target[1] + 4], fill=ACCENT)
    if side == "r":
        pen.line([(x - 8, y + 10), (target[0], target[1])],
                 fill=MUTED, width=2)
    else:
        pen.line([(x + 8, y + 10), (target[0], target[1])],
                 fill=MUTED, width=2)


callout(760, 430, "BREWS TOMORROW,", (560, 500), "l")
pen.text((760, 458), "TODAY", font=sans_b(19), fill=INK, anchor="la")
callout(760, 620, "0 WATTS \u2014 RUNS ON", (600, 690), "l")
pen.text((760, 648), "NOSTALGIA", font=sans_b(19), fill=INK, anchor="la")
callout(250, 560, "POURS YESTERDAY'S", (272, 560), "r")
pen.text((250, 588), "TEA \u2014 UPWARDS", font=sans_b(19), fill=INK,
         anchor="ra")

# ---------------- footer ----------------
pen.line([(72, 920), (952, 920)], fill=FAINT_LINE, width=2)
pen.text((512, 936), "MODEL YK-02  \u00b7  IMPOSSIBLE APPLIANCES CO.  \u00b7  "
         "NO BATTERIES  \u00b7  NO PARADOXES (GUARANTEED)",
         font=sans(17), fill=MUTED, anchor="ma")
pen.text((512, 968), "Yesterday's tea, served at exactly the right time.",
         font=serif_i(17), fill=MUTED, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
