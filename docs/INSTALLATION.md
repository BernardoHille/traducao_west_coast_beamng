# Instalação — West Coast USA, Localização PT-BR

Para instalar, você precisa só do BeamNG.drive e do arquivo ZIP do mod. Não é preciso Git, Python nem nenhuma outra ferramenta, e nenhum arquivo do jogo é editado.

## Requisitos

- **BeamNG.drive 0.39.4.0.** É a versão em que o mod foi feito e validado; outras versões não foram testadas (ver [`release/KNOWN_ISSUES.md`](release/KNOWN_ISSUES.md)).
- O arquivo `traducao_ptbr_wcusa_v1.0.0.zip`, da página de [Releases](https://github.com/BernardoHille/traducao_west_coast_beamng/releases) do projeto. Baixe o **ZIP anexado à release**, não o "Source code (zip)", que é o código do repositório e não funciona como mod.

## 1. Conferir o arquivo (opcional)

A release traz o arquivo `traducao_ptbr_wcusa_v1.0.0.sha256` com o código SHA-256 do ZIP. No Windows, abra o PowerShell na pasta do download e rode:

```
Get-FileHash .\traducao_ptbr_wcusa_v1.0.0.zip -Algorithm SHA256
```

O valor mostrado deve ser igual ao do arquivo `.sha256` e ao das notas da release. Se for diferente, baixe de novo.

## 2. Copiar para a pasta de mods

O BeamNG lê os mods da pasta `mods` dentro da **pasta de usuário** do jogo. Não use a pasta de instalação do Steam: o próprio jogo avisa ali "DO NOT INSTALL MODS HERE".

No Windows, a pasta de usuário padrão é:

```
%LOCALAPPDATA%\BeamNG\BeamNG.drive\current\
└── mods\
    └── traducao_ptbr_wcusa_v1.0.0.zip   ← coloque o ZIP aqui
```

Para chegar lá, cole `%LOCALAPPDATA%\BeamNG\BeamNG.drive\current\mods` na barra de endereço do Explorador de Arquivos. Se você mudou a pasta de usuário do BeamNG, use a pasta `mods` dela.

**Não descompacte o ZIP.** O BeamNG carrega o mod direto do arquivo.

## 3. Ativar e usar

1. Abra o BeamNG.drive. Um mod novo na pasta `mods` aparece ativo no gerenciador de mods (**Mods** no menu principal). Ele aparece com o nome do arquivo, `traducao_ptbr_wcusa_v1.0.0`.
2. Carregue o mapa **West Coast USA**.

Para conferir: as placas de parada mostram **PARE**, e as placas de velocidade mostram km/h.

## Atualizar para uma versão nova

Apague o ZIP da versão anterior da pasta `mods` antes de colocar o novo. Como o nome do arquivo inclui a versão, duas versões na pasta seriam carregadas como dois mods.

## Desinstalar

1. Desative o mod no gerenciador de mods do jogo, ou apague `traducao_ptbr_wcusa_v1.0.0.zip` da pasta `mods`.
2. Carregue o mapa de novo. Se o West Coast já estava aberto, abra outro mapa e depois volte, ou reinicie o jogo.

O jogo volta ao original: placas STOP, limites em mph, combustível em galão. Não é preciso limpar o cache, porque o mod traz as malhas já compiladas e não deixa arquivos na pasta temporária do jogo.

## Problemas comuns

| Sintoma | O que fazer |
|---|---|
| Nada aparece traduzido | Confira se o ZIP está em `...\current\mods\` (e não numa subpasta ou descompactado) e se o mod está ativo em **Mods**. |
| Parte traduzida, parte não, depois de ativar ou desativar com o mapa aberto | Abra outro mapa e volte ao West Coast, ou reinicie o jogo. O jogo guarda o mapa carregado na sessão. |
| Placas misturadas ou valores estranhos | Outro mod pode estar substituindo os mesmos arquivos (placas, marcações, dados do West Coast). Desative os outros mods de West Coast para testar. |
| Versão do jogo diferente de 0.39.4.0 | Não suportado oficialmente. Veja as limitações de compatibilidade em `docs/release/KNOWN_ISSUES.md`. |
