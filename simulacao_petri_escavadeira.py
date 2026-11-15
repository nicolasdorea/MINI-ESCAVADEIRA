import numpy as np

# Definicao dos 10 Lugares e 8 Transicoes da Mini Escavadeira Didatica
lugares = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'PC', 'PO']
transicoes = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']

# Matriz de Entrada D- (10 lugares x 8 transicoes)
D_minus = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0],  # P0: Repouso
    [0, 1, 0, 0, 0, 0, 0, 0],  # P1: Plataforma orientada para coleta
    [0, 0, 1, 0, 0, 0, 0, 0],  # P2: Lanca e braco aproximados
    [0, 0, 0, 1, 0, 0, 0, 0],  # P3: Cacamba recolhendo
    [0, 0, 0, 0, 1, 0, 0, 0],  # P4: Braco elevado
    [0, 0, 0, 0, 0, 1, 0, 0],  # P5: Plataforma girada para descarga
    [0, 0, 0, 0, 0, 0, 1, 0],  # P6: Cacamba descarregando
    [0, 0, 0, 0, 0, 0, 0, 1],  # P7: Retorno a posicao inicial
    [1, 0, 0, 0, 0, 0, 0, 0],  # PC: Comando START
    [0, 0, 1, 0, 0, 0, 0, 0],  # PO: Objeto detectado (sensor ultrassonico)
])

# Matriz de Saida D+ (10 lugares x 8 transicoes)
D_plus = np.array([
    [0, 0, 0, 0, 0, 0, 0, 1],  # P0
    [1, 0, 0, 0, 0, 0, 0, 0],  # P1
    [0, 1, 0, 0, 0, 0, 0, 0],  # P2
    [0, 0, 1, 0, 0, 0, 0, 0],  # P3
    [0, 0, 0, 1, 0, 0, 0, 0],  # P4
    [0, 0, 0, 0, 1, 0, 0, 0],  # P5
    [0, 0, 0, 0, 0, 1, 0, 0],  # P6
    [0, 0, 0, 0, 0, 0, 1, 0],  # P7
    [0, 0, 0, 0, 0, 0, 0, 0],  # PC
    [0, 0, 0, 0, 0, 0, 0, 0],  # PO
])

# Matriz de Incidencia C = D+ - D-
C = D_plus - D_minus

# Marcacao Inicial M0
M0 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 1, 1])

def transicoes_habilitadas(M, D_m):
    habilitadas = []
    for j in range(D_m.shape[1]):
        if np.all(M >= D_m[:, j]):
            habilitadas.append(transicoes[j])
    return habilitadas

def disparar(M, idx_t, D_m, C_mat):
    if not np.all(M >= D_m[:, idx_t]):
        raise ValueError(f"Transicao {transicoes[idx_t]} nao habilitada!")
    u = np.zeros(C_mat.shape[1], dtype=int)
    u[idx_t] = 1
    return M + C_mat @ u

if __name__ == "__main__":
    print("=== MATRIZ DE INCIDENCIA C = D+ - D- ===")
    print(C)
    M = M0.copy()
    print(f"\nM0 = {M.tolist()} | Habilitadas: {transicoes_habilitadas(M, D_minus)}")
    for i, t_nome in enumerate(transicoes):
        M = disparar(M, i, D_minus, C)
        print(f"Apos {t_nome} -> M{i+1} = {M.tolist()} | Habilitadas: {transicoes_habilitadas(M, D_minus)}")
