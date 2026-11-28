"""Generates infographic 01, Enforcing AI Policy: a two-page LinkedIn carousel (1080 x 1350 each, dark theme).

Usage:
    python3 build-01.py dark  tower-workshop-logo-gold.png <out-dir>
    python3 build-01.py light tower-workshop-logo-navy.png <out-dir>
Writes 01-enforcing-ai-policy[-light]-p1.svg and -p2.svg. Both themes share every word of copy.
Set MONTSERRAT_TTF if the font file lives somewhere other than the default path.
Requires Pillow and the Montserrat font (used to measure text so chips and wrapped lines fit).
"""
import base64, os, sys
from PIL import Image, ImageFont

theme, logo_path, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
assert theme in ("dark", "light")
FONT_FILE = os.environ.get("MONTSERRAT_TTF",
                           "/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf")

# Tower Workshop brand palette (same tokens as 00, dark theme)
NAVY, GOLD, WHITE, WARM, GRAY = "#051937", "#B67E28", "#FFFFFF", "#E5E3DC", "#CFCFCF"
YEL, GOLD_LT, TERRA = "#FFC207", "#FFBA54", "#D3967E"
BLUE, BLUE_LT = "#3870C2", "#7FA6DE"
PANEL, STRIP, LINE, SUBTLE = "#0B2347", "#081D3D", "#24406A", "#AEB8C6"
CHAR = "#303636"
# Theme tokens. The hook always sits on navy, so "WHITE"/"YEL" in the header stay literal.
T = dict(bg=NAVY, band=None, head=WHITE, body=WARM, muted=SUBTLE, panel=PANEL, strip=STRIP, line=LINE,
         accent=BLUE_LT, label=GOLD_LT, dest=("#1F3A5F", BLUE_LT, WHITE, WARM),
         policy=("#1F3A5F", WHITE), alert=YEL, closing=WHITE, ftag=WHITE, faccent=GOLD_LT)
if theme == "light":
    T.update(bg=WHITE, band=NAVY, head=NAVY, body=CHAR, muted="#5E6B78", panel=WHITE, strip="#F4F3EF",
             line=GRAY, accent=BLUE, label=GOLD, dest=("#E9EFF8", BLUE, NAVY, CHAR),
             policy=(NAVY, WHITE), alert=GOLD, closing=NAVY, ftag=NAVY, faccent=GOLD)
SUFFIX = "" if theme == "dark" else "-light"
FONT = "Montserrat, 'Segoe UI', Helvetica, Arial, sans-serif"
W, H = 1080, 1350
L, R = 52, 1004

_fonts = {}
def tw(s, size, weight=500):
    """Rendered width of s in Montserrat (entities unescaped)."""
    key = (size, weight)
    if key not in _fonts:
        f = ImageFont.truetype(FONT_FILE, size)
        f.set_variation_by_axes([weight])
        _fonts[key] = f
    return _fonts[key].getlength(s.replace("&amp;", "&"))

def wrap(s, size, weight, width):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, size, weight) <= width: cur = t
        else: lines.append(cur); cur = w_
    lines.append(cur)
    return lines

class Page:
    def __init__(self, n):
        self.o = []
        self.add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
        self.add(f"<title>Enforcing AI Policy — page {n} of 2</title>")
        self.add("<defs>" + self.marker("aBlue", T["accent"]) + self.marker("aGold", GOLD) + "</defs>")
        self.add(f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>')
    def add(self, s): self.o.append(s)
    @staticmethod
    def marker(id_, col, size=7):
        return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="{size}" markerHeight="{size}" '
                f'orient="auto"><path d="M0 0L10 5L0 10z" fill="{col}"/></marker>')
    def text(self, x, y, s, size, fill=WHITE, weight=500, anchor="start", ls=0, extra=""):
        lsp = f' letter-spacing="{ls}"' if ls else ""
        self.add(f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}"{lsp}{extra}>{s}</text>')
    def para(self, x, y, s, size, width, fill=WHITE, weight=500, lh=1.35, extra=""):
        lines = wrap(s, size, weight, width)
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * lh, ln, size, fill, weight, extra=extra)
        return y + (len(lines) - 1) * size * lh
    def arrow(self, x1, y1, x2, y2, col=None, mk="aBlue", w=2.5, dash=""):
        col = col or T["accent"]
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{col}" stroke-width="{w}" fill="none"{d} marker-end="url(#{mk})"/>')
    def chips(self, x, y, items, maxw, size=15):
        cx, cy = x, y
        for it in items:
            w_ = tw(it, size, 600) + 28
            if cx + w_ > x + maxw: cx, cy = x, cy + 40
            self.add(f'<rect x="{cx:.1f}" y="{cy}" width="{w_:.1f}" height="30" rx="15" fill="none" stroke="{T["accent"]}" stroke-width="1.5"/>')
            self.text(cx + 14, cy + 20.5, it, size, T["accent"], 600)
            cx += w_ + 10
        return cy + 30
    def header(self, kicker, line1, line2, page, band_h=252):
        if T["band"]:
            self.add(f'<rect width="{W}" height="{band_h}" fill="{T["band"]}"/>')
            self.add(f'<rect y="{band_h}" width="{W}" height="4" fill="{GOLD}"/>')
        self.add(f'<rect x="{L}" y="48" width="64" height="4" fill="{GOLD}"/>')
        self.text(L, 90, kicker, 16, GOLD_LT, 700, ls=4)
        self.text(R, 90, f"{page} / 2", 16, SUBTLE, 600, "end", 2)
        self.text(L, 160, line1, 48, WHITE, 700)
        self.text(L, 228, line2, 58, YEL, 800)
    def footer(self, cue=None):
        fy = 1240
        self.add(f'<line x1="{L}" y1="{fy}" x2="{R}" y2="{fy}" stroke="{T["line"]}" stroke-width="1"/>')
        if cue:
            self.text(L, fy + 52, cue, 20, T["alert"], 700)
        else:
            self.add(f'<text x="{L}" y="{fy+52}" font-size="21" font-weight="700" fill="{T["ftag"]}">Governance defines. '
                     f'Engineering enforces. <tspan fill="{T["faccent"]}">Evidence verifies.</tspan></text>')
        b64 = base64.b64encode(open(logo_path, "rb").read()).decode()
        iw, ih = Image.open(logo_path).size
        lw = 176; lh = lw * ih / iw
        self.add(f'<image x="{R-lw}" y="{fy+12}" width="{lw}" height="{lh:.1f}" href="data:image/png;base64,{b64}"/>')
    def save(self, path):
        self.add("</svg>")
        open(path, "w").write("\n".join(self.o))

# ---------------- Line icons (drawn on a 64 x 64 grid) ----------------
def icon(p, name, x, y, s=1.0, col=None, acc=None, ring=True, ring_r=46):
    col, acc = col or T["accent"], acc or T["label"]
    g = f'<g transform="translate({x:.1f} {y:.1f}) scale({s})" fill="none" stroke="{col}" stroke-width="{2.6/s:.2f}" stroke-linecap="round" stroke-linejoin="round">'
    a = f'stroke="{acc}"'
    body = {
        # Cloud behind a boom barrier: who may reach which cloud AI app
        "casb": f'<path d="M17 30 H47 a8.5 8.5 0 0 0 0-17 a12 12 0 0 0-22.5-3.5 a9 9 0 0 0-7.5 20.5 z"/>'
                f'<rect x="8" y="38" width="7" height="20" rx="1.5"/>'
                f'<path d="M15 44 H58" stroke-width="{4.2/s:.2f}"/>'
                f'<path d="M24 44 H30 M38 44 H44 M52 44 H57" {a} stroke-width="{4.2/s:.2f}"/>'
                f'<path d="M4 58 H60"/>',
        # Hub with keyhole, one input and three routed outputs: identity, authorization, routing
        "gateway": f'<path d="M3 32 H18"/><path d="M13 27 L18 32 L13 37"/>'
                   f'<rect x="19" y="19" width="26" height="26" rx="5"/>'
                   f'<circle cx="32" cy="29" r="3.2" {a}/><path d="M32 32.5 V38" {a}/>'
                   f'<path d="M45 32 L56 14 M45 32 H56 M45 32 L56 50"/>'
                   f'<circle cx="58" cy="13" r="2.6"/><circle cx="58.5" cy="32" r="2.6"/><circle cx="58" cy="51" r="2.6"/>',
        # Message bubble under a magnifying glass: content inspection
        "guardrails": f'<path d="M8 8 H44 a4 4 0 0 1 4 4 V30 a4 4 0 0 1-4 4 H22 L13 42 V34 H8 a4 4 0 0 1-4-4 V12 a4 4 0 0 1 4-4 z"/>'
                      f'<path d="M12 17 H38 M12 25 H30" {a}/>'
                      f'<circle cx="44" cy="44" r="10"/><path d="M51.5 51.5 L60 60"/>'
                      f'<path d="M39.5 44 L43 47.5 L49 41" {a}/>',
        # Person at a laptop
        "employee": f'<circle cx="32" cy="16" r="8"/><path d="M18 40 a14 12 0 0 1 28 0"/>'
                    f'<rect x="14" y="42" width="36" height="14" rx="2"/><path d="M8 58 H56"/>',
        # Application window with code brackets
        "app": f'<rect x="6" y="10" width="52" height="42" rx="4"/><path d="M6 20 H58"/>'
               f'<circle cx="12" cy="15" r="1.2"/><circle cx="17" cy="15" r="1.2"/>'
               f'<path d="M24 29 L18 36 L24 43 M40 29 L46 36 L40 43" {a}/><path d="M35 27 L29 45"/>',
    }[name]
    if ring:
        cx, cy = x + 32 * s, y + 32 * s
        p.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{ring_r}" fill="{T["strip"]}" stroke="{T["line"]}" stroke-width="1.5"/>')
    p.add(g + body + "</g>")

# ======================= PAGE 1 =======================
p = Page(1)
p.header("ENFORCING AI POLICY", "Your policy says no.", "Which control enforces it?", 1, band_h=302)
p.text(L, 276, "A policy without a control is just a wish.", 23, WARM, 500, extra=' font-style="italic"')

LW = 450                      # lane width
LX = [L, R - LW]              # lane x
MID = [x + LW / 2 for x in LX]

ly = 326 if theme == "dark" else 344   # light: clear the navy hook band
for x, lab in zip(LX, ["HUMAN ACCESS", "PROGRAMMATIC ACCESS"]):
    p.text(x, ly, lab, 15, T["label"], 700, ls=3)
    p.add(f'<line x1="{x}" y1="{ly+14}" x2="{x+LW}" y2="{ly+14}" stroke="{T["line"]}" stroke-width="1"/>')

# Sources
sy, sh = ly + 32, 70
for x, ic, title, sub in [(LX[0], "employee", "Employees", "Using AI tools in a browser"),
                          (LX[1], "app", "Applications and agents", "Calling models through APIs")]:
    p.add(f'<rect x="{x}" y="{sy}" width="{LW}" height="{sh}" rx="6" fill="none" stroke="{T["line"]}" stroke-width="1.5"/>')
    icon(p, ic, x + 18, sy + 13, 0.68, col=T["head"], ring=False)
    p.text(x + 80, sy + 31, title, 20, T["head"], 700)
    p.text(x + 80, sy + 55, sub, 16, T["muted"], 400, extra=' font-style="italic"')

def station(x, y, ic, nickname, name, chips_, h=196):
    # measure chip rows first so the card always fits its tags
    probe = Page.__new__(Page); probe.o = []
    h = max(h, Page.chips(probe, x + 132, y + 98, chips_, LW - 150) - y + 28)
    p.add(f'<rect x="{x}" y="{y}" width="{LW}" height="{h}" rx="6" fill="{T["panel"]}" stroke="{T["line"]}" stroke-width="1.5"/>')
    p.add(f'<rect x="{x}" y="{y}" width="6" height="{h}" fill="{BLUE}"/>')
    icon(p, ic, x + 30, y + 30, 1.0, ring_r=48)
    tx = x + 132
    p.text(tx, y + 42, nickname.upper(), 14, T["label"], 700, ls=2.5)
    p.text(tx, y + 76, name, 27, T["head"], 700)
    p.chips(tx, y + 98, chips_, LW - 150)
    return y + h

r1 = sy + sh + 40
e1 = station(LX[0], r1, "casb", "The access checkpoint", "CASB / SSE",
             ["Shadow AI", "App discovery", "Access control", "DLP"])
g1 = station(LX[1], r1, "gateway", "The transaction broker", "API gateway",
             ["Identity", "Authorization", "Routing", "Quotas"])
r2 = g1 + 40
g2 = station(LX[1], r2, "guardrails", "The content checkpoint", "Inline guardrails",
             ["Prompt inspection", "Response inspection", "Content filtering"])
r3 = g2 + 40
dh = 84
for x, title, sub in [(LX[0], "Approved AI SaaS", "Provider-native controls apply"),
                      (LX[1], "Authorized models", "Approved model endpoints only")]:
    p.add(f'<rect x="{x}" y="{r3}" width="{LW}" height="{dh}" rx="6" fill="{T["dest"][0]}" stroke="{T["dest"][1]}" stroke-width="1.5"/>')
    p.text(x + LW / 2, r3 + 36, title, 21, T["dest"][2], 700, "middle")
    p.text(x + LW / 2, r3 + 62, sub, 16, T["dest"][3], 400, "middle", extra=' font-style="italic"')

# Flow arrows
for m in MID:
    p.arrow(m, sy + sh + 2, m, r1 - 4)
p.arrow(MID[1], g1 + 2, MID[1], r2 - 4)
p.arrow(MID[1], g2 + 2, MID[1], r3 - 4)
ax = LX[0] + 62
p.arrow(ax, e1 + 2, ax, r3 - 4)
# Annotation beside the long human-path arrow: the asymmetry is the lesson
ann_x = ax + 34
p.text(ann_x, r2 + 50, "WHY ONLY ONE CHECKPOINT?", 14, T["label"], 700, ls=2.5)
p.para(ann_x, r2 + 84, "Once an employee reaches an approved AI app, that provider’s own controls take over. "
       "The CASB decides which apps, and what data, get through.", 17, LW - (ann_x - LX[0]) - 6, T["body"], 400, 1.45)

# Evidence strip
ey = r3 + dh + 36
p.add(f'<rect x="{L}" y="{ey}" width="{R-L}" height="64" fill="{T["strip"]}" stroke="{T["line"]}" stroke-width="1.5"/>')
p.add(f'<rect x="{L}" y="{ey}" width="6" height="64" fill="{GOLD}"/>')
p.text(L + 28, ey + 39, "EVIDENCE", 14, T["label"], 700, ls=2.5)
p.text(L + 150, ey + 39, "Every checkpoint logs what it allowed and what it blocked.", 18, T["body"], 500)

p.footer(cue="Swipe: one policy, three checkpoints  →")
p.save(os.path.join(out_dir, f"01-enforcing-ai-policy{SUFFIX}-p1.svg"))
print("p1 evidence strip bottom:", ey + 64)

# ======================= PAGE 2 =======================
p = Page(2)
p.header("ENFORCING AI POLICY", "One policy.", "Three checkpoints.", 2)

# Policy card
py_, ph = (270 if theme == "dark" else 288), 128
p.add(f'<rect x="{L}" y="{py_}" width="{R-L}" height="{ph}" rx="6" fill="{T["policy"][0]}" stroke="{GOLD}" stroke-width="2"/>')
p.add(f'<rect x="{L}" y="{py_}" width="6" height="{ph}" fill="{GOLD}"/>')
p.text(L + 28, py_ + 38, "THE POLICY", 14, GOLD_LT, 700, ls=2.5)
p.para(L + 28, py_ + 78, "“Customer data may not be sent to unapproved AI services or shown to unauthorized users.”",
       25, R - L - 60, T["policy"][1], 600, 1.35)

rows = [
    ("casb", "CASB / SSE", "An employee tries to upload a customer file to an unapproved AI website.",
     "UPLOAD BLOCKED", "Logged: user, file, destination"),
    ("gateway", "API GATEWAY", "An application calls a model endpoint that isn’t on the approved list.",
     "REQUEST REJECTED", "Logged: app identity, endpoint"),
    ("guardrails", "INLINE GUARDRAIL", "A model’s response includes a customer’s account number.",
     "DATA MASKED", "Logged: rule triggered, field masked"),
]
ry, rh, gap = py_ + ph + 28, 158, 20
CHIP_W = 236
for ic, name, scen, outcome, logged in rows:
    p.add(f'<rect x="{L}" y="{ry}" width="{R-L}" height="{rh}" rx="6" fill="{T["panel"]}" stroke="{T["line"]}" stroke-width="1.5"/>')
    p.add(f'<rect x="{L}" y="{ry}" width="6" height="{rh}" fill="{BLUE}"/>')
    icon(p, ic, L + 34, ry + rh / 2 - 32, 1.0, ring_r=46)
    tx = L + 140
    p.text(tx, ry + 40, name, 14, T["accent"], 700, ls=2.5)
    p.para(tx, ry + 74, scen, 20, R - CHIP_W - 40 - tx, T["head"], 500, 1.4)
    p.text(tx, ry + rh - 20, logged, 15, T["muted"], 500, extra=' font-style="italic"')
    cx = R - CHIP_W - 24
    p.add(f'<rect x="{cx}" y="{ry + rh/2 - 22}" width="{CHIP_W}" height="44" rx="22" fill="{BLUE}"/>')
    p.text(cx + CHIP_W / 2, ry + rh / 2 + 6, outcome, 16, WHITE, 800, "middle", 1.5)
    ry += rh + gap

# Blind spots
by, bh = ry + 12, 104
p.add(f'<rect x="{L}" y="{by}" width="{R-L}" height="{bh}" rx="6" fill="none" stroke="{T["alert"]}" stroke-width="2" stroke-dasharray="8 6"/>')
p.text(L + 28, by + 40, "WHAT THESE CAN MISS", 15, T["alert"], 700, ls=3)
p.text(L + 28, by + 76, "AI built into approved SaaS apps  ·  Personal devices  ·  Models run locally", 19, T["body"], 500)

# Closing
cy = by + bh + 58
p.text(L, cy, "No single checkpoint is enough.", 34, T["closing"], 800)
p.text(L, cy + 40, "Each sees different traffic. Effective governance layers complementary controls.", 19, T["body"], 400)

p.footer()
p.save(os.path.join(out_dir, f"01-enforcing-ai-policy{SUFFIX}-p2.svg"))
print("p2 closing baseline:", cy + 40)
