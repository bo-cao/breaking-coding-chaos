"""BCC architecture — large type for web, natural sub-tasks (not fixed slots)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1600, 980
BG = (250, 251, 252)
INK = (15, 23, 42)
MUTED = (100, 116, 139)
LINE = (226, 232, 240)
WHITE = (255, 255, 255)
BLUE = (37, 99, 235)
BLUE_MID = (96, 165, 250)
BLUE_SOFT = (239, 246, 255)
VIOLET = (124, 58, 237)
VIOLET_SOFT = (245, 243, 255)
TEAL = (13, 148, 136)
TEAL_SOFT = (240, 253, 250)
GREEN = (22, 163, 74)
AMBER = (217, 119, 6)
AMBER_SOFT = (255, 247, 237)
GRAY = (148, 163, 184)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def font(size, bold=False):
    cands = []
    if bold:
        cands += [
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ]
    cands += [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for p in cands:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


ft = font(48, True)
fh = font(32, True)
fb = font(28, True)
fn = font(26)


def round_box(xy, r, fill, outline=None, w=3):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)


def tw(s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def tc(x, y, s, fill, f):
    d.text((x - tw(s, f) // 2, y), s, fill=fill, font=f)


# Example sub-tasks only — user's own map replaces these
TASKS = [
    ("Auth", GREEN, "done"),
    ("API", GREEN, "done"),
    ("Billing", AMBER, "now"),
    ("Deploy", GRAY, "later"),
]

# ── Title ───────────────────────────────────────────────
d.text((56, 28), "How it works", fill=INK, font=ft)
d.text(
    (56, 92),
    "One project bar · each sub-task gets plan-spar → clean-cut",
    fill=MUTED,
    font=fn,
)

# ── THROUGHLINE ─────────────────────────────────────────
round_box((40, 145, 1560, 380), 24, WHITE, BLUE, 3)

round_box((64, 168, 320, 224), 14, BLUE_SOFT, None, 0)
d.text((88, 182), "THROUGHLINE", fill=BLUE, font=fb)
d.text((340, 184), "Project progress", fill=INK, font=fh)

bar_x0, bar_y0, bar_x1, bar_y1 = 64, 250, 1536, 320
n = len(TASKS)
sw = (bar_x1 - bar_x0) / n
gap = 14
centers = []

for i, (name, lab_c, mode) in enumerate(TASKS):
    x0 = int(bar_x0 + i * sw + (gap if i else 0))
    x1 = int(bar_x0 + (i + 1) * sw - gap)
    if i == 0:
        x0 = bar_x0
    if i == n - 1:
        x1 = bar_x1
    cx = (x0 + x1) // 2
    centers.append(cx)

    if mode == "done":
        round_box((x0, bar_y0, x1, bar_y1), 16, BLUE, None, 0)
        tc(cx, 338, name, GREEN, fb)
    elif mode == "now":
        round_box((x0, bar_y0, x1, bar_y1), 16, LINE, None, 0)
        mid = x0 + int((x1 - x0) * 0.45)
        round_box((x0, bar_y0, mid, bar_y1), 16, BLUE_MID, None, 0)
        d.rounded_rectangle(
            (x0 - 4, bar_y0 - 4, x1 + 4, bar_y1 + 4),
            radius=18,
            outline=AMBER,
            width=4,
        )
        tc(cx, 338, f"{name}  ·  now", AMBER, fb)
    else:
        round_box((x0, bar_y0, x1, bar_y1), 16, LINE, None, 0)
        tc(cx, 338, name, GRAY, fb)

cur_cx = centers[2]
d.polygon([(cur_cx - 18, 390), (cur_cx + 18, 390), (cur_cx, 424)], fill=AMBER)

# ── Focus ───────────────────────────────────────────────
round_box((40, 440, 1560, 520), 18, AMBER_SOFT, AMBER, 3)
d.text((72, 462), "Now:  Billing", fill=AMBER, font=fh)
d.text((360, 464), "—  one sub-task, one PLAN.md", fill=INK, font=fh)

# ── Cards (plenty of height: 550–850) ───────────────────
y0, y1 = 550, 850
w_spar = 620
w_gate = 160
w_cut = 620
x_spar = 40
x_gate = 700
x_cut = 900

# PLAN-SPAR
round_box((x_spar, y0, x_spar + w_spar, y1), 24, WHITE, VIOLET, 3)
round_box((x_spar + 32, y0 + 32, x_spar + 270, y0 + 92), 14, VIOLET_SOFT, None, 0)
d.text((x_spar + 52, y0 + 48), "PLAN-SPAR", fill=VIOLET, font=fb)
d.text((x_spar + 32, y0 + 130), "This sub-task only", fill=INK, font=fh)
d.text((x_spar + 32, y0 + 200), "Align & lock PLAN.md for Billing", fill=MUTED, font=fn)
d.text((x_spar + 32, y0 + 260), "Not Auth / API / Deploy", fill=MUTED, font=fn)

# APPROVE
round_box((x_gate, y0 + 70, x_gate + w_gate, y1 - 70), 20, TEAL, None, 0)
tc(x_gate + w_gate // 2, (y0 + y1) // 2 - 22, "APPROVE", WHITE, fb)
tc(x_gate + w_gate // 2, (y0 + y1) // 2 + 22, "you", WHITE, fn)
cy = (y0 + y1) // 2
d.polygon(
    [(x_spar + w_spar + 6, cy - 14), (x_gate - 4, cy), (x_spar + w_spar + 6, cy + 14)],
    fill=TEAL,
)
d.polygon(
    [(x_gate + w_gate + 4, cy - 14), (x_cut - 6, cy), (x_gate + w_gate + 4, cy + 14)],
    fill=TEAL,
)

# CLEAN-CUT
round_box((x_cut, y0, x_cut + w_cut, y1), 24, WHITE, TEAL, 3)
round_box((x_cut + 32, y0 + 32, x_cut + 270, y0 + 92), 14, TEAL_SOFT, None, 0)
d.text((x_cut + 52, y0 + 48), "CLEAN-CUT", fill=TEAL, font=fb)
d.text((x_cut + 32, y0 + 130), "Ship this sub-task", fill=INK, font=fh)
d.text((x_cut + 32, y0 + 200), "Minimal code · verify PLAN", fill=MUTED, font=fn)
d.text((x_cut + 32, y0 + 260), "Write back · bar advances", fill=MUTED, font=fn)

# ── Bottom ──────────────────────────────────────────────
round_box((40, 880, 1560, 950), 18, BLUE_SOFT, BLUE, 3)
tc(
    W // 2,
    902,
    "Next: Deploy gets its own plan-spar → clean-cut.   Sub-tasks are yours — not fixed slots.",
    INK,
    fn,
)

out = os.path.join(os.path.dirname(__file__), "architecture.png")
img.save(out, "PNG", optimize=True)
print("wrote", out, img.size)
