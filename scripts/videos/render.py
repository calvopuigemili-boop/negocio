"""Renderiza los vídeos de TikTok fotograma a fotograma.

Uso:
  python3 scripts/videos/render.py                 # todos
  python3 scripts/videos/render.py 01-cobrar-factura  # uno
  python3 scripts/videos/render.py 01-cobrar-factura --fotos 2.5 8  # capturas sueltas para revisar

Cada vídeo es un HTML de esta carpeta que define DURATION, render(t) y SOUNDS.
Requiere: pip install playwright numpy · Chromium en /opt/pw-browsers · ffmpeg.
"""
import glob
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI.parent.parent / "tiktok"
CHROME = sorted(glob.glob("/opt/pw-browsers/chromium*/chrome-linux/chrome"))[-1]
FPS = 30
SR = 44100


def _env(n, ataque=0.002, caida=0.05):
    t = np.arange(n) / SR
    return np.minimum(t / ataque, 1) * np.exp(-t / caida)


def efecto(tipo):
    """Efectos de sonido sintetizados (suaves, sin derechos de terceros)."""
    rng = np.random.default_rng(len(tipo))
    if tipo == "tecla":
        n = int(SR * 0.03)
        ruido = rng.standard_normal(n)
        ruido = np.convolve(ruido, np.ones(6) / 6, mode="same")
        return 0.18 * ruido * _env(n, 0.0005, 0.006)
    if tipo == "enviar":
        n = int(SR * 0.18)
        t = np.arange(n) / SR
        f = 500 + 1400 * t / t[-1]
        return 0.22 * np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.005, 0.05)
    if tipo == "pop":
        n = int(SR * 0.22)
        t = np.arange(n) / SR
        a = np.sin(2 * np.pi * 880 * t) * (t < 0.08) + np.sin(2 * np.pi * 1320 * t) * (t >= 0.08)
        return 0.2 * a * _env(n, 0.003, 0.07)
    if tipo == "ding":
        n = int(SR * 0.7)
        t = np.arange(n) / SR
        a = np.sin(2 * np.pi * 1568 * t) + 0.5 * np.sin(2 * np.pi * 2093 * t)
        return 0.16 * a * _env(n, 0.002, 0.18)
    if tipo == "swoosh":
        n = int(SR * 0.45)
        ruido = rng.standard_normal(n)
        k = np.hanning(n)
        filtrado = np.convolve(ruido, np.ones(30) / 30, mode="same")
        return 0.35 * filtrado * k
    if tipo == "caja":
        n = int(SR * 0.5)
        t = np.arange(n) / SR
        a = np.sin(2 * np.pi * 2637 * t) + np.sin(2 * np.pi * 3520 * t)
        return 0.12 * a * _env(n, 0.002, 0.12)
    if tipo == "tic":
        n = int(SR * 0.02)
        return 0.12 * rng.standard_normal(n) * _env(n, 0.0005, 0.004)
    raise ValueError(tipo)


def pista_audio(sonidos, duracion, destino):
    pista = np.zeros(int(SR * (duracion + 1)))
    for s in sonidos:
        x = efecto(s["tipo"])
        i = int(s["t"] * SR)
        if 0 <= i < len(pista):
            fin = min(len(pista), i + len(x))
            pista[i:fin] += x[: fin - i]
    pista = np.clip(pista, -1, 1)
    with wave.open(str(destino), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((pista * 32767).astype(np.int16).tobytes())


def renderizar(nombre, fotos=None):
    html = AQUI / f"{nombre}.html"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(html.as_uri())
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        duracion = pg.evaluate("DURATION")
        if fotos:
            for t in fotos:
                pg.evaluate(f"render({t})")
                pg.screenshot(path=str(AQUI / f"_revision-{nombre}-{t}.png"))
            b.close()
            return
        sonidos = pg.evaluate("SOUNDS")
        destino_dir = SALIDA / nombre
        destino_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "audio.wav"
            pista_audio(sonidos, duracion, wav)
            ff = subprocess.Popen(
                ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                 "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
                 str(destino_dir / "video.mp4")],
                stdin=subprocess.PIPE)
            for i in range(int(duracion * FPS)):
                pg.evaluate(f"render({i / FPS})")
                ff.stdin.write(pg.screenshot(type="jpeg", quality=93))
            ff.stdin.close()
            ff.wait()
            pg.evaluate(f"render({duracion * 0.15})")
            pg.screenshot(path=str(destino_dir / "portada.jpg"), type="jpeg", quality=90)
        b.close()
    print(destino_dir / "video.mp4")


def main():
    args = sys.argv[1:]
    fotos = None
    if "--fotos" in args:
        i = args.index("--fotos")
        fotos = [float(x) for x in args[i + 1:]]
        args = args[:i]
    nombres = args or sorted(p.stem for p in AQUI.glob("[0-9]*.html"))
    for n in nombres:
        renderizar(n, fotos)


if __name__ == "__main__":
    main()
