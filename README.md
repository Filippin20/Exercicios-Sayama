# Exercícios Capítulo 4 – Sayama (Complex Systems)

Soluções dos exercícios 4.12, 4.13 e 4.15 do livro:
> *Introduction to the Modeling and Analysis of Complex Systems* – Hiroki Sayama

## Estrutura

```
cap4_sayama/
├── exercise_4_12.py   # Modelo linear x_t = a * x_{t-1}
├── exercise_4_13.py   # Modelo presa-predador + correção
├── exercise_4_15.py   # Dinâmica de opinião pública
├── figuras/           # Gráficos gerados automaticamente
└── README.md
```

## Descrição dos exercícios

### Exercício 4.12 — Modelo linear univariado

Implementação e exploração do modelo:

$$x_t = a \cdot x_{t-1}$$

**Comportamentos observados:**

| Valor de `a` | Comportamento |
|---|---|
| `a > 1` | Crescimento exponencial |
| `0 < a < 1` | Decaimento exponencial |
| `a = 1` | Estado estacionário |
| `a = 0` | Colapso imediato |
| `-1 < a < 0` | Oscilação amortecida |
| `a = -1` | Oscilação de período 2 |
| `a < -1` | Oscilação explosiva |

---

### Exercício 4.13 — Modelo presa-predador

Exploração do modelo Lotka-Volterra discreto (Eqs. 4.34–4.35):

$$x_t = x_{t-1} + r x_{t-1}\left(1 - \frac{x_{t-1}}{K}\right) - \frac{b\,y_{t-1}}{1+b\,y_{t-1}}\,x_{t-1}$$

$$y_t = y_{t-1} - d\,y_{t-1} + c\,x_{t-1}\,y_{t-1}$$

**Problema encontrado:** para valores altos de `c` e baixos de `d`, os predadores crescem indefinidamente (comportamento biologicamente inválido).

**Correção proposta:** adicionar um termo logístico nos predadores com capacidade de suporte $K_y$:

$$y_t = y_{t-1} + \left(-d\,y_{t-1} + c\,x_{t-1}\,y_{t-1}\right)\left(1 - \frac{y_{t-1}}{K_y}\right)$$

---

### Exercício 4.15 — Dinâmica de opinião pública

Modelo com três ideologias: conservador ($p_c$), liberal ($p_l$) e neutro ($p_n = 1 - p_c - p_l$).

**Regra de troca:** o fluxo de X para Y é proporcional a $\max(0,\,p_Y - p_X) \cdot p_X$.

**Seis fluxos** considerados: C→L, C→N, L→C, L→N, N→C, N→L.

**Resultado geral:** o sistema sempre converge para um dos seguintes estados finais:
- Dominância da posição mais popular inicialmente
- Equilíbrio quando todas as posições começam iguais (ponto fixo instável)

## Como executar

```bash
pip install matplotlib numpy
python exercise_4_12.py
python exercise_4_13.py
python exercise_4_15.py
```

As figuras são salvas automaticamente na pasta `figuras/`.
