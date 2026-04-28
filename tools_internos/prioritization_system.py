import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def run_prioritization_simulation():
    """
    Sistema de Priorização — Fórmula alinhada com a documentação:
    Score = Risco(40%) + Vulnerabilidade(30%) + Urgência(30%)
    """
    print("Iniciando Sistema de Priorização (Parte 3)...")
    
    np.random.seed(42)
    n = 10000
    
    df = pd.DataFrame({
        'id_chamado': range(n),
        'prob_atraso': np.random.uniform(0.05, 0.95, n),
        'vulnerabilidade': np.random.uniform(0.1, 1.0, n),
        'urgencia_cat': np.random.choice([0.3, 0.6, 1.0], n, p=[0.5, 0.3, 0.2])
    })
    
    # Fórmula do Score (3 componentes — alinhada com documentação do Notebook 03)
    W_RISCO, W_VULN, W_URG = 0.40, 0.30, 0.30
    
    df['score'] = (
        df['prob_atraso'] * W_RISCO +
        df['vulnerabilidade'] * W_VULN +
        df['urgencia_cat'] * W_URG
    )
    
    # Ground truth
    df['atraso_real'] = np.random.binomial(1, df['prob_atraso'])
    
    # Simulação (Budget = 20%)
    k = int(n * 0.20)
    total_atrasos = df['atraso_real'].sum()
    
    np.random.seed(0)
    captura_random = df.sample(k)['atraso_real'].sum()
    captura_score = df.nlargest(k, 'score')['atraso_real'].sum()
    
    ganho = (captura_score / captura_random - 1) * 100
    
    print(f"Total de Atrasos: {total_atrasos}")
    print(f"Captura Aleatória (20%): {captura_random}")
    print(f"Captura Score PIC (20%): {captura_score}")
    print(f"Ganho de Eficiência: {ganho:.1f}%")
    
    # Curva de Lift
    df_sorted = df.sort_values('score', ascending=False).reset_index(drop=True)
    df_sorted['cum_atrasos'] = df_sorted['atraso_real'].cumsum() / total_atrasos
    df_sorted['percentile'] = (df_sorted.index + 1) / n
    
    if not os.path.exists("results/figures"):
        os.makedirs("results/figures")
    
    plt.figure(figsize=(10, 6))
    plt.fill_between(df_sorted['percentile'], df_sorted['cum_atrasos'], alpha=0.3, color='#1976D2')
    plt.plot(df_sorted['percentile'], df_sorted['cum_atrasos'], color='#1976D2', linewidth=2, label='Score PIC')
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Aleatório')
    plt.axvline(x=0.2, color='#D32F2F', linestyle=':', linewidth=2, label='Budget 20%')
    plt.title("Curva de Lift: Eficiência do Sistema de Priorização", fontweight='bold')
    plt.xlabel("% de Chamados Priorizados")
    plt.ylabel("% de Atrasos Capturados")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/figures/lift_curve.png", dpi=150)
    plt.close()
    
    print("Simulação concluída.")

if __name__ == "__main__":
    run_prioritization_simulation()
