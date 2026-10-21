# Créditos e direitos

## Autor

- **Bernardo Hille**: concepção, localização, produção, ferramentas, QA e documentação.

## Testes

- **Testadores voluntários da fase de QA** (Fase 8), que participaram de forma anônima.

## Jogo-base

- **BeamNG.drive**, da **BeamNG GmbH**. O mapa West Coast USA, as texturas, as malhas e os dados de nível originais pertencem à BeamNG GmbH.
- Este mod contém **versões modificadas** de assets do jogo (texturas, malhas e arquivos de dados do nível) e alguns assets novos. Ele só funciona com uma cópia legítima do BeamNG.drive, e o pacote não traz nenhum arquivo do jogo sem modificação.

## Referências normativas

- **Manual Brasileiro de Sinalização de Trânsito** (Vol. I — Sinalização Vertical de Regulamentação; Vol. IV — Sinalização Horizontal), publicado pela **SENATRAN**, e as resoluções do **CONTRAN** que o aprovam. Lista completa em [`docs/LOCALIZATION_RULES.md`](LOCALIZATION_RULES.md).
- Esses documentos foram usados **só como referência** para formas, cores, textos e convenções. SENATRAN e CONTRAN não participaram deste projeto e não o endossam.

## Ferramentas e bibliotecas

- **Python** com **Pillow** e **NumPy**: composição das texturas, validadores e ferramentas de produção.
- **texconv** (Microsoft **DirectXTex**): conversão para DDS no formato do jogo. Não é distribuído no repositório nem no pacote.
- **BeamNG MCP** (interface de automação do jogo): QA automatizado no próprio BeamNG.drive.
- **Claude Code** (Anthropic): assistência no desenvolvimento das ferramentas, no QA e na documentação.
- **Fontes tipográficas** instaladas no sistema do autor (Windows e Microsoft Office: Bahnschrift, Arial, Arial Narrow, Franklin Gothic, Gill Sans, Agency FB, Rockwell, Tw Cen MT, Segoe UI, entre outras). Foram usadas para desenhar texto dentro das texturas. **Nenhum arquivo de fonte é distribuído.**

## Endosso

Este é um projeto independente. **Nem a BeamNG GmbH, nem a SENATRAN, nem o CONTRAN endossam, patrocinam ou revisaram este mod.** Os nomes aparecem só para identificar o jogo-base e as referências usadas.

## Direitos e licença

O repositório **não tem um arquivo `LICENSE`**, e esta versão não escolhe uma licença. A situação de cada tipo de conteúdo:

| Conteúdo | Situação |
|---|---|
| Assets modificados do jogo (texturas, malhas, dados de nível no pacote) | derivados de assets da BeamNG GmbH; os direitos sobre o original continuam com ela. Este projeto não reivindica nem concede direitos sobre eles |
| Assets novos (placas R-19, faces das placas em km/h) | feitos pelo autor a partir de masters próprios e das referências normativas; são distribuídos junto com o mod |
| Código e scripts próprios (`tools/`, `working/**/*.py`) | autoria de Bernardo Hille; sem licença definida, todos os direitos reservados ao autor |
| Documentação e artigo (`docs/`) | autoria de Bernardo Hille; sem licença definida, todos os direitos reservados ao autor |

Para usar o código ou a documentação fora deste projeto, fale com o autor. Uma licença para o código próprio pode ser definida numa versão futura, mas ela não cobrirá os assets do jogo.
