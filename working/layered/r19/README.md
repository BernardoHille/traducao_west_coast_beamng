# Masters R-19 (Fase 5)

`build_r19.py` tem **um** conjunto de parâmetros (diâmetro, orla, alturas, cores, fonte), que gera três saídas sempre coerentes:

- `r19_<valor>.svg`: master vetorial em metros, com viewBox = painel 0,7317 × 1,0 m do `sign_speed*.dae`. Editável em qualquer editor SVG;
- `working/png/r19/t_r19_<valor>_b.color.png`: cor 512×1024, cobre o painel inteiro; fora do disco fica a cor da orla, para não haver halo;
- `working/png/r19/t_r19_o.data.png`: máscara do disco, a mesma para todos os valores e também para o verso.

```bash
python working/layered/r19/build_r19.py            # 10 e 40
python working/layered/r19/build_r19.py 50 60 80   # expansão futura (só múltiplos de 10)
```

Especificação seguida (MBST Vol. I, R-19): placa circular, fundo branco, orla vermelha (aqui 10 % do diâmetro), algarismos pretos centralizados e "km/h" abaixo.
- Fonte: Bahnschrift, aproximação da Série D/E(M) → `human_typography_review_required`.
- O textura fina do branco vem do painel branco **original** do atlas (luminância de baixa frequência), para o disco não destoar das outras placas.
