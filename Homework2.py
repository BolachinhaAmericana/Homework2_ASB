'''
IPS-ESTB
Segundo Ano, Segundo Semestre
Licenciatura em Bioinformatica
Maio 2022

UC: ASB
Docente: Francisco Pina Martins
Homework #2
Realizado por: 

Duarte Valente
Goncalo Alves
Pedro Peixoto
Joao Yanga
'''


import sys

'''
Variaveis que vao guardar os valores do STDIN.
'''
fileName = sys.argv[1]
ngen= sys.argv[2]
outG= sys.argv[3]

'''
Funcao lambda para executar o valor do nome do ficheiro.
Para um ficheiro (x)
'''
inputFile = lambda x : open("{}".format(x))




def seqFastaEnterRemover():
    '''
    Esta funcao serve para trabalhar com o ficheiro fasta inicial
    para que fique mais facil trabalhar em funcoes futuras.

    Esta a mudar a maneira como as sequencias do fasta ficam apresentadas, 
    ao inves da sequencias estar apresentada em multiplas linhas passa a estar apenas numa.
    '''
    noenter = ''
    for lines in inputFile(fileName):
        lines = lines.removesuffix('\n')
        if '>' in lines:
            noenter = noenter+'\n'+lines+'\n'
            
        else:
            noenter = noenter + lines
    return noenter

def getAccnList():
    '''
    Vai Criar uma lista com todos os nomes/referencias das sequencias.
    Obtem-se estes valores ao criar uma lista apenas
    com as linhas do ficheiro fasta formatado pela funcao "seqFastaRemover()"
    que tenham o caracter ">".
    '''
    accnList = []
    for line in seqFastaEnterRemover().split('\n'):
        if '>' in line:
            line = line.removeprefix('>')
            if len(line) > 99:
                Error='Error, Sequences References Can not Have More Then 99 Characters!!!'
                return Error
            else:
                accnList.append(line)
    return accnList

def getSeqList():
    '''
    Vai Criar uma lista com todas as sequencias.
    Obtem-se estes valores ao criar uma lista apenas
    com as linhas do ficheiro fasta formatado pela funcao "seqFastaRemover()"
    que nao tenham o caracter ">".
    '''
    seqList = []
    for line in seqFastaEnterRemover().split('\n'):
        if '>' not in line:
            nchar = len(line)
            seqList.append(line)
    return seqList

'''
Com os valores das funcoes definidas anteriormente, fomos determinar o numero de caracteres que cada
sequencia tem assim como o numero de taxas do nosso ficheiro input.
'''
nchar = len(getSeqList()[1])
ntax = len(getAccnList())
'''
Aqui criamos um dicionario com as chaves sendo as referencias as sequencias que extraimos com a funcao
"getAccnList()" e os valores sendo as sequencias.
'''
Dictitems = zip(getAccnList(), getSeqList()[1:])
setDict = lambda x : dict(x)

def formatNexusText():
    '''
    Esta Funcao tem como objetivo preparar todo o formato NEXUS e ajustar o mesmo
    com todos os valores obtidos anteriormente, sendo eles de input ou de retorno de alguma
    funcao anteriormente executada.
    '''

    print("""
#NEXUS

BEGIN DATA;
DIMENSIONS NTAX={} NCHAR= {} ;
FORMAT DATATYPE=DNA MISSING=N GAP=-;
MATRIX
""".format(ntax, nchar))
    for keys, item in setDict(Dictitems).items() or setDict(Dictitems).keys():
        print("     {}  {}".format(keys, item))
    print("""  ;
END;
""")

    print("""begin mrbayes;
set autoclose=yes;
outgroup={};
mcmcp ngen={} printfreq=1000 samplefreq=100 diagnfreq=1000 nchains=4 savebrlens=yes filename={};
mcmc;
sumt filename={};
end;
""".format(outG, ngen, fileName[:7], fileName[:7]))

formatNexusText()
