# Controles de Interação

Interaja com a cena (`PrCG.py`) usando as teclas abaixo. Pressione as teclas na janela da aplicação.

## Controlos do Carro (Física Realista)

O carro agora funciona com **física de direção realista** (direção Ackermann):
- As **rodas dianteiras viram** conforme conduz.
- O **volante gira** automaticamente conforme a direção.
- A direção funciona de forma **diferente em marcha-atrás** (como num carro real).
- O carro faz **curvas suaves** baseadas na velocidade e ângulo de direção.

### Controlos de Movimento:
- `W` / `w`: **Manter pressionado** para acelerar para a frente.
- `S` / `s`: **Manter pressionado** para acelerar para trás (marcha-atrás) ou travar.
- `A` / `a`: **Manter pressionado** para virar as rodas para a **esquerda** (apenas quando em movimento).
- `D` / `d`: **Manter pressionado** para virar as rodas para a **direita** (apenas quando em movimento).
- `Espaço`: Parar o carro completamente e centralizar a direção.

**Dica:** Quanto mais rápido estiver, maior será o raio da curva. Em marcha-atrás, a direção inverte (tal como num carro real)!

## Controlos da Garagem e Portas:
- `G` / `g`: Abrir / fechar o portão da garagem (não fecha se o carro estiver no meio).
- `Q` / `q`: Abrir / fechar a porta **esquerda** do carro.
- `E` / `e`: Abrir / fechar a porta **direita** do carro.

## Outros Controlos:
- `C` / `c`: Alternar modo de câmara.
- `Esc`: Sair da aplicação.

### Teclas Especiais (Câmara Livre):
- `←` / `→` (setas esquerda/direita): Rodar a câmara horizontalmente.
- `↑` / `↓` (setas cima/baixo): Ajustar o ângulo vertical da câmara.
- `Page Up` / `Page Down`: Aproximar / afastar a câmara.

## Modos de Câmara

- **Tecla `C`**: alterna entre os modos de câmara disponíveis.
- **Modo 0 — Câmara Livre**: câmara orbital controlada pelo utilizador (setas e PageUp/PageDown). Não segue automaticamente o carro.
- **Modo 1 — 3ª Pessoa**: câmara posicionada atrás e acima do carro; segue automaticamente o carro e olha para o seu centro.
- **Modo 2 — 1ª Pessoa**: câmara colocada na posição do condutor (vista do volante); segue o carro e mostra a cena em primeira pessoa.

**Nota:** Nos modos 1 e 2 a câmara segue o carro automaticamente, portanto as teclas de setas alteram a vista apenas quando estiver no modo livre.