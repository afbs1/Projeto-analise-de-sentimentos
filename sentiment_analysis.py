###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Ayrton Fernando
#
# Email:    afbs@cin.ufpe.br
#            
#
# Data:        2016-06-10
#
# Descricao:  Este é um modelo de arquivo para ser utilizado para a implementacao
#                do projeto pratico da disciplina de Programacao 1. 
#                 A descricao do projeto encontra-se no site da disciplina e trata-se
#                de uma adaptacao do projeto disponivel em 
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#                O objetivo deste projeto é implementar um sistema de analise de
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#            Copyright(c) 2016 Ayrton Fernando
#
###############################################################################

import sys
import re

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        é mantida intacta.
    '''    
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result



def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' é uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' é uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))
                    


def readTrainingSet(fname):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''
    words = dict()
    a = open (fname, 'r')
    b = open ('stopwords.txt', 'r')

    stopwords = []
    for linha in b: 
        st = linha
        st = (clean_up(st))
        stopwords.append(st)
    #Limpando e separando a linha do trainSet em uma variável
    for linha in a:
        s = linha
        s = (clean_up(s))
        s = list(split_on_separators(s, ' '))
        nota = int(s.pop(0))
        #Aplicando stop words e salvando as palavras e notas
        for x in s:
            if x in stopwords:
                continue
            elif x in words:
                words[x] = [words[x][0] + 1, ((words[x][1] * words[x][0]) + nota) / (words[x][0] + 1)]
            elif x not in words:
                words[x] = [1, nota]
    b.close()
    a.close()
    return words

def readTestSet(fname):
    ''' Esta função lê o arquivo contendo o conjunto de teste
	    retorna um vetor/lista de pares (escore,texto) dos
	    comentarios presentes no arquivo.
    '''    
    reviews = []
    a = open (fname, 'r')
    b = open ('stopwords.txt', 'r')

    #Aplicando também as stop words e limpando
    stopwords = []
    for linha in b:
        st = linha
        st = (clean_up(st))
        stopwords.append(st)
    #Percorrendo a linha, isolando a nota e juntando a string sem as stop words    
    for linha in a:
        s = linha
        s = (clean_up(s))
        s = list(split_on_separators(s, ' '))
        nota = int(s.pop(0))
        s = ' '.join([x for x in s if x not in stopwords])
        reviews.append((nota, s))

    b.close()
    a.close()   
    return reviews

def computeSentiment(review,words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario é a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore é 2.
        Review é a parte textual de um comentario.
        Words é o dicionário com as palavras e seus escores médios no conjunto
        de treinamento.
    '''
    score = 0.0
    count = 0.0
    #Separando as palavras, procurando e atribuindo seus valores de acordo com o que foi aprendido
    review = review.split(' ')
    count = len(review)
    for x in review:
        if x in words:
            score = score + words[x][1]
        elif x not in words:
            score = score + 2
            
    return score/count

def computeSumSquaredErrors(reviews,words):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario é obtido com a
        funcao computeSentiment. 
        Reviews é um vetor de pares (escore,texto)
        Words é um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''    
    sse = 0.0
    soma = []
    #Calculando o SSE utilizando os parametros e a função computeSentiment()
    for pos in range(len(reviews)):
        dif = ((computeSentiment(reviews[pos][1], words)) - float(reviews[pos][0])) **2
        soma.append(dif)
    sse = (sum(soma))/(len(reviews))
    return sse

    
def main():
    
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (é parte do
    # projeto).
    
    # A ordem dos parametros é a seguinte: o primeiro é o nome do arquivo
    # com o conjunto de treinamento, em seguida o arquivo do conjunto de teste.
    
    if len(sys.argv) < 3:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        sys.exit(0)
    else:
        # Lendo conjunto de treinamento e computando escore das palavras
        words = readTrainingSet(sys.argv[1])
        
        # Lendo conjunto de teste
        reviews = readTestSet(sys.argv[2])
        
        # Inferindo sentimento e computando soma dos quadrados dos erros
        sse = computeSumSquaredErrors(reviews,words)
        
        print ('A soma do quadrado dos erros é: {0}'.format(sse))
        ex = input('Pressione enter para finalizar.')

if __name__ == '__main__':
    main()
    
    
