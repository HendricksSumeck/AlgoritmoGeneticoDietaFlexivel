# -*- coding: utf-8 -*-
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import copy

import OperacoesAG as ag
rand.seed(None)

alimentos = ['Arroz', "Ovo", "Frango", "Batata doce"]
alimentosKcal = [128, 240, 163, 77]
alimentosProteina = [2, 15, 31, 1]
alimentosGordura = [1, 18, 3, 1]
alimentosCarboidratos = [28, 1, 1, 18]

#%% Inicializacao do Algoritmo Genetico
tam_dna = 4
qtd_ind = 100
geracoes = 2000
prob_mutacao = 3
amp_mut = 0.5
individuos_salvos = 2
tipo = 'maximizacao' # maximizacao ou minimizacao

#%% Definicao dos limites
lim_sup = [10589,8687,12398,8912,11424,10654,13957,19904,11535]
lim_inf = [0,0,0,0,0,0,0,0,0]

#%%# Vetor de probabilidade
# S_selection = ini_LinearRanking(0, qtd_ind); % inicializar vetor de probabilidades
S_selection = ag.ini_ExponentialRanking(0.97, qtd_ind)

#%% Avaliacao da populacao inicial
org = ag.gera_populacao (qtd_ind, tam_dna, lim_sup, lim_inf)
retorno = ag.avaliacao_dieta_flexivel (org, qtd_ind, tam_dna, individuos_salvos, alimentosKcal, alimentosProteina, alimentosGordura, alimentosCarboidratos)
org = ag.ordena(org, tipo)
print('best fit: ', org['fitness'][-1])

def dna2imagem(dna, forma):
    imagem = np.zeros(forma)

    u = 0
    for i in range(forma[0]):
        for j in range(forma[1]):
            for k in range(forma[2]):
                imagem[i][j][k] = dna[u]
                u += 1

    return imagem


#%% Loop do Genético
melhor = org['fitness'][-1]

for geracao in range(0, geracoes):
    org2 = copy.deepcopy(org)

    for filho in range(0, qtd_ind - individuos_salvos):
        pai = ag.RankingSelection(S_selection, qtd_ind)
        mae = ag.RankingSelection(S_selection, qtd_ind)
        ag.cruzamento(org2, org, pai, mae, filho, tam_dna)

        ag.mutacao(org, filho, tam_dna, lim_sup, lim_inf, geracao, geracoes, amp_mut, prob_mutacao)

    retorno = ag.avaliacao_dieta_flexivel (org, qtd_ind, tam_dna, individuos_salvos, alimentosKcal, alimentosProteina, alimentosGordura, alimentosCarboidratos)
    org = ag.ordena(org, tipo)

    print('Geração: ', geracao ,' best fit: ', org['fitness'][-1])

print("fim")

#%% print
dna_best = org['dna'][-1]
melhor = org['fitness'][-1]

calorias = 0
proteinas = 0
gordura = 0
carbo = 0
for i in range(0, len(dna_best)):
    calorias += dna_best[i] / alimentosKcal[i]
    proteinas += dna_best[i] / alimentosProteina[i]
    gordura += dna_best[i] / alimentosGordura[i]
    carbo += dna_best[i] / alimentosCarboidratos[i]
    print('%.1f\tg de %s' %(dna_best[i], alimentos[i]))

print('Calorias: %.1f gramas' %calorias)
print('Proteinas: %.1f gramas' %proteinas)
print('Gordura: %.1f gramas' %gordura)
print('Carbo: %.1f gramas' %carbo)

print('Total de calorias: %.1f kcal' %melhor)
