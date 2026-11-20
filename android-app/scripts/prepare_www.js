// Monta a pasta www do app Android: copia o site e carrega o runtime do Capacitor
// (é ele que cria o Capacitor.registerPlugin usado pra falar com o GPS em segundo plano).
const fs = require("fs");
const path = require("path");
const app = path.resolve(__dirname, "..");
const root = path.resolve(app, "..");
const www = path.join(app, "www");
fs.rmSync(www, { recursive: true, force: true });
fs.mkdirSync(www, { recursive: true });
fs.cpSync(path.join(root, "assets"), path.join(www, "assets"), { recursive: true });
fs.copyFileSync(path.join(root, "manifest.webmanifest"), path.join(www, "manifest.webmanifest"));
fs.copyFileSync(path.join(app, "node_modules", "@capacitor", "core", "dist", "capacitor.js"), path.join(www, "capacitor.js"));
let html = fs.readFileSync(path.join(root, "index.html"), "utf8");
if (!html.includes("</head>")) throw new Error("index.html sem </head>");
html = html.replace("</head>", '<script src="capacitor.js"></script>\n</head>');
fs.writeFileSync(path.join(www, "index.html"), html);
console.log("www pronto com capacitor.js");
