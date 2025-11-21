# Controles de Interação

Interaja com a cena (`PrCG.py`) usando as teclas abaixo. Pressione as teclas na janela da aplicação.

- `g` / `G`: Abrir / fechar o portão da garagem (não fecha se o carro estiver no meio).
- `e` / `E`: Abrir / fechar a porta esquerda.
- `d` / `D`: Abrir / fechar a porta direita.
- `s` / `S`: Mover o carro para +X (avançar).
- `w` / `W`: Mover o carro para -X (recuar).
- `Space`: Parar o carro.
- `Esc`: Sair da aplicação.

Teclas especiais:

- `←` / `→` (setas esquerda/direita): Rodar a câmara horizontalmente.
- `↑` / `↓` (setas cima/baixo): Ajustar o ângulo vertical da câmara.
- `Page Up` / `Page Down`: Aproximar / afastar a câmara.

Modos de câmara

## Modos de Câmara

- **Tecla `C`**: alterna entre os modos de câmara disponíveis.
- **Modo 0 — Câmara Livre**: câmara orbital controlada pelo utilizador (setas e PageUp/PageDown). Não segue automaticamente o carro.
- **Modo 1 — 3ª Pessoa**: câmara posicionada atrás e acima do carro; segue automaticamente o carro e olha para o seu centro
- **Modo 2 — 1ª Pessoa**: câmara colocada na posição do condutor (vista do volante); segue o carro e mostra a cena em primeira pessoa.

Nota: Nos modos 1 e 2 a câmara segue o carro automaticamente, portanto as teclas de setas alteram a vista apenas quando estiver no modo livre.
