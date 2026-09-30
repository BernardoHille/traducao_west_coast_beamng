# Relatório de conversão — PoC `t_roadsigns_b.color`

**Data:** 30/09/2026 · **Fase:** 1 (Proof of Concept do override)

> A textura do PoC é a referência PT-BR antiga, usada **só** para tornar o override visível. **Não** é uma tradução aprovada.

## Arquivos

| Papel | Caminho | SHA-256 |
|---|---|---|
| Original (imutável) | `source/originals/dds/t_roadsigns_b.color.dds` | `eba34c89118af2f421e5ac60100fc46e12352f630255c3c55d51bb922f22f51c` (confere com o manifesto ✔) |
| Fonte do PoC | `working/temporary/poc/t_roadsigns_b.color_poc.png`, cópia de `source/reference_ptbr/t_roadsigns_b.color_ptbr.png` | `d41ba2c0ec6e67917983a903a443c0f81f044c0d624dad0a3d615f77ee7a3938` (idêntico à referência ✔) |
| DDS do PoC | `export/dds/poc/t_roadsigns_b.color.dds` | `ab70d9eade62888cb561ae430178041c4bff6a051aa74b163e13e8d2e7fc2af4` |

## Comparação de cabeçalho (lida diretamente dos arquivos)

| Propriedade | Original | PoC | Resultado |
|---|---|---|---|
| Width | 2048 | 2048 | ✔ |
| Height | 1024 | 1024 | ✔ |
| FourCC | `DX10` | `DX10` | ✔ |
| Format (DXGI) | 99 = `BC7_UNORM_SRGB` | 99 = `BC7_UNORM_SRGB` | ✔ |
| Color space | sRGB | sRGB | ✔ |
| Mipmaps | 12 (cadeia completa até 1×1) | 12 | ✔ |
| Resource dimension | 3 (Texture2D) | 3 (Texture2D) | ✔ |
| Array size / miscFlag | 1 / 0 | 1 / 0 | ✔ |
| Header flags / caps | `0xA1007` / `0x401008` | `0xA1007` / `0x401008` | ✔ |
| Pitch / linear size | 2097152 | 2097152 | ✔ |
| Alpha mode (DX10 `miscFlags2`) | 0 = UNKNOWN | 1 = STRAIGHT | ⚠️ diferença só de metadado, gravado pelo texconv. Não mudou o resultado no jogo. |
| File size | 2.796.388 bytes | 2.796.388 bytes | ✔ (148 bytes de cabeçalho + 2.796.240 bytes de dados BC7, igual ao valor calculado para a cadeia de 12 níveis) |

## Verificação de pixels (decodificação com Pillow)

| Comparação | PSNR RGB | Interpretação |
|---|---|---|
| DDS PoC × PNG fonte do PoC | 46,2 dB (erro de alfa máx. 29) | Compressão BC7 fiel à fonte |
| DDS original × PNG original | exato (∞) | O PNG original é a decodificação exata do DDS |
| DDS PoC × DDS original | 18,4 dB | Visualmente diferente, como esperado para o PoC |

## Documentação × arquivo real

Nenhuma divergência. A auditoria e o manifesto dizem 2048×1024 BC7 sRGB, e o arquivo confirma: DXGI 99, 12 mipmaps.

## Conversão

- Ferramenta: **texconv** (Microsoft DirectXTex), release `may2026`, FileVersion `2026.5.8.1`
- Origem: `https://github.com/microsoft/DirectXTex/releases/download/may2026/texconv.exe`
  - SHA-256 `dcfdec10244e02cf5037fba089c55fb7e1326b1c8181742d77d15fa5cb5eef06`, igual ao digest publicado pelo GitHub
  - Assinatura Authenticode válida (Microsoft Corporation)
- Local: `tools/conversion/bin/texconv.exe` (fora do Git)
- Compressão feita na GPU (DirectCompute, NVIDIA GeForce RTX 4060)
- Comando:

```
texconv.exe -nologo -f BC7_UNORM_SRGB -srgb -m 0 -dx10 -y -o export/dds/poc working/temporary/poc/t_roadsigns_b.color_poc.png
```

- `-srgb`: entrada e saída em sRGB, sem conversão de gama.
- `-m 0`: gera a cadeia completa de mipmaps.
- A saída `t_roadsigns_b.color_poc.dds` foi renomeada para `t_roadsigns_b.color.dds`.
