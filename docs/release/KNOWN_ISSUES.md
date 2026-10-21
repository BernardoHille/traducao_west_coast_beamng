# Problemas e limitações conhecidas — 1.0.0

**Nenhum problema bloqueador conhecido na versão 1.0.0.**

O que segue são limitações de escopo e comportamentos conhecidos, registrados durante o desenvolvimento e o QA. Nenhum deles impede o uso do mod.

## Compatibilidade

- **Feito e validado só no BeamNG.drive 0.39.4.0.** Os dados de nível do mod (limites de via, radares, zonas, `slotTraffic.json`, frases do pavimento, `info.json` do mapa) são cópias completas dos arquivos do jogo com alguns valores trocados. Se uma atualização do BeamNG mudar esses arquivos, o mod continuaria carregando as cópias da 0.39.4 e esconderia as mudanças oficiais do mapa. Depois de uma atualização do jogo, use uma versão do mod feita para ela.
- **Outros mods que substituem os mesmos arquivos** (texturas de placas e marcações, dados de nível do West Coast) entram em conflito: só um deles vale. Mods que criam mapas separados, como os que ficam em outra pasta `levels/`, não interferem.

## Texturas compartilhadas com outros mapas

Algumas texturas ficam em pastas globais do jogo e aparecem traduzidas em qualquer mapa que as use:
- atlas `t_roadsigns`: fora do West Coast, só os cavaletes de obra `construction_sign_big_a/b/c` usam esse atlas;
- marcações no pavimento (`t_decal_roadmarkings`);
- outdoors, placas de posto, indústria, estúdio, mapa de ônibus e `clutter_commercial`;
- `ind_industrial_signs_d` no caminho de Jungle Rock Island.

Os limites em km/h, os radares e as placas R-19 valem só no West Coast. Não houve QA documentado em East Coast, Utah ou outros mapas.

## Fora do escopo

- **Interface do jogo** (menus, HUD, missões em texto): é tradução do próprio BeamNG, não deste mod.
- **Painel de preço do posto** (`s_fuel_sign_trilobite`: SELF SERVE GASOLINE, Regular/Mid-Grade/Premium Unleaded, Diesel, FOOD MART): continua em inglês.
- **Placar da arrancada:** a velocidade de saída aparece em mph, por código global do jogo que vale para todos os mapas. A ficha impressa (timeslip) já mostra km/h.
- **Preservados de propósito:** marcas e nomes próprios, por exemplo SPEARLEAF, TURBO BURGER e TORRES TIRES; termos usados no Brasil, como DRIFT, DIESEL e "% OFF"; o chinês de Chinatown; letras miúdas ilegíveis.
- **Moeda:** os preços desenhados passam a R$ sem conversão de câmbio, mantendo o número da arte. O dinheiro do jogo não muda.

## Camada funcional (km/h)

- **Combustível em litro:** os painéis dos postos mostram o preço por litro. O valor cobrado no abastecimento é o mesmo do jogo.
- **Duas placas urbanas mostram 100 km/h** (Chinatown e o trevo junction1): é o limite que o motor do jogo aplica nessas vias, e a placa mostra o que a IA faz de fato.
- **O limite vale por objeto de via (DecalRoad)**, não por trecho. Nas cabines das docas, os cerca de 13 m depois das placas ficam a 10 km/h até a via seguinte. Quatro placas nas transições das docas regulam a via seguinte: o validador registra isso como aviso informativo.
- **Missões `arrive`:** têm campo de limite, mas o jogo não o usa (`maxSpeedActive = false`). Ficaram sem alteração.
- **Zonas de velocidade** (`city.sites` e garageToGarage): foram convertidas para km/h, mas nenhum código do jogo 0.39.4 lê esse valor.

## Trechos feitos para cenários de pesquisa

O pacote inclui dois trechos regulamentados criados para cenários acadêmicos de ADAS. Eles são distribuídos porque fazem parte da versão aprovada na Fase 8. São coerentes por si (placa, via e radar) e **não exigem** nenhum outro mod:
- **zona de 50 km/h** em 1,27 km da via expressa onde começam os cenários ADAS Speed Alert, com R-19 50 na entrada e R-19 120 na saída. Fora desses cenários, quem dirige ali encontra uma redução sinalizada para 50 numa via de 120;
- **corredor de 70 km/h** em 216 m da avenida do Event 01, com R-19 70 e o radar 2 a 70. Sem esse corredor, a avenida estaria a 60, como as outras vias que eram 35 mph.

Os mods de pesquisa (ADAS Speed Alert, Event 01, Reaction Test) **não fazem parte** deste pacote. No Reaction Test, o tráfego ambiente roda a 50 nessa zona e o participante vê a placa R-19 50, enquanto a instrução do cenário fala em 40–70.

## Gerenciador de mods

O jogo só lê o arquivo `mod_info/.../info.json` de mods baixados do repositório oficial. Por isso, o gerenciador de mods mostra este mod pelo nome do arquivo (`traducao_ptbr_wcusa_v1.0.0`), sem descrição. O nome com a versão também faz uma versão nova aparecer como outro mod: remova a anterior antes de instalar a nova (ver `docs/INSTALLATION.md`).
