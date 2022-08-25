# -*- coding: utf-8 -*-

"""

Created on Mon May 23 19:39:03 2022

@author: luan.magalhaes

"""

########################################### GERACAO MAILILNG CHURN ##############################################

# LENDO BIBLIOTECAS
import mysql.connector as sql # CONEXAO BANCO DE DADOS
import pandas as pd # PANDAS
import re # ALGUMAS FORMULAS USADAS NA VALIDACAO DE TELEFONE
import numpy as np # NUMPY
from pathlib import Path
from datetime import datetime


# LENDO BASE CHURN
base_churn = pd.read_excel('P:/magnos/Churn/historico_churn/ChurnAgosto.xlsx')


############################# CRIANDO CONEXAO COM O BANCO DE DADOS ADAPTER
db_connection = sql.connect(host = '192.168.30.63', 
                            database = 'master_adapter_comercial', 
                            user = 'luan.magalhaes',
                            passwd = 'C@D8nSQx')

# CRIANDO BASE DE CPF
base_cpf = pd.read_sql(
""" SELECT DISTINCT 
cli.Nome,
cli.IDCliente,
(CASE
WHEN cli.CPF IS NULL THEN cli.CNPJ ELSE cli.CPF END) AS CPF2,
cli.TelefoneFixo,
cli.TelefoneMovel
FROM master_adapter_comercial.TB_Cliente cli
WHERE cli.IDCliente in %s """ % str(tuple(list(base_churn['IDCliente'].drop_duplicates()))), con=db_connection)

# https://discuss.dizzycoding.com/passing-a-list-of-values-from-python-to-the-in-clause-of-an-sql-query/

# CRIANDO BASE DE PAGAMENTOS
base_pagamentos = pd.read_sql(
""" SELECT DISTINCT
(CASE
WHEN fatm.IDContrato IS NULL THEN fatp.IDContrato ELSE fatm.IDContrato END) AS IDContratoCompleto,
fat.IDCliente,
fat.IDFatura,
fat.DataPagamento AS DataPagamentoFatura,
fat.ValorPago,
1 AS FLAG_PAGO
FROM master_adapter_financeiro.TB_Fatura fat
LEFT JOIN master_adapter_comercial.TB_Cliente cli ON fat.IDCliente = cli.IDCliente
LEFT JOIN master_adapter_financeiro.TB_FaturamentoMes fatm ON fat.IDFatura = fatm.IDFatura
LEFT JOIN master_adapter_financeiro.TB_FaturaParcelamento fatp ON fat.IDFatura = fatp.IDFatura 
WHERE DATEDIFF(CURDATE(), DATE(DataPagamento))<=20 AND fat.DataPagamento IS NOT NULL """, con=db_connection)

base_pagamentos.rename(columns = {'IDContratoCompleto':'IDContrato'}, inplace = True) # Renomeando IDContrato

# CRIANDO BASE PARA PEGAR STATUS DE CONTRATO
base_contrato = pd.read_sql(
""" SELECT
crt.IDContrato,
tsc.IDStatusContrato,
tsc.DescricaoStatusContrato,
DATE(crt.DataCancelamentoContrato) AS DataCancelamentoAtual
FROM master_adapter_comercial.TB_Contrato crt
LEFT JOIN master_adapter_comercial.TB_StatusContrato tsc ON crt.IDStatusContrato = tsc.IDStatusContrato
WHERE crt.IDContrato IN %s """ % str(tuple(list(base_churn['IDContrato'].drop_duplicates()))), con=db_connection)


# CRIANDO BASE PARA PEGAR STATUS DE CONTRATO
base_idfatura = pd.read_sql(
""" SELECT
IDFatura,
Valor
FROM master_adapter_financeiro.TB_Fatura
WHERE Valor >0
AND IDFatura IN %s """ % str(tuple(list(base_churn['IDFatura'].drop_duplicates()))), con=db_connection)


## Trazendo VALOR para a base original LEFT JOIN
 
base_churn = pd.merge(base_churn,
                     base_idfatura,
                     on='IDFatura',
                     how='left') 



base_cpf.rename(columns = {'CPF2':'CPF'},
                inplace = True) # Renomeando CPF

## Trazendo cpf para a base original LEFT JOIN 
validacao = pd.merge(base_churn,
                     base_cpf,
                     on='IDCliente',
                     how='left') 

# Trazendo pagamentos para a base pelo IDFATURA

## LEFT JOIN PARA TRAZER PAGOS
validacao = pd.merge(validacao,
                     base_pagamentos.drop(["IDCliente","IDContrato"], axis=1), # RETIRANDO IDS PARA NAO GERAR DUPLICIDADE
                     on='IDFatura',how='left')

# Retirando clientes pagos

validacao = validacao[validacao['FLAG_PAGO'].isna()] ## FILTRANDO CLIENTES SEM PAGAMENTO

validacao = validacao.drop(columns=["FLAG_PAGO",
                                    "ValorPago",
                                    "DataPagamentoFatura"]) ## REMOVENDO COLUNAS

##################### Trazendo pagamentos para a base e retirando pagos pelo IDCONTRATO

# FILTRANDO PAGAMENTO NOS ULTIMOS DIAS
base_pagamentos = base_pagamentos[(pd.to_datetime("today").date() - base_pagamentos["DataPagamentoFatura"]).dt.days<=20]

base_pagamentos[['IDContrato','FLAG_PAGO']].drop_duplicates() # SELECIONANDO IDCliente e Fatura e retirando distintos

## LEFT JOIN PARA TRAZER PAGOS
validacao = pd.merge(validacao,
base_pagamentos[['IDContrato','FLAG_PAGO']].drop_duplicates(),
on='IDContrato',how='left')

validacao = validacao[validacao['FLAG_PAGO'].isna()] # DEIXANDO APENAS CLIENTES QUE NAO PAGARAM NA BASE

validacao = validacao.drop(["FLAG_PAGO"], axis=1) # RETIRANDO COLUNA FLAG PAGO


# ACIONANDO ZEROS PARA PREENCHER 14 DIGITOS NO CPF
validacao["CPF"] = validacao["CPF"].str.zfill(14) # https://stackoverflow.com/questions/23836277/add-leading-zeros-to-strings-in-pandas-dataframe


# UNINDO TELEFONE FIXO E MOVEL EM UMA SO COLUNA
validacao = validacao.reset_index()

#validacao.columns

validacao = pd.melt(validacao,
                      id_vars=['IDContrato',
                               'IDCliente',
                               'IDContrato2',
                               'IDFatura',
                               'DataVencimento',
                               'DataPagamento',
                               'DiasVencimento',
                               'dataAte',
                               'DataCancel',
                               'Nome',
                               'CPF',
                               'Valor'], value_vars=['TelefoneFixo','TelefoneMovel'])

# Renomeando TELEFONE
validacao.rename(columns = {'value':'contato',
                            'variable':'campo_telefone_sistema'}, inplace = True)


# EXCLUINDO COLUNA DE TIPO DE TELEFONE PARA DEPOIS RETIRAR LINHAS DUPLICADAS
# del validacao["campo_telefone_sistema"]

validacao = validacao.drop(["campo_telefone_sistema"], axis=1)

validacao = validacao.drop_duplicates() # RETIRANDO TODOS OS DUPLICADOS


validacao['contato'] =validacao['contato'].astype({'contato':'string'}) # CONVERTENDO COLUNA DE TELEFONE EM STRING

# REMOÇÃO DE LETRAS E ESPAÇOS (APENAS NÚMEROS) ------------------------------------------
validacao['fone'] = validacao['contato'].str.extract('(\d*\.*\d*)?$').astype(str).replace('\.','', regex=True)


validacao['fone'] = np.where(validacao['fone'].str.slice(2, 3)==0,
                                    validacao['fone'].str.slice(0, 2)+validacao['fone'].str.slice(3, 11),
                                    validacao['fone'])

# CONTANDO QUANTIDADE DE CARACTERES 
validacao['tamanho_tel'] = validacao.fone.astype(str).str.len()


# CRIANDO VALIDACAO PELOS CARACTERES
validacao['TIPO_FONE'] = np.where(
    (validacao['tamanho_tel'] ==11) &
    (validacao['fone'].str.slice(3, 4).isin(["2","3","4","5","6","7","8","9"])== True) &
    (validacao['fone'].str.slice(2, 3).isin(["9"])== True ),'CELULAR',
    ## SEGUNDA REGRA
    np.where((validacao['tamanho_tel'] ==10) & (validacao['fone'].str.slice(2, 3).isin(["6","7","8","9"]) == True),"CELULAR",
    ## TERCEIRA REGRA
    np.where((validacao['tamanho_tel'] ==10) & (validacao['fone'].str.slice(2, 3).isin(["0","6","7","8","9"]) == False),"FIXO","INVALIDO")))

# ACIONANDO 9 DIGITO PARA CELULAR
validacao['fone'] = np.where((validacao['tamanho_tel'] <=10) &
                              (validacao['TIPO_FONE']=='CELULAR'),validacao['fone'].str.slice(0, 2)+"9"+validacao['fone'].str.slice(2, 11),validacao['fone'])

# IDENTIFICANDO TELEFONES COM NÚMEROS REPETIDOS
validacao['TIPO_FONE'] = np.where((validacao['fone'].str.contains('|'.join(['000000','111111','222222',
                                                                            '333333','444444','555555',
                                                                            '666666','777777','888888','999999'])))==True,'INVALIDO',validacao['TIPO_FONE'])

# SELECIONANDO APENAS DDD VÁLIDOS

validacao['TIPO_FONE'] = np.where((validacao['fone'].str.slice(0, 2).isin(["11","12","13","14","15","16","17","18","19","21","22","24","27","28","31","32","33","34","35","37", "38","41","42","43","44","45","46","47","48","49","51","53","54","55","61","62","63","64","65","66","67","68","69","71","73","74","75","77","79","81","82","83","84","85","86","87","88","89","91","92","93","94","95","96","97","98","99"]))==True,
                                  validacao['TIPO_FONE'],
                                  "INVALIDO")

validacao = validacao[validacao['TIPO_FONE']!='INVALIDO'] # RETIRANDO TELEFONES INVALIDOS

validacao = validacao.drop(["tamanho_tel","TIPO_FONE"], axis=1) # RETIRANDO COLUNAS


################################################## LENDO ACIONAMENTOS OLOS #############################################

# PEGANDO CAMINHO COM ARQUIVOS CSV
p = Path(r'Z:/Relatório Olos/Dump_TabAuto/2022/02')

# FILTRANDO ARQUIVOS CSV
all_files = p.glob('*.txt')

df = pd.DataFrame({'files' : all_files})

# ADICIONANDO DATA DE MODIFICACAO DOS ARQUIVOS
df['date'] = pd.to_datetime(df['files'].apply(lambda x : x.stat().st_mtime),unit='s')

# FILTRANDO DATA PARA LER ARQUIVOS
trg_files = df[df['date'] >= pd.Timestamp('now') - pd.DateOffset(days=7)]['files'].tolist()

# LENDO ARQUIVOS
dfs = [pd.read_table((f), delimiter ="|", encoding= 'unicode_escape', low_memory=False) for f in trg_files]

# CONCATENANDO A LISTA EM UM ÚNICO DATAFRAME
dump_olos = pd.concat(dfs) #, axis = 1)

dump_olos['Telefone'] = dump_olos['DDD'].astype('str')+dump_olos['Telefone'].astype('str') # Using Series.astype() to convert column to string 

dump_olos = dump_olos.drop(['Organizacao','IdCLiente','DispositionId','Rota','DDD'], axis=1) # REMOVENDO COLUNAS

# Lendo de para
de_x_para = pd.read_excel('P:/magnos/PLANILHAS_COBRANCA/OLOS_DE_PARA.xlsx')

## LEFT JOIN PARA TRAZER REPIQUE
dump_olos = pd.merge(dump_olos,
de_x_para[['Status','REPIQUE']],
on='Status',how='left')

dump_olos["DataHora"] = pd.to_datetime(dump_olos["DataHora"]).dt.date # CONVERTENDO COLUNA DE DATA 

# 1 dia
repique_d1 = dump_olos[dump_olos['REPIQUE']=='D+1']
repique_d1 = repique_d1[(pd.to_datetime("today").date() - repique_d1["DataHora"]).dt.days<=1]

# 2 dias
repique_d2 = dump_olos[dump_olos['REPIQUE']=='D+2']
repique_d2 = repique_d2[(pd.to_datetime("today").date() - repique_d2["DataHora"]).dt.days<=2]

# 5 dias
repique_d5 = dump_olos[dump_olos['REPIQUE']=='D+5']
repique_d5 = repique_d5[(pd.to_datetime("today").date() - repique_d5["DataHora"]).dt.days<=7]

# 30 dias
#repique_d30 = dump_olos[dump_olos['REPIQUE']=='D+30']
#repique_d30 = repique_d30[(pd.to_datetime("today").date() - repique_d30["DataHora"]).dt.days<=30]

base_para_retirar = pd.concat([repique_d1, repique_d2,repique_d5
                               #,repique_d30
                               ]) # UNINDO BASES

# ACIONANDO ZEROS PARA PREENCHER 14 DIGITOS NO CPF
base_para_retirar["CPF"] = base_para_retirar["CPF"].str.zfill(14) # https://stackoverflow.com/questions/23836277/add-leading-zeros-to-strings-in-pandas-dataframe

################################ Group by para pegar cpfs 
base_para_retirar_cpf = base_para_retirar.groupby(['CPF']).agg(
    ULTIMA_NEGOCIACAO = ('DataHora', 'max'))

# JOIN PARA TRAZER FLAG DE RETIRADA DE REPIQUE
validacao = pd.merge(validacao,
base_para_retirar_cpf,
on='CPF',how='left')

validacao = validacao[validacao['ULTIMA_NEGOCIACAO'].isna()] #RETIRANDO REPIQUE

validacao = validacao.drop(["ULTIMA_NEGOCIACAO"], axis=1) # RETIRANDO COLUNA FLAG


#### RETIRANDO PELO TELEFONE

################################ Group by para pegar cpfs 

# Renomeando TELEFONE
base_para_retirar.rename(columns = {'Telefone':'fone'}, inplace = True)

# AGRUPANDO BASE PELO TELEFONE
base_para_retirar_telefone = base_para_retirar.groupby(['fone']).agg(
    ULTIMA_NEGOCIACAO = ('DataHora', 'max'))

# JOIN PARA TRAZER FLAG DE RETIRADA DE REPIQUE
validacao = pd.merge(validacao,
base_para_retirar_telefone,
on='fone',how='left')

validacao = validacao[validacao['ULTIMA_NEGOCIACAO'].isna()] #RETIRANDO REPIQUE

validacao = validacao.drop(["ULTIMA_NEGOCIACAO"], axis=1) # RETIRANDO COLUNA FLAG


################################################## LENDO ACIONAMENTOS ACTYON #############################################

# PEGANDO CAMINHO COM ARQUIVOS CSV
p = Path(r'Z:/Relatorios/Historico Actyon/2022')

# FILTRANDO ARQUIVOS CSV
all_files = p.glob("./**/*.csv")

df = pd.DataFrame({'files' : all_files})

# ADICIONANDO DATA DE MODIFICACAO DOS ARQUIVOS
df['date'] = pd.to_datetime(df['files'].apply(lambda x : x.stat().st_mtime),unit='s')

# FILTRANDO DATA PARA LER ARQUIVOS
trg_files = df[df['date'] >= pd.Timestamp('now') - pd.DateOffset(days=10)]['files'].tolist()

# LENDO ARQUIVOS
dfs = [pd.read_table((f), delimiter =";",encoding="ISO-8859-1") for f in trg_files]


# CONCATENANDO A LISTA EM UM ÚNICO DATAFRAME
acionamentos_para_retirar = pd.concat(dfs) #, axis = 1)

# Lendo de para
de_x_para = pd.read_excel('P:/magnos/PLANILHAS_COBRANCA/de_para_mob.xlsx')

## LEFT JOIN PARA TRAZER REPIQUE
acionamentos_para_retirar = pd.merge(acionamentos_para_retirar,
de_x_para[['ACIONAMENTO','REPIQUE']],
on='ACIONAMENTO',how='left')

# CONVERTENDO DATA
acionamentos_para_retirar['DATA_INCLUSAO'] = pd.to_datetime(acionamentos_para_retirar['DATA_INCLUSAO'], format='%d/%m/%Y %H:%M:%S') 

acionamentos_para_retirar['DATA_INCLUSAO'] = pd.to_datetime(acionamentos_para_retirar['DATA_INCLUSAO']).dt.date # CONVERTENDO COLUNA DE DATA 

# 1 dia
repique_d1 = acionamentos_para_retirar[acionamentos_para_retirar['REPIQUE']=='D+1']
repique_d1 = repique_d1[(pd.to_datetime("today").date() - repique_d1['DATA_INCLUSAO']).dt.days<=2]

# 2 dias
repique_d2 = acionamentos_para_retirar[acionamentos_para_retirar['REPIQUE']=='D+2']
repique_d2 = repique_d2[(pd.to_datetime("today").date() - repique_d2['DATA_INCLUSAO']).dt.days<=4]

# 5 dias
repique_d5 = acionamentos_para_retirar[acionamentos_para_retirar['REPIQUE']=='D+5']
repique_d5 = repique_d5[(pd.to_datetime("today").date() - repique_d5['DATA_INCLUSAO']).dt.days<=7]


# 30 dias
#repique_d30 = acionamentos_para_retirar[acionamentos_para_retirar['REPIQUE']=='D+30']
#repique_d30 = repique_d30[(pd.to_datetime("today").date() - repique_d30['DATA_INCLUSAO']).dt.days<=30]


base_para_retirar = pd.concat([repique_d1, repique_d2,repique_d5
                               #,repique_d30
                               ]) # UNINDO BASES

# ACIONANDO ZEROS PARA PREENCHER 14 DIGITOS NO CPF

base_para_retirar["CPF"] = base_para_retirar["CPF"].values.astype(str)

base_para_retirar["CPF"] = base_para_retirar["CPF"].str.zfill(14) # https://stackoverflow.com/questions/23836277/add-leading-zeros-to-strings-in-pandas-dataframe


################################ Group by para pegar cpfs 
base_para_retirar = base_para_retirar.groupby(['CPF']).agg(
    ULTIMA_NEGOCIACAO = ('DATA_INCLUSAO', 'max'))


# JOIN PARA TRAZER FLAG DE RETIRADA DE REPIQUE
validacao = pd.merge(validacao,
base_para_retirar,
on='CPF',how='left')

validacao = validacao[validacao['ULTIMA_NEGOCIACAO'].isna()] #RETIRANDO REPIQUE

validacao = validacao.drop(["ULTIMA_NEGOCIACAO"], axis=1) # RETIRANDO COLUNA FLAG

# JOIN PARA TRAZER STATUS ATUAL DE CONTRATO
validacao = pd.merge(validacao,
base_contrato,
on='IDContrato',how='left')

validacao['DataCancelamentoAtual'] = pd.to_datetime(validacao['DataCancelamentoAtual'], format='%Y-%m-%d') # TRATANDO COLUNA DE DATA
#join PARA TRAZER COLUNA PONTUAÇÃO

########################################### FILTRANDO BASE APTA PARA COBRANCA ####################################
##################################################################################################################


# FILTRAR PREVISAO DE CANCELAMENTO
validacao = validacao[(validacao['DataCancel'] >= pd.to_datetime('2022-07-01', format='%Y-%m-%d')) & # INICIAL
                      (validacao['DataCancel'] <= pd.to_datetime('2022-08-31', format='%Y-%m-%d'))] # FINAL


 
 # FILTRAR DATA DE CANCELAMENTO ATUAL
date = pd.to_datetime('2022-07-20', format='%Y-%m-%d')

churn_nao_cancelado = validacao[(validacao['DataCancelamentoAtual'].isna())]  # FILTRANDO CHURN NAO CANCELADO

churn_cancelado = validacao[(validacao['DataCancelamentoAtual'].notnull())] # FILTRANDO CHURN CANCELADO

churn_cancelado = churn_cancelado[(churn_cancelado['DataCancelamentoAtual'] >= date)] # FILTRANDO CHURN CANCELADO PELA DATA DE CANCELAMENTO

validacao = pd.concat([churn_nao_cancelado,churn_cancelado]) # UNINDO BASE CANCELADA E NAO CANCELADA

validacao = validacao.drop(["contato"], axis=1) # RETIRANDO TELEFONE



"""
##################################################################################################################

CAMPO AJUSTADO PARA RETIRAR DUPLICIDADE DE FATURAS

##################################################################################################################

"""


################################ Group by para pegar cpfs 
validacao = pd.merge(
validacao,
validacao.groupby(['IDContrato']).agg(
    max_cancelamento = ('DataCancel', 'max')),
on = 'IDContrato',
how = 'left')

validacao = validacao[validacao['DataCancel']==validacao['max_cancelamento']]


# RETIRANDO CLIENTES DUPLICADOS
validacao['teste'] = validacao.groupby(['IDCliente','IDContrato','CPF','fone']).cumcount()+1 # ADICIONANDO COLUNA COM CONTADOR

validacao = validacao[validacao['teste']==1]



"""
##################################################################################################################

CAMPO AJUSTADO PARA RETIRAR DUPLICIDADE DE FATURAS

##################################################################################################################

"""



# CRIANDO FAIXA DE  TELEFONE

validacao['teste'] = validacao.groupby(['IDCliente','IDContrato','CPF']).cumcount()+1 # ADICIONANDO COLUNA COM CONTADOR

validacao['campo_telefone'] = np.where(validacao['teste']==1,'TelefoneFixo','TelefoneMovel')

validacao = validacao.drop(["teste","max_cancelamento"], axis=1) # RETIRANDO COLUNA DE TESTE




# TRANSPONDO LINHA DE TELEFONES EM COLUNAS
validacao = validacao.pivot(index=['IDContrato',
 'IDCliente',
 'IDContrato2',
 'IDFatura',
 'DataVencimento',
 'DataPagamento',
 'DiasVencimento',
 'dataAte',
 'DataCancel',
 'Nome',
 'CPF',
 'IDStatusContrato',
 'DescricaoStatusContrato',
 'DataCancelamentoAtual',
 'Valor'], columns='campo_telefone', values='fone').reset_index()


# RETIRANDO CLIENTES DUPLICADOS (DEIXANDO FATURAS DIFERENTES NA BASE)
validacao['teste'] = validacao.groupby(['IDCliente','CPF']).cumcount()+1 # ADICIONANDO COLUNA COM CONTADOR

validacao = validacao[validacao['teste']==1] # FILTRANDO LINHAS UNICAS

validacao = validacao.drop(["teste"], axis=1) # RETIRANDO COLUNA DE TESTE

# ZERANDO TELEFONES REPETIDOS NA COLUNA TELEFONE MOVEL
validacao['TelefoneMovel'] = np.where(validacao['TelefoneFixo']==validacao['TelefoneMovel'],np.nan,validacao['TelefoneMovel'])




# LENDO PONTUACAO

base_pontuacao = pd.read_csv('Z:/1. PONTUACAO DE TELEFONES/PONTUACAO_TELEFONES.csv', on_bad_lines='skip',sep=";")



################################ Group by para pegar cpfs 
base_pontuacao_resumo = base_pontuacao.groupby(['IDCliente']).agg(
    PONTUACAO_MAXIMA = ('PONTUACAO', 'max'))


# JOIN PARA PEGAR PONTUACAO
validacao = pd.merge(validacao,
base_pontuacao_resumo,
on='IDCliente',how='left')


#################################### CRIANDO LAYOUT EAGLE ##########################################



# CRIANDO COLUNAS PARA GERAR LAYOUT

validacao['E_mail'] = ''
validacao['Cidade'] = ''
validacao['UF'] = ''
validacao['Faixa_Atr'] = ''
validacao['Numero_de_telefone_2'] = ''
validacao['Telefone_3'] = ''
validacao['Telefone_4'] = ''
validacao['Numero_de_Parcelas'] = 1
validacao['ID_PAR_02'] = ''
validacao['ID_PAR_03'] = ''
validacao['Valor_PAR_01'] = validacao['Valor'] 
validacao['Valor_PAR_02'] = ''
validacao['Valor_PAR_03'] = ''
validacao['Data_Vcto_PAR_02'] = ''
validacao['Data_Vcto_PAR_03'] = ''
validacao['Produto'] = ''
validacao['CUSTOMER_ID'] = validacao['IDCliente']
validacao['Field_24'] = validacao['PONTUACAO_MAXIMA']

# RENOMEANDO ALGUMAS COLUNAS
validacao.rename(columns = {'CPF':'CPF_CNPJ',
                            'TelefoneFixo':'Numero_de_Telefone',
                            'TelefoneMovel':'Numero_de_Celular',
                            'IDFatura':'ID_PAR_01',
                            'DataVencimento':'Data_Vcto_PAR_01',
                            'Valor':'Valor_em_aberto'}, inplace = True) # Renomeando Colunas


validacao = validacao.drop(["PONTUACAO_MAXIMA"], axis=1)


# CRIANDO BASE FINAL PARA EXPORTACAO
base_eagle = validacao[['Nome',
                    'CPF_CNPJ',
                    'E_mail',
                    'Cidade',
                    'UF',                    
                    'Numero_de_Telefone',
                    'Numero_de_Celular',
                    'Numero_de_telefone_2',
                    'Telefone_3',
                    'Telefone_4',
                    'IDCliente',
                    'Numero_de_Parcelas',
                    'Faixa_Atr',
                    'Produto',
                    'Valor_em_aberto',
                    'ID_PAR_01',
                    'Valor_PAR_01',
                    'Data_Vcto_PAR_01',
                    'ID_PAR_02',
                    'Valor_PAR_02',
                    'Data_Vcto_PAR_02',
                    'ID_PAR_03',
                    'Valor_PAR_03',
                    'Data_Vcto_PAR_03',
                    'CUSTOMER_ID',
                    'Field_24']]



# CRIANDO FLAG COM DATA DO DIA PARA ADICIONAR NO ARQUIVO EXPORTADO
currentdate = datetime.now().strftime("%Y%m%d")

# EXPORTANDO ARQUIVO TXT
base_eagle.to_csv('Z:/MAILINGS/MAILING_CHURN/2022/MAILING_CHURN_{}.txt'.format(currentdate), header=True, index=None, sep=';', mode='w')