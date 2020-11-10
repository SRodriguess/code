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

#inicia o arquivo de logs
arquivo=open("./log",'a')
horario=datetime.now().strftime('%d/%m/%y   %H:%M')
arquivo.write('Inicio: '+horario+'\n') # grava a hora de inicio da Análise no log

genoma= sys.argv[1] #pega o nome do arquivo pasado como segundo argumento
caminho=sys.argv[0]

parametros= modulos.carregarConfig(caminho)

# faz a verificação do tipo de arquivo que será análisado(fasta ou fna)
if genoma[-3]=="f":
	saida=genoma.replace('.fna','')
elif genoma[-3]=="s":
	saida=genoma.replace('.fasta','')
else:
	print(VERMELHO+"ERRO!\nTipo de Arquivo Inválido\n"+NORMAL)
	exit()
#verifica se o arquivo tabular do genoma já existe
arquivoTab=os.path.exists('./'+saida+".tab")
opcao=0
if (arquivoTab):
	print('arquivo ' +genoma+' tabular já existe \nQuer pular a Análise do RepeatMasker? \n S ou N?')
	opcao=input()
# refaz a análise (por escolha do usuário)
if (opcao == 'n' or opcao ==  'N'):
	numero_proc= input("Digite o Numero de Processadores que Será Usado;\n")
	""" tenta chamar o programa REpeatMasker 
	se estiver tudo certo ele vai fazer os demais processos
		*nota01 parametros["programa"] é a primeira linha do arquivo configuracao.conf 
		 que contem o caminho do RepeatMasker
		 *nota02 parametros["email"] é a segunda linha do arquivo configuracao.conf 
		 que contem o Email que vai ser enviado os alertas """
	
	try:
		system(parametros["programa"]+" "+ numero_proc+" "+genoma) # *nota01
		if(os.path.exists('./'+genoma+".out")):
			system("awk -v OFS='\t' '$1=$1' "+genoma+".out > "+saida+".tab") # transforma a saída em um arquivo tabular
			system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab") # cria um arquivo coma as colunas 10 e 11 da saída
			#modulos.enviar_email("Analise Finalizada",parametros[1]) # *nota 02
		else:
			exit()
	except:
		print(VERMELHO+"ERRO Na Analise do Arquivo: "+genoma+NORMAL) # mensagem de erro na tela	
		#modulos.enviar_email("ERRO na Analise do Arquivo: "+genoma,parametros[1]) # mensagem de erro no email
		exit() # é pra fechar o programa
	else:
		estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab") # faz a contagem e pré-estrutura os dados
		modulos.criar_txt2(estrutura,saida) # cria o arquivo de saida com os dados

elif(opcao == 's' or opcao ==  'S'):
	""" Faz os processos de estruturação dos dados caso já exista um arquivo tabular(Por escolha do Usuário) """
	system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab")
	estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab")
	modulos.criar_txt2(estrutura,saida ) 

else:
	"""execução padrão dos processos (quando não existe um arquivo tabular) """
	numero_proc= input("Digite o Numero de Processadores que Será Usado;\n")
	try:
		system(parametros["programa"]+" "+ numero_proc+" "+genoma)
		if(os.path.exists('./'+genoma+".out")):
			system("awk -v OFS='\t' '$1=$1' "+genoma+".out > "+saida+".tab") # transforma a saída em um arquivo tabular
			system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab") # cria um arquivo coma as colunas 10 e 11 da saída
			#modulos.enviar_email("Analise Finalizada",parametros[1]) # *nota 02
		else:
			exit()
	except:
		print(VERMELHO+"ERRO Na Analise do Arquivo: "+genoma+NORMAL)	
		#modulos.enviar_email("ERRO na Analise do Arquivo: "+genoma,parametros[1])
		exit()
	else:
		estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab")
		modulos.criar_txt2(estrutura,saida)

modulos.removeLixo(saida,parametros["residuos"])
horario=datetime.now().strftime('%d/%m/%y   %H:%M') # Pega a hora do fim dos processos
arquivo.write('Fim: '+horario+'\n') # escreve no arquivo de log quando terminou os processos
arquivo.close() # fecha o arquivo de log
