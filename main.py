# -*- coding: utf-8 -*-
from os import system
from datetime import datetime
import os.path
import sys
import modulos

#definição de cor para erro
VERMELHO   = "\033[1;31m"
NORMAL = "\033[0;0m"

# carrega as configurações
#configuração do RepeatMasker
#parametros=["/usr/local/RepeatMasker/RepeatMasker -dir . -species Human -e rmblast -pa","null"] 

# Gera um nome para o arquivo basedo no caminho(string) passado
# Pega substring começando do fim da string até a primeira '/' -> EX: '/usr/GCF003.fna' -> 'GCF003.fna'
# Importante que não tenha o caracter '/' no fim do caminho do arquivo -> EX: '/usr/GCF003.fna/' -> error
# Aqui eh util para gerar arquivo de log basedo no nome
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

nome_arquivo = GerarNomeArquivo(sys.argv[1])
print("\tNome do Genoma: "+nome_arquivo)

#inicia o arquivo de logs
str_log = "./log_"+nome_arquivo+".log"
arquivo=open(str_log,'a')
horario=datetime.now().strftime('%d/%m/%y   %H:%M')
arquivo.write('Inicio: '+horario+'\n') # grava a hora de inicio da Análise no log

local_genoma = sys.argv[1] #pega o nome do arquivo pasado como segundo argumento
print("\tLocal do Genoma: "+local_genoma)
caminho=sys.argv[0]

genoma = nome_arquivo

parametros= modulos.carregarConfig(caminho)

# faz a verificação do tipo de arquivo que será análisado(fasta ou fna)
print("Genoma [-3]: "+genoma[-3])
if genoma[-3]=="f":
	saida=genoma.replace('.fna','')
elif genoma[-3]=="s":
	saida=genoma.replace('.fasta','')
else:
	print(VERMELHO+"ERRO!\nTipo de Arquivo Inválido\n"+NORMAL)
	exit()

print("\tNome p. Saidas: "+saida)

#verifica se o arquivo tabular do genoma já existe
arquivoTab=os.path.exists('./'+saida+".tab")
opcao=0
if (arquivoTab):
	# print('arquivo ' +genoma+' tabular já existe \nQuer pular a Análise do RepeatMasker? \n S ou N?')
	# opcao=input()
	opcao = 'n'
# refaz a análise (por escolha do usuário)
if (opcao == 'n' or opcao ==  'N'):
	# numero_proc= input("Digite o Numero de Processadores que Será Usado;\n")
	""" tenta chamar o programa REpeatMasker 
	se estiver tudo certo ele vai fazer os demais processos
		*nota01 parametros["programa"] é a primeira linha do arquivo configuracao.conf 
		 que contem o caminho do RepeatMasker
		 *nota02 parametros["email"] é a segunda linha do arquivo configuracao.conf 
		 que contem o Email que vai ser enviado os alertas """
	numero_proc = 8
	try:
		print("\tComando 1: "+parametros["programa"]+" "+ numero_proc+" -s "+local_genoma)
		system(parametros["programa"]+" "+ str(numero_proc)+" -s "+local_genoma) # *nota01		

		if(os.path.exists('./'+genoma+".out")):
			print("\tComando 2: "+"awk -v OFS='\t' '$1=$1' "+genoma+".out > "+saida+".tab")
			system("awk -v OFS='\t' '$1=$1' "+genoma+".out > "+saida+".tab") # transforma a saída em um arquivo tabular
			
			print("\tComando 3: "+"awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab")
			system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab") # cria um arquivo coma as colunas 10 e 11 da saída
			#modulos.enviar_email("Analise Finalizada",parametros[1]) # *nota 02
		else:
			exit()
	except:
		print(VERMELHO+"extp1: ERRO Na Analise do Arquivo: "+genoma+NORMAL) # mensagem de erro na tela	
		#modulos.enviar_email("ERRO na Analise do Arquivo: "+genoma,parametros[1]) # mensagem de erro no email
		exit() # é pra fechar o programa
	else:
		estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab") # faz a contagem e pré-estrutura os dados
		modulos.criar_txt2(estrutura,saida) # cria o arquivo de saida com os dados

elif(opcao == 's' or opcao ==  'S'):
	""" Faz os processos de estruturação dos dados caso já exista um arquivo tabular(Por escolha do Usuário) """
	print("\tComando 4: "+"awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab")
	system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab")

	estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab")
	modulos.criar_txt2(estrutura,saida ) 

else:
	"""execução padrão dos processos (quando não existe um arquivo tabular) """
	# numero_proc= input("Digite o Numero de Processadores que Será Usado;\n")
	numero_proc = 8
	try:
		print("\tComando 5: "+parametros["programa"]+" "+ numero_proc+" -s "+local_genoma)
		system(parametros["programa"]+" "+ str(numero_proc)+" -s "+local_genoma)

		if(os.path.exists('./'+genoma+".out")):
			print("\tComando 6: "+"awk -v OFS='\t' '$1=$1' "+genoma+".out > "+saida+".tab")
			system("awk -v OFS='\t' '$1=$1' "+genoma+".out > "+saida+".tab") # transforma a saída em um arquivo tabular

			print("\tComando 7: "+"awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab")
			system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab") # cria um arquivo coma as colunas 10 e 11 da saída
			#modulos.enviar_email("Analise Finalizada",parametros[1]) # *nota 02
		else:
			exit()
	except:
		print(VERMELHO+"extp2: ERRO Na Analise do Arquivo: "+genoma+NORMAL)	
		#modulos.enviar_email("ERRO na Analise do Arquivo: "+genoma,parametros[1])
		exit()
	else:
		estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab")
		modulos.criar_txt2(estrutura,saida)

modulos.removeLixo(saida,parametros["residuos"])
horario=datetime.now().strftime('%d/%m/%y   %H:%M') # Pega a hora do fim dos processos
arquivo.write('Fim: '+horario+'\n') # escreve no arquivo de log quando terminou os processos
arquivo.close() # fecha o arquivo de log