import os
import sys

local_arq_genomas = sys.argv[1]
arquivo_genomas = open(local_arq_genomas, "r")

# Forca utilizacao de arquivo com extensao '.list' para evitar conflito 
    # entre possíveis arquivos do tipo '.txt', '.fna', '.tab', '.out' etc.
extensao_arq_entrada = local_arq_genomas[-5:]
if extensao_arq_entrada != ".list":
    print("Arquivo de entrada deve ser '.list' para evitar conflito com outros arquivos nas operações com 'mv' ! ")
    sys.exit()

# Gera um nome para o arquivo basedo no caminho(string) passado
# Pega substring começando do fim da string até a primeira '/' -> EX: '/usr/GCF003.fna' -> 'GCF003.fna'
# Importante que não tenha o caracter '/' no fim do caminho do arquivo -> EX: '/usr/GCF003.fna/' -> error
def GerarNomeArquivo(string):
    indice_final = len(string) - 1
    indice = indice_final
    aux = 0
    while string[indice] != "/" and indice >= 0:
        aux += 1
        indice -= 1
    
    indice_inicial = indice_final-aux+1
    sub_string = string[indice_inicial:indice_final+1]
    return sub_string

# INICIAR -------------------------------------------------------------------
# Para cada linha do arquivo de genomas de entrada
for linha in arquivo_genomas:
    linha = linha.replace("\n", "")
    if len(linha) > 0:
        nome_genoma = GerarNomeArquivo(linha)
        print("\n-> Carregando: "+nome_genoma)
        os.system("python3 main.py "+linha)

        # -> gera nome do genoma 
        # -> cria pasta baseado no nome 
        # -> move todos os artefatos de saída para a pasta criada
        os.system("mkdir "+nome_genoma)
        os.system("mv *.out *.tab *.masked *.tbl *.log *.txt "+nome_genoma)
        print(" --------- ")

# --------------------------------------------------------------------------