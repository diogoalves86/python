#!/usr/bin/python
#-*-coding=utf8-*-

__author__ = 'Diogo Alves'
__description__ = "Este script foi criado com o intuito de facilitar e automatizar algumas tarefas diárias minhas (Diogo Alves)"

import subprocess, os, argparse, sys

class Automatizer:
    def altera_comando(self, novoValor):
        self.comando = novoValor

    def executa_comando(self, comando):
        self.comando = comando
        processo = subprocess.check_output([self.comando], shell=True)
        return processo

    def processa_texto_por_string(self, stringPesquisada):
        arquivos = []
        textoParcial = self.processo
        #Lógica para a identificação de todos os arquivos modificados
        for i in range(0, self.processo.count(stringPesquisada)):
            indice = textoParcial.find(stringPesquisada)
            textoParcial = textoParcial[indice:]
            nomeArquivo = textoParcial[len(stringPesquisada):]
            nomeArquivo = nomeArquivo[1:nomeArquivo.index("\n")]
            textoParcial = textoParcial[textoParcial.index(nomeArquivo):]
            arquivos.append(nomeArquivo)
        return arquivos

    def verifica_antes_commitar(self):
        self.arquivos = self.processa_texto_por_string("modified:  ")
        for arquivo in self.arquivos:
            print("Processando arquivo: %s" % arquivo)
            self.processo = self.executa_comando("git diff %s" % arquivo)
            if self.processo == "":
                self.processo = self.executa_comando("git diff --cached %s" % arquivo)

            if "var_dump(" in self.processo:
                print("Foi detectado um var_dump() no seu código!")
                print("Estas alterações ainda não foram salvas, atente-se para alterá-las antes de commitar!")
                print("Arquivo onde foi encontrado o erro %s" % arquivo)
                print("COMANDO DIGITADO: \"%s\". OUTPUT SEGUE ABAIXO: \n" % self.comando)
                os.system(self.comando)
                print("--------------------------------------------------------------------------------------------------------------------------")
                sys.exit(1)
            else:
                print("Arquivo %s OK!" % arquivo)

    def verifica_commit(self):
        if "var_dump(" in self.processo:
            print("Foi detectado uma função var_dump() no seu ultimo commit.")
            print("""Atente-se para corrigi-lo! Segue abaixo o commit para verificar e corrigir.
            Commit Hash: %s
                  """ % self.commitHash)
            os.system(self.comando + self.commitHash)
            print("--------------------------------------------------------------------------------------------------------------------------")
            sys.exit(1)
        else:
            print("O seu código não apresenta var_dump()")

    def var_dump_finder(self):
        self.processo = self.executa_comando("git status")
        self.verifica_antes_commitar()
        self.processo = self.executa_comando("git show")
        self.commitHash = self.processo[7:48]
        self.processo = self.executa_comando("git diff --cached")
        self.processo = self.executa_comando("git show %s" % self.commitHash)
        self.verifica_commit()

    def personareportal_git_master_update(self, novoBranch=None):
        self.executa_comando("cd ~/devel/personare/portal/workcopy")
        print("Acessando diretório WorkCopy Personare...")
        self.executa_comando("git checkout master")
        print("Fazendo checkout para o branch \"master\"...")
        self.executa_comando("git fetch")
        print("Fazendo o fetch para pegar os novos branchs criados")
        self.executa_comando("git pull origin master")
        print("Fazendo pull da última versão do branch \"master\"...")
        if novoBranch != None:
            self.executa_comando("git checkout -b %s" % novoBranch)
        print("Todos os passos foram realizados com sucesso, até mais!")

class Cliente:
    def __init__(self):
        parse = argparse.ArgumentParser(prog="Automatizer",
                                        description="Esse é o aplicativo automatizador de tarefas",
                                        usage="python ./automatizer.py [OPTIONS]")
        parse.add_argument("--varDumpFinder", help="Verifica ocorrências de var_dump no código", action="store", type=bool, required=False)
        parse.add_argument("--gitPersonarePortal", help="Acessa o branch master e faz o pull dele.", action="store", type=bool, required=False)
        self.args = parse.parse_args()
        self.automatizer = Automatizer()

    def processa_requesicao(self):
        if self.args.varDumpFinder == True:
            self.automatizer.var_dump_finder()
        if self.args.gitPersonarePortal == True :
            self.automatizer.personareportal_git_master_update()

programa = Cliente()
programa.processa_requesicao()