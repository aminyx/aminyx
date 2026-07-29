"""Генератор баннера профиля.

Ограничения, из которых вырос дизайн:
  - у README нет своего CSS, вся типографика живёт внутри SVG;
  - GitHub рендерит SVG как картинку, внешние шрифты не грузятся —
    только моноширинный стек с запасными вариантами;
  - ширина глифов различается между Consolas / SF Mono / Liberation Mono,
    поэтому графика не привязана к ширине текста, всё по левому краю.

Мотив: hex-дамп. Выбран не как украшение — он мгновенно читается как
«низкий уровень, память, трафик, криптография», то есть ровно то, чем
занимается владелец. В ASCII-колонке справа лежат настоящие слова.
"""
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1280, 340
MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace"

THEMES = {
    "banner": dict(
        bg="#06080B", panel="#0A0E14", hair="#1B2635", fg="#F0F6FC",
        muted="#5A6673", dim="#93A1B0", accent="#22D3EE", accent2="#34D399",
        grid=0.45, hexop=0.66,
    ),
}

# ASCII-колонка складывается в осмысленные слова — деталь для тех, кто присмотрится
PAYLOAD = [
    "fullstack.go",
    "cybersec.eng",
    "rust::tokio!",
    "kotlin+droid",
    "post-quantum",
    "zero.trust.x",
    "ship_it_safe",
    "aminyx@gh://",
]


def hexdump_rows(strings, start=0x00400000):
    """Строка -> (смещение, hex-байты, ascii). Полностью детерминированно."""
    rows = []
    for i, s in enumerate(strings):
        raw = s.encode("ascii", "replace")[:14].ljust(14, b"\x20")
        hexes = " ".join(f"{b:02x}" for b in raw)
        ascii_col = "".join(chr(b) if 32 <= b < 127 else "." for b in raw)
        rows.append((f"{start + i * 16:08x}", hexes, ascii_col))
    return rows


def build(name, c):
    p = []
    add = p.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Aminyx — full-stack developer and cybersecurity engineer">')
    add('<title>Aminyx — full-stack developer · cybersecurity</title>')

    add('<defs>')
    # затухание hex-дампа к правому краю, чтобы блок не обрывался стеной
    add('<linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="1"/>'
        '<stop offset="0.95" stop-color="#fff" stop-opacity="1"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    add('<mask id="mR"><rect x="580" y="0" width="700" height="340" fill="url(#fadeR)"/></mask>')
    add(f'<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{c["accent"]}"/>'
        f'<stop offset="1" stop-color="{c["accent2"]}" stop-opacity="0.2"/></linearGradient>')
    add(f'<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{c["accent"]}" stop-opacity="0.9"/>'
        f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></linearGradient>')
    add('<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
        f'<path d="M40 0H0V40" fill="none" stroke="{c["hair"]}" stroke-width="1" '
        f'opacity="{c["grid"]}"/></pattern>')
    add(f'<linearGradient id="panelFade" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{c["bg"]}" stop-opacity="1"/>'
        f'<stop offset="1" stop-color="{c["bg"]}" stop-opacity="0"/></linearGradient>')
    add('</defs>')

    add(f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>')
    add(f'<rect width="{W}" height="{H}" rx="18" fill="url(#grid)"/>')

    # ── правый блок: hex-дамп ──────────────────────────────────────────
    add('<g mask="url(#mR)">')
    y = 84
    for off, hexes, asc in hexdump_rows(PAYLOAD):
        add(f'<text x="638" y="{y}" font-family="{MONO}" font-size="15" '
            f'fill="{c["muted"]}" opacity="0.75">{off}</text>')
        add(f'<text x="730" y="{y}" font-family="{MONO}" font-size="15" letter-spacing="0.4" '
            f'fill="{c["dim"]}" opacity="{c["hexop"]}">{hexes}</text>')
        add(f'<text x="1100" y="{y}" font-family="{MONO}" font-size="15" '
            f'fill="{c["accent"]}" opacity="0.82">|{asc}|</text>')
        y += 33
    add('</g>')

    # ── левый блок: имя и роли ────────────────────────────────────────
    # мягкая подложка, чтобы дамп не мешал читать текст
    add(f'<rect x="0" y="0" width="556" height="{H}" rx="18" fill="{c["bg"]}"/>')
    add(f'<rect x="556" y="0" width="110" height="{H}" fill="url(#panelFade)"/>')

    add(f'<rect x="76" y="96" width="3" height="208" rx="1.5" fill="url(#bar)"/>')

    add(f'<text x="108" y="114" font-family="{MONO}" font-size="14" letter-spacing="5.5" '
        f'fill="{c["muted"]}">$ whoami</text>')
    add(f'<text x="104" y="208" font-family="{MONO}" font-size="104" font-weight="700" '
        f'letter-spacing="-1" fill="{c["fg"]}">aminyx</text>')
    add(f'<rect x="108" y="234" width="352" height="1.5" fill="url(#rule)"/>')
    add(f'<text x="108" y="266" font-family="{MONO}" font-size="17" letter-spacing="2.4" '
        f'fill="{c["accent"]}">full-stack developer</text>')
    add(f'<text x="108" y="292" font-family="{MONO}" font-size="17" letter-spacing="2.4" '
        f'fill="{c["accent2"]}">cybersecurity engineer</text>')

    add(f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="18" '
        f'fill="none" stroke="{c["hair"]}" stroke-width="1.5"/>')
    add('</svg>')

    f = OUT / f"{name}.svg"
    f.write_text("\n".join(p), encoding="utf-8")
    return f


for n, cc in THEMES.items():
    f = build(n, cc)
    print(f"  {f.name}: {f.stat().st_size} bytes")


# ── полоса стека ──────────────────────────────────────────────────────
# Отдельной картинкой, потому что GitHub принудительно ставит картинкам
# в markdown display:block — ряд из отдельных бейджей всегда рассыпается
# в столбик. Одна картинка решает это и даёт единую типографику с баннером.

SW, SH = 1280, 214

COLS = [
    (108, 236, [
        ("languages", "rust · go · kotlin · python · typescript"),
        ("platform",  "linux · docker · postgresql · nginx"),
        ("web",       "next.js · typescript · vanilla js"),
    ]),
    (700, 820, [
        ("security",  "tls/quic · post-quantum · fuzzing"),
        ("tooling",   "git · github actions · wireshark"),
        ("mobile",    "android · kotlin · coroutines"),
    ]),
]


def build_stack(c):
    p = []
    add = p.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{SW}" height="{SH}" '
        f'viewBox="0 0 {SW} {SH}" role="img" aria-label="Stack: languages, platform, security">')
    add('<title>Stack</title><defs>')
    add(f'<linearGradient id="sbar" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{c["accent"]}"/>'
        f'<stop offset="1" stop-color="{c["accent2"]}" stop-opacity="0.2"/></linearGradient>')
    add('<pattern id="sgrid" width="40" height="40" patternUnits="userSpaceOnUse">'
        f'<path d="M40 0H0V40" fill="none" stroke="{c["hair"]}" stroke-width="1" '
        f'opacity="{c["grid"]}"/></pattern>')
    add('</defs>')
    add(f'<rect width="{SW}" height="{SH}" rx="18" fill="{c["bg"]}"/>')
    add(f'<rect width="{SW}" height="{SH}" rx="18" fill="url(#sgrid)"/>')
    add(f'<rect x="76" y="46" width="3" height="{SH-92}" rx="1.5" fill="url(#sbar)"/>')
    add(f'<rect x="668" y="46" width="3" height="{SH-92}" rx="1.5" fill="url(#sbar)" opacity="0.6"/>')

    for lx, vx, rows in COLS:
        y = 74
        for label, value in rows:
            add(f'<text x="{lx}" y="{y}" font-family="{MONO}" font-size="13.5" '
                f'letter-spacing="3.2" fill="{c["dim"]}" opacity="0.85">{label}</text>')
            parts = []
            for j, tok in enumerate(value.split(" · ")):
                if j:
                    parts.append(f'<tspan fill="{c["muted"]}" opacity="0.65">  ·  </tspan>')
                parts.append(f'<tspan fill="{c["fg"]}">{tok}</tspan>')
            add(f'<text x="{vx}" y="{y}" font-family="{MONO}" font-size="16" '
                f'letter-spacing="0.5">{"".join(parts)}</text>')
            y += 54

    add(f'<rect x="0.75" y="0.75" width="{SW-1.5}" height="{SH-1.5}" rx="18" '
        f'fill="none" stroke="{c["hair"]}" stroke-width="1.5"/>')
    add('</svg>')
    f = OUT / "stack.svg"
    f.write_text("\n".join(p), encoding="utf-8")
    return f


f = build_stack(THEMES["banner"])
print(f"  {f.name}: {f.stat().st_size} bytes")
