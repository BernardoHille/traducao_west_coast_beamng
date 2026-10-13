# Fase 7 — MOD OFF / ON

Procedimento: troca de estado sempre passando por outro nível (smallgrid) antes do West Coast; cache `current/temp` sem `.cdae` do mod (os `.cdae` compilados durante o trabalho foram copiados para o mod e apagados de `temp`).

| Item | Mod desligado | Mod ligado |
|---|---|---|
| via DR989 | 56.3 km/h | 60 km/h |
| via junction1 | 100 km/h | 100 km/h |
| via DR272_phase5 | 40.2 km/h | 40 km/h |
| via DR652_event01 | 56.3 km/h | 70 km/h |
| via DR1009 | 56.3 km/h | 60 km/h |
| via DR666 | 56.3 km/h | 60 km/h |
| via DR571 | 56.3 km/h | 60 km/h |
| via DR312_adas | 120 km/h | 50 km/h |
| speedTrapTrigger2 | 15.6464 | 19.4444 |
| speedTrapTrigger3 | 15.6464 | 16.6667 |
| speedTrapTrigger4 | 15.6464 | 27.7778 |
| speedTrapTrigger5 | 15.6464 | 16.6667 |
| speedTrapTrigger6 | 15.6464 | 16.6667 |
| speedTrapTrigger7 | 15.6464 | 16.6667 |
| grupo ptbr_functional_signs | absent | 14 objetos |
| localUnits | {'diesel': 'gallonUS', 'gasoline': 'gallonUS'} | absent |
| `/levels/west_coast_usa/city.sites.json` | jogo | mod |
| `/gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json` | jogo | mod |
| `/levels/west_coast_usa/slotTraffic.json` | jogo | mod |
| `/levels/west_coast_usa/info.json` | jogo | mod |

Também com o mod desligado: as 47 placas do `roadsigns.dae` voltam a SPEED LIMIT / MPH (`tests/screenshots/phase7/speed_plates/*_original.jpg`), a cabine volta a DO NOT STOP / SPEED LIMIT 25 e a faixa do pedágio a 60 km/h; nenhum `.cdae` foi gravado em `temp`. O início do Event 01 é patch do mod de pesquisa (não do mod de tradução) e continua no corredor com o mod desligado.
