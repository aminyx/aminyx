"""Генератор баннера профиля.

Ограничения, из которых вырос дизайн:
  - README не имеет своего CSS, поэтому вся типографика — внутри SVG;
  - GitHub рендерит SVG как картинку, внешние шрифты не грузятся, поэтому
    только моноширинный стек с запасными вариантами;
  - ширина глифов у Consolas / SF Mono / Liberation Mono различается, поэтому
    графика НЕ привязана к ширине текста и всё выровнено по левому краю
    с большим запасом справа.

Мотив: трасса трафика (столбики) + узлы сети. Палитра холодная, один акцент.
Фиолетовый неон прошлой версии убран намеренно.
"""
import math
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1280, 320
MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace"

THEMES = {
    "banner-dark": dict(
        bg="#07090D", hair="#161E28", fg="#EAF1F8", muted="#6F7B88",
        accent="#22D3EE", accent2="#2DD4BF", grid_op="0.5", trace_op="0.55",
    ),
    "banner-light": dict(
        bg="#FBFCFD", hair="#E2E8F0", fg="#0A0F16", muted="#57626E",
        accent="#0891B2", accent2="#0D9488", grid_op="0.85", trace_op="0.40",
    ),
}


def trace_bars(x0, y_base, width, height, n=110, seed=7):
    """Столбики переменной высоты. Детерминированно: сумма несоизмеримых синусов."""
    out, step = [], width / n
    for i in range(n):
        t = i / n
        v = (math.sin(t * 11.3 + seed) * 0.5
             + math.sin(t * 27.7 + seed * 2) * 0.3
             + math.sin(t * 53.1 + seed * 3) * 0.2)
        h = max(2.0, abs(v) * height)
        # плавное затухание к обоим краям, чтобы трасса не обрывалась резко
        fade = math.sin(min(1.0, t * 1.15) * math.pi) ** 0.6
        out.append((x0 + i * step, y_base - h, h, fade))
    return out


def build(name, c):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="Aminyx — full-stack developer and cybersecurity">',
         '<title>Aminyx — full-stack developer · cybersecurity</title>', '<defs>']
    add = p.append

    # мягкое затухание сетки и трассы влево — вместо непрозрачной подложки,
    # которая в прошлой версии давала видимый вертикальный шов
    add('<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0.00" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="0.34" stop-color="#000" stop-opacity="0.35"/>'
        '<stop offset="0.62" stop-color="#000" stop-opacity="1"/>'
        '<stop offset="1.00" stop-color="#000" stop-opacity="1"/></linearGradient>')
    add('<mask id="rightOnly"><rect width="%d" height="%d" fill="url(#fade)"/></mask>' % (W, H))
    add(f'<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{c["accent"]}"/>'
        f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></linearGradient>')
    add(f'<linearGradient id="tick" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{c["accent"]}"/>'
        f'<stop offset="1" stop-color="{c["accent2"]}" stop-opacity="0.25"/></linearGradient>')
    add('<pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">'
        f'<path d="M34 0H0V34" fill="none" stroke="{c["hair"]}" stroke-width="1" '
        f'opacity="{c["grid_op"]}"/></pattern>')
    add('</defs>')

    add(f'<rect width="{W}" height="{H}" rx="16" fill="{c["bg"]}"/>')
    add(f'<g mask="url(#rightOnly)"><rect width="{W}" height="{H}" rx="16" fill="url(#grid)"/></g>')

    # трасса трафика
    add('<g mask="url(#rightOnly)">')
    for x, y, h, fade in trace_bars(540, 250, 720, 140):
        add(f'<rect x="{x:.1f}" y="{y:.1f}" width="3.4" height="{h:.1f}" rx="1.7" '
            f'fill="{c["accent"]}" opacity="{0.08 + float(c["trace_op"]) * fade:.3f}"/>')
    add('</g>')

    # узлы сети в правой трети
    nodes = [(812, 92), (936, 62), (1064, 104), (1180, 72), (1112, 156), (880, 152)]
    add('<g mask="url(#rightOnly)">')
    for i, (x1, y1) in enumerate(nodes):
        x2, y2 = nodes[(i + 1) % len(nodes)]
        add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["accent2"]}" '
            f'stroke-width="1" opacity="0.3"/>')
    for x, y in nodes:
        add(f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="{c["accent"]}" '
            f'stroke-width="1" opacity="0.25"/>')
        add(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{c["accent"]}" opacity="0.92"/>')
    add('</g>')

    # левый акцентный штрих
    add('<rect x="70" y="86" width="3" height="206" rx="1.5" fill="url(#tick)"/>')

    # текстовый блок: ритм 112 / 196 / 236 / 264
    add(f'<text x="102" y="100" font-family="{MONO}" font-size="14" letter-spacing="5" '
        f'fill="{c["muted"]}">$ whoami</text>')
    add(f'<text x="102" y="210" font-family="{MONO}" font-size="92" font-weight="700" '
        f'letter-spacing="1" fill="{c["fg"]}">aminyx</text>')
    add(f'<text x="102" y="258" font-family="{MONO}" font-size="16" letter-spacing="3" '
        f'fill="{c["accent"]}">full-stack developer  ·  cybersecurity</text>')
    add(f'<text x="102" y="286" font-family="{MONO}" font-size="14" letter-spacing="2.4" '
        f'fill="{c["muted"]}">rust · go · kotlin · python · typescript</text>')

    add(f'<rect x="102" y="302" width="300" height="1" fill="url(#rule)"/>')
    add(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{c["hair"]}"/>')
    add('</svg>')

    f = OUT / f"{name}.svg"
    f.write_text("\n".join(p), encoding="utf-8")
    return f


for n, cc in THEMES.items():
    f = build(n, cc)
    print(f"  {f.name}: {f.stat().st_size} bytes")
