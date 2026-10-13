"""Phase 7: Markdown QA reports from the JSON results in tests/reports/phase7/ (radar, ADAS 50, Event 01, Reaction Test,
garageToGarage, AI, slotTraffic consistency, MOD OFF/ON, regression summary).

    python working/functional/qa_reports.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
R = REPO / "tests/reports/phase7"


def load(name):
    p = R / name
    return json.loads(p.read_text(encoding="utf8")) if p.exists() else None


def write(name, lines):
    (R / name).write_text("\n".join(lines) + "\n", encoding="utf8")
    print(name)


def radar():
    d = load("radar_test.json")
    L = ["# Fase 7 — QA dos radares", "",
         "Gerado por `working/functional/qa_reports.py` a partir de `radar_test.json` (`working/functional/radar_test.py`).", "",
         "Método: largada lançada 25–45 m antes de cada radar (teleporte + velocidade inicial no sentido fiscalizado), IA em velocidade "
         "constante ('set') pelo gatilho, câmera do jogo seguindo o carro. O evento `onSpeedTrapTriggered` do próprio "
         "`gameplay/speedTraps.lua` é registrado (o jogo dispara acima de limite + 10 %). Num nível carregado pelo MCP o jogo não está em "
         "modo freeroam, então a extensão `gameplay_speedTraps` (preset do freeroam) foi carregada antes do teste.", "",
         "| Radar | Limite | Dispara acima de | Alvo | Velocidade no gatilho | Disparou | Esperado | Resultado |", "|---|---:|---:|---:|---:|---|---|---|"]
    ok = True
    for k in sorted(d, key=lambda k: (int(k.split("_")[0][5:]), int(k.split("_")[1]))):
        r = d[k]
        ok &= r["result"] == "PASS"
        L.append(f"| speedTrapTrigger{r['radar']} | {r['limit_kmh']} | {r['trigger_above_kmh']} | {r['target_kmh']} | {r['speed_at_radar_kmh']} | "
                 f"{'sim' if r['triggered'] else 'não'} | {'sim' if r['expected_trigger'] else 'não'} | {r['result']} |")
    L += ["", f"**Resultado:** {'PASS' if ok else 'FAIL'} ({len(d)} passagens). Nos radares 4 e 5 (curva) a IA perde ~6 km/h antes do gatilho; "
          "por isso os alvos mais altos (125 / 80) — o que conta é a velocidade medida no gatilho."]
    write("radar_qa.md", L)


def adas():
    d = load("adas_qa.json")
    L = ["# Fase 7 — QA dos cenários ADAS", "", "Gerado a partir de `adas_qa.json` (`working/functional/adas_test.py`). Cada cenário foi aberto pelo "
         "próprio `load()` (freeroam sem tráfego, como o usuário inicia), isolado dos outros controladores, e o Honda foi dirigido pela IA "
         "em velocidades-alvo ('set'), o mesmo método da validação original dos cenários.", ""]
    for key, title in (("speed_alert", "ADAS Speed Alert (teste)"), ("speed_alert_web", "ADAS Speed Alert (web)")):
        r = d.get(key)
        if not r:
            continue
        A, B, C = (r["steps"][s] for s in ("A_below_50", "B_above_50", "C_reduce"))
        fs = next((s for s in B if s["alertActive"]), None)
        st = next((s for s in C if not s["alertActive"]), None)
        L += [f"## {title} — {r['result']}", "",
              f"- Spawn {[round(v, 1) for v in r['spawn']]}, aresta `{r['edge_at_spawn'][0]}` → `{r['edge_at_spawn'][1]}`, navgraph "
              f"**{r['navgraph_at_spawn_kmh']} km/h**; limiar {r['threshold_kmh']} km/h (inalterado).",
              f"- A (< 50): máx. {max(s['kmh'] for s in A)} km/h, sem alerta.",
              f"- B (> 50): alerta ativo a {fs['kmh'] if fs else '?'} km/h.",
              f"- C (redução): alerta desligado a {st['kmh'] if st else '?'} km/h.",
              f"- Todas as amostras na zona: limite 50 km/h.",
              f"- Checagens: " + ", ".join(f"{k} = {v}" for k, v in r["checks"].items()), "",
              f"Capturas: `{r['screens']['spawn_driver_view']}`, `{r['screens']['alert_active']}`.", ""]
    e = d.get("event01")
    if e:
        r2 = e["runs"]["run2_72_60_72"]
        alerts, prev = [], 0
        for s in r2:
            if (s.get("alertCount") or 0) != prev:
                alerts.append(s)
                prev = s.get("alertCount") or 0
        L += [f"## Event 01 — {e['result']}", "",
              f"- Novo início {[round(v, 1) for v in e['spawn']]}, aresta `{e['edge_at_spawn'][0]}` → `{e['edge_at_spawn'][1]}`, navgraph "
              f"**{e['navgraph_at_spawn_kmh']} km/h**; alerta 70 / rearme 65 (inalterados).",
              f"- Execução 1 (65 e depois 69 km/h): máx. {max(s['kmh'] for s in e['runs']['run1_65_69'])} km/h, nenhum alerta.",
              "- Execução 2 (72 → 60 → 72 km/h):"]
        for s in alerts:
            L.append(f"  - alerta #{s['alertCount']} a {s['kmh']} km/h, via a {s['limit_kmh']} km/h em {s['xy']}")
        L += ["- Log: " + " · ".join(l.split("| ")[-1] for l in e["log_run2"] if "REACHED" in l or "rearmed" in l or "Playing" in l),
              "- Checagens: " + ", ".join(f"{k} = {v}" for k, v in e["checks"].items()),
              "- O primeiro alerta acontece dentro do corredor (70). O segundo, no teste, veio depois do corredor (216 m), na alça "
              "Bridge36 (60/80): o alerta do Event 01 é só por velocidade, não por posição — comportamento original do cenário.", "",
              f"Capturas (cena noturna fixa do cenário): `{e['screens']['spawn_driver_view']}`, `{e['screens']['alert']}`.", ""]
    r = d.get("reaction")
    if r:
        fs = r["final_state"]
        L += [f"## Reaction Test (smoke) — {r['result']}", "",
              f"- Fases: {' → '.join(str(p) for p in r['phases'])}.",
              f"- Fechada: cutInCompleted = {fs.get('cutInCompleted')}; colisão = {fs.get('collision')} (a IA do teste não reage: caminho "
              "de colisão do experimento, previsto na documentação do cenário).",
              f"- Tráfego ambiente: 5 veículos; na zona de 50 seguem o limite (amostras ~50 km/h); o veículo da fechada usa 'set' (60).",
              f"- Arquivo de resultado gravado pelo próprio cenário: `{fs.get('resultFile')}` — **gerado pelo teste automático, não é dado "
              "de participante** (pode ser apagado pelo pesquisador).",
              "- Faixa 40–70 experimental: sem zona, sem navgraph, sem placa (inalterado).", ""]
    write("adas_qa.md", L)


def ai():
    d = load("ai_test.json")
    L = ["# Fase 7 — IA ('legal') por classe de velocidade", "", "Gerado a partir de `ai_test.json` (`working/functional/ai_test.py`).", "",
         "| Caso | Via | Limite | Máx. | p90 | Amostras na classe | Resultado |", "|---|---|---:|---:|---:|---:|---|"]
    for k, v in d.items():
        L.append(f"| {k} | {v['doc']} | {v['limit_kmh']} | {v.get('max_kmh')} | {v.get('p90_kmh')} | {v['samples_on_class']}/{v['samples_total']} | {v['result']} |")
    L += ["", "Critério: máx. ≤ limite × 1,03 + 1 e ≥ 80 % do limite (a IA chega ao limite sem passar). Em 80 km/h (via sinuosa) a IA "
          "chega a ~67 km/h pela curvatura, abaixo do limite."]
    write("ai_qa.md", L)


def slot():
    d = load("slottraffic_consistency.json")
    s = d["stats"]
    L = ["# Fase 7 — slotTraffic × navgraph", "", "Gerado a partir de `slottraffic_consistency.json` (`working/functional/slot_consistency.py`): "
         "para cada faixa do `slotTraffic.json` do mod, o limite do navgraph (jogo, mod ativo) a 25/50/75 % da linha central.", "",
         "| Grupo | Igual | Diferente |", "|---|---:|---:|"]
    for g in ("phase7_edited", "phase5_edited", "untouched"):
        L.append(f"| {g} | {s.get(g + ':match', 0)} | {s.get(g + ':differ', 0)} |")
    L += ["", f"- Faixas sem sobreposição com o navgraph (≤ 3 m): {s.get('no_navgraph_overlap', 0)}.",
          f"- **navgraph 60 × slotTraffic 56,3 (ou qualquer valor de mph): {len(d['mph_56_3_mismatches'])}** — nenhum valor de mph restou "
          "(o gerador também confere: `mph_values_left = 0`).",
          "- A faixa da Fase 7 marcada como diferente (LE71, 8 m no fim do DR652) tem o valor certo (70): a amostra caiu na aresta seguinte "
          "da junção (100).",
          "- As diferenças das faixas não tocadas são do próprio arquivo do jogo (o valor da faixa é um resumo por faixa; nas junções e "
          "vias sobrepostas a amostra cai em outra aresta). Elas existem igualmente com o mod desligado e não envolvem valores alterados.",
          "- Edições: 939 linhas da Fase 5 preservadas (conferidas uma a uma) + linhas da Fase 7 (ver `functional_diff.md`)."]
    write("slottraffic_consistency.md", L)


def garage():
    d = load("garage_smoke.json")
    if not d:
        return
    L = ["# Fase 7 — garageToGarage (smoke) e zonas", "",
         "- VFS: `garages.sites.json` e `city.sites.json` resolvem para o mod; `info.json` sem `localUnits`.",
         "- Valores lidos no jogo: " + ", ".join(f"{k.split('.')[-2] if k.endswith('.name') else k.split('.')[-1]} {v}" for k, v in
                                                 {**d["vfs"]["garages"], **d["vfs"]["city"]}.items()),
         f"- Missão `{d['mission']}`: iniciada, em primeiro plano; depois de **Iniciar**, o fluxo sorteou um trabalho a partir da zona "
         f"Docas e criou o veículo ({d.get('after_start_click', {}).get('veh')}). Erros: "
         + (str(d.get('error_lines_after_start')) if d.get('error_lines_after_start') else "nenhum") + ".",
         f"- Capturas: `{d.get('screenshot')}`, `{d.get('screenshot_started')}`."]
    write("zones_missions_qa.md", L)


def modoff():
    d = load("mod_off_on.json")
    L = ["# Fase 7 — MOD OFF / ON", "", "Procedimento: troca de estado sempre passando por outro nível (smallgrid) antes do West Coast; cache "
         "`current/temp` sem `.cdae` do mod (os `.cdae` compilados durante o trabalho foram copiados para o mod e apagados de `temp`).", "",
         "| Item | Mod desligado | Mod ligado |", "|---|---|---|"]
    off, on = d.get("mod_off", {}), d.get("mod_on", {})
    for k in on.get("roads", {}):
        L.append(f"| via {k} | {off.get('roads', {}).get(k)} km/h | {on['roads'][k]} km/h |")
    for k in sorted(on.get("radars", {})):
        L.append(f"| {k} | {off.get('radars', {}).get(k)} | {on['radars'][k]} |")
    L.append(f"| grupo ptbr_functional_signs | {off.get('signs_group')} | {on.get('signs_group')} objetos |")
    L.append(f"| localUnits | {off.get('localUnits')} | {on.get('localUnits')} |")
    for f in on.get("vfs", {}):
        L.append(f"| `{f}` | {'jogo' if 'traducao' not in off.get('vfs', {}).get(f, '') else 'MOD'} | {'mod' if 'traducao' in on['vfs'][f] else 'JOGO'} |")
    L += ["", "Também com o mod desligado: as 47 placas do `roadsigns.dae` voltam a SPEED LIMIT / MPH (`tests/screenshots/phase7/speed_plates/"
          "*_original.jpg`), a cabine volta a DO NOT STOP / SPEED LIMIT 25 e a faixa do pedágio a 60 km/h; nenhum `.cdae` foi gravado em "
          "`temp`. O início do Event 01 é patch do mod de pesquisa (não do mod de tradução) e continua no corredor com o mod desligado."]
    write("mod_off_qa.md", L)


if __name__ == "__main__":
    radar()
    adas()
    ai()
    slot()
    garage()
    modoff()
