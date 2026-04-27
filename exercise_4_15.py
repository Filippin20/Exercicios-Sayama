# =============================================================
# Exercício 4.15 – Sayama, Capítulo 4
# Livro: Introduction to the Modeling and Analysis of Complex Systems
# Autor do código: Filippo de Oliveira Barbosa
#
# Objetivo:
#   Modelar a dinâmica de opiniões políticas com três opções:
#   conservador, liberal e neutro.
#
# Como construí o modelo (passo a passo):
#
#   Passo 1 – Variáveis de estado:
#     pc = popularidade do conservadorismo  (0 ≤ pc ≤ 1)
#     pl = popularidade do liberalismo      (0 ≤ pl ≤ 1)
#     pn = 1 - pc - pl  (popularidade dos neutros, implícita)
#     Restrição: pc + pl ≤ 1 e ambas ≥ 0.
#
#   Passo 2 – Regra de troca de ideologia:
#     As pessoas tendem a adotar a posição mais popular.
#     A taxa de migração de X para Y é proporcional a
#     max(0, p_Y - p_X), ou seja, só ocorre se Y for mais popular.
#     O fluxo efetivo de X→Y é: fluxo(X→Y) = max(0, p_Y - p_X) · p_X
#     (taxa de atração vezes a fração atual de X)
#
#   Passo 3 – Seis fluxos possíveis:
#     f_cl: conservador → liberal
#     f_cn: conservador → neutro
#     f_lc: liberal → conservador
#     f_ln: liberal → neutro
#     f_nc: neutro → conservador
#     f_nl: neutro → liberal
#
#   Passo 4 – Equações de diferença:
#     pc(t) = pc(t-1) + f_lc + f_nc - f_cl - f_cn
#     pl(t) = pl(t-1) + f_cl + f_nl - f_lc - f_ln
#     pn(t) = 1 - pc(t) - pl(t)
#
#   Passo 5 – Normalização numérica:
#     Após cada passo, normalizo para que pc+pl+pn = 1 exatamente,
#     evitando acúmulo de erros de ponto flutuante.
# =============================================================

import matplotlib.pyplot as plt
import os

os.makedirs("figuras", exist_ok=True)

# ------------------------------------------------------------------
# Funções de simulação (padrão: initialize / observe / update)
# ------------------------------------------------------------------

def inicializar(pc0, pl0):
    """Define as condições iniciais de pc e pl."""
    global pc, pl
    global pcs, pls, pns
    pc, pl = pc0, pl0
    pcs = [pc]
    pls = [pl]
    pns = [1 - pc - pl]

def observar():
    """Registra o estado atual."""
    global pc, pl, pcs, pls, pns
    pcs.append(pc)
    pls.append(pl)
    pns.append(1 - pc - pl)

def atualizar():
    """Aplica as equações de dinâmica de opinião."""
    global pc, pl
    pn = 1 - pc - pl

    # Calculo os seis fluxos de troca
    f_cl = max(0, pl - pc) * pc   # conservador → liberal
    f_cn = max(0, pn - pc) * pc   # conservador → neutro
    f_lc = max(0, pc - pl) * pl   # liberal → conservador
    f_ln = max(0, pn - pl) * pl   # liberal → neutro
    f_nc = max(0, pc - pn) * pn   # neutro → conservador
    f_nl = max(0, pl - pn) * pn   # neutro → liberal

    # Calculo os novos valores
    npc = pc + f_lc + f_nc - f_cl - f_cn
    npl = pl + f_cl + f_nl - f_lc - f_ln
    npn = pn + f_cn + f_ln - f_nc - f_nl

    # Normalizo para evitar deriva numérica (garante soma = 1)
    total = npc + npl + npn
    pc = npc / total
    pl = npl / total

def simular(pc0, pl0, T=100):
    """Roda a simulação e retorna as séries temporais."""
    inicializar(pc0, pl0)
    for _ in range(T):
        atualizar()
        observar()
    return list(pcs), list(pls), list(pns)

# ------------------------------------------------------------------
# Cenários testados (diferentes condições iniciais)
# ------------------------------------------------------------------
cenarios = [
    (0.40, 0.10, "pc0=0.40, pl0=0.10\nConservador domina"),
    (0.10, 0.40, "pc0=0.10, pl0=0.40\nLiberal domina"),
    (0.33, 0.33, "pc0=pl0=0.33\nEmpate inicial"),
    (0.10, 0.10, "pc0=pl0=0.10\nNeutro domina"),
    (0.45, 0.45, "pc0=0.45, pl0=0.45\nExtremismo polarizado"),
    (0.25, 0.35, "pc0=0.25, pl0=0.35\nLiberal com leve vantagem"),
]

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
fig.suptitle("Exercicio 4.15 – Dinamica de Opiniao Politica
"
             "(Conservador / Liberal / Neutro)",
             fontsize=12, fontweight="bold")
axes = axes.flatten()

for ax, (pc0, pl0, lbl) in zip(axes, cenarios):
    pcs_r, pls_r, pns_r = simular(pc0, pl0)
    t = range(len(pcs_r))
    ax.plot(t, pcs_r, color="#a13544", lw=2,   label="Conservador (pc)")
    ax.plot(t, pls_r, color="#01696f", lw=2,   label="Liberal (pl)")
    ax.plot(t, pns_r, color="#d19900", lw=2, ls="--", label="Neutro (pn)")
    ax.axhline(1/3, color="gray", lw=0.6, ls=":", alpha=0.6)  # linha de equilíbrio
    ax.set_ylim(-0.05, 1.05)
    ax.set_title(lbl, fontsize=9)
    ax.set_xlabel("t (rodada de pesquisa)", fontsize=8)
    ax.set_ylabel("Popularidade", fontsize=8)
    ax.legend(fontsize=7, loc="center right")
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.25)

# Imprimo o estado final de cada cenário
print("\n=== Resultados finais (t=100) ===")
for pc0, pl0, lbl in cenarios:
    pcs_r, pls_r, pns_r = simular(pc0, pl0)
    print(f"Condição inicial: pc={pc0:.2f}, pl={pl0:.2f}")
    print(f"  Final → Conservador: {pcs_r[-1]:.4f} | "
          f"Liberal: {pls_r[-1]:.4f} | Neutro: {pns_r[-1]:.4f}\n")

plt.tight_layout()
plt.savefig("figuras/ex4_15_opiniao_politica.png", dpi=150, bbox_inches="tight")
plt.show()
print("Figura salva em figuras/ex4_15_opiniao_politica.png")
