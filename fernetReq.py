from cryptography.fernet import Fernet

def Cripta(chiave, dato):
    dato = dato.encode('utf-8')
    f = Fernet(chiave)
    return f.encrypt(dato)

def Decripta(chiave, dato):
    f = Fernet(chiave)
    dato = f.decrypt(dato)
    return dato.decode('utf-8')


def GeneraKey():
    return Fernet.generate_key()

def LeggiKey(file):
    return file.read()