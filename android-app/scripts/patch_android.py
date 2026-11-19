#!/usr/bin/env python3
"""Ajusta o projeto Android gerado pelo Capacitor (roda no GitHub Actions depois de `npx cap add android`):
- número da versão (pra atualização instalar por cima)
- assinatura com a chave fixa do app (senão o Android recusa atualizar)
- ícone da Fernweh Riders
- ícone e textos da notificação de gravação
"""
import os
import re
import shutil
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
APP = HERE.parent                      # android-app/
ROOT = APP.parent                      # repositório
AND = APP / "android" / "app"
RES = AND / "src" / "main" / "res"

run = int(os.environ.get("BUILD_NUMBER", "1"))

# ---------- versão e assinatura ----------
g = AND / "build.gradle"
s = g.read_text(encoding="utf-8")
s = re.sub(r"versionCode \d+", f"versionCode {run}", s)
s = re.sub(r'versionName "[^"]*"', f'versionName "1.{run}"', s)
signing = """
    signingConfigs {
        fernweh {
            storeFile file("../../fernweh-app.keystore")
            storePassword "fernwehriders"
            keyAlias "fernweh"
            keyPassword "fernwehriders"
        }
    }
"""
assert "buildTypes {" in s, "build.gradle sem buildTypes"
s = s.replace("    buildTypes {", signing + "    buildTypes {", 1)
s = re.sub(r"(release \{\s*\n)", r"\1            signingConfig signingConfigs.fernweh\n", s, count=1)
g.write_text(s, encoding="utf-8")

# ---------- ícone do app ----------
src = Image.open(ROOT / "assets" / "icon-512.png").convert("RGBA")
sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for dens, px in sizes.items():
    d = RES / f"mipmap-{dens}"
    d.mkdir(parents=True, exist_ok=True)
    im = src.resize((px, px), Image.LANCZOS)
    for name in ("ic_launcher.png", "ic_launcher_round.png"):
        im.save(d / name)
    fg = d / "ic_launcher_foreground.png"
    if fg.exists():
        fg.unlink()
# sem ícone adaptativo: usa a logo redonda como está
shutil.rmtree(RES / "mipmap-anydpi-v26", ignore_errors=True)

# ---------- notificação de gravação ----------
dr = RES / "drawable"
dr.mkdir(parents=True, exist_ok=True)
(dr / "ic_tracking.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#FFFFFFFF"
        android:pathData="M12,2C8.13,2 5,5.13 5,9c0,5.25 7,13 7,13s7,-7.75 7,-13c0,-3.87 -3.13,-7 -7,-7zM12,11.5c-1.38,0 -2.5,-1.12 -2.5,-2.5s1.12,-2.5 2.5,-2.5 2.5,1.12 2.5,2.5 -1.12,2.5 -2.5,2.5z"/>
</vector>
""", encoding="utf-8")

st = RES / "values" / "strings.xml"
x = st.read_text(encoding="utf-8")
extra = """    <string name="capacitor_background_geolocation_notification_channel_name">Gravação de viagem</string>
    <string name="capacitor_background_geolocation_notification_icon">drawable/ic_tracking</string>
    <string name="capacitor_background_geolocation_notification_color">#0E5C46</string>
"""
x = x.replace("</resources>", extra + "</resources>")
st.write_text(x, encoding="utf-8")

print(f"Android ajustado: versão 1.{run} (código {run})")
