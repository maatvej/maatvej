#!/usr/bin/env python3
"""Build the SVG assets of the GitHub profile README, in dark and light variants.

    python assets/src/build.py

Edit the CONTENT section below, run the script and commit assets/*.svg.
Brand logos come from simple-icons (CC0) and are vendored in icons.json.
Only the standard library is used.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
ICONS = json.loads((SRC / "icons.json").read_text(encoding="utf-8"))

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": {
        "card": "#151b23", "border": "#2a313c", "text": "#f0f6fc", "muted": "#9198a1",
        "subtle": "#656c76", "chip": "#1b222b", "chip_border": "#2f3742", "chip_text": "#d1d7e0",
        "ink": "#f0f6fc", "tint": 0.12,
    },
    "light": {
        "card": "#ffffff", "border": "#d1d9e0", "text": "#1f2328", "muted": "#59636e",
        "subtle": "#818b98", "chip": "#f6f8fa", "chip_border": "#d1d9e0", "chip_text": "#25292e",
        "ink": "#1f2328", "tint": 0.08,
    },
}

BRAND = {"dark": ("#38bdf8", "#a78bfa", "#f472b6"), "light": ("#0284c7", "#7c3aed", "#db2777")}

ACCENTS = {
    "cyan": {"dark": ("#22d3ee", "#60a5fa"), "light": ("#0891b2", "#2563eb")},
    "violet": {"dark": ("#a78bfa", "#f472b6"), "light": ("#7c3aed", "#db2777")},
    "amber": {"dark": ("#fbbf24", "#fb923c"), "light": ("#b45309", "#ea580c")},
    "emerald": {"dark": ("#34d399", "#2dd4bf"), "light": ("#047857", "#0d9488")},
    "indigo": {"dark": ("#818cf8", "#c084fc"), "light": ("#4f46e5", "#9333ea")},
    "sky": {"dark": ("#38bdf8", "#2dd4bf"), "light": ("#0369a1", "#0f766e")},
    "rose": {"dark": ("#fb7185", "#fdba74"), "light": ("#e11d48", "#ea580c")},
}

# Brand colours that vanish on one of the backgrounds get a readable stand-in.
LOGO_OVERRIDES = {
    "dark": {
        "numpy": "#4dabcf", "pandas": "#e70488", "sqlite": "#4fa3d9", "django": "#44b78b",
        "flask": "#e6edf3", "ollama": "#e6edf3", "openai": "#e6edf3", "optuna": "#6ba3ff",
    },
    "light": {
        "duckdb": "#1f2328", "clickhouse": "#b88a00", "ruff": "#1f2328", "huggingface": "#e0a800",
        "linux": "#1f2328", "openai": "#1f2328", "optuna": "#1e4fa8", "react": "#087ea4",
    },
}

# --------------------------------------------------------------------------- text metrics
# Helvetica/Arial advance widths (1/1000 em) for ASCII 32..126; used to lay out chips and
# to warn when a line would overflow. System fonts differ a little, so layouts keep slack.
_REG = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278,
        556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556,
        1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
        667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556,
        333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
        556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584]
_BOLD = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278,
         556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611,
         975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778,
         667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556,
         333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611,
         611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584]
_OTHER = {"×": 584, "→": 1000, "—": 1000, "–": 556, "·": 278, "≈": 584, "α": 578, "β": 575,
          "↗": 1000, "●": 600, "’": 222}


def text_width(s: str, size: float, weight: int = 400, mono: bool = False) -> float:
    if mono:
        return len(s) * 0.61 * size
    w = 0.0
    for ch in s:
        code = ord(ch)
        if 32 <= code <= 126:
            reg, bold = _REG[code - 32], _BOLD[code - 32]
            w += reg + (bold - reg) * min(max((weight - 400) / 300, 0), 1)
        else:
            w += _OTHER.get(ch, 600)
    return w * size / 1000 * 1.03


def check(label: str, s: str, size: float, max_w: float, weight: int = 400, mono: bool = False) -> None:
    w = text_width(s, size, weight, mono)
    if w > max_w:
        print(f"  ! overflow in {label}: {s!r} is ~{w:.0f}px, room {max_w:.0f}px")


# --------------------------------------------------------------------------- svg helpers
def attrs(**kw) -> str:
    return "".join(f' {k.rstrip("_").replace("_", "-")}="{v}"' for k, v in kw.items() if v is not None)


def text(x, y, s, size, fill, weight=400, family=SANS, anchor=None, cls=None, **kw) -> str:
    return (f'<text x="{x:g}" y="{y:g}" font-family="{family}" font-size="{size:g}" font-weight="{weight}"'
            f' fill="{fill}"{attrs(text_anchor=anchor, class_=cls, **kw)}>{escape(s)}</text>')


def lin(gid, colors, x2=1, y2=0, opacity=None) -> str:
    n = len(colors) - 1
    stops = "".join(f'<stop offset="{i / n:g}" stop-color="{c}"{attrs(stop_opacity=opacity)}/>' for i, c in enumerate(colors))
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{stops}</linearGradient>'


def icon_gradient(gid, colors) -> str:
    # Icons contain straight vertical strokes; a bounding-box gradient on a zero-width
    # shape paints nothing, so icon gradients live in the icon's own 44 x 44 space.
    stops = "".join(f'<stop offset="{i}" stop-color="{c}"/>' for i, c in enumerate(colors))
    return f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="44" y2="44">{stops}</linearGradient>'


BASE_CSS = """
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes slide{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:none}}
@keyframes pulse{0%{opacity:.75;transform:scale(1)}80%,100%{opacity:0;transform:scale(3.4)}}
@keyframes eq{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.45)}}
@keyframes drift1{from{transform:translate(0,0)}to{transform:translate(70px,26px)}}
@keyframes drift2{from{transform:translate(0,0)}to{transform:translate(-60px,30px)}}
@keyframes wave{from{transform:translateX(0)}to{transform:translateX(-1000px)}}
.rise{animation:rise .8s cubic-bezier(.2,.7,.2,1) both}
.fade{animation:fade 1s ease both}
.eq{transform-box:fill-box;transform-origin:center;animation:eq 1.6s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def document(w, h, body, title, defs="", css="") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"'
            f' role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>{BASE_CSS}{css}</style><defs>{defs}</defs>{body}</svg>\n')


def delay(seconds: float) -> str:
    return f"animation-delay:{seconds:.2f}s"


def logo(slug, x, y, size, theme) -> str:
    icon = ICONS[slug]
    color = LOGO_OVERRIDES[theme].get(slug, "#" + icon["hex"])
    return (f'<svg x="{x:g}" y="{y:g}" width="{size}" height="{size}" viewBox="0 0 24 24">'
            f'<path d="{icon["path"]}" fill="{color}"/></svg>')


def chip(x, y, label, theme, slug=None, h=28, size=13) -> tuple[str, float]:
    t = THEMES[theme]
    pad, icon_w = 11, (15 + 7 if slug else 0)
    w = pad + icon_w + text_width(label, size) + pad
    out = f'<rect x="{x:g}" y="{y:g}" width="{w:.1f}" height="{h}" rx="{h / 2:g}" fill="{t["chip"]}" stroke="{t["chip_border"]}"/>'
    if slug:
        out += logo(slug, x + pad, y + (h - 15) / 2, 15, theme)
    out += text(x + pad + icon_w, y + h / 2 + size * 0.36, label, size, t["chip_text"], 500)
    return out, w


def chip_row(x, y, items, theme, max_x, gap=8, h=28, line_gap=10) -> tuple[str, float]:
    """Lay chips left to right, wrapping at max_x. Returns markup and the bottom y."""
    out, cx, cy = "", x, y
    for item in items:
        slug, label = item if isinstance(item, tuple) else (None, item)
        _, w = chip(0, 0, label, theme, slug, h)
        if cx > x and cx + w > max_x:
            cx, cy = x, cy + h + line_gap
        markup, w = chip(cx, cy, label, theme, slug, h)
        out += markup
        cx += w + gap
    return out, cy + h


# --------------------------------------------------------------------------- icons (44 x 44)
def gear_path(cx, cy, r_out, r_in, teeth=8) -> str:
    step, pts = 2 * math.pi / teeth, []
    for i in range(teeth):
        a = i * step - math.pi / 2
        for da, r in ((-0.30, r_in), (-0.16, r_out), (0.16, r_out), (0.30, r_in)):
            pts.append((cx + r * math.cos(a + da * step), cy + r * math.sin(a + da * step)))
    return "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in pts) + " Z"


def icon(name, accent_id, solid) -> str:
    s = f'fill="none" stroke="url(#{accent_id})" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"'
    if name == "forecast":
        body = ('<path d="M6 7 V37 H39" opacity=".45"/>'
                '<path d="M10 31 L16 24 L21 27 L27 18"/>'
                '<path d="M27 18 L32.5 14.5 L38.5 10" stroke-dasharray="2.6 3.4"/>'
                f'<path d="M27 18 L39 5 L39 17 Z" fill="{solid}" fill-opacity=".22" stroke="none"/>'
                f'<circle cx="27" cy="18" r="2.7" fill="{solid}" stroke="none"/>')
    elif name == "sql":
        body = ('<path d="M10 6 H34 A5 5 0 0 1 39 11 V25 A5 5 0 0 1 34 30 H20 L12 37 V30 H10 A5 5 0 0 1 5 25 V11 A5 5 0 0 1 10 6 Z"/>'
                f'<text x="22" y="22.2" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="700"'
                f' fill="{solid}" stroke="none">SQL</text>')
    elif name == "gear":
        body = f'<path d="{gear_path(22, 22, 18, 13.6)}"/><circle cx="22" cy="22" r="5.4"/>'
    elif name == "tag":
        body = ('<path d="M6.5 21 L21 6.5 H35.5 A2 2 0 0 1 37.5 8.5 V23 L23 37.5 A2.4 2.4 0 0 1 19.6 37.5'
                ' L6.5 24.4 A2.4 2.4 0 0 1 6.5 21 Z"/>'
                f'<circle cx="31" cy="13" r="2.2" fill="{solid}" stroke="none"/>'
                '<path d="M26.5 18.5 L17 28"/><circle cx="17.6" cy="19.4" r="2"/><circle cx="26" cy="27.2" r="2"/>')
    elif name == "wave":
        bars = [(7, 9), (13, 18), (19, 28), (25, 16), (31, 24), (37, 11)]
        body = "".join(f'<path class="eq" style="{delay(i * 0.18)}" d="M{x} {22 - h / 2:g} V{22 + h / 2:g}"/>'
                       for i, (x, h) in enumerate(bars))
    elif name == "plane":
        body = ('<path d="M39 6 L5 19.5 L15.5 24 L19 35.5 L24.5 28.5 L31.5 34 Z"/>'
                '<path d="M15.5 24 L39 6 M19 35.5 L20.5 26.5"/>')
    elif name == "clock":
        body = ('<circle cx="22" cy="22" r="16"/><path d="M22 12 V22 L29 26"/>'
                f'<circle cx="22" cy="22" r="2" fill="{solid}" stroke="none"/>')
    else:
        raise ValueError(name)
    return f'<g {s}>{body}</g>'


# --------------------------------------------------------------------------- CONTENT
EXPERIENCE = [
    dict(
        slug="exp-pricing", accent="cyan", icon="forecast", period="JUN 2026 — NOW",
        meta=["Production ML", "Team project", "Retail pricing"],
        title="Retail Markdown Pricing Pipeline",
        desc="TFT demand forecasts → 21-scenario price curves → margin optimizer within turnover targets",
        pills=[("6×", "faster optimizer · 882 → 148 s"), ("~18×", "faster preprocessing · Polars"),
               ("229K", "demand curves per run")],
        chips=["TFT", ("lightning", "Lightning"), ("optuna", "Optuna"), ("polars", "Polars"),
               ("duckdb", "DuckDB"), ("postgresql", "PostgreSQL"), ("nvidia", "GPU · Docker")],
    ),
    dict(
        slug="exp-text2sql", accent="violet", icon="sql", period="APR — JUN 2026",
        meta=["LLM application", "Team project", "Retail analytics"],
        title="LLM Text-to-SQL Assistant",
        desc="Business questions in plain Russian → ClickHouse SQL → a table, a chart and a commentary",
        pills=[("9 LLMs", "per-request model switching"), ("Guardrails", "from real ClickHouse failures"),
               ("Multi-turn", "follow-ups → concrete filters")],
        chips=["Prompt engineering", ("openai", "OpenAI SDK"), "Yandex AI Studio", ("clickhouse", "ClickHouse"),
               ("flask", "Flask"), ("docker", "Docker")],
    ),
    dict(
        slug="exp-reliability", accent="amber", icon="gear", period="JAN — FEB 2026",
        meta=["Desktop application", "Team project", "Backend owner"],
        title="Equipment Reliability & PM Planning",
        desc="Censored Weibull fits, Monte Carlo life cycles and budget-cut maintenance plans — one offline .exe",
        pills=[("6 of 8", "API router modules built"), ("1 file", ".exe, runs fully offline"),
               ("E2E", "API scenario tests")],
        chips=[("fastapi", "FastAPI"), "SQLAlchemy async", ("pydantic", "Pydantic v2"),
               ("pandas", "pandas"), "PyInstaller", "PyStray"],
    ),
    dict(
        slug="exp-elasticity", accent="emerald", icon="tag", period="OCT 2025 — JAN 2026",
        meta=["Analytics platform", "Main backend dev", "FMCG pricing"],
        title="Promo Elasticity & Pricing Simulator",
        desc="Uplift-vs-discount curves, what-if price simulations and profit-optimal discounts for FMCG",
        pills=[("~70%", "of all project commits"), ("1.4M", "weekly sales records"),
               ("3 tenants", "on one star schema")],
        chips=[("fastapi", "FastAPI"), ("scipy", "SciPy curve_fit"), ("scikitlearn", "Isotonic regression"),
               "statsmodels", ("sqlite", "SQLite"), ("docker", "Compose")],
    ),
]

EIDOS = dict(
    slug="proj-eidos", accent="indigo", icon="wave", period="AUG 2026",
    meta=["Personal project", "Solo developer", "Self-hosted"], hint="maatvej/Eidos ↗",
    title="Eidos — Offline-First Meeting AI",
    desc="Recordings → speaker-attributed transcripts, summaries, decisions and action items, fully local",
    pills=[("Whisper", "large-v3-turbo + pyannote"), ("32-dim", "voice embeddings in NumPy"),
           ("237 tests", "152 pytest + 85 Vitest")],
    chips=[("fastapi", "FastAPI"), ("django", "Django 5"), ("react", "React 19"), ("typescript", "TypeScript"),
           ("ollama", "Ollama"), ("ffmpeg", "FFmpeg")],
)

SMALL_PROJECTS = [
    dict(
        slug="proj-stickers", accent="sky", icon="plane", sub="TELEGRAM BOT · OCT 2026",
        title="Sticker Converter Bot",
        lines=["Static, Lottie and VP9 video stickers → PNG, GIF,", "APNG, WebP or WebM with transparency kept;",
               "flicker-free GIFs, 58 pytest cases."],
        chips=[("telegram", "aiogram 3"), ("ffmpeg", "ffmpeg"), "rlottie", "Pillow"],
    ),
    dict(
        slug="proj-chronos", accent="rose", icon="clock", sub="TIME SERIES · SEP 2025",
        title="Chronos-T5 Fine-Tuning",
        lines=["Full fine-tuning of Chronos-T5-Large for retail", "sales: 14.9M rows → 182K series, streamed",
               "training, probabilistic WAPE evaluation."],
        chips=[("huggingface", "Transformers"), ("pytorch", "PyTorch"), "GluonTS", ("apacheparquet", "Parquet")],
    ),
]

HIGHLIGHTS = [
    ("OPTIMIZER", "6×", "faster optimizer", ["882 s → 148 s on the", "largest category"], "cyan", "forecast"),
    ("POLARS", "~18×", "faster preprocessing", ["pandas → Polars with", "bit-identical output"], "violet", "wave"),
    ("SCALE", "229K", "demand curves / run", ["TFT × 21 price scenarios", "× 6-week horizon"], "emerald", "tag"),
    ("LLM", "9", "models, one assistant", ["Text-to-SQL over", "ClickHouse"], "amber", "sql"),
]

STACK = [
    ("ML & FORECASTING", "cyan", [("pytorch", "PyTorch"), ("lightning", "Lightning"), "TFT", ("optuna", "Optuna"),
                                  ("scikitlearn", "scikit-learn"), "statsmodels", ("scipy", "SciPy"),
                                  ("huggingface", "Transformers")]),
    ("DATA", "emerald", [("polars", "Polars"), ("pandas", "pandas"), ("numpy", "NumPy"), ("duckdb", "DuckDB"),
                         ("clickhouse", "ClickHouse"), ("postgresql", "PostgreSQL"), ("sqlite", "SQLite"),
                         ("apacheparquet", "Parquet")]),
    ("LLM & SPEECH", "violet", [("openai", "OpenAI-compatible APIs"), "Yandex AI Studio", ("ollama", "Ollama"),
                                "Faster-Whisper", "pyannote.audio", ("ffmpeg", "FFmpeg")]),
    ("BACKEND", "amber", [("fastapi", "FastAPI"), ("django", "Django"), ("flask", "Flask"),
                          ("pydantic", "Pydantic v2"), "SQLAlchemy", ("telegram", "aiogram")]),
    ("MLOPS & TOOLS", "sky", [("docker", "Docker"), ("nvidia", "CUDA GPUs"), ("gitlab", "GitLab CI"), ("uv", "uv"),
                              ("ruff", "Ruff"), ("pytest", "pytest"), ("git", "Git"), ("linux", "Linux")]),
    ("LANGUAGES & FRONTEND", "rose", [("python", "Python"), "SQL", ("typescript", "TypeScript"), ("gnubash", "Bash"),
                                      ("react", "React"), ("vite", "Vite"), ("tailwindcss", "Tailwind CSS"),
                                      ("vitest", "Vitest")]),
]


# --------------------------------------------------------------------------- banner
def banner(theme) -> str:
    W, H = 1000, 280
    t, (c1, c2, c3) = THEMES[theme], BRAND[theme]
    dark = theme == "dark"
    bg = ("#0a0f1e", "#0f172a", "#1d1645") if dark else ("#f7fbff", "#eef3ff", "#f7f0ff")
    name_c, tag_c = ("#f0f6fc", "#9fb0c8") if dark else ("#0f172a", "#475569")
    blob_op = (0.30, 0.26, 0.20) if dark else (0.22, 0.18, 0.14)

    defs = (lin("bg", bg, 1, 1) + lin("brand", (c1, c2, c3)) + lin("histg", (c1, c2))
            + f'<linearGradient id="areag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}" stop-opacity=".30"/>'
              f'<stop offset="1" stop-color="{c1}" stop-opacity="0"/></linearGradient>'
            + '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>'
            + f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1"'
              f' fill="{t["ink"]}" fill-opacity="{0.09 if dark else 0.07}"/></pattern>'
            + f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>')

    # chart geometry
    x0, dx, base, scale = 560, 22, 232, 170
    hist = [0.30, 0.36, 0.33, 0.42, 0.38, 0.47, 0.44, 0.40, 0.49, 0.55, 0.51, 0.60, 0.64]
    med = [0.64, 0.62, 0.67, 0.70, 0.68, 0.73, 0.76]
    outer = [0, 0.05, 0.09, 0.12, 0.15, 0.18, 0.21]
    inner = [0, 0.025, 0.045, 0.06, 0.075, 0.09, 0.105]
    y = lambda v: base - v * scale
    hp = [(x0 + i * dx, y(v)) for i, v in enumerate(hist)]
    now = hp[-1][0]
    fx = [now + i * dx for i in range(len(med))]

    def smooth(pts):
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
        for i in range(len(pts) - 1):
            p0, p1, p2 = pts[max(i - 1, 0)], pts[i], pts[i + 1]
            p3 = pts[min(i + 2, len(pts) - 1)]
            a = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            b = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += f" C{a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        return d

    def band(half):
        top = [(x, y(m + h)) for x, m, h in zip(fx, med, half)]
        bot = [(x, y(m - h)) for x, m, h in zip(fx, med, half)][::-1]
        return "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in top + bot) + " Z"

    hist_d = smooth(hp)
    area_d = hist_d + f" L{now:.1f},{base} L{x0},{base} Z"
    grid = "".join(f'<path d="M{x0} {gy} H{fx[-1]}" stroke="{t["ink"]}" stroke-opacity=".07" stroke-dasharray="2 6"/>'
                   for gy in (80, 118, 156, 194))

    chart = (
        grid
        + f'<path d="M{x0} {base} H{fx[-1]}" stroke="{t["ink"]}" stroke-opacity=".18"/>'
        + f'<path class="fade" style="{delay(1.5)}" d="{area_d}" fill="url(#areag)"/>'
        + f'<path class="hist" d="{hist_d}" pathLength="1" fill="none" stroke="url(#histg)" stroke-width="3"'
          f' stroke-linecap="round" stroke-linejoin="round"/>'
        + f'<path d="M{now} 50 V{base}" stroke="{t["ink"]}" stroke-opacity=".28" stroke-dasharray="3 4"/>'
        + text(now, 42, "now", 11.5, tag_c, 500, MONO, "middle", "fade", style=delay(1.8))
        + f'<g class="fc">'
          f'<path d="{band(outer)}" fill="{c2}" fill-opacity="{0.20 if dark else 0.16}"/>'
          f'<path d="{band(inner)}" fill="{c2}" fill-opacity="{0.28 if dark else 0.22}"/>'
          f'<path d="{smooth(list(zip(fx, map(y, med))))}" fill="none" stroke="{c3}" stroke-width="2.6"'
          f' stroke-dasharray="5 5" stroke-linecap="round"/></g>'
        + f'<circle class="ring" cx="{now}" cy="{hp[-1][1]:.1f}" r="5" fill="none" stroke="{c1}" stroke-width="2" opacity="0"/>'
        + f'<circle cx="{now}" cy="{hp[-1][1]:.1f}" r="4.6" fill="{c1}" stroke="{bg[1]}" stroke-width="2"/>'
        + text(x0, 254, "weekly demand", 11.5, tag_c, 500, MONO, cls="fade", style=delay(1.8))
        + text(fx[-1], 254, "forecast · p10–p90", 11.5, tag_c, 500, MONO, "end", "fade", style=delay(2.6))
    )

    left = (
        text(56, 76, "HI THERE, I'M", 13, c1, 600, MONO, cls="rise", letter_spacing="3", style=delay(0.05))
        + text(54, 136, "Matvey Musatov", 56, name_c, 800, cls="rise", letter_spacing="-1", style=delay(0.15))
        + text(56, 178, "ML Engineer · Python Developer", 25, "url(#brand)", 700, cls="rise", style=delay(0.3))
        + text(56, 212, "Demand forecasting · Price optimization · LLM apps", 16, tag_c, 400, cls="rise", style=delay(0.45))
    )
    check("banner name", "Matvey Musatov", 56, 470, 800)
    check("banner role", "ML Engineer · Python Developer", 25, 470, 700)

    # location pill with a map-pin glyph
    pin_x, pin_y = 56, 232
    loc = "Saint Petersburg"
    loc_w = 34 + text_width(loc, 13, 500) + 14
    bio = "ML & AI solutions for business"
    bio_w = 14 + text_width(bio, 13, 500) + 14
    pill_fill, pill_stroke = ("#ffffff", "#ffffff") if dark else ("#0f172a", "#0f172a")
    pills = (
        f'<g class="rise" style="{delay(0.6)}">'
        f'<rect x="{pin_x}" y="{pin_y}" width="{loc_w:.1f}" height="26" rx="13" fill="{pill_fill}" fill-opacity=".06"'
        f' stroke="{pill_stroke}" stroke-opacity=".14"/>'
        f'<path d="M{pin_x + 19} {pin_y + 20} c-4.2-4.6-6-7.4-6-9.6a6 6 0 0 1 12 0c0 2.2-1.8 5-6 9.6z" fill="none"'
        f' stroke="{c1}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<circle cx="{pin_x + 19}" cy="{pin_y + 10.6}" r="2" fill="{c1}"/>'
        + text(pin_x + 34, pin_y + 17.6, loc, 13, tag_c, 500)
        + f'<rect x="{pin_x + loc_w + 10:.1f}" y="{pin_y}" width="{bio_w:.1f}" height="26" rx="13" fill="{pill_fill}"'
          f' fill-opacity=".06" stroke="{pill_stroke}" stroke-opacity=".14"/>'
        + text(pin_x + loc_w + 24, pin_y + 17.6, bio, 13, tag_c, 500)
        + "</g>"
    )

    css = (".hist{stroke-dasharray:1;animation:draw 2.2s cubic-bezier(.6,.05,.3,1) .5s both}"
           ".fc{animation:slide 1s ease 2.4s both}"
           ".ring{transform-box:fill-box;transform-origin:center;animation:pulse 2.6s ease-out 3s infinite both}"
           ".blob-a{animation:drift1 16s ease-in-out infinite alternate}.blob-b{animation:drift2 20s ease-in-out infinite alternate}")
    body = (
        f'<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="url(#bg)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#dots)"/>'
        f'<g filter="url(#blur)"><circle class="blob-a" cx="320" cy="-30" r="150" fill="{c1}" fill-opacity="{blob_op[0]}"/>'
        f'<circle class="blob-b" cx="930" cy="40" r="170" fill="{c2}" fill-opacity="{blob_op[1]}"/>'
        f'<circle class="blob-a" cx="700" cy="330" r="150" fill="{c3}" fill-opacity="{blob_op[2]}"/></g>'
        f'{chart}{left}{pills}</g>'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="{t["ink"]}"'
        f' stroke-opacity="{0.10 if dark else 0.12}"/>'
    )
    return document(W, H, body, "Matvey Musatov — ML Engineer & Python Developer", defs, css)


# --------------------------------------------------------------------------- highlight tiles
def highlights(theme) -> str:
    W, H, gap = 1000, 190, 16
    t = THEMES[theme]
    tw = (W - gap * 3) / 4
    defs, body = "", ""
    for i, (label, value, title, caption, accent, ic) in enumerate(HIGHLIGHTS):
        a1, a2 = ACCENTS[accent][theme]
        defs += lin(f"hl{i}", (a1, a2), 1, 1) + icon_gradient(f"hli{i}", (a1, a2))
        x = i * (tw + gap)
        inner = tw - 44
        check("highlight title", title, 16, inner, 600)
        for line in caption:
            check("highlight caption", line, 13.5, inner)
        body += (
            f'<g class="rise" style="{delay(0.1 + i * 0.12)}">'
            f'<rect x="{x + .5:.1f}" y=".5" width="{tw - 1:.1f}" height="{H - 1}" rx="14" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<rect x="{x + 22:.1f}" y=".5" width="44" height="3" rx="1.5" fill="url(#hl{i})"/>'
            + text(x + 22, 38, label, 12, a1, 700, MONO, letter_spacing="1.6")
            + f'<g transform="translate({x + tw - 46:.1f} 16) scale(.6)" opacity=".9">{icon(ic, f"hli{i}", a1)}</g>'
            + text(x + 20, 96, value, 46, f"url(#hl{i})", 800, letter_spacing="-1")
            + text(x + 22, 128, title, 16, t["text"], 600)
            + text(x + 22, 152, caption[0], 13.5, t["muted"])
            + text(x + 22, 170, caption[1], 13.5, t["muted"])
            + "</g>"
        )
    return document(W, H, body, "Highlights: 6× faster optimizer, ~18× faster preprocessing, 229K demand curves per run, 9 LLMs", defs)


# --------------------------------------------------------------------------- cards
def wide_card(theme, c) -> str:
    W, H, panel, x0, right = 1000, 236, 212, 240, 972
    t = THEMES[theme]
    a1, a2 = ACCENTS[c["accent"]][theme]
    defs = lin("acc", (a1, a2), 1, 1) + lin("tint", (a1, a2), 1, 1, opacity=t["tint"]) + icon_gradient("iacc", (a1, a2))
    check(c["slug"] + " title", c["title"], 25, right - x0, 700)
    check(c["slug"] + " desc", c["desc"], 15, right - x0)
    check(c["slug"] + " period", c["period"], 13, panel - 44, 700, mono=True)

    pills, pw = "", (right - x0 - 2 * 12) / 3
    for i, (value, label) in enumerate(c["pills"]):
        px = x0 + i * (pw + 12)
        check(c["slug"] + " pill", label, 13, pw - 30)
        pills += (f'<rect x="{px:.1f}" y="100" width="{pw:.1f}" height="62" rx="12" fill="{t["chip"]}" stroke="{t["chip_border"]}"/>'
                  + text(px + 16, 129, value, 21, "url(#acc)", 800)
                  + text(px + 16, 149, label, 13, t["muted"]))
    chips, bottom = chip_row(x0, 180, c["chips"], theme, right)
    if bottom > 208:
        print(f"  ! chips wrap in {c['slug']}")

    meta = (text(32, 142, c["meta"][0], 14, t["text"], 600)
            + text(32, 163, c["meta"][1], 13.5, t["muted"]) + text(32, 184, c["meta"][2], 13.5, t["muted"]))
    hint = text(32, 214, c["hint"], 12, a1, 600, MONO) if c.get("hint") else ""
    body = (
        f'<g class="rise">'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>'
        f'<path d="M16.5 .5 H{panel} V{H - .5} H16.5 A16 16 0 0 1 .5 {H - 16.5} V16.5 A16 16 0 0 1 16.5 .5 Z" fill="url(#tint)"/>'
        f'<path d="M{panel} .5 V{H - .5}" stroke="{t["border"]}"/>'
        f'<g transform="translate(30 28)">{icon(c["icon"], "iacc", a1)}</g>'
        + text(32, 116, c["period"], 13, a1, 700, MONO, letter_spacing=".4")
        + meta + hint
        + text(x0, 54, c["title"], 25, t["text"], 700)
        + text(x0, 82, c["desc"], 15, t["muted"])
        + pills + chips + "</g>"
    )
    return document(W, H, body, f'{c["title"]} — {c["desc"]}', defs)


def small_card(theme, c) -> str:
    W, H = 490, 226
    t = THEMES[theme]
    a1, a2 = ACCENTS[c["accent"]][theme]
    defs = lin("tint", (a1, a2), 1, 1, opacity=t["tint"] * 1.6) + icon_gradient("iacc", (a1, a2))
    check(c["slug"] + " title", c["title"], 20, W - 84 - 40, 700)
    for line in c["lines"]:
        check(c["slug"] + " line", line, 14, W - 48)
    chips, bottom = chip_row(24, 174, c["chips"], theme, W - 24)
    if bottom > 202:
        print(f"  ! chips wrap in {c['slug']}")
    body = (
        f'<g class="rise">'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>'
        f'<rect x="22" y="20" width="52" height="52" rx="14" fill="url(#tint)"/>'
        f'<g transform="translate(26.6 24.6) scale(.79)">{icon(c["icon"], "iacc", a1)}</g>'
        + text(88, 44, c["title"], 20, t["text"], 700)
        + text(88, 65, c["sub"], 11.5, a1, 700, MONO, letter_spacing="1")
        + text(W - 24, 42, "↗", 17, t["subtle"], 400, anchor="end")
        + "".join(text(24, 104 + i * 21, line, 14, t["muted"]) for i, line in enumerate(c["lines"]))
        + chips + "</g>"
    )
    return document(W, H, body, f'{c["title"]} — {" ".join(c["lines"])}', defs)


# --------------------------------------------------------------------------- stack board
def stack(theme) -> str:
    """Bento grid: two boxes per row, each box a category with wrapped logo chips."""
    W, gap, pad, top = 1000, 16, 18, 52
    t = THEMES[theme]
    bw = (W - gap) / 2
    defs, body, y = "", "", 0.5
    for r in range(0, len(STACK), 2):
        boxes = []
        for col, (label, accent, items) in enumerate(STACK[r:r + 2]):
            x = col * (bw + gap)
            chips, bottom = chip_row(x + pad, y + top, items, theme, x + bw - pad, line_gap=8)
            boxes.append((x, label, accent, chips, bottom))
        h = max(b[4] for b in boxes) + pad - y
        for col, (x, label, accent, chips, _) in enumerate(boxes):
            i = r + col
            a1, a2 = ACCENTS[accent][theme]
            defs += lin(f"st{i}", (a1, a2))
            body += (f'<g class="rise" style="{delay(0.08 * i)}">'
                     f'<rect x="{x + .5:.1f}" y="{y:.1f}" width="{bw - 1:.1f}" height="{h:.1f}" rx="14"'
                     f' fill="{t["card"]}" stroke="{t["border"]}"/>'
                     f'<rect x="{x + pad:.1f}" y="{y:.1f}" width="36" height="3" rx="1.5" fill="url(#st{i})"/>'
                     + text(x + pad + 1, y + 32, label, 12, a1, 700, MONO, letter_spacing="1.6")
                     + chips + "</g>")
        y += h + gap
    H = math.ceil(y - gap + 0.5)
    alt = "Tech stack: " + "; ".join(f"{lbl.title()}: " + ", ".join(i if isinstance(i, str) else i[1] for i in items)
                                     for lbl, _, items in STACK)
    return document(W, H, body, alt, defs)


# --------------------------------------------------------------------------- footer
def footer(theme) -> str:
    W, H = 1000, 92
    c1, c2, c3 = BRAND[theme]
    dark = theme == "dark"

    def wave_path(amp, base, phase):
        d = f"M0 {H}"
        for x in range(0, 2001, 10):
            d += f" L{x} {base + amp * math.sin((x / 1000) * 2 * math.pi * 2 + phase):.1f}"
        return d + f" L2000 {H} Z"

    # one gradient period per 1000px, so the -1000px wave loop stays seamless
    stops = "".join(f'<stop offset="{i / 4:g}" stop-color="{c}"/>' for i, c in enumerate((c1, c2, c3, c2, c1)))
    defs = (f'<linearGradient id="wg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="0"'
            f' spreadMethod="repeat">{stops}</linearGradient>')
    body = (
        f'<g style="animation:wave 18s linear infinite"><path d="{wave_path(12, 44, 0)}" fill="url(#wg)"'
        f' fill-opacity="{0.35 if dark else 0.28}"/></g>'
        f'<g style="animation:wave 11s linear infinite reverse"><path d="{wave_path(9, 58, 1.7)}" fill="url(#wg)"'
        f' fill-opacity="{0.75 if dark else 0.6}"/></g>'
    )
    return document(W, H, body, "Footer wave", defs)


# --------------------------------------------------------------------------- main
def main() -> None:
    builders = {
        "banner": banner,
        "highlights": highlights,
        "stack": stack,
        "footer": footer,
        **{c["slug"]: (lambda th, c=c: wide_card(th, c)) for c in EXPERIENCE + [EIDOS]},
        **{c["slug"]: (lambda th, c=c: small_card(th, c)) for c in SMALL_PROJECTS},
    }
    for name, build in builders.items():
        for theme in THEMES:
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(build(theme), encoding="utf-8")
        print(f"built {name}-{{dark,light}}.svg")


if __name__ == "__main__":
    main()
