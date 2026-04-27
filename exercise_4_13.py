# =============================================================
# Exercício 4.13 – Sayama, Capítulo 4
# Livro: Introduction to the Modeling and Analysis of Complex Systems
# Autor do código: Filippo de Oliveira Barbosa
#
# Objetivo:
#   Explorar diferentes configurações de parâmetros do modelo
#   presa-predador desenvolvido na Seção 4.6, e corrigir o
#   comportamento inválido (crescimento indefinido de predadores).
#
# Modelo original (Eqs. 4.34–4.35):
#   x_t = x_{t-1} + r·x_{t-1}·(1 - x_{t-1}/K)
#                 - [b·y_{t-1}/(1 + b·y_{t-1})]·x_{t-1}
#
#   y_t = y_{t-1} - d·y_{t-1} + c·x_{t-1}·y_{t-1}
#
#   Onde:
#     x = população de presas
#     y = população de predadores
#     r = taxa de crescimento intrínseco das presas
#     K = capacidade de suporte do ambiente (para as presas)
#     b = eficiência de predação (resposta funcional)
#     d = taxa de mortalidade dos predadores
#     c = eficiência de conversão (presa → predador)
#
# Problema encontrado:
#   Quando c é grande e d é pequeno, os predadores crescem
#   indefinidamente — o que é biologicamente impossível,
#   pois qualquer espécie enfrenta limitações de recursos
#   além da disponibilidade de presas.
#
# Correção proposta:
#   Adicionei um termo logístico nos predadores com
#   capacidade de suporte K_y, que limita o crescimento:
#
#   y_t = y_{t-1} + (-d·y_{t-1} + c·x_{t-1}·y_{t-1})·(1 - y_{t-1}/K_y)
#
# =============================================================

import matplotlib.pyplot as plt
import os

os.makedirs("figuras", exist_ok=True)

# ------------------------------------------------------------------
# Parâmetros padrão
# ------------------------------------------------------------------
K_DEFAULT  = 5.0    # capacidade de suporte das presas
KY_DEFAULT = 10.0   # capacidade de suporte dos predadores (versão corrigida)
T          = 200    # passos de tempo

# ------------------------------------------------------------------
# Funções de simulação (padrão: initialize / observe / update)
# ------------------------------------------------------------------
def inicializar(x0, y0):
    """Inicializa o estado do sistema."""
    global x, y, xs, ys
    x, y = x0, y0
    xs, ys = [x], [y]

def observar():
    """Registra o estado atual."""
    global x, y, xs, ys
    xs.append(x)
    ys.append(y)

# --- Versão original (pode apresentar explosão de predadores) ---

def atualizar_original(r, b, d, c, K):
    """Aplica as Eqs. 4.34-4.35 do livro."""
    global x, y
    taxa_predacao = (b * y) / (1 + b * y)
    nx = x + r * x * (1 - x / K) - taxa_predacao * x
    ny = y - d * y + c * x * y
    x = max(nx, 0.0)   # população não pode ser negativa
    y = max(ny, 0.0)

def simular_original(r, b, d, c, K=K_DEFAULT, x0=1.0, y0=1.0, T=T):
    """Simulação com o modelo original."""
    inicializar(x0, y0)
    for _ in range(T):
        atualizar_original(r, b, d, c, K)
        observar()
    return list(xs), list(ys)

# --- Versão corrigida (crescimento logístico para predadores) ---

def atualizar_corrigido(r, b, d, c, K, Ky):
    """Versão corrigida: predadores têm capacidade de suporte K_y."""
    global x, y
    taxa_predacao = (b * y) / (1 + b * y)
    nx = x + r * x * (1 - x / K) - taxa_predacao * x
    # O fator (1 - y/K_y) impede o crescimento ilimitado dos predadores
    ny = y + (-d * y + c * x * y) * (1 - y / Ky)
    x = max(nx, 0.0)
    y = max(ny, 0.0)

def simular_corrigido(r, b, d, c, K=K_DEFAULT, Ky=KY_DEFAULT, x0=1.0, y0=1.0, T=T):
    """Simulação com o modelo corrigido."""
    inicializar(x0, y0)
    for _ in range(T):
        atualizar_corrigido(r, b, d, c, K, Ky)
        observar()
    return list(xs), list(ys)

# ------------------------------------------------------------------
# Cenários para o modelo ORIGINAL
# ------------------------------------------------------------------
param_original = [
    dict(r=1, b=1, d=1,   c=1,   label="Padrao: r=b=d=c=1"),
    dict(r=2, b=1, d=1,   c=1,   label="Alto crescimento da presa: r=2"),
    dict(r=1, b=2, d=1,   c=1,   label="Alta pressao de predicao: b=2"),
    dict(r=1, b=0.5, d=0.3, c=0.5, label="Baixo d e c (coexistencia)"),
    dict(r=1, b=1, d=0.1, c=2,   label="[INVALIDO] c=2, d=0.1 (explosao)"),
]

fig, axes = plt.subplots(len(param_original), 2, figsize=(13, 18))
fig.suptitle("Exercicio 4.13 – Modelo original: exploracao de parametros",
             fontsize=13, fontweight="bold")

for i, ps in enumerate(param_original):
    xs_r, ys_r = simular_original(ps["r"], ps["b"], ps["d"], ps["c"])
    t = range(len(xs_r))
    ax_t, ax_p = axes[i, 0], axes[i, 1]
    ax_t.plot(t, xs_r, label="Presa (x)", color="#01696f", lw=1.5)
    ax_t.plot(t, ys_r, label="Predador (y)", color="#a13544", lw=1.5, ls="--")
    ax_t.set_title(ps["label"], fontsize=9); ax_t.set_xlabel("t"); ax_t.set_ylabel("Pop.")
    ax_t.legend(fontsize=7); ax_t.grid(True, alpha=0.25)
    ax_p.plot(xs_r, ys_r, color="#006494", lw=1.2, alpha=0.8)
    ax_p.set_xlabel("Presa (x)"); ax_p.set_ylabel("Predador (y)")
    ax_p.set_title("Espaco de fase"); ax_p.grid(True, alpha=0.25)

plt.tight_layout()
plt.savefig("figuras/ex4_13_original.png", dpi=150, bbox_inches="tight")
plt.show()

# ------------------------------------------------------------------
# Cenários para o modelo CORRIGIDO
# ------------------------------------------------------------------
param_corrigido = [
    dict(r=1, b=1, d=0.1, c=2,  Ky=10, label="Corrigido: c=2, d=0.1, Ky=10"),
    dict(r=1, b=1, d=0.1, c=2,  Ky=20, label="Corrigido: c=2, d=0.1, Ky=20"),
    dict(r=1, b=1, d=1,   c=1,  Ky=10, label="Padrao corrigido com Ky=10"),
]

fig, axes = plt.subplots(len(param_corrigido), 2, figsize=(13, 11))
fig.suptitle("Exercicio 4.13 – Modelo CORRIGIDO (logistica nos predadores)",
             fontsize=12, fontweight="bold")

for i, ps in enumerate(param_corrigido):
    xs_r, ys_r = simular_corrigido(ps["r"], ps["b"], ps["d"], ps["c"], Ky=ps["Ky"])
    t = range(len(xs_r))
    ax_t, ax_p = axes[i, 0], axes[i, 1]
    ax_t.plot(t, xs_r, label="Presa (x)", color="#01696f", lw=1.5)
    ax_t.plot(t, ys_r, label="Predador (y)", color="#a13544", lw=1.5, ls="--")
    ax_t.set_title(ps["label"], fontsize=9); ax_t.set_xlabel("t"); ax_t.set_ylabel("Pop.")
    ax_t.legend(fontsize=7); ax_t.grid(True, alpha=0.25)
    ax_p.plot(xs_r, ys_r, color="#006494", lw=1.2, alpha=0.8)
    ax_p.set_xlabel("Presa (x)"); ax_p.set_ylabel("Predador (y)")
    ax_p.set_title("Espaco de fase"); ax_p.grid(True, alpha=0.25)

plt.tight_layout()
plt.savefig("figuras/ex4_13_corrigido.png", dpi=150, bbox_inches="tight")
plt.show()
print("Figuras salvas em figuras/")
