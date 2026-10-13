# Fase 7 — Unidade de combustível

## Como o jogo trata `localUnits` (0.39.4)

| Onde | O que faz |
|---|---|
| `levels/west_coast_usa/info.json` | `"localUnits": {"gasoline": "gallonUS", "diesel": "gallonUS"}`. **Nenhum outro nível do jogo declara `localUnits`** |
| `lua/ge/extensions/freeroam/facilities/fuelPrice.lua` | O preço interno é **por litro** (`getFuelPrice`: "always metric unit"). Só nos painéis de preço dos postos: `if levelUnit[fuelType] == "gallonUS" then price = price * 3.78541` |
| `lua/ge/extensions/career/modules/fuel.lua` | Envia `localUnits` à interface; a energia já vem em L (`readableUnit`) |
| `ui/…/refuel/refuelStore.js` | `unitToLabel = {"gallonUS": "gal"}`, `factorSIToLocalUnit = {"gallonUS": 0.26417}`. **Qualquer outro valor cai em "L", fator 1** |

O único valor reconhecido é `gallonUS`. Não existe string de litro: o litro é o **padrão**, ou seja, a ausência da entrada. Para não inventar string, a entrada foi **removida** (override de `info.json` no mod; `working/functional/fuel_units.json`). Todo o resto do arquivo é idêntico, o que é conferido com um leitor de JSON tolerante, porque o arquivo do jogo tem vírgulas finais.

## Preço

- Não há conversão cambial (a regra do projeto é R$ sem câmbio). O número continua o mesmo do jogo.
- O preço-base é por litro (ex.: gasolina 1,37 na trilobite_garage).
  - Com `gallonUS`, o painel mostrava o preço por galão: 1,37 × 3,785 = 5,186, ou "518 9/10" (o 4º dígito é fixado em 9 nos postos americanos).
  - Agora mostra o mesmo preço por litro: "136 9/10" para 1,366 (painel lido no jogo, posto trilobite_city).
- O valor cobrado no abastecimento não muda: litros × preço por litro. A interface de abastecimento exibe L e preço por L.
- **Solução mínima coerente:** só a unidade exibida muda, e a economia do jogo fica igual.

Captura: `tests/screenshots/phase7/adas/fuel_board_trilobite_city_*.jpg`.

**Achado fora do escopo (Fase 8):** o painel `s_fuel_sign_trilobite.dae` tem textos em inglês ("SELF SERVE GASOLINE", "Regular/Mid-Grade/Premium Unleaded", "Diesel", "FOOD MART") que não estão na matriz. É trabalho visual, que esta fase não faz. Fica registrado para a Fase 8.

Mod desligado: `localUnits` volta a `gallonUS` (`tests/reports/phase7/mod_off_qa.md`).
