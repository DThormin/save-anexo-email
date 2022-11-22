import imaplib
import email
import os
import base64

#Conectar ao servidor de email Gmail com IMAP
objCon = imaplib.IMAP4_SSL("imap.gmail.com")

# login e senha da caixa de email
login = "email@gmail.com"
senha = "12345xxxx"

conexao = objCon.login(login,senha)

# Ler caixa de enrrada
objCon.select(mailbox='inbox', readonly=True)
resposta,idDosEmails = objCon.search(None, 'All')

#decodificando o email e jogando em uma variável
for num in idDosEmails[0].split():
    resultado,dados = objCon.fetch(num,'(RFC822)')
    texto_do_email = dados[0][1]
    texto_do_email = texto_do_email.decode('utf-8')
    texto_do_email = email.message_from_string(texto_do_email)
    #print(texto_do_email)
    #dividindo as partes
    for part in texto_do_email.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('content-Disposition') is None:
            continue
        #pegar arquivo com nome em anexo
        fileName = part.get_filename()
        #criar arquivo com o mesmo nome na pasta local
        arquivo = open(fileName,'wb')
        #escrever o binario do anexo no arquivo
        arquivo.write(part.get_payload(decode=True))
        arquivo.close()

