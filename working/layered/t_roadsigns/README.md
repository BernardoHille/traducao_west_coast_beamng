# Master reproduzível — `t_roadsigns` (Fase 5)

Não há PNG achatado editado à mão. O atlas PT-BR é **gerado** a partir dos originais do jogo:

| Arquivo | Papel |
|---|---|
| `layout.json` | "Overlays" em dados: para cada elemento, a caixa editada, o que apagar (`erase`, `fill_boxes`), o texto, a fonte (Bahnschrift, peso/largura) e a caixa da altura de maiúscula. É o arquivo que se edita para mudar um texto |
| `build_t_roadsigns.py` | Composição determinística: `regions` (evidência de UV → `regions.json` + `allowed_regions.json`), `build` (PNG), `preview` (antes/depois) |
| `regions.json` | Gerado: meshes instanciados do West Coast que amostram cada caixa (cobertura UV) |
| `mesh_usage.json` | Gerado por `tools/production/scan_level_usage.py`: instâncias de cada mesh no nível |

```bash
python working/layered/t_roadsigns/build_t_roadsigns.py regions   # precisa de source/originals/meshes (extraídos do jogo, só leitura)
python working/layered/t_roadsigns/build_t_roadsigns.py build     # -> working/png/t_roadsigns_b.color.png + t_roadsigns_o.data.png
python working/layered/t_roadsigns/build_t_roadsigns.py preview   # -> working/temporary/t_roadsigns_preview/ (fora do Git)
python tools/validation/validate.py texture working/png/t_roadsigns_b.color.png
python tools/validation/validate.py texture working/png/t_roadsigns_o.data.png
tools/conversion/bin/texconv.exe -nologo -f BC7_UNORM_SRGB -srgb -m 0 -dx10 -y -o export/dds/t_roadsigns working/png/t_roadsigns_b.color.png
tools/conversion/bin/texconv.exe -nologo -f BC7_UNORM      -m 0 -dx10 -y -o export/dds/t_roadsigns working/png/t_roadsigns_o.data.png
```

O script se recusa a rodar se o SHA-256 dos originais não bater com o manifesto. A saída é determinística: RNG com semente fixa e fonte do sistema. Plano, inventário e tipografia estão em [`docs/production/t_roadsigns_plan.md`](../../../docs/production/t_roadsigns_plan.md).
