import Crypto
import os
import binascii
from dotenv import load_dotenv
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# randomGenerator=  Crypto.Random.new().read
# privateKey=RSA.generate(1024,randomGenerator)
# publicKey=privateKey.public_key()

# privateKey=privateKey.exportKey(format='DER')
# publicKey=publicKey.exportKey(format='DER')

# privateKey=binascii.hexlify(privateKey).decode('utf-8')
# publicKey=binascii.hexlify(publicKey).decode('utf-8')
# print(privateKey)
# print(publicKey)

load_dotenv()

# print(os.getenv('privateKey'))
# print(os.getenv('publicKey'))

privateKey=RSA.import_key(binascii.unhexlify(os.getenv('privateKey')))
publicKey=RSA.import_key(binascii.unhexlify(os.getenv('publicKey')))

mensajeU="DanielEncript"
mensajeU=mensajeU.encode('utf-8')

cipher=PKCS1_OAEP.new(publicKey)
encripU=cipher.encrypt(mensajeU)
print("<<Usuario>>")
print(str(encripU))

mensajeC="a1e2i3o4u56a"
mensajeC=mensajeC.encode('utf-8')

encripC=cipher.encrypt(mensajeC)

print("<<Contraseña>>")
print(str(encripC))

# cipher=PKCS1_OAEP.new(privateKey)
# mensaje=cipher.decrypt(encripM)

# print(mensaje)
