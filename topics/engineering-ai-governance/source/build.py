"""Generates the Engineering AI Governance overview infographic (1080 x 1350, LinkedIn 4:5).

Usage:
    python3 build.py dark  logos/tower-workshop-logo-gold.png 00-engineering-ai-governance.svg
    python3 build.py light logos/tower-workshop-logo-navy.png 00-engineering-ai-governance-light.svg

Both themes share every word of copy below; only colors differ.
Requires Pillow (to read the logo size). Text is set in Montserrat.
"""
import base64, sys
from PIL import Image

theme, logo_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
assert theme in ("dark", "light")

# Tower Workshop brand palette; light tints only where a brand hue fails contrast on navy
NAVY, BLUE, GOLD, GRAY, WHITE = "#051937", "#3870C2", "#B67E28", "#CFCFCF", "#FFFFFF"
YEL, GOLD_LT, TERRA, WARM, CHAR = "#FFC207", "#FFBA54", "#D3967E", "#E5E3DC", "#303636"

DARK = dict(bg=NAVY, panel="#0B2347", strip="#081D3D", line="#24406A", head=WHITE, body="#AEB8C6",
            kicker=GOLD_LT, label_gold=GOLD_LT, stop=YEL,
            enforce=(BLUE, "#7FA6DE"), operate=("#6E8784", "#9DB3AF"), validate=(TERRA, TERRA),
            runtime="#7FA6DE", evidence="#AEB8C6", ev_fill="#1F3A5F", ev_stroke=GOLD,
            footer_tag=WHITE, footer_accent=GOLD_LT, header_band=None)
LIGHT = dict(bg=WHITE, panel=WHITE, strip="#F4F3EF", line=GRAY, head=NAVY, body=CHAR,
             kicker=GOLD_LT, label_gold=GOLD, stop=GOLD,
             enforce=(BLUE, BLUE), operate=("#495A58", "#495A58"), validate=(TERRA, "#A9644E"),
             runtime=BLUE, evidence=NAVY, ev_fill=NAVY, ev_stroke=NAVY,
             footer_tag=NAVY, footer_accent=GOLD, header_band=NAVY)
T = DARK if theme == "dark" else LIGHT

FONT = "Montserrat, 'Segoe UI', Helvetica, Arial, sans-serif"
W, H = 1080, 1350
L, R = 52, 1004
GAP = 34
CW = (R - L - 2 * GAP) / 3

o = []
def add(s): o.append(s)
def text(x, y, s, size, fill, weight=500, anchor="start", ls=0, extra=""):
    lsp = f' letter-spacing="{ls}"' if ls else ""
    add(f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{lsp}{extra}>{s}</text>')
def marker(id_, col, size=7):
    return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="{size}" markerHeight="{size}" '
            f'orient="auto"><path d="M0 0L10 5L0 10z" fill="{col}"/></marker>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
add("<title>Engineering AI Governance — Overview</title>")
add("<defs>" + marker("aGold", GOLD) + marker("aEv", T["evidence"]) + marker("aRun", T["runtime"], 6)
    + marker("aTerra", TERRA, 6) + "</defs>")
add(f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>')

# ---- Hook (on navy in both themes, so "Now what?" stays brand yellow)
if T["header_band"]:
    add(f'<rect width="{W}" height="256" fill="{T["header_band"]}"/>')
    add(f'<rect y="256" width="{W}" height="4" fill="{GOLD}"/>')
add(f'<rect x="{L}" y="48" width="64" height="4" fill="{GOLD}"/>')
text(L, 90, "OVERVIEW  ·  ENGINEERING AI GOVERNANCE", 16, T["kicker"], 700, ls=4)
text(L, 160, "You’ve written your AI policy.", 48, WHITE, 700)
text(L, 232, "Now what?", 66, YEL, 800)
sub_y, gy = (276, 310) if theme == "dark" else (296, 326)
text(L, sub_y, "A policy only matters when controls enforce it, testing challenges it, and evidence proves it.",
     20, WARM if theme == "dark" else CHAR, 400)

# ---- Governance panel
gh = 172
add(f'<rect x="{L}" y="{gy}" width="{R-L}" height="{gh}" fill="{T["panel"]}" stroke="{T["line"]}" stroke-width="1.5"/>')
add(f'<rect x="{L}" y="{gy}" width="{R-L}" height="6" fill="{GOLD}"/>')
text(L + 28, gy + 42, "GOVERN", 15, T["label_gold"], 700, ls=3)
text(L + 28, gy + 74, "What is AI allowed to do?", 24, T["head"], 700)
text(L + 28, gy + 106, "Mission &amp; risk   ·   Regulation &amp; standards   ·   AI use policy   ·   Data policy",
     18, T["body"], 500)
add(f'<rect x="{L+1}" y="{gy+122}" width="{R-L-2}" height="{gh-123}" fill="{T["strip"]}"/>')
add(f'<line x1="{L}" y1="{gy+122}" x2="{R}" y2="{gy+122}" stroke="{T["line"]}" stroke-width="1"/>')
text(L + 28, gy + 154, "POLICY AS CODE", 14, T["label_gold"], 700, ls=2)
text(L + 214, gy + 154, "Versioned in Git  ·  Tested and approved  ·  Deployed to every control point", 17, T["body"], 500)

# ---- "Stop line" between policy and execution
sy = gy + gh + 26
add(f'<line x1="{L}" y1="{sy}" x2="{R}" y2="{sy}" stroke="{T["stop"]}" stroke-width="2" stroke-dasharray="8 6"/>')
chip = "MOST ORGANIZATIONS STOP HERE"
cw = len(chip) * 11.6 + 28
add(f'<rect x="{R-cw:.1f}" y="{sy-15}" width="{cw:.1f}" height="30" fill="{T["bg"]}"/>')
text(R - 14, sy + 5.5, chip, 15, T["stop"], 700, "end", 2)

# ---- Policy distribution connectors
cols_x = [L + i * (CW + GAP) for i in range(3)]
mids = [x + CW / 2 for x in cols_x]
bus = sy + 30
cy0 = bus + 36
add(f'<path d="M{mids[1]:.1f} {gy+gh} V{bus}" stroke="{GOLD}" stroke-width="2.5" fill="none"/>')
add(f'<path d="M{mids[0]:.1f} {bus} H{mids[2]:.1f}" stroke="{GOLD}" stroke-width="2.5" fill="none"/>')
for m in mids:
    add(f'<path d="M{m:.1f} {bus} V{cy0-2}" stroke="{GOLD}" stroke-width="2.5" fill="none" marker-end="url(#aGold)"/>')

# ---- Columns
cols = [
    (T["enforce"], "ENFORCE", "Can we stop it?", "Control access and use", [
        ("Cloud access controls", "CASB / SSE  ·  workforce access"),
        ("API gateway", "Applications and agents"),
        ("Inline guardrails", "Inspect prompts and responses"),
        ("Data loss prevention", "Block, mask, or redact"),
    ]),
    (T["operate"], "OPERATE", "Can we run it safely?", "Run AI inside policy", [
        ("Prompts &amp; context", "System prompts and templates"),
        ("Enterprise data retrieval", "RAG  ·  permissions enforced"),
        ("Model routing", "Policy-aware model selection"),
        ("LLMs, tools &amp; agents", "Inference and tool calls"),
    ]),
    (T["validate"], "VALIDATE", "Can we break it first?", "Challenge the controls", [
        ("Prompt injection", "Direct and indirect"),
        ("Jailbreak testing", "Attempts to bypass guardrails"),
        ("Data exfiltration", "Leakage via outputs and tools"),
        ("Continuous evaluation", "Re-test on every change"),
    ]),
]
ROW = 72 if theme == "dark" else 70
ch = 124 + 4 * ROW + 10
for ((bar, lab), label, q, sub, items), x in zip(cols, cols_x):
    add(f'<rect x="{x:.1f}" y="{cy0}" width="{CW:.1f}" height="{ch}" fill="{T["panel"]}" stroke="{T["line"]}" stroke-width="1.5"/>')
    add(f'<rect x="{x:.1f}" y="{cy0}" width="{CW:.1f}" height="6" fill="{bar}"/>')
    px = x + 22
    text(px, cy0 + 42, label, 15, lab, 700, ls=3)
    text(px, cy0 + 74, q, 22, T["head"], 700)
    text(px, cy0 + 102, sub, 17, T["body"], 400, extra=' font-style="italic"')
    yy = cy0 + 124
    for name, desc in items:
        add(f'<line x1="{px}" y1="{yy}" x2="{x+CW-22:.1f}" y2="{yy}" stroke="{T["line"]}" stroke-width="1"/>')
        text(px, yy + 32, name, 19, T["head"], 600)
        text(px, yy + 57, desc, 15.5, T["body"], 400)
        yy += ROW

# Runtime: Enforce -> Operate ; Adversarial testing: Validate -> Operate
ay = cy0 + 124 + ROW * 1.5
g1 = cols_x[0] + CW
add(f'<path d="M{g1+3:.1f} {ay} H{g1+GAP-4:.1f}" stroke="{T["runtime"]}" stroke-width="4" marker-end="url(#aRun)"/>')
g2 = cols_x[1] + CW
add(f'<path d="M{g2+GAP-3:.1f} {ay+ROW} H{g2+4:.1f}" stroke="{TERRA}" stroke-width="3.5" stroke-dasharray="4 3" marker-end="url(#aTerra)"/>')

# ---- Evidence connectors
ey = cy0 + ch + 42
for m in mids:
    add(f'<path d="M{m:.1f} {cy0+ch} V{ey-2}" stroke="{T["evidence"]}" stroke-width="2.5" fill="none" marker-end="url(#aEv)"/>')

# ---- Evidence band (the payoff)
eh = 124
add(f'<rect x="{L}" y="{ey}" width="{R-L}" height="{eh}" fill="{T["ev_fill"]}" stroke="{T["ev_stroke"]}" stroke-width="2"/>')
add(f'<rect x="{L}" y="{ey}" width="6" height="{eh}" fill="{GOLD}"/>')
text(L + 28, ey + 40, "PROVE", 15, YEL if theme == "light" else GOLD_LT, 700, ls=3)
text(L + 28, ey + 72, "Can we prove it?", 24, WHITE, 700)
text(R - 26, ey + 72, "What your auditor and board will ask for", 17, GOLD_LT, 500, "end", extra=' font-style="italic"')
text(L + 28, ey + 104, "AI usage telemetry  ·  Control effectiveness  ·  Findings &amp; remediation  ·  Audit &amp; authorization",
     16.5, WARM, 500)

# ---- Feedback loop
fx = 1040
add(f'<path d="M{R} {ey+eh/2} H{fx} V{gy+gh/2} H{R+4}" stroke="{GOLD}" stroke-width="3" fill="none" marker-end="url(#aGold)"/>')
lab_y = (ey + eh / 2 + gy + gh / 2) / 2
add(f'<rect x="{fx-13}" y="{lab_y-168}" width="26" height="336" fill="{T["bg"]}"/>')
text(fx, lab_y, "EVIDENCE INFORMS GOVERNANCE", 13, T["label_gold"], 700, "middle", 2.5,
     f' transform="rotate(-90 {fx} {lab_y})" dominant-baseline="central"')

# ---- Legend
ly = ey + eh + 42
lx = L
for col, dash, lab in [(GOLD, "", "Policy distribution"), (T["runtime"], "", "Runtime requests"),
                       (TERRA, "5 4", "Adversarial testing"), (T["evidence"], "", "Evidence")]:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<line x1="{lx}" y1="{ly-5}" x2="{lx+34}" y2="{ly-5}" stroke="{col}" stroke-width="3"{d}/>')
    text(lx + 44, ly, lab, 15, T["body"], 500)
    lx += 44 + len(lab) * 9.4 + 40

# ---- Footer
fy = ly + 26
add(f'<line x1="{L}" y1="{fy}" x2="{R}" y2="{fy}" stroke="{T["line"]}" stroke-width="1"/>')
add(f'<text x="{L}" y="{fy+52}" font-size="21" font-weight="700" fill="{T["footer_tag"]}">Governance defines. '
    f'Engineering enforces. <tspan fill="{T["footer_accent"]}">Evidence verifies.</tspan></text>')
b64 = base64.b64encode(open(logo_path, "rb").read()).decode()
iw, ih = Image.open(logo_path).size
lw = 176; lh = lw * ih / iw
add(f'<image x="{R-lw}" y="{fy+12}" width="{lw}" height="{lh:.1f}" href="data:image/png;base64,{b64}"/>')
add("</svg>")

open(out_path, "w").write("\n".join(o))
print(f"{theme}: wrote {out_path}; footer bottom at y={fy + 12 + lh:.0f} of {H}")
