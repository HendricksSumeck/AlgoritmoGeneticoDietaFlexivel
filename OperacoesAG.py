# -*- coding: utf-8 -*-
import numpy as np
import random as rand

#%% zeros
rand.seed(None)

def zeros (tam):
    lista = []
    for i in range(0, tam):
        lista.append(0)
    return lista

#%% ini_ExponentialRanking
def ini_ExponentialRanking(c, qtd_ind):

    k = (c - 1.0) / (c ** qtd_ind - 1.0)
    S_tmp =  zeros (qtd_ind)

    i = 1
    S_tmp[i - 1] = k * pow(c, qtd_ind - i)

    for i in range(2, qtd_ind + 1):
        S_tmp[i - 1] = S_tmp[i - 2] + k * c ** (qtd_ind - i)

    diff1 =  (S_tmp[1] - S_tmp[0]) /  2.0
    diff2 =  (S_tmp[qtd_ind - 1] - S_tmp[qtd_ind - 2]) /  2.0
    minimo = S_tmp[0]
    maximo = S_tmp[qtd_ind - 1]
    a = (( 1.0 -  diff1 -  diff2) / (maximo -  minimo))
    b = (diff1 -  a *  minimo)

    a =  a * 32767.0
    b =  b * 32767.0

    for i in range(0, qtd_ind):
        S_tmp[i] = np.round(a * S_tmp[i] +  b)

    return S_tmp

#%% ini_LinearRanking
def ini_LinearRanking(tx_rep_pior, qtd_ind):

    tx_rep_melhor = 2 - tx_rep_pior
    S_tmp =  zeros (qtd_ind)

    i = 1
    S_tmp[i - 1] = (1.0 / qtd_ind) * (tx_rep_pior + (tx_rep_melhor - tx_rep_pior) * (i - 1) / (qtd_ind - 1))

    for i in range(2, qtd_ind + 1):
        S_tmp[i - 1] = S_tmp[i - 2] + ( 1.0 / qtd_ind) * (tx_rep_pior + (tx_rep_melhor - tx_rep_pior) * (i - 1) / (qtd_ind - 1))

    diff1 =  (S_tmp[1] - S_tmp[0]) /  2.0
    diff2 =  (S_tmp[qtd_ind - 1] - S_tmp[qtd_ind - 2]) /  2.0
    minimo = S_tmp[0]
    maximo = S_tmp[qtd_ind - 1]
    a = (( 1.0 -  diff1 -  diff2) / ( maximo -  minimo))
    b = ( diff1 -  a *  minimo)

    a =  a *  32767.0;
    b =  b *  32767.0;

    for i in range(0, qtd_ind):
        S_tmp[i] = np.round(a *  S_tmp[i] +  b)

    return S_tmp

#%% gera_populacao
def gera_populacao (qtd_ind, tam_dna, lim_sup, lim_inf):

    fitness = zeros(qtd_ind)
    dna = []
    for i in range(0, qtd_ind):
        dna_org = []
        for j in range(0, tam_dna):
             valor = (lim_sup[j] - lim_inf[j]) * (rand.randint(0, 32767) / 32767.0) + lim_inf[j]
             dna_org.append(valor)
        dna.append(dna_org)
    org = {'dna' : dna, 'fitness' : fitness}
    return org


#%% avaliacao da dieta flexivel
def avaliacao_dieta_flexivel (org, qtd_ind, tam_dna, individuos_salvos, alimentosKcal, alimentosProteina, alimentosGordura, alimentosCarboidratos):
    retorno = 0

    for i in range(0, qtd_ind - individuos_salvos):
        org['fitness'][i] = definicao_problema_dieta_flexivel(org['dna'][i], tam_dna, alimentosKcal, alimentosProteina, alimentosGordura, alimentosCarboidratos)

    return retorno


#%% definicao_problema da dieta flexivel
def definicao_problema_dieta_flexivel(dna, tam_dna, kcal, pro, gor, car):
    calorias = 0
    proteinas = 0
    gordura = 0
    carbo = 0
    soma = 0
    
    for i in range(0, len(dna)):
        calorias += dna[i] / kcal[i] / 100
        proteinas += dna[i] / pro[i]
        gordura += dna[i] / gor[i]
        carbo += dna[i] / car[i]
        
        soma += dna[i] * kcal[i] / 100
        
        if calorias > 3196: # Passou o numero de calorias maximas
            soma = soma / calorias
        if proteinas > 240: # Passou o numero de proteinas maximas
            soma = soma / proteinas
        if gordura > 124: # Passou o numero de gordura maximas
            soma = soma / gordura
        if carbo > 280: # Passou o numero de carbo maximas
            soma = soma / carbo
            
    return soma

#%% ordena
def ordena(org, ordem):
    idx_fit = np.argsort(org['fitness'])
    fitness = zeros(len(org['fitness']))
    dna = zeros(len(org['fitness']))
    for i in range(0, len(org['fitness'])):
        fitness[i] = org['fitness'][idx_fit[i]]
        dna[i] = org['dna'][idx_fit[i]]
    if ordem == 'minimizacao':
        dna = dna[::-1]
        fitness = fitness[::-1]
    org2 = {'dna' : dna, 'fitness' : fitness}
    return org2

#%% RankingSelection
def RankingSelection  (S_selection, qtd_ind):
    return buscabinaria(rand.randint(0, 32767), qtd_ind, S_selection)

#%% buscabinaria
def buscabinaria(x, n, v):
    inicio = 0
    fim = n - 1
    while fim - inicio != 1:
        meio = np.int32((inicio + fim)/2)
        if v[meio] < x :
            inicio = meio
        else:
            fim = meio

    if abs(v[inicio] - x) < abs(v[fim] - x):
        meio = inicio
    else:
        meio = fim

    return meio

#%% cruzamento
def cruzamento (Origem, Destino, pai, mae, filho, tam_dna):
    B = rand.randint(0, 32767) / 32767.0

    for i in range(0, tam_dna):
        Destino['dna'][filho][i] = B * Origem['dna'][mae][i] + (1.0 - B) * Origem['dna'][pai][i]

#%% mutacao
def mutacao (org, individuo, tam_dna, lim_sup, lim_inf, geracao, geracoes, b, prob_mutacao):

    for gene in range(0, tam_dna):
        if rand.uniform(0, 100) <= prob_mutacao:
            if rand.randint(0,1) == 0:
                org['dna'][individuo][gene] += delta_mut(geracao, lim_sup[gene] - org['dna'][individuo][gene], geracoes, b)
            else:
                org['dna'][individuo][gene] -= delta_mut(geracao, org['dna'][individuo][gene] - lim_inf[gene], geracoes, b)

#%% delta_mut
def delta_mut (t, y, T, b):
    r = rand.randint(0, 32767) / 32767.0

    vlinha = y * (1 - r**((1 - t / T)*b))

    return vlinha
