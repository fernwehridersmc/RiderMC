#!/usr/bin/env python3
"""Monta o index.html final: pega src/app.html e embute o Leaflet,
para o app abrir sem internet (só o mapa de fundo precisa de rede).

Uso:  python3 tools/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "src" / "app.html").read_text(encoding="utf-8")
css = (ROOT / "tools" / "vendor" / "leaflet.css").read_text(encoding="utf-8")
js = (ROOT / "tools" / "vendor" / "leaflet.js").read_text(encoding="utf-8")

# Os ícones de marcador padrão do Leaflet não são usados (o app desenha os próprios).
out = src.replace("/*@LEAFLET_CSS@*/", css).replace("/*@LEAFLET_JS@*/", js.replace("</script", "<\\/script"))
assert "@LEAFLET" not in out, "placeholder não substituído"
(ROOT / "index.html").write_text(out, encoding="utf-8")
print(f"index.html gerado ({len(out.encode()) // 1024} KB)")
