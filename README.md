# Diário de Estrada · Fernweh Riders

Diário de viagens de moto do casal **Fernweh Riders (P&D)** — Paola e Deverson, base em Pato Branco–PR.
Projeto pessoal, feito por hobby.

**App:** https://fernwehridersmc.github.io/RiderMC/

## O que faz (versão 2)
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
- Backup: exporta e importa um arquivo `.json` com tudo, fotos incluídas (lê também backups da versão 1)

## Onde ficam os dados
Só no celular: viagens no `localStorage`, fotos no `IndexedDB`. Nada vai para servidor, nenhuma chave de API.
Exporte o backup depois de cada viagem e guarde no Drive.

## Offline
O `sw.js` guarda o app e os pedaços de mapa já vistos. Sem sinal, o app abre normal; só áreas do mapa nunca vistas ficam em branco.

## Como editar
- O código fica em `src/app.html`.
- Rode `python3 tools/build.py` para gerar o `index.html` (ele embute o Leaflet 1.9.4 de `tools/vendor/`).
