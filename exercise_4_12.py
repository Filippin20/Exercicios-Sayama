# =============================================================
# Exercício 4.12 – Sayama, Capítulo 4
# Livro: Introduction to the Modeling and Analysis of Complex Systems
# Autor do código: Filippo de Oliveira Barbosa
#
# Objetivo:
#   Implementar uma simulação do modelo discreto linear
#       x_t = a * x_{t-1}
#   e observar como o comportamento do sistema muda para
#   diferentes valores do parâmetro 'a'.
#
# Como construí o modelo:
#   1. Identifiquei a variável de estado: x (escalar real)
#   2. A regra de atualização é simples: multiplicar por 'a'
#   3. A solução fechada é x_t = a^t * x_0 (sistema linear)
#   4. Rodei a simulação para vários valores de 'a' e plotei
#      os resultados para entender os diferentes regimes:
#        a > 1   → crescimento exponencial
#        0 < a < 1 → decaimento exponencial
#        a = 1   → estado estacionário
#        a = 0   → colapso no primeiro passo
#        -1 < a < 0 → oscilação amortecida
#        a = -1  → oscilação de período 2
#        a < -1  → oscilação explosiva (divergência)
# =============================================================

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

os.makedirs("figuras", exist_ok=True)

# ------------------------------------------------------------------
# Parâmetros gerais
# ------------------------------------------------------------------
T  = 30    # número de passos de tempo
x0 = 1.0   # condição inicial

# Valores de 'a' que vou testar
a_labels = [
    ("a = 1.2  (crescimento exp.)",    1.2),
    ("a = 0.8  (decaimento exp.)",     0.8),
    ("a = 1.0  (estado estacionário)", 1.0),
    ("a = 0.0  (colapso imediato)",    0.0),
    ("a = -0.8 (oscilacao amortecida)",-0.8),
    ("a = -1.0 (oscilacao periodo 2)", -1.0),
    ("a = -1.2 (oscilacao explosiva)", -1.2),
]

# ------------------------------------------------------------------
# Funções de simulação (padrão do livro: initialize / observe / update)
# ------------------------------------------------------------------
def inicializar(x_inicial):
    """Define o estado inicial do sistema."""
    global x, resultado
    x = x_inicial
    resultado = [x]

def observar():
    """Registra o estado atual na série temporal."""
    global x, resultado
    resultado.append(x)

def atualizar(a):
    """Aplica a regra de evolução: x_t = a * x_{t-1}."""
    global x
    x = a * x

def simular(a, x0=1.0, T=30):
    """Roda a simulação completa e retorna a série temporal."""
    inicializar(x0)
    for _ in range(T):
        atualizar(a)
        observar()
    return list(resultado)

# ------------------------------------------------------------------
# Geração dos gráficos – um subplot por valor de 'a'
# ------------------------------------------------------------------
fig = plt.figure(figsize=(14, 10))
fig.suptitle("Exercício 4.12 – Modelo $x_t = a\\,x_{t-1}$",
             fontsize=14, fontweight="bold")
gs   = gridspec.GridSpec(3, 3, hspace=0.60, wspace=0.45)
axes = [fig.add_subplot(gs[i // 3, i % 3]) for i in range(len(a_labels))]

for ax, (lbl, a) in zip(axes, a_labels):
    serie = simular(a, x0, T)
    ax.plot(serie, color="#01696f", lw=1.8, marker="o", markersize=2.5)
    ax.axhline(0, color="gray", lw=0.7, ls="--")
    ax.set_title(lbl, fontsize=8.5, pad=4)
    ax.set_xlabel("t", fontsize=8)
    ax.set_ylabel("$x_t$", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.3)

for ax in axes[len(a_labels):]:
    ax.set_visible(False)

plt.savefig("figuras/ex4_12_trajetorias.png", dpi=180, bbox_inches="tight")
plt.show()
print("Figura salva em figuras/ex4_12_trajetorias.png")
