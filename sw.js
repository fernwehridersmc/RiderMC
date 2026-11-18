// Diário de Estrada — service worker: deixa o app abrir sem internet
// e guarda os pedaços de mapa já vistos para quando faltar sinal na estrada.
const VERSAO = "v1";
const APP = "app-" + VERSAO;
const TILES = "tiles-v1";
const FONTES = "fontes-v1";
const MAX_TILES = 3000;
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./assets/logo-160.webp", "./assets/icon-192.png", "./assets/icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(APP).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k.startsWith("app-") && k !== APP).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

async function limitar(nome, max) {
  const c = await caches.open(nome);
  const ks = await c.keys();
  for (let i = 0; i < ks.length - max; i++) await c.delete(ks[i]);
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  // Mapa: usa o que já tem guardado, senão busca e guarda
  if (url.hostname.endsWith("tile.openstreetmap.org")) {
    e.respondWith(caches.open(TILES).then(async c => {
      const hit = await c.match(req);
      if (hit) return hit;
      try {
        const r = await fetch(req);
        if (r.ok) { c.put(req, r.clone()); limitar(TILES, MAX_TILES); }
        return r;
      } catch (err) {
        return new Response("", { status: 504 });
      }
    }));
    return;
  }

  // Fontes do Google: guarda depois da primeira vez
  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {
    e.respondWith(caches.open(FONTES).then(async c => {
      const hit = await c.match(req);
      const net = fetch(req).then(r => { if (r.ok || r.type === "opaque") c.put(req, r.clone()); return r; }).catch(() => hit);
      return hit || net;
    }));
    return;
  }

  // O próprio app: tenta a versão nova, cai para a guardada se estiver sem internet
  if (url.origin === self.location.origin) {
    e.respondWith(
      fetch(req).then(r => {
        if (r.ok) caches.open(APP).then(c => c.put(req, r.clone()));
        return r;
      }).catch(() => caches.match(req).then(h => h || caches.match("./index.html")))
    );
  }
});
