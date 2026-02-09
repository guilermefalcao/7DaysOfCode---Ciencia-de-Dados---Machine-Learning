"""
Dia 6 - #7DaysOfCode Ciência de Dados
Teste A/B - Validação de Hipóteses

Sistema de Recomendação vs Versão Controle
Análise estatística para validar se o sistema de recomendação
melhora a taxa de conversão do e-commerce.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime

def carregar_dados():
    """Carrega e prepara os dados do teste A/B"""
    df = pd.read_csv('ab_test_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    return df

def estatisticas_descritivas(df):
    """Calcula estatísticas descritivas por grupo"""
    print("=" * 60)
    print("📊 ESTATÍSTICAS DESCRITIVAS DO TESTE A/B")
    print("=" * 60)
    
    # Contagem por grupo
    grupo_counts = df['group'].value_counts()
    print(f"\n👥 Distribuição dos usuários:")
    print(f"Controle (sem recomendação): {grupo_counts['control']} usuários")
    print(f"Treatment (com recomendação): {grupo_counts['treatment']} usuários")
    
    # Taxa de conversão por grupo
    conversao_por_grupo = df.groupby('group')['converted'].agg(['count', 'sum', 'mean'])
    conversao_por_grupo.columns = ['Total_Usuarios', 'Conversoes', 'Taxa_Conversao']
    
    print(f"\n📈 Taxa de Conversão por Grupo:")
    print(conversao_por_grupo)
    
    # Diferença entre grupos
    taxa_control = conversao_por_grupo.loc['control', 'Taxa_Conversao']
    taxa_treatment = conversao_por_grupo.loc['treatment', 'Taxa_Conversao']
    diferenca = taxa_treatment - taxa_control
    
    print(f"\n🎯 Diferença na Taxa de Conversão:")
    print(f"Treatment - Control = {diferenca:.4f} ({diferenca*100:.2f}%)")
    
    return conversao_por_grupo

def visualizacoes(df):
    """Cria visualizações dos dados"""
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Taxa de conversão por grupo
    conversao = df.groupby('group')['converted'].mean()
    axes[0,0].bar(conversao.index, conversao.values, color=['#ff7f0e', '#1f77b4'])
    axes[0,0].set_title('Taxa de Conversão por Grupo')
    axes[0,0].set_ylabel('Taxa de Conversão')
    for i, v in enumerate(conversao.values):
        axes[0,0].text(i, v + 0.01, f'{v:.3f}', ha='center')
    
    # 2. Distribuição de conversões
    conversao_counts = df.groupby(['group', 'converted']).size().unstack()
    conversao_counts.plot(kind='bar', ax=axes[0,1], color=['#d62728', '#2ca02c'])
    axes[0,1].set_title('Distribuição de Conversões')
    axes[0,1].set_ylabel('Número de Usuários')
    axes[0,1].legend(['Não Converteu', 'Converteu'])
    axes[0,1].tick_params(axis='x', rotation=0)
    
    # 3. Conversões ao longo do tempo
    conversao_diaria = df.groupby(['date', 'group'])['converted'].mean().unstack()
    conversao_diaria.plot(ax=axes[1,0], marker='o')
    axes[1,0].set_title('Taxa de Conversão ao Longo do Tempo')
    axes[1,0].set_ylabel('Taxa de Conversão')
    axes[1,0].legend(['Control', 'Treatment'])
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # 4. Boxplot das conversões
    df_melted = df.melt(id_vars=['group'], value_vars=['converted'])
    sns.boxplot(data=df, x='group', y='converted', ax=axes[1,1])
    axes[1,1].set_title('Distribuição de Conversões por Grupo')
    axes[1,1].set_ylabel('Converteu (0/1)')
    
    plt.tight_layout()
    plt.show()

def teste_hipotese(df):
    """Executa teste de hipótese bicaudal para comparar proporções"""
    print("\n" + "=" * 60)
    print("🧪 TESTE DE HIPÓTESE - TESTE Z PARA PROPORÇÕES")
    print("=" * 60)
    
    # Separar dados por grupo
    control = df[df['group'] == 'control']['converted']
    treatment = df[df['group'] == 'treatment']['converted']
    
    # Estatísticas dos grupos
    n1, n2 = len(control), len(treatment)
    x1, x2 = control.sum(), treatment.sum()
    p1, p2 = x1/n1, x2/n2
    
    print(f"\n📋 Dados do Teste:")
    print(f"Grupo Controle: {x1}/{n1} conversões (p1 = {p1:.4f})")
    print(f"Grupo Treatment: {x2}/{n2} conversões (p2 = {p2:.4f})")
    
    # Hipóteses
    print(f"\n🎯 Hipóteses:")
    print(f"H0: p1 = p2 (não há diferença entre os grupos)")
    print(f"H1: p1 ≠ p2 (há diferença entre os grupos)")
    print(f"Nível de significância: α = 0.05")
    print(f"Teste: Bicaudal")
    
    # Teste Z para duas proporções
    # Proporção combinada
    p_combined = (x1 + x2) / (n1 + n2)
    
    # Erro padrão
    se = np.sqrt(p_combined * (1 - p_combined) * (1/n1 + 1/n2))
    
    # Estatística Z
    z_stat = (p2 - p1) / se
    
    # P-valor (teste bicaudal)
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # Valor crítico para α = 0.05 (bicaudal)
    z_critical = stats.norm.ppf(0.975)  # 1.96
    
    print(f"\n📊 Resultados do Teste:")
    print(f"Proporção combinada: {p_combined:.4f}")
    print(f"Erro padrão: {se:.4f}")
    print(f"Estatística Z: {z_stat:.4f}")
    print(f"Valor crítico (±): {z_critical:.4f}")
    print(f"P-valor: {p_value:.4f}")
    
    # Interpretação
    print(f"\n🎯 Interpretação:")
    if p_value < 0.05:
        print(f"✅ REJEITAMOS H0 (p-valor = {p_value:.4f} < 0.05)")
        print(f"Há evidência estatística de diferença significativa entre os grupos.")
        if p2 > p1:
            print(f"🚀 O sistema de recomendação MELHORA a taxa de conversão!")
        else:
            print(f"⚠️  O sistema de recomendação PIORA a taxa de conversão!")
    else:
        print(f"❌ NÃO REJEITAMOS H0 (p-valor = {p_value:.4f} >= 0.05)")
        print(f"Não há evidência estatística de diferença significativa.")
        print(f"🤔 O sistema de recomendação não tem impacto significativo.")
    
    # Intervalo de confiança para a diferença
    diff = p2 - p1
    se_diff = se
    ic_lower = diff - z_critical * se_diff
    ic_upper = diff + z_critical * se_diff
    
    print(f"\n📏 Intervalo de Confiança (95%) para a diferença:")
    print(f"[{ic_lower:.4f}, {ic_upper:.4f}]")
    
    return {
        'z_stat': z_stat,
        'p_value': p_value,
        'diferenca': diff,
        'ic_95': (ic_lower, ic_upper)
    }

def main():
    """Função principal"""
    print("🚀 Iniciando Análise do Teste A/B")
    print("Sistema de Recomendação vs Versão Controle")
    
    # Carregar dados
    df = carregar_dados()
    print(f"\n📁 Dataset carregado: {len(df)} registros")
    
    # Estatísticas descritivas
    stats_desc = estatisticas_descritivas(df)
    
    # Visualizações
    print(f"\n📊 Gerando visualizações...")
    visualizacoes(df)
    
    # Teste de hipótese
    resultado_teste = teste_hipotese(df)
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📋 RESUMO EXECUTIVO")
    print("=" * 60)
    
    taxa_control = df[df['group'] == 'control']['converted'].mean()
    taxa_treatment = df[df['group'] == 'treatment']['converted'].mean()
    
    print(f"Taxa de Conversão - Controle: {taxa_control:.2%}")
    print(f"Taxa de Conversão - Treatment: {taxa_treatment:.2%}")
    print(f"Diferença: {resultado_teste['diferenca']:.2%}")
    print(f"P-valor: {resultado_teste['p_value']:.4f}")
    
    if resultado_teste['p_value'] < 0.05:
        print(f"\n🎉 CONCLUSÃO: O sistema de recomendação tem impacto significativo!")
    else:
        print(f"\n🤷 CONCLUSÃO: Não há evidência de impacto significativo.")

if __name__ == "__main__":
    main()