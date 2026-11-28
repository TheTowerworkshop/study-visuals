"""Generates infographic 02, Governing the AI Technology Stack: a three-page LinkedIn carousel
(1080 x 1350 per page) in a dark or light theme.

Usage:
    python3 build-02.py dark  tower-workshop-logo-gold.png <out-dir>
    python3 build-02.py light tower-workshop-logo-navy.png <out-dir>
Writes 02-governing-the-ai-technology-stack[-light]-p1.svg, -p2.svg and -p3.svg.
Both themes share every word of copy. Requires Pillow plus the Montserrat and DejaVu Sans Mono
fonts (used to measure text so wrapped lines and labels fit). Set MONTSERRAT_TTF / MONO_TTF if the
font files live somewhere other than the default paths.
"""
import base64, os, sys
from PIL import Image, ImageFont

theme, logo_path, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
assert theme in ("dark", "light")
FONT_FILE = os.environ.get("MONTSERRAT_TTF",
                           "/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf")
MONO_FILE = os.environ.get("MONO_TTF", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
BASE = "02-governing-the-ai-technology-stack"

# Tower Workshop brand palette (same tokens as 00 and 01)
NAVY, GOLD, WHITE, WARM, GRAY = "#051937", "#B67E28", "#FFFFFF", "#E5E3DC", "#CFCFCF"
YEL, GOLD_LT, TERRA = "#FFC207", "#FFBA54", "#D3967E"
BLUE, BLUE_LT = "#3870C2", "#7FA6DE"
PANEL, STRIP, LINE, SUBTLE = "#0B2347", "#081D3D", "#24406A", "#AEB8C6"
CHAR = "#303636"

# Theme tokens. The hook always sits on navy, so header colors stay literal.
# 02 zooms in on the Operate column of 00, so its accent is the series green-gray.
T = dict(bg=NAVY, band=None, head=WHITE, body=WARM, muted=SUBTLE, panel=PANEL, strip=STRIP, line=LINE,
         accent="#9DB3AF", bar="#6E8784", pol=BLUE_LT, dat=GOLD_LT, deny=TERRA, label=GOLD_LT,
         hi=("#1F3A5F", WHITE), alert=YEL, closing=WHITE, ftag=WHITE, faccent=GOLD_LT,
         code_bg="#020E22", code_key="#9DB3AF", code_val=WARM, code_cmt="#7D8796")
if theme == "light":
    T.update(bg=WHITE, band=NAVY, head=NAVY, body=CHAR, muted="#5E6B78", panel=WHITE, strip="#F4F3EF",
             line=GRAY, accent="#495A58", bar="#495A58", pol=BLUE, dat=GOLD, deny="#A9644E", label=GOLD,
             hi=(NAVY, WHITE), alert=GOLD, closing=NAVY, ftag=NAVY, faccent=GOLD)
SUFFIX = "" if theme == "dark" else "-light"

FONT = "Montserrat, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"
W, H = 1080, 1350
L, R = 52, 1004
PAGES = 3

_fonts = {}
def tw(s, size, weight=500):
    key = (size, weight)
    if key not in _fonts:
        f = ImageFont.truetype(FONT_FILE, size)
        f.set_variation_by_axes([weight])
        _fonts[key] = f
    return _fonts[key].getlength(s.replace("&amp;", "&").replace("&gt;", ">"))

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
        self.n, self.o = n, []
        self.add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
        self.add(f"<title>Governing the AI Technology Stack — page {n} of {PAGES}</title>")
        self.add("<defs>" + self.marker("aAcc", T["accent"]) + self.marker("aPol", T["pol"])
                 + self.marker("aMuted", T["muted"]) + "</defs>")
        self.add(f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>')
    def add(self, s): self.o.append(s)
    @staticmethod
    def marker(id_, col, size=7):
        return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="{size}" markerHeight="{size}" '
                f'orient="auto"><path d="M0 0L10 5L0 10z" fill="{col}"/></marker>')
    def text(self, x, y, s, size, fill, weight=500, anchor="start", ls=0, extra=""):
        lsp = f' letter-spacing="{ls}"' if ls else ""
        self.add(f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}"{lsp}{extra}>{s}</text>')
    def para(self, x, y, s, size, width, fill, weight=500, lh=1.38, extra="", anchor="start"):
        lines = wrap(s, size, weight, width)
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * lh, ln, size, fill, weight, anchor, extra=extra)
        return y + (len(lines) - 1) * size * lh
    def line(self, d, col, w=2.5, dash="", mk=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        me = f' marker-end="url(#{mk})"' if mk else ""
        self.add(f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linejoin="round"{da}{me}/>')
    def box(self, x, y, w, h, fill=None, stroke=None, bar=None, rx=6, sw=1.5, dash=""):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                 f'fill="{fill or T["panel"]}" stroke="{stroke or T["line"]}" stroke-width="{sw}"{da}/>')
        if bar:
            self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="6" height="{h:.1f}" fill="{bar}"/>')
    def pill(self, x, y, label, col, size=13, filled=False, anchor="start"):
        w_ = tw(label, size, 700) + 22
        if anchor == "end": x -= w_
        fill = col if filled else "none"
        self.add(f'<rect x="{x:.1f}" y="{y}" width="{w_:.1f}" height="24" rx="12" fill="{fill}" stroke="{col}" stroke-width="1.5"/>')
        self.text(x + w_ / 2, y + 16.5, label, size, (T["bg"] if filled else col), 700, "middle", 0.5)
        return w_
    def header(self, kicker, line1, line2, sub=None, band_h=252, l1_size=48):
        if T["band"]:
            self.add(f'<rect width="{W}" height="{band_h}" fill="{T["band"]}"/>')
            self.add(f'<rect y="{band_h}" width="{W}" height="4" fill="{GOLD}"/>')
        self.add(f'<rect x="{L}" y="48" width="64" height="4" fill="{GOLD}"/>')
        self.text(L, 90, kicker, 16, GOLD_LT, 700, ls=4)
        self.text(R, 90, f"{self.n} / {PAGES}", 16, SUBTLE, 600, "end", 2)
        self.text(L, 160, line1, l1_size, WHITE, 700)
        self.text(L, 228, line2, 58, YEL, 800)
        if sub:
            self.text(L, 276, sub, 23, WARM, 500, extra=' font-style="italic"')
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
    def save(self):
        self.add("</svg>")
        path = os.path.join(out_dir, f"{BASE}{SUFFIX}-p{self.n}.svg")
        open(path, "w").write("\n".join(self.o))
        return path

KICKER = "GOVERNING THE AI TECHNOLOGY STACK"

# =========================== PAGE 1: the transaction ===========================
p = Page(1)
p.header(KICKER, "A prompt goes in. An answer comes out.", "What happens in between?",
         "Eight steps, and where policy acts on each.", band_h=302, l1_size=44)

top = 334 if theme == "dark" else 350
LX0, LX1 = 92, 596          # lifecycle column (left of it: the tool-call loop)
CX0, CX1 = 636, R           # control-plane column
p.text(LX0, top, "ONE AI TRANSACTION", 15, T["label"], 700, ls=3)
p.text(CX0, top, "CONTROL PLANE", 15, T["label"], 700, ls=3)
for a, b in ((L, LX1), (CX0, CX1)):
    p.add(f'<line x1="{a}" y1="{top+14}" x2="{b}" y2="{top+14}" stroke="{T["line"]}" stroke-width="1"/>')

steps = [
    ("User prompt", "Request and user identity", ()),
    ("API gateway", "Authenticate and authorize the caller", ("POLICY",)),
    ("Input inspection", "DLP and prompt guardrails", ("POLICY", "DATA")),
    ("Context assembly", "System + user prompt + retrieved data (untrusted)", ("DATA",)),
    ("Model routing", "Select a model permitted for this data", ("POLICY", "DATA")),
    ("LLM inference", "Generate a response or a tool request", ()),
    ("Output inspection", "Evaluate, then redact or block", ("POLICY", "DATA")),
    ("Response or action", "Deliver the answer, or request a tool", ("POLICY",)),
]
sy0, sh, sg = top + 32, 78, 14
step_mid = []
for i, (title, sub, tags) in enumerate(steps):
    y = sy0 + i * (sh + sg)
    model = title == "LLM inference"
    p.box(LX0, y, LX1 - LX0, sh, fill=(T["hi"][0] if model else T["panel"]),
          stroke=(T["accent"] if model else T["line"]), bar=T["bar"])
    cx, cy = LX0 + 38, y + sh / 2
    ncol = T["hi"][1] if model else T["accent"]
    p.add(f'<circle cx="{cx}" cy="{cy}" r="17" fill="none" stroke="{ncol}" stroke-width="2"/>')
    p.text(cx, cy + 6, str(i + 1), 17, ncol, 700, "middle")
    tcol = T["hi"][1] if model else T["head"]
    p.text(LX0 + 70, y + 33, title, 20, tcol, 700)
    p.text(LX0 + 70, y + 59, sub, 15.5, (WARM if (model and theme == "light") else T["body"]), 400)
    tx = LX1 - 14
    for tag in reversed(tags):
        tx -= p.pill(tx, y + 14, tag, T["pol"] if tag == "POLICY" else T["dat"], 12, anchor="end") + 8
    step_mid.append(cy)
    if i < len(steps) - 1:
        p.line(f"M{LX0+38} {y+sh+1} V{y+sh+sg-2}", T["accent"], 2, mk="aAcc")

# Tool calls loop back to the gateway for authorization
lx = 66
p.line(f"M{LX0} {step_mid[7]} H{lx} V{step_mid[1]} H{LX0-3}", T["pol"], 2.5, dash="6 4", mk="aPol")
mid_loop = (step_mid[1] + step_mid[7]) / 2
LOOP_LABEL = "TOOL CALLS RETURN FOR AUTHORIZATION"
mask = tw(LOOP_LABEL, 11.5, 700) + 1.5 * len(LOOP_LABEL) + 28
p.add(f'<rect x="{lx-11}" y="{mid_loop-mask/2:.1f}" width="22" height="{mask:.1f}" fill="{T["bg"]}"/>')
p.text(lx, mid_loop, LOOP_LABEL, 11.5, T["pol"], 700, "middle", 1.5,
       f' transform="rotate(-90 {lx} {mid_loop})" dominant-baseline="central"')
steps_bottom = sy0 + len(steps) * (sh + sg) - sg

# Control plane: policy management and data protection, the two cross-cutting capabilities
def cp_group(y, h, tag, col, title):
    p.box(CX0, y, CX1 - CX0, h, fill=T["strip"])
    p.add(f'<rect x="{CX0}" y="{y}" width="{CX1-CX0}" height="5" fill="{col}"/>')
    p.pill(CX0 + 18, y + 20, tag, col, 12)
    p.text(CX0 + 18, y + 72, title, 19, T["head"], 700)
def cp_item(y, title, sub, col):
    p.box(CX0 + 18, y, CX1 - CX0 - 36, 62, fill=T["panel"])
    p.add(f'<rect x="{CX0+18}" y="{y}" width="4" height="62" fill="{col}"/>')
    p.text(CX0 + 36, y + 26, title, 17, T["head"], 700)
    p.text(CX0 + 36, y + 49, sub, 14.5, T["body"], 400)

g1y = sy0
g1h = 96 + 3 * 62 + 2 * 26 + 18
cp_group(g1y, g1h, "POLICY", T["pol"], "Policy management")
iy = g1y + 92
for j, (t_, s_) in enumerate([("Git", "Versioned policies"), ("CI/CD pipeline", "Review, test, deploy"),
                              ("Policy engine", "Allow or deny, with conditions")]):
    cp_item(iy, t_, s_, T["pol"])
    if j < 2:
        p.line(f"M{(CX0+CX1)/2} {iy+63} V{iy+86}", T["pol"], 2, mk="aPol")
    iy += 62 + 26
g2y = g1y + g1h + 22
g2h = steps_bottom - g2y
cp_group(g2y, g2h, "DATA", T["dat"], "Data protection")
iy = g2y + 92
for t_, s_ in [("Classification", "Labels data by sensitivity"), ("DLP rules", "Content and destination rules"),
               ("RAG entitlements", "Who may retrieve what")]:
    cp_item(iy, t_, s_, T["dat"])
    iy += 62 + (g2h - 92 - 18 - 3 * 62) / 2

# Evidence strip
ey = steps_bottom + 30
p.box(L, ey, R - L, 60, fill=T["strip"], bar=GOLD, rx=0)
p.text(L + 28, ey + 37, "EVIDENCE", 14, T["label"], 700, ls=2.5)
p.text(L + 150, ey + 37, "Every step writes to the audit trail.", 18, T["body"], 500)
p.footer(cue="Swipe: three ideas behind the stack  →")
print("p1:", p.save(), "| control groups end", g2y + g2h, "| items end", iy - 12, "| strip bottom", ey + 60)

# =========================== PAGE 2: three concepts ===========================
p = Page(2)
p.header(KICKER, "Inside the stack:", "Where trust gets decided.")
DX0, DX1 = L + 24, L + 444            # diagram area inside each row
TX0 = DX1 + 34                        # text column
TW = R - 24 - TX0

def concept(y, h, letter, title, expl, principle):
    p.box(L, y, R - L, h, bar=T["bar"])
    p.add(f'<line x1="{DX1+14}" y1="{y+22}" x2="{DX1+14}" y2="{y+h-22}" stroke="{T["line"]}" stroke-width="1"/>')
    p.text(TX0, y + 44, letter, 15, T["accent"], 800, ls=3)
    p.text(TX0, y + 76, title, 23, T["head"], 700)
    yy = p.para(TX0, y + 108, expl, 16.5, TW, T["body"], 400)
    py = yy + 24
    p.text(TX0, py + 14, "SECURITY PRINCIPLE", 12.5, T["label"], 700, ls=2)
    p.para(TX0, py + 40, principle, 17, TW, T["head"], 600, 1.35)

rh, rg = 284, 18
ry = 286 if theme == "dark" else 290

# A. Anatomy of a prompt
concept(ry, rh, "A", "Anatomy of a prompt",
        "A model sees one block of text, assembled from sources with very different levels of trust.",
        "Untrusted content must never be treated as trusted instructions.")
by = ry + 30
for k, (lab, who, trusted) in enumerate([("System instructions", "Your organization", True),
                                         ("User request", "The user", False),
                                         ("Retrieved documents", "Your data, any author", False)]):
    yy = by + k * 58
    col = T["accent"] if trusted else T["deny"]
    p.box(DX0, yy, 300, 48, fill=T["strip"], stroke=col, rx=4, dash=("" if trusted else "5 4"))
    p.text(DX0 + 14, yy + 21, lab, 15.5, T["head"], 700)
    p.text(DX0 + 14, yy + 39, who, 12.5, T["muted"], 400, extra=' font-style="italic"')
    p.text(DX0 + 300 + 12, yy + 29, "TRUSTED" if trusted else "UNTRUSTED", 11.5, col, 800, ls=1)
p.line(f"M{DX0+150} {by+3*58-8} V{by+3*58+14}", T["accent"], 2, mk="aAcc")
mcy = by + 3 * 58 + 18
p.box(DX0 + 40, mcy, 220, 40, fill=T["hi"][0], stroke=T["accent"], rx=4)
p.text(DX0 + 150, mcy + 26, "MODEL CONTEXT", 15, T["hi"][1], 800, "middle", 2)

# B. Retrieval-augmented generation
ry += rh + rg
concept(ry, rh, "B", "Retrieval-augmented generation",
        "With RAG, the AI looks up enterprise documents before answering, but only ones this user may open.",
        "Enforce entitlements before retrieved information enters the model.")
by = ry + 28
p.box(DX0 + 90, by, 230, 40, fill=T["strip"], stroke=T["dat"], rx=4)
p.text(DX0 + 205, by + 26, "User’s entitlements", 15.5, T["head"], 700, "middle")
docs_y = by + 70
dxs = [DX0 + 40, DX0 + 170, DX0 + 300]
for k, dx in enumerate(dxs):
    ok = k < 2
    col = T["accent"] if ok else T["deny"]
    p.line(f"M{DX0+205} {by+40} V{by+54} H{dx+40} V{docs_y-4}", T["muted"], 1.5)
    p.add(f'<path d="M{dx} {docs_y} H{dx+60} L{dx+80} {docs_y+20} V{docs_y+84} H{dx} Z" fill="{T["panel"]}" '
          f'stroke="{col}" stroke-width="2" stroke-linejoin="round"/>')
    p.line(f"M{dx+60} {docs_y} V{docs_y+20} H{dx+80}", col, 2)
    for ln in range(3):
        p.line(f"M{dx+12} {docs_y+34+ln*14} H{dx+(60 if ln < 2 else 44)}", T["muted"], 2)
    bx, byy = dx + 76, docs_y + 78                     # badge on the lower-right corner
    p.add(f'<circle cx="{bx}" cy="{byy}" r="14" fill="{col}"/>')
    mark = (f'<path d="M{bx-6} {byy} l4.5 4.5 l8 -8.5" stroke="{T["bg"]}" stroke-width="3" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"/>' if ok else
            f'<path d="M{bx-5} {byy-5} l10 10 M{bx+5} {byy-5} l-10 10" stroke="{T["bg"]}" stroke-width="3" '
            f'stroke-linecap="round"/>')
    p.add(mark)
p.text(dxs[2] + 40, docs_y + 118, "Not entitled", 13, T["deny"], 700, "middle")
mcy = docs_y + 122
for dx in dxs[:2]:
    p.line(f"M{dx+40} {docs_y+86} V{mcy-3}", T["accent"], 2, mk="aAcc")
p.box(DX0 + 20, mcy, 240, 38, fill=T["hi"][0], stroke=T["accent"], rx=4)
p.text(DX0 + 140, mcy + 25, "MODEL CONTEXT", 14, T["hi"][1], 800, "middle", 2)

# C. Policy-aware model routing
ry += rh + rg
concept(ry, rh, "C", "Policy-aware model routing",
        "Which model handles a request depends on the data, the user, the model’s capabilities, cost, and where the data may be processed.",
        "A model router is a security decision point, not just a performance optimization.")
by = ry + 26
fx = DX0
for f_ in ["Classification", "Permissions", "Capability", "Cost", "Jurisdiction"]:
    w_ = tw(f_, 12, 700) + 18
    if fx + w_ > DX1 - 10: fx, by = DX0, by + 30
    p.add(f'<rect x="{fx:.1f}" y="{by}" width="{w_:.1f}" height="22" rx="11" fill="none" stroke="{T["muted"]}" stroke-width="1.2"/>')
    p.text(fx + w_ / 2, by + 15.5, f_, 12, T["muted"], 700, "middle")
    fx += w_ + 7
ry_r = by + 40
p.box(DX0 + 70, ry_r, 280, 40, fill=T["strip"], stroke=T["pol"], rx=4)
p.text(DX0 + 210, ry_r + 26, "Router  ·  restricted data", 15, T["head"], 700, "middle")
mods = [("Public", "model API", False), ("Shared", "enterprise model", False), ("Private model,", "approved region", True)]
mw, mg = 134, 9
my = ry_r + 78
for k, (a, b, ok) in enumerate(mods):
    mx = DX0 + k * (mw + mg)
    col = T["accent"] if ok else T["deny"]
    p.line(f"M{DX0+210} {ry_r+40} V{ry_r+58} H{mx+mw/2} V{my-3}", col, 2, dash=("" if ok else "5 4"))
    p.box(mx, my, mw, 58, fill=(T["hi"][0] if ok else T["strip"]), stroke=col, rx=4, dash=("" if ok else "5 4"))
    tc = T["hi"][1] if ok else T["muted"]
    p.text(mx + mw / 2, my + 24, a, 13.5, tc, 700, "middle")
    p.text(mx + mw / 2, my + 43, b, 13.5, tc, 700 if ok else 500, "middle")
    p.text(mx + mw / 2, my + 80, "✓ Allowed" if ok else "✕ Denied", 12.5, col, 800, "middle")
p.footer(cue="Swipe: how a policy becomes code  →")
print("p2:", p.save(), "| last row bottom", ry + rh, "| models bottom", my + 84)

# =========================== PAGE 3: policy as code ===========================
p = Page(3)
p.header(KICKER, "From documentation", "to deployed rule.")
y0 = 286 if theme == "dark" else 292

# Pipeline (left)
PX0, PX1 = L, L + 330
p.text(PX0, y0 + 18, "D  ·  POLICY AS CODE", 15, T["accent"], 800, ls=3)
pipe = [("Policy decision", "Governance approves the rule"), ("Git commit", "Versioned as AI-DATA-004 v1.3.0"),
        ("Review + test", "Peer review, automated tests"), ("Deploy", "Pushed to the policy engine")]
py, ph, pg = y0 + 40, 102, 36
for k, (t_, s_) in enumerate(pipe):
    yy = py + k * (ph + pg)
    last = k == len(pipe) - 1
    p.box(PX0, yy, PX1 - PX0, ph, fill=(T["hi"][0] if last else T["panel"]),
          stroke=(T["accent"] if last else T["line"]), bar=T["bar"])
    p.text(PX0 + 26, yy + 42, t_, 21, (T["hi"][1] if last else T["head"]), 700)
    p.para(PX0 + 26, yy + 70, s_, 16, PX1 - PX0 - 40, (WARM if last and theme == "light" else T["body"]), 400)
    if not last:
        p.line(f"M{(PX0+PX1)/2} {yy+ph+2} V{yy+ph+pg-3}", T["accent"], 2.5, mk="aAcc")
pipe_bottom = py + len(pipe) * (ph + pg) - pg

# Human-readable rule and code (right)
QX0 = PX1 + 34
p.text(QX0, y0 + 18, "THE SAME RULE, TWO WAYS", 15, T["label"], 700, ls=3)
qy = y0 + 40
p.box(QX0, qy, R - QX0, 104, fill=T["hi"][0], stroke=GOLD, bar=GOLD, sw=2)
p.text(QX0 + 26, qy + 34, "HUMAN-READABLE POLICY", 12.5, GOLD_LT, 700, ls=2)
p.para(QX0 + 26, qy + 66, "“Restricted information may only be processed in approved environments.”",
       19, R - QX0 - 48, WHITE, 600, 1.35)
cy0 = qy + 104 + 18
code = [
    ("k", "policy", "AI-DATA-004"),
    ("k", "version", "1.3.0"),
    ("k", "description", "&gt;"),
    ("v", "  Restricted information may only be", None),
    ("v", "  processed in approved environments.", None),
    ("b", "", None),
    ("k", "when", ""),
    ("k", "  data.classification", "restricted"),
    ("k", "  destination.approved_for_restricted", "false"),
    ("b", "", None),
    ("k", "then", ""),
    ("k", "  action", "deny"),
    ("k", "  audit", "true"),
]
lh_, csz = 27, 16.5
ch = 30 + len(code) * lh_ + 14
cbg = T["code_bg"] if theme == "dark" else NAVY
p.box(QX0, cy0, R - QX0, ch, fill=cbg, stroke=T["line"] if theme == "dark" else NAVY, rx=6)
for dot, c_ in enumerate(("#D3967E", "#FFBA54", "#9DB3AF")):
    p.add(f'<circle cx="{QX0+20+dot*16}" cy="{cy0+18}" r="4.5" fill="{c_}" opacity="0.8"/>')
p.text(R - 18, cy0 + 22, "ai-data-004.yaml", 12, "#7D8796", 500, "end", extra=f' font-family="{MONO}"')
for k, (kind, a, b) in enumerate(code):
    yy = cy0 + 54 + k * lh_
    x = QX0 + 22
    if kind == "b": continue
    if kind == "v":
        p.add(f'<text xml:space="preserve" x="{x}" y="{yy}" font-family="{MONO}" font-size="{csz}" fill="{WARM}">{a}</text>')
        continue
    val = "" if b == "" else f' <tspan fill="{GOLD_LT if b in ("deny", "false", "restricted") else WARM}">{b}</tspan>'
    p.add(f'<text xml:space="preserve" x="{x}" y="{yy}" font-family="{MONO}" font-size="{csz}" '
          f'fill="#9DB3AF">{a}:{val}</text>')
code_bottom = cy0 + ch
p.text(QX0, code_bottom + 24, "Illustrative policy definition, not vendor-specific executable code.",
       13, T["muted"], 500, extra=' font-style="italic"')

# Principle + closing
zy = max(pipe_bottom, code_bottom + 24) + 30
p.box(L, zy, R - L, 62, fill=T["strip"], bar=GOLD, rx=0)
p.text(L + 28, zy + 38, "SECURITY PRINCIPLE", 12.5, T["label"], 700, ls=2)
p.text(L + 28 + tw("SECURITY PRINCIPLE", 12.5, 700) + 2 * 18 + 24, zy + 38,
       "Policy changes deserve the same discipline as production software.", 17, T["head"], 600)
cy = zy + 62 + 66
p.text(L, cy, "Every component of the AI stack is a control point,", 30, T["closing"], 800)
p.text(L, cy + 42, "a trust boundary, or a source of risk.", 30, T["closing"], 800)
p.text(L, cy + 92, "Next in the series: Testing and Proving AI Security", 17, T["muted"], 600, extra=' font-style="italic"')
p.footer()
print("p3:", p.save(), "| pipeline bottom", pipe_bottom, "| code bottom", code_bottom, "| last line", cy + 92)
