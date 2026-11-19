# Diário de Estrada · Fernweh Riders

Diário de viagens de moto do casal **Fernweh Riders (P&D)** — Paola e Deverson, base em Pato Branco–PR.
Projeto pessoal, feito por hobby.

**App:** https://fernwehridersmc.github.io/RiderMC/

## O que faz (versão 5)
- Importa um ou vários arquivos GPX (viagem de vários dias = vários GPX numa viagem só)
- Mostra a rota no mapa (OpenStreetMap) e calcula km e datas
- Paradas: toca no mapa (ou usa o GPS do celular), escolhe o tipo (posto, comida, ponto turístico, monumento, pernoite), escreve a observação, põe fotos e o link do vídeo
- Paradas aparecem como marcos de km na linha do tempo da viagem
- Início com o total do ano (km, viagens, dias, paradas) e todas as rotas no mesmo mapa
- 5 abas: Início, Viagens, Mapa, Moto e Mais
- Gastos por viagem (combustível, comida, hospedagem, pedágio, manutenção, outros) com custo por km
- Abastecimentos com litros e odômetro; km/l pelo método do tanque cheio
- Manutenção da moto com aviso por km e por meses (óleo, corrente, relação, freios, pneus, filtro, revisão)
- Resumo do ano: km por mês, gasto por categoria e recordes
- Mapa geral com filtro por ano e por tipo de parada; botão "Ir com Waze" em cada parada
- Recebe GPX pelo "Compartilhar" do Android (com o app instalado na tela inicial)
- Estatísticas do GPX: tempo rodando, tempo total, média, máxima, altitude, subida acumulada, km por dia e perfil de altitude
- Lugares favoritos ("vale voltar") com Waze
- Rota Biker: lista dos monumentos, visitados e faltando, ligação com a parada do tipo monumento, camada no mapa
- Planejar viagem: roteiro de destinos (abre no Google Maps), checklist de bagagem e "Começar viagem"
- Mídia em cada viagem: fotos, vídeos (360 ou normais, ligados a uma parada) e postagens
- Galeria com todas as fotos, filtro por viagem e tipo
- Postagens: Instagram, Estrada X ou outra; ideia/produzindo/postado; série, link e views; sugestões de favoritos e monumentos sem post
- Imagem pra postar (story 9:16 ou feed 4:5) com rota, números, logo e foto de fundo; compartilha direto pelo Android
- Backup: exporta e importa um arquivo `.json` com tudo, fotos incluídas (lê também backups da versão 1)

## Onde ficam os dados
Só no celular: viagens no `localStorage`, fotos no `IndexedDB`. Nada vai para servidor, nenhuma chave de API.
Exporte o backup depois de cada viagem e guarde no Drive.

## Offline
O `sw.js` guarda o app e os pedaços de mapa já vistos. Sem sinal, o app abre normal; só áreas do mapa nunca vistas ficam em branco.

## Como editar
- O código fica em `src/app.html`.
- Rode `python3 tools/build.py` para gerar o `index.html` (ele embute o Leaflet 1.9.4 de `tools/vendor/`).

## App Android (gravação do trajeto)
- Baixar: https://github.com/fernwehridersmc/RiderMC/releases/latest/download/diario-fernweh.apk
- É o mesmo `index.html` embrulhado com Capacitor 7 (pasta `android-app/`), mais o plugin
  `@capacitor-community/background-geolocation`, que grava com a tela apagada (notificação fixa "Gravando a viagem").
- Cada push no `index.html`, em `assets/` ou em `android-app/` dispara o GitHub Actions (`.github/workflows/android.yml`),
  que gera o APK e publica em Releases.
- O APK é assinado com `android-app/fernweh-app.keystore` (chave fixa, pra atualização instalar por cima).
  Projeto pessoal: a senha está no `scripts/patch_android.py`. Se um dia for pra Play Store, trocar por uma chave guardada em segredo.
- O app e o site guardam os dados separados: use Backup → Exportar num e Importar no outro.
