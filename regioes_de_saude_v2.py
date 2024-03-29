# -*- coding: utf-8 -*-
"""Welcome To Colaboratory

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Domdoug/Regioes-de-Saude/blob/master/Regioes_de_Saude.ipynb
"""

import pandas as pd
import numpy as np
import re

nome_colunas = ['CD_MUNICIPIO', 'SG_UF', 'NM_REGIAO_SAUDE_ATUAL', 'NM_MUNICIPIO',
       'NM_REGIAO_SAUDE_ANTERIOR', 'NM_MUNICIPIOS_IN_37', 'ESTADO', 'REGIAO_PAIS']

# df_regioes = pd.read_excel('BI_Regionais de saude.xlsx', sheet_name='Dados', skiprows=1, usecols="A:H", names=nome_colunas)
df_regioes = pd.read_excel('/home/doug/Documentos/Programas python/Regioes_Saude/BI_Regionais de saude.xlsx', sheet_name='Dados', skiprows=1, usecols="A:H", names=nome_colunas)
df_regioes.sort_values(by='SG_UF', ascending=True).head()
df_regioes.shape   # (5571, 8)
df_regioes.tail()
# INICIO DO PROCESSAMENTO

# Esta linha e para agilizar o groupby. Talvez desnecessaria. Lógica do do SAS
df_regioes.sort_values(by=['NM_REGIAO_SAUDE_ATUAL', 'SG_UF'], inplace=True)

# Aplicar na coluna CD_MUNICIPIO uma funcao para colocar os codigos do municipios em formato de conjunto para comparar,
# agrupados por regiao atual e UF, com o agrupamento dos municipios correspondentes da regiao anterior

lista1 = df_regioes.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF'])['CD_MUNICIPIO'].apply(lambda x:list(set(x)))

# Agora a lista para a Região de Saúde anterior
df_regioes.sort_values(by=['NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF'], inplace=True)

# Agora o código para a lista2: Regiao de Saude Anterior
lista2 = df_regioes.groupby(['NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF'])['CD_MUNICIPIO'].apply(lambda x:list(set(x)))

# Para transformar o formato agrupado em DataFrame
lista1 = lista1.reset_index()
lista2 = lista2.reset_index()

lista1.head()

lista2.head()

lista1.shape # (438, 3)

lista2.shape  # (358, 3)

# ================ TESTES=========================

# verificar se tem regiões que abrangem mais de uma UF:
# df_regioes.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF']).size()
df_unicos = df_regioes.drop_duplicates(subset=['NM_REGIAO_SAUDE_ATUAL', 'SG_UF'])

df_unicos.shape  #438, 8

# Agrupa para selecionar Região de Saúde no DataFrame. Depois aplica o o metodo duplicated, para selecionar os efetivamente repetidos
linhas_duplicadas = df_regioes.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF'], as_index=False).count()

linhas_duplicadas.shape  # (438, 8)

# Seleciona todas as linhas duplicadas baseadas em uma lista de colunas. O parametro keep é para exibir todos os repetidos e não o último ou primeiro
linhas_duplicadas = linhas_duplicadas[linhas_duplicadas.duplicated(subset=['NM_REGIAO_SAUDE_ATUAL'], keep=False)]
linhas_duplicadas.shape  #(17, 8)
linhas_duplicadas.head()
# Análise: Observando o campo NM_REGIAO_SAUDE_ATUAL e SG_UF, observa-se que: As regiões repetidas e que são de UF's contíguas São: Baixo Amazonas (AM e PA).
# O restante não são contíguas. Destaque para a Região de Saúde nomeada de "NORTE". Observando-se RJ e ES, que são contíguos, porém as respectivas Regiões situam-se no Norte de cada Estado.



# Até aqui, para a região Norte, não tem Problemas
teste = lista1[lista1['NM_REGIAO_SAUDE_ATUAL']=='Norte']
# Para o caso da Região Baixo Amazonas que abrange 2 UF's, deve-se colocar a condição de agregar, para este caso, as duas UF's 
# teste = lista1[lista1['NM_REGIAO_SAUDE_ATUAL']=='Baixo Amazonas']

'''
# teste.to_excel('teste2.xlsx')
lista1.to_excel('lista1.xlsx')

teste.shape

teste.head()

teste['CD_MUNICIPIO'].str.len()

teste = lista1[lista1['NM_REGIAO_SAUDE_ATUAL']=='Baixo Amazonas']

teste['CD_MUNICIPIO'].str.len()
'''
# verificar se tem regiões (ANTERIOR que abrangem mais de uma UF:
# df_regioes.groupby(['NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF']).size()
df_unicos = df_regioes.drop_duplicates(subset=['NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF'])

df_unicos.shape  #362, 8

# Agrupa para selecionar Região de Saúde no DataFrame. Depois aplica o o metodo duplicated, para selecionar os efetivamente repetidos
linhas_duplicadas = df_regioes.groupby(['NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF'], as_index=False).count()
linhas_duplicadas.shape # 358, 8

# Seleciona todas as linhas duplicadas baseadas em uma lista de colunas. O parametro keep é para exibir todos os repetidos e não o último ou primeiro
linhas_duplicadas = linhas_duplicadas[linhas_duplicadas.duplicated(subset=['NM_REGIAO_SAUDE_ANTERIOR'], keep=False)]
linhas_duplicadas.shape  #(17, 8)
linhas_duplicadas
# Análise: Observando o campo NM_REGIAO_SAUDE_ANTERIOR e SG_UF, observa-se que: As regiões repetidas e que são de UF's contíguas São: Baixo Amazonas (AM e PA).
# O restante não são contíguas.

# ================ FIM DOS TESTES =====================

# ========ROTINA INTERMEDIARIA================

# Rotina para agregar a regiao 'Baixo Amazonas' das UF's: AM e PA, por tratar-se de região interestadual. Caso único. Agregado, por motivos técnicos, ao estado do AM
lista_aux1 = lista1[lista1['NM_REGIAO_SAUDE_ATUAL']=='Baixo Amazonas']
lista_aux2 = lista2[lista2['NM_REGIAO_SAUDE_ANTERIOR']=='Baixo Amazonas']

lista_aux1.head()

lista_aux2.head()

# uso do drop para SG_UF  para facilitar o gropuby por NM_REGIAO_SAUDE_ATUAL
lista_aux1_new = lista_aux1.drop('SG_UF', axis=1)
lista_aux2_new = lista_aux2.drop('SG_UF', axis=1)

lista_aux1_fim = lista_aux1_new.groupby('NM_REGIAO_SAUDE_ATUAL')['CD_MUNICIPIO'].sum().reset_index()
lista_aux2_fim = lista_aux2_new.groupby('NM_REGIAO_SAUDE_ANTERIOR')['CD_MUNICIPIO'].sum().reset_index()

lista_aux1_fim.head()

lista_aux2_fim.head()

# len(lista_aux2_fim['CD_MUNICIPIO'])
# Contar list of values within a pandas df
# contar1 = [sum(a) for a in zip(*lista_aux1_fim['CD_MUNICIPIO'])]
contar1 = list(lista_aux1_fim['CD_MUNICIPIO'])
contar2 = list(lista_aux2_fim['CD_MUNICIPIO'])
contar1
contar2

len(contar1) # 1
len(contar2)

#atualizacao somente da linha onde está o baixo amazonas. Não esquecer de deletar a outra linha. Baixo Amazonas (PA)
lista1.loc[lista1['NM_REGIAO_SAUDE_ATUAL']=='Baixo Amazonas', 'CD_MUNICIPIO'] = contar1
# lista1 = lista1.drop(lista1[(lista1['NM_REGIAO_SAUDE_ATUAL']=='Baixo Amazonas') & (lista1['SG_UF']=='PA')].index) # nao esquecer index
lista1[lista1['NM_REGIAO_SAUDE_ATUAL']=='Baixo Amazonas']
# para a lista 2: Regiao de Saude Anterior
lista2.loc[lista2['NM_REGIAO_SAUDE_ANTERIOR']=='Baixo Amazonas', 'CD_MUNICIPIO'] = contar2
# lista2 = lista2.drop(lista2[(lista2['NM_REGIAO_SAUDE_ANTERIOR']=='Baixo Amazonas') & (lista2['SG_UF']=='PA')].index) # nao esquecer index
lista2[lista2['NM_REGIAO_SAUDE_ANTERIOR']=='Baixo Amazonas']



# =========================================
# OPERAÇÕES DE CONCATENAÇÃO DAS LISTAS DE MUNICIPIOS EM LISTA POR REGIOES COM O DATAFRAME ORIGINAL

df_regioes_concat1 = pd.merge(df_regioes, lista1, how = 'left', left_on=['NM_REGIAO_SAUDE_ATUAL','SG_UF'], right_on=['NM_REGIAO_SAUDE_ATUAL','SG_UF'])
# Agora concatenação com a Regiao anterior, na otica da lista 2
df_regioes_concat2 = pd.merge(df_regioes, lista2, how = 'left', left_on=['NM_REGIAO_SAUDE_ANTERIOR','SG_UF'], right_on=['NM_REGIAO_SAUDE_ANTERIOR','SG_UF'])

df_regioes_concat1.shape # (5571, 9)
df_regioes_concat2.shape # (5571, 9)

df_regioes_concat1.head()
df_regioes_concat1[df_regioes_concat1['NM_REGIAO_SAUDE_ATUAL']=='Baixo Amazonas']
df_regioes_concat2.head()
df_regioes_concat2[df_regioes_concat2['NM_REGIAO_SAUDE_ANTERIOR']=='Baixo Amazonas']

# Renomear coluna que foi gerada na juncao do passo anterior
df_regioes_concat1.rename(columns={'CD_MUNICIPIO_y':'lista_regiao_atual'}, inplace=True)
df_regioes_concat2.rename(columns={'CD_MUNICIPIO_y':'lista_regiao_anterior'}, inplace=True)

# Verificar como os dataframes ficaram apos renomear coluna

df_regioes_concat1.head()
df_regioes_concat2.head()

# como são dois dataframes muito identicos em colunas, usei esta técnica para selecionar as do segundo dataframe que sejam diferentes
colunas_mantidas = df_regioes_concat2.columns.difference(df_regioes_concat1.columns)

colunas_mantidas # Index(['lista_regiao_anterior'], dtype='object')

df_regioes_concat = pd.merge(df_regioes_concat1, df_regioes_concat2[colunas_mantidas], left_index=True, right_index=True, how='outer')

df_regioes_concat.rename(columns={'CD_MUNICIPIO_x':'CD_MUNICIPIO'}, inplace=True)

df_regioes_concat['flag_atual'] = np.where(df_regioes_concat['lista_regiao_atual'] == df_regioes_concat['lista_regiao_anterior'], 0, 1)

df_regioes_concat.head()



# ============ PASSO PARA MERGE COM A TABLE DE MUNICIPIOS PARA AGREGAR CAMPOS DESTA TABELA

# df_municipios = pd.read_excel('AR_BR_RG_UF_MES_MIC_MUN_2018.xls', sheet_name='AR_BR_MUN_2018')
# Colunas originais: ID	CD_GCUF	NM_UF	NM_UF_SIGLA	CD_GCMUN	NM_MUN_2018	AR_MUN_2018

# DATAFRAME COM A AREA DO MUNICIPIO
nome_colunas = ['ID', 'CD_GCUF','NM_UF', 'NM_UF_SIGLA', 'CD_GC_MUN', 'NM_MUN_2018', 'AR_MUN_2018']
df_municipios_area = pd.read_excel('/home/doug/Documentos/Programas python/Regioes_Saude/Area_municipais_2018.xls', sheet_name='AR_BR_MUN_2018', names=nome_colunas)
df_municipios_area = df_municipios_area[pd.notnull(df_municipios_area['ID'])]
df_municipios_area.columns # Index(['ID', 'CD_GCUF', 'NM_UF', 'NM_UF_SIGLA', 'CD_GC_MUN', 'NM_MUN_2018', 'AR_MUN_2018'] Campo área: AR_MUN_2018
df_municipios_area.sort_values(by='NM_UF_SIGLA', ascending=True, inplace=True)
df_municipios_area.reset_index() # 5572 rows × 8 columns
# converter de float para object
df_municipios_area['CD_GC_MUN'] = df_municipios_area['CD_GC_MUN'].astype(int).astype(str)
df_municipios_area.head()
df_municipios_area.shape # (5572,7)
df_municipios_area.tail()


# DATAFRAME COM POPULACAO DO MUNICIPIO: Atencao, tem que ter instrucao para remover notas para rodape que tem na coluna numerica populacao: ([0-9]+[.?!])(\d+) Este comando seleciona o número, mas queremos o contrário para substituir
# UF	COD. UF	COD. MUNIC	NOME DO MUNICÍPIO	 POPULAÇÃO ESTIMADA 
nome_colunas = ['UF', 'COD_UF', 'COD_MUNIC', 'NM_MUNICIPIO', 'POPULACAO'] # ATENCAO: CONCATENAR OS CAMPOS COD_UF + COD_MUNIC = RENOMEAR PAR CD_GC_MUN
df_municipios_pop = pd.read_excel('/home/doug/Documentos/Programas python/Regioes_Saude/populacao_estimativa_dou_2018_20181019.xls', sheet_name='Municípios', skiprows=1, names=nome_colunas)
primeira_linha_vazia = df_municipios_pop[df_municipios_pop.isnull().all(axis=1)==True].index.tolist()[0]  # 5570: corresponde toda a primeira linha vazia no Dataframe

df_municipios_pop = df_municipios_pop.loc[0:primeira_linha_vazia-1] # menos um para não incluir a linha vazia
# df_municipios_pop.loc[13:20] # ponto onde tem uma nota de rodape
df_municipios_pop.sort_values(by='UF', ascending=True, inplace=True)
df_municipios_pop.reset_index() # 5572 rows × 8 columns
df_municipios_pop.head()
df_municipios_pop.columns  # Index(['UF', 'COD_UF', 'COD_MUNIC', 'NM_MUNICIPIO', 'POPULACAO'], dtype='object')
df_municipios_pop.tail()
df_municipios_pop.shape # (5570,4)

# Limpar os indicadores de nota de rodape nos valores da coluna 'populacao' com regex
# ([0-9]+[.?!])(\d+) Este comando seleciona o número, mas queremos o contrário para substituir
# df_municipios_pop['POPULACAO'] = [re.sub(r'([0-9]+[.?!])(\d+)','', str(x)) for x in df_municipios_pop['POPULACAO']]
# Este funcionou: \s\W+\d+\W+
df_municipios_pop['POPULACAO'] = [re.sub(r'(\s\W+\d+\W+)','', str(x)) for x in df_municipios_pop['POPULACAO']]
# retirar o ponto:
df_municipios_pop['POPULACAO'] = df_municipios_pop['POPULACAO'].str.replace('.','')

# df_municipios_pop['POPULACAO'] = df_municipios_pop['POPULACAO'].astype(int)
# CONFERIR
df_municipios_pop[(df_municipios_pop['UF']=='RO') & (df_municipios_pop.index==16)] # linha 16, com nota para rodape. Ver o uso do Regex. OK!!

# CONCATENAR OS CAMPOS CAMPOS COD_UF + COD_MUNIC = RENOMEAR PAR CD_GC_MUN
# remover .0 dos respectivos campos
df_municipios_pop.info()
'''
UF              5570 non-null object
COD_UF          5570 non-null float64
COD_MUNIC       5570 non-null float64
NM_MUNICIPIO    5570 non-null object
POPULACAO       5570 non-null object
'''
df_municipios_pop['COD_MUNIC'] = df_municipios_pop['COD_MUNIC'].astype(int).astype(str)
df_municipios_pop['COD_UF'] = df_municipios_pop['COD_UF'].astype(int).astype(str)
# adicionar zeros no inicio de COD_MUNIC (que sumiu na importacao). Tamanho do campo COD_MUN = 5
df_municipios_pop['COD_MUNIC'] = df_municipios_pop['COD_MUNIC'].str.zfill(5)
# concatenar esses campos:
df_municipios_pop['CD_GC_MUN'] = df_municipios_pop['COD_UF'] + df_municipios_pop['COD_MUNIC']
# deletar as colunas COD_UF e COD_MUNIC
df_municipios_pop.drop(columns=['COD_UF', 'COD_MUNIC'], inplace=True)

# UNIR OS DATAFRAMES MUNICIPIOS AREA E POPULACAO E CAMPO CALCULADO DE DENSIDADE
df_municipios = pd.merge(df_municipios_pop, df_municipios_area, how='outer', left_on='CD_GC_MUN', right_on='CD_GC_MUN')
df_municipios.head()
df_municipios.tail()
df_municipios.shape # (5572, 10)

# Drop em algumas colunas desnecessarias
df_municipios.drop(columns=['ID', 'CD_GCUF'], inplace=True)
# verificar qual a diferenca entre os dois dataframes anterior, pois um deles tem menos linha que o outro:
df_municipios['UF']
df_municipios[pd.isnull(df_municipios['UF'])]
'''
UF	NM_MUNICIPIO	POPULACAO	CD_GC_MUN	NM_UF	NM_UF_SIGLA	NM_MUN_2018	AR_MUN_2018
5570	NaN	NaN	NaN	4300002	Rio Grande do Sul	RS	LAGOA DOS PATOS	10158.754
5571	NaN	NaN	NaN	4300001	Rio Grande do Sul	RS	LAGOA MIRIM	2859.139
'''
# Calcular a densidade demografica:
# df_municipios['densidade_dem'] = df_municipios['POPULACAO'].div(df_municipios['AR_MUN_2018'])
df_municipios['densidade_dem'] = df_municipios['POPULACAO'].astype(float) / df_municipios['AR_MUN_2018'].astype(float)

# df_municipios.dropna(axis=0, how='any', subset=['CD_GCMUN'], inplace=True)

# ==================== ESTATISTICAS ==================
df_municipios['CD_MUNICIPIO_NDV'] = df_municipios['CD_GC_MUN'].astype(str).str[:6]
type(df_municipios['CD_MUNICIPIO_NDV'][0]) # str
df_regioes_concat['CD_MUNICIPIO'] = df_regioes_concat['CD_MUNICIPIO'].astype(str)

# Finalmente: adicionada a base de regioes de saude com a base de municipios (populacao, area, densidade demografica)
df_final = pd.merge(df_regioes_concat, df_municipios, how = 'outer', left_on='CD_MUNICIPIO', right_on='CD_MUNICIPIO_NDV')
df_final.head()
df_final.rename(columns={'SG_UF_x':'SG_UF'}, inplace=True)

# df_regioes_concat.to_excel('teste.xlsx')

# 1) Instrucao para gerar as regioes que nao tiveram alteracao na composicao de municipios
df_reg_mesmos_municipios = df_final[df_final['flag_atual']==0]  # SELECAO
df_reg_mesmos_municipios.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF']).count() # 157 regioes de saude. Otica Regiao Atual (2018). PARA ESTATISTICA: 157 REGIOES DE SAUDE SEM ALTERACOES
df_reg_mesmos_municipios.groupby(['NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF']).count() # 157 regioes de saude. Otica Regiao Atual (2018). Ok 157 REGIOES SEM ALTERACAO
# 2) Quantidade de municipios envolvidos nas regioes onde não teve alteração
df_reg_mesmos_municipios.shape  #(2169, 21). 2.169 municipios. 
municipios_sem_mudar_regiao = df_reg_mesmos_municipios.shape[0]  # outra forma para encontrar o numero de instancia


# ======================================================
# resumo1 = df_final[['SG_UF', 'NM_MUNICIPIO', 'NM_REGIAO_SAUDE_ATUAL']]

# resumo2 = df_reg_mesmos_municipios.groupby(['NM_REGIAO_SAUDE_ATUAL','NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF']).count()['CD_MUNICIPIO'].reset_index()
# resumo2.sort_values('CD_MUNICIPIO', ascending=False, inplace=True)

# 5) As 5 Maiores regioes de saude em extensão territorial, por UF, que não sofreu alteração no número de municípios.,
qtde_mesma_uf_soma_area = df_reg_mesmos_municipios.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF'])['AR_MUN_2018'].sum().reset_index()
plan_qtde_mesma_uf_soma_area_maiores = qtde_mesma_uf_soma_area.sort_values('AR_MUN_2018', ascending=False).head()

# 6) As 5 Menores regioes de saude em extensão territorial, por UF,  que não sofreu alteração no número de municípios.,
plan_qtde_mesma_uf_soma_area_menores = qtde_mesma_uf_soma_area.sort_values('AR_MUN_2018', ascending=True).head()

# ====================================================
def divide_colunas(df_sub):
    return df_sub['POPULACAO'].astype(float).sum() / df_sub['AR_MUN_2018'].astype(float).sum()

qtde_mesma_uf_media_densidade = df_reg_mesmos_municipios.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF']).apply(divide_colunas).reset_index() # média
qtde_mesma_uf_media_densidade.columns
qtde_mesma_uf_media_densidade.rename(columns={0:'DENSIDADE'}, inplace=True)
# 7) As 5 Maiores regioes de saude em densidade demografica, por UF, que não sofreram alteração no número de municípios.
plan_qtde_mesma_uf_media_densidade_maiores = qtde_mesma_uf_media_densidade.sort_values('DENSIDADE', ascending=False).head()

# 8) As 5 Menores regioes de saude em densidade demografica, por UF, que não sofreram alteração no número de municípios.
plan_qtde_mesma_uf_media_densidade_menores = qtde_mesma_uf_media_densidade.sort_values('DENSIDADE', ascending=True).head()


# =====================================
# 3) Quantitativo de regioes que tiveram alteracoes:
df_diferencas = df_final[df_final['flag_atual']==1]  # SELECAO
df_diferencas.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF']).count() # 281 regioes de saude que foram alteradas. Otica Regiao Atual (2018). PARA ESTATISTICA: 281 REGIOES DE SAUDE QUE SOFRERAM ALTERACOES
df_diferencas.groupby(['NM_REGIAO_SAUDE_ANTERIOR', 'SG_UF']).count() # 201 regioes de saude que foram alteradas. Otica Regiao Atual (2018). Ok 155 REGIOES SEM ALTERACAO
# 4) Quantidade de municipios envolvidos nas regioes onde não teve alteração
df_diferencas.shape # (3402, 21)


# 5) As 5 Maiores regioes de saude em extensão territorial, por UF, que sofreu alteração no número de municípios.,
qtde_diferenca_uf_soma_area = df_diferencas.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF'])['AR_MUN_2018'].sum().reset_index()
plan_qtde_diferenca_uf_soma_area_maiores = qtde_diferenca_uf_soma_area.sort_values('AR_MUN_2018', ascending=False).head()

# 6) As 5 Menores regioes de saude em extensão territorial, por UF,  que sofreu alteração no número de municípios.,
plan_qtde_diferenca_uf_soma_area_menores = qtde_diferenca_uf_soma_area.sort_values('AR_MUN_2018', ascending=True).head()

# ====================================================
qtde_diferenca_uf_media_densidade = df_diferencas.groupby(['NM_REGIAO_SAUDE_ATUAL', 'SG_UF']).apply(divide_colunas).reset_index() # média
qtde_diferenca_uf_media_densidade.columns
qtde_diferenca_uf_media_densidade.rename(columns={0:'DENSIDADE'}, inplace=True)
# 7) As 5 Maiores regioes de saude em densidade demografica, por UF, que sofreram alteração no número de municípios.
plan_qtde_diferenca_uf_media_densidade_maiores = qtde_diferenca_uf_media_densidade.sort_values('DENSIDADE', ascending=False).head()

# 8) As 5 Menores regioes de saude em densidade demografica, por UF, que sofreram alteração no número de municípios.
plan_qtde_diferenca_uf_media_densidade_menores = qtde_diferenca_uf_media_densidade.sort_values('DENSIDADE', ascending=True).head()


# Regiao com a maior quantidade de hospitais


# Regiao com a menor quantidade de hospitais


# Regiao com a maior quantidade de servicos de urgencia e emergencia


# Regiao com a menor quantidade de servicos de urgencia e emergencia

# Obs: verificação de um erro no código: df_regioes_concat['flag_municipio_entrou'] = df_regioes_concat['lista_regiao_atual'].map(set) - df_regioes_concat['lista_regiao_anterior'].map(set)
df_final[df_final['NM_REGIAO_SAUDE_ANTERIOR'].isnull()]
df_final.info()
# Deletar o municipios 4300002 (LAGOA DOS PATOS) e 4300001 (LAGOA MIRIM), pois são municipios criados pos arquivo de 2018. Municipios criados no final de 2018
# df_final = df_final.drop('SG_UF', axis=0)
# Alternativa ao drop e mais rápido:
df_final.drop(df_final[(df_final['CD_GC_MUN'] == '4300002') | (df_final['CD_GC_MUN'] == '4300001')].index, inplace=True)

# bacalhau: correção da linha do Municipio: Mojui dos Campos. Pertence ao BAixo Amazonas. Então, copiar o vetor de qualquer municipio desta regiao
# PAREI AQUI


df_final.sort_values('SG_UF', ascending=True, inplace=True)
# instrucao para preencher o dataframe, na coluna lista_regiao_anterior com uma lista vazia, porque nao havia municipios em 2011, comparado com 2018
for row in df_final.loc[df_final['lista_regiao_anterior'].isnull(), 'lista_regiao_anterior'].index:
    df_final.at[row, 'lista_regiao_anterior'] = []

# testes
df_final[df_final['lista_regiao_anterior'].isnull()]
df_final[df_final['lista_regiao_atual'].isnull()]
df_final[df_final['NM_REGIAO_SAUDE_ATUAL']=='Baixo Acre e Purus']
df_final[df_final['NM_REGIAO_SAUDE_ATUAL']=='Norte']

# AJUSTAR O DATAFRAME==========================DF_REGIOES_CONCAT PARA  DF_REGIAO_FINAL # SELECAO
# diferenca das listas de municipios entre a lista atual e anterior, dentro do escopo de cada municipio, como instancia
df_final['flag_municipio_entrou'] = df_final['lista_regiao_atual'].map(set) - df_final['lista_regiao_anterior'].map(set)
df_final['flag_municipio_saiu'] = df_final['lista_regiao_anterior'].map(set) - df_final['lista_regiao_atual'].map(set)


# Quantidades:
df_final['cont_municipio_entrou'] = [len(x) for x in df_final['flag_municipio_entrou']]
df_final['cont_municipio_saiu'] = [len(x) for x in df_final['flag_municipio_saiu']]

# Testes de consistencia
df_final[(df_final['flag_atual']==0)&(df_final['cont_municipio_entrou']>1)] # OK
df_final[(df_final['flag_atual']==0)&(df_final['cont_municipio_saiu']>1)]  # OK


df_estatistica_entrada = df_final[(df_final['flag_atual']==1)&(df_final['cont_municipio_entrou']!=0)]
df_estatistica_entrada.shape # (1330, 25)

df_result_atual = df_estatistica_entrada.groupby(['SG_UF','NM_REGIAO_SAUDE_ATUAL'])['cont_municipio_entrou', 'cont_municipio_saiu'].agg(['count','min','max','mean']).reset_index()
df_result_atual  # 89 ROWS X 10 COLUMNS

df_result_anterior = df_estatistica_entrada.groupby(['SG_UF','NM_REGIAO_SAUDE_ANTERIOR'])['cont_municipio_entrou', 'cont_municipio_saiu'].agg(['count','min','max','mean']).reset_index()
df_result_anterior.head()


# Resultados para excel (gerencial)

# Create a Pandas Excel writer 
with pd.ExcelWriter('/home/doug/Documentos/Programas python/Regioes_Saude/Resumo_demanda_Ops_326305.xlsx') as writer:
    lista1.to_excel(writer, sheet_name='lista1')
    lista2.to_excel(writer, sheet_name='lista2')
    linhas_duplicadas.to_excel(writer, sheet_name='linhas_duplicadas')
    df_unicos.to_excel(writer, sheet_name='unicos')
    df_final.to_excel(writer, sheet_name='final')
    df_reg_mesmos_municipios.to_excel(writer, sheet_name='df_reg_mesmos_municipios')
    qtde_mesma_uf_soma_area.to_excel(writer, sheet_name='qtde_mesma_uf_soma_area')
    plan_qtde_mesma_uf_soma_area_maiores.to_excel(writer, sheet_name='qtde_mesma_uf_soma_area_ma')
    plan_qtde_mesma_uf_soma_area_menores.to_excel(writer, sheet_name='qtde_mesma_uf_soma_area_me')
    qtde_mesma_uf_media_densidade.to_excel(writer, sheet_name='qtde_mesma_uf_media_densidade')
    plan_qtde_mesma_uf_media_densidade_maiores.to_excel(writer, sheet_name='uf_media_dens_ma')
    plan_qtde_mesma_uf_media_densidade_menores.to_excel(writer, sheet_name='uf_media_dens_me')
    df_diferencas.to_excel(writer, sheet_name='df_diferencas')
    qtde_diferenca_uf_soma_area.to_excel(writer, sheet_name='qtde_diferenca_uf_soma_area')
    plan_qtde_diferenca_uf_soma_area_maiores.to_excel(writer, sheet_name='diferenca_uf_soma_area_ma')
    plan_qtde_diferenca_uf_soma_area_menores.to_excel(writer, sheet_name='diferenca_uf_soma_area_me')
    qtde_diferenca_uf_media_densidade.to_excel(writer, sheet_name='diferenca_uf_media_densidade')
    plan_qtde_diferenca_uf_media_densidade_maiores.to_excel(writer, sheet_name='diferenca_uf_media_dens_ma')
    plan_qtde_diferenca_uf_media_densidade_menores.to_excel(writer, sheet_name='diferenca_uf_media_dens_me')
    df_estatistica_entrada.to_excel(writer, sheet_name='df_estatistica_entrada')
    df_result_atual.to_excel(writer, sheet_name='df_result_atual')
    df_result_anterior.to_excel(writer, sheet_name='df_result_anterior')

 
# Close the Pandas Excel writer 
# object and output the Excel file. 
writer.save()
writer.close()


df_result_atual.to_excel('resultado_atual.xlsx')
df_result_anterior.to_excel('resultado_anterior.xlsx')
df_estatistica_entrada.to_excel('resumo_geral_movimentacao.xlsx')

# Sum list of values within a pandas df
# df = [sum(a) for a in zip(*df['Val'])]

# REmover caracteres com Regex
'''
# option 1 - faster way
df['team'] =  [re.sub(r'[\n\r]*','', str(x)) for x in df['team']]

# option 2
df['team'] =  df['team'].apply(lambda x: re.sub(r'[\n\r]*','', str(x)))
'''

'''
Now say you want each row to be divided by the sum of each group (e.g., the total sum of AZ) and also retain all the original columns. 
Just adjust the above function (change the calculation and return the whole sub dataframe):
def divide_two_cols(df_sub):
    df_sub['divs'] = df_sub['bene_1_count'] / float(df_sub['bene_2_count'].sum())
    return df_sub

df.groupby('state').apply(divide_two_cols)
'''