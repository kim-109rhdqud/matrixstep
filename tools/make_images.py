#!/usr/bin/env python3
"""파비콘·OG 이미지를 다시 만들 때만 실행해요 (Pillow와 Noto Sans CJK 폰트 필요). 결과는 static/ 에 저장돼요."""
import os
from PIL import Image, ImageDraw, ImageFont
SITE = "행렬 계산기"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")

def images():
    open(os.path.join(OUT, "favicon.svg"), "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1F4FD8"/>'
        '<path d="M24 16h-7v32h7M40 16h7v32h-7" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    def mark(size):
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = size / 64
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(14 * k), fill="#1F4FD8")
        w = int(5 * k)
        for pts in ([(24, 16), (17, 16), (17, 48), (24, 48)], [(40, 16), (47, 16), (47, 48), (40, 48)]):
            d.line([(x * k, y * k) for x, y in pts], fill="white", width=w, joint="curve")
        return im
    mark(180).convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))
    # OG 이미지 1200×630
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#F7F8FA"); d = ImageDraw.Draw(im)
    bold = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 84, index=1)
    reg = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 34, index=1)
    mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 40)
    im.paste(mark(88), (80, 92), mark(88))
    d.text((80, 230), SITE, font=bold, fill="#12151A")
    d.text((80, 350), "역행렬 · 행렬식 · RREF · 연립방정식", font=reg, fill="#565D69")
    d.text((80, 402), "분수로 정확하게, 풀이 과정까지", font=reg, fill="#565D69")
    d.rounded_rectangle([80, 500, 80 + 8, 540], radius=4, fill="#1F4FD8")
    # 오른쪽 행렬 그림
    vals = [["2", "1", "1"], ["1", "3", "2"], ["1", "0", "0"]]
    x0, y0, cw, rh = 770, 180, 105, 92
    for i, r in enumerate(vals):
        for j, v in enumerate(r):
            tw = d.textlength(v, font=mono); d.text((x0 + j * cw + (cw - tw) / 2, y0 + i * rh + 20), v, font=mono, fill="#12151A")
    L, R, T, B = x0 - 12, x0 + 3 * cw + 12, y0, y0 + 3 * rh
    for pts in ([(L + 16, T), (L, T), (L, B), (L + 16, B)], [(R - 16, T), (R, T), (R, B), (R - 16, B)]):
        d.line(pts, fill="#12151A", width=5)
    d.text((x0 + 30, B + 30), "A⁻¹ = ?", font=mono, fill="#1F4FD8")
    im.save(os.path.join(OUT, "og.png"), optimize=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    images()
