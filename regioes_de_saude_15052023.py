import pandas as pd
import numpy as np
# importar planilha Atual: sheet: "Atual_15052023", da coluna A-G
# Pular primeira linha: skiprows 
# usecols="A:G"
# nomear colunas: 
nome_colunas = ['CD_MUNICIPIO', 'SG_UF', 'CD_REGIAO_SAUDE_2023', 'NM_REGIAO_SAUDE_ATUAL', 'NM_MUNICIPIO',
       'NM_REGIAO_SAUDE_ANTERIOR', 'NM_MUNICIPIOS_IN_37']

df_regioes = pd.read_excel(r'D:\\ANS\\estudos\\RegioesSaudeVaziosAssistenciais\\Regionais de saude_comparativo2023.xlsm', sheet_name='Atual_15052023', skiprows=1, usecols="A:G", names=nome_colunas)
# df_regioes = pd.read_excel(r'/home/doug/Documentos/Programas python/Regionais de saude  - comparativo.xlsm', sheet_name='Atual em 08-10-18', skiprows=1, usecols="A:F", names=nome_colunas)

df_regioes.columns

# Importante. Classificar!!!
df_regioes.sort_values(by=['SG_UF', 'NM_REGIAO_SAUDE_ATUAL', 'NM_REGIAO_SAUDE_ANTERIOR'], inplace=True)

# USANDO AGRUPAMENTO
# número de regiões atuais
agrupamento1 = df_regioes.groupby(['NM_REGIAO_SAUDE_ATUAL'])['NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF'].count()
# resposta: Name: NM_REGIAO_SAUDE_ANTERIOR, Length: 428, dtype: int64

# número de regiões atuais
agrupamento2 = df_regioes.groupby(['NM_REGIAO_SAUDE_ATUAL', 'NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF'])['NM_REGIAO_SAUDE_ATUAL', 'NM_REGIAO_SAUDE_ANTERIOR'].count()

# contagem do número de informacoes distintas
agrupamento3 = df_regioes.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF']).agg({"NM_REGIAO_SAUDE_ANTERIOR": pd.Series.nunique})

df_filtrado = agrupamento3[agrupamento3['NM_REGIAO_SAUDE_ANTERIOR'] > 1]

'''
PASSO IMPORTANTE: COMPOSIÇÃO DE TODOS OS MUNICÍPIOS ENVOLVIDOS 
NAS REGIÕES DE SAÚDE QUE SOFRERAM ALTERAÇÕES:
Exemplos de regiões de Saúde:
a) 22ª Região Cascavel: Envolve, agora, municí­pios que pertenciam
as regiões de Saúde de Fortaleza e Aracati
b) Baixo Acre e Purus: Era a antiga Região de Saúde 'Acre', porém envolveu, agora,
o município de Jordão, que pertencia a Região de Saúde 'Cruzeiro do Sul' 
c) Imperatriz: Englobou, quase totalmente, as regiões: Chapada das Mesas; Serras e Tocantins

'''
regiao_municip_diferente = pd.merge(df_filtrado, df_regioes, how = 'left', left_on='NM_REGIAO_SAUDE_ATUAL', right_on='NM_REGIAO_SAUDE_ATUAL')

# Exportar resultado para o Excel
with pd.ExcelWriter(r'D:\\ANS\\estudos\\RegioesSaudeVaziosAssistenciais\\Resultados_15052023.xlsx') as writer:
       agrupamento1.to_excel(writer, sheet_name='Agrupamento1')
       agrupamento2.to_excel(writer, sheet_name='Agrupamento2')
       agrupamento3.to_excel(writer, sheet_name='Agrupamento3')
       regiao_municip_diferente.to_excel(writer, sheet_name='Reg_Muni_Dif')



