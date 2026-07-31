# RideRadar — Queue Data Collector

Coleta automática de tempo de fila (dado público, gratuito) dos parques que o
grupo vai visitar, para servir de base histórica própria de previsão no
[RideRadar](../rideradar-app) — o bot de copiloto de parques.

Roda via GitHub Actions (`workflow_dispatch` + cron a cada 5 minutos), sem
precisar de nenhum servidor. Cada execução consulta a
[API pública do queue-times.com](https://queue-times.com/en-US/pages/api)
para cada parque listado em `collector/parks.json` e adiciona uma linha por
atração em `data/{park_id}.csv`. Se houver mudança, o próprio workflow
commita e dá push no repositório.

## Estrutura

```
collector/
  collect.py     -- script de coleta (só usa a stdlib do Python)
  parks.json      -- lista de parques monitorados (id do queue-times.com)
data/
  {park_id}.csv   -- uma linha por atração por coleta: timestamp_utc,land,ride_id,ride_name,is_open,wait_time
```

## Adicionar/remover parque

Edite `collector/parks.json` com o `id` do parque em
[queue-times.com/parks.json](https://queue-times.com/parks.json).

## Rodar localmente

```
python3 collector/collect.py
```

## Atribuição

Dado fornecido por [Queue-Times.com](https://queue-times.com/en-US), conforme
exigido pelos termos de uso da API pública deles.
