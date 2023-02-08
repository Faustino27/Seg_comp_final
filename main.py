import base64
import hashlib
import sys
from rsa import RSA
from oaep import OAEP

def main(args):
    if len(args) < 1:
        print("Nenhum arquivo selecionado")
        exit(1)

    #simulando criptografia da mensagem

    faustino = RSA()
    enzo = RSA()
    faustinoCript= cript(faustino, args[0])
    input(f'Arquivo ~~{args[0]}~~ foi criptografado, pressione enter para continuar')

    decript(faustino, faustinoCript, args[0])
    # if(len(args) > 1):
    #     enzoCript = cript(enzo, args[1])
    #     decript(enzo, enzoCript)
    




def cript(rsa, fileName):
    oaep = OAEP(1024)
    #le a mensagem
    with open(fileName, 'rb') as f:
        file = f.read()
    
    #faz o hash da mensagem
    fileHashClaro = hashlib.sha3_256(file).digest().hex()
    
    #print(f'A mensagem lida foi: \n',file.decode('utf-8'))
    print("O hash da mensagem é: ", fileHashClaro)

    #oaep do hash
    oaepCript = oaep.oaep(int(fileHashClaro, 16))
    print("OAEP do hash: ",oaepCript[0])

    #rsa do resultado do oaep
    hashCifrado = rsa.encryptPublic(int(oaepCript[0]))
    print("Hash cifrado com RSA: ", hashCifrado)

    #cria os arquivos bin
    fileHash64 = base64.b64encode(hashCifrado.to_bytes(calc_num_bytes(hashCifrado), 'big'))
    fileMensagem64 = base64.b64encode(file)
    name = fileName.split(".")[0]
    with open(name +'hash.bin', 'wb') as f:
        f.write(fileHash64)
    with open(name +'message.bin', 'wb') as f:
        f.write(fileMensagem64)
    

    return oaep, oaepCript[1]


def decript(rsa, data, fileName):
    # rsa, oaep, size, file
    name = fileName.split(".")[0]

    #abrimos o hash e o arquivo e decodificamos a base 64
    with open(name+'hash.bin', 'rb') as f:
        hashReceived = base64.b64decode(f.read())
    with open(name+'message.bin', 'rb') as f:
        messageReceived = base64.b64decode(f.read())

    with open('messageDeciphered.bin', 'wb') as f:
        f.write(messageReceived)
    #remove a criptografia rsa
    descifrado = rsa.decryptPrivate(int.from_bytes(hashReceived, 'big'))
    print("RSA REVERSO: ", descifrado)

    #remove os bits inúteis adicionados pelo rsa
    oaepDecript = data[0].reverseOaep(descifrado, data[1])
    print("OAEP REVERSO: ",hex(oaepDecript))
    hashMensagem = int(hashlib.sha3_256(messageReceived).digest().hex(),16)
    oaepDecript = int(oaepDecript)

    if checkHash(hashMensagem, oaepDecript):
        print("Os hash são iguais")
    else:
        print("Os hashs são diferentes")
        print(f"O hash obtido da mensagem foi {hashMensagem} e o hash enviado foi {oaepDecript}")
        print("SUBTRAÇÃO: ", hashMensagem - oaepDecript)

def calc_num_bytes(n: int):
    cnt = 0 
    while n != 0:
        n >>= 8
        cnt += 1
    return cnt


def checkHash(hashGiven, hashMade):
    if(hashMade - hashGiven == 0):
        return True
    return False

main(sys.argv[1:])