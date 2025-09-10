import sys
from enum import Enum

class errorParsing(Enum):
    ERR_NO_HAY = 0
    ERR_CMD_NO_ENCONTRADO = 1
    ERR_MAL_ARG = 2
    ERR_TOKEN_PK_NO_ENCONTRADO = 3
    ERR_TOKEN_COMA_NO_ENCONTRADO = 4
    ERR_SIN_ESPACIO = 5
    ERR_CAR_NO_NUMERICO = 6
    ERR_LRECL_NO_ENCONTRADO = 7
    ERR_FK_NO_ENCONTRADO = 8
    ERR_REG_NO_ENCONTRADO = 9
    ERR_PK_MAL_LARGO = 10

class Rpar:
    def __init__(self):
        self.comando = None
        self.archivo = None
        self.pkpos = None
        self.pklen = None
        self.lrecl = None
        self.fkpos = None
        self.fklen = None
        self.fkArchivo = None
        self.registro = None
        self.pk = None

def main():
    args = sys.argv
    rpar = Rpar()
    resultado = parsing(rpar,len(args), args)
    if(resultado == errorParsing(0)):
        print("\nParsing exitoso\n")
        muestro_par(rpar)
    else:
        print(f"\nParsing con error: {resultado}: {errores[resultado.value]}\n")

def parsing(rpar, argc, argv):
    for comando in comandos:
        if(comando == argv[1]):
            rpar.comando = argv[1]
            resultado = comandos[argv[1]](rpar, argc, argv)
            return resultado
    return errorParsing(1)

def parsing_crear(rpar, argc, argv):

    # Validar cantidad de argumentos
    if( not(argc == 5 or argc == 6) ):
        return errorParsing(2)

    # Almacenar el nombre del archivo
    rpar.archivo = argv[2]

    # Validar token PK=
    tokenPK = argv[3][0:3]
    if(tokenPK != "PK="):
        return errorParsing(3)
    
    # Validar contenido de pk
    validarPk = parsing_num1num2(argv, 20)
    if(validarPk[2] != errorParsing(0)):
        return validarPk[2]
    
    # Almacenar contenido PK
    rpar.pkpos = validarPk[0]
    rpar.pklen = validarPk[1]

    # Validar argumento LRECL
    tokenLRECL = argv[4][0:6]
    if(tokenLRECL != "LRECL="):
        return errorParsing(7)
    
    # Validar que LRECL sea numero
    try:
        numero1 = argv[4][6:]
        if(len(numero1)<=20):
            rpar.lrecl = int(numero1)
        else:
            return errorParsing(5)
    except ValueError:
        return errorParsing(6)

    # Validar si hay FK
    if(argc == 6):
        tokenFK = argv[5][0:3]
        if(tokenFK != "FK="):
            return errorParsing(8)
        else:    
            validarFk = parsing_num1alfa2(argv, 20)
            if(validarFk[2] != errorParsing(0)):
                return validarFk[2]
            # Almacenar contenido FK
            rpar.fkpos = validarFk[0]
            rpar.fkArchivo = validarFk[1]

    # Validar PK con respecto a LRECL
    if(rpar.pklen > rpar.lrecl):
        return errorParsing(10)
    
    if( (rpar.pkpos + rpar.pklen) > (rpar.lrecl -1)):
        return errorParsing(10)

    return errorParsing(0)

def parsing_insertar(rpar, argc, argv):

    if(argc != 4):
        return errorParsing(2)

    rpar.archivo = argv[2]
    validarRegistro = argv[3][0:4]
    if(validarRegistro != "REG="):
        return errorParsing(9)

    rpar.registro = argv[3][4:]

    return errorParsing(0)

def parsing_borrar(rpar, argc, argv):
    
    if(argc != 4):
        return errorParsing(2)

    rpar.archivo = argv[2]
    validarPK = argv[3][0:3]
    if(validarPK != "PK="):
        return errorParsing(3)
    rpar.pk = argv[3][3:]

    return errorParsing(0)

def parsing_leer(rpar, argc, argv):
    return parsing_borrar(rpar, argc, argv)

def parsing_mostrar(rpar, argc, argv):

    if(argc != 3):
        return errorParsing(2)
    rpar.archivo = argv[2]
    return errorParsing(0)

def parsing_cambiar(rpar, argc, argv):

    if(argc != 5):
        return errorParsing(2)
    
    rpar.archivo = argv[2]

    validarPK = argv[3][0:3]
    if(validarPK != "PK="):
        return errorParsing(3)
    rpar.pk = argv[3][3:]

    validarRegistro = argv[4][0:4]
    if(validarRegistro != "REG="):
        return errorParsing(9)
    rpar.registro = argv[4][4:]

    return errorParsing(0)

def parsing_num1num2(argv, largo):

    # Validar que existe caracter ","
    lista = [None,None,None]
    indiceComa = argv[3].find(",")

    if(indiceComa == -1):
        lista[2] = errorParsing(4)
        return lista
    
    numero1 = argv[3][3:indiceComa]
    numero2 = argv[3][indiceComa+1:]

    # Validar largo de caracteres
    if(len(numero1) > largo):
        lista[2] = errorParsing(5)
        return lista
    if(len(numero2) > largo):
        lista[2] = errorParsing(5)
        return lista

    # Validar que sean numeros
    try:
        numero1 = int(numero1)
        numero2 = int(numero2)
        lista= [numero1,numero2,errorParsing(0)]
    except ValueError:
        lista[2] = errorParsing(6)
        return lista
    
    return lista

def parsing_num1alfa2(argv, largo):
    # Validar que existe caracter ","
    lista = [None,None,None]
    indiceComa = argv[5].find(",")

    if(indiceComa == -1):
        lista[2] = errorParsing(4)
        return lista
    
    numero1 = argv[5][3:indiceComa]
    alfa2 = argv[5][indiceComa+1:]

    # Validar largo de caracteres
    if(len(numero1) > largo):
        lista[2] = errorParsing(5)
        return lista
    if(len(alfa2) > largo):
        lista[2] = errorParsing(5)
        return lista

    # Validar numero1
    try:
        numero1 = int(numero1)
        lista= [numero1,alfa2,errorParsing(0)]
    except ValueError:
        lista[2] = errorParsing(6)
        return lista

    return lista

def muestro_par(rpar):
    print(f"Comando: {rpar.comando}\nArchivo: {rpar.archivo}\nPosicion PK: {rpar.pkpos}\nLargo PK: {rpar.pklen}\n")
    print(f"Largo registro: {rpar.lrecl}\nPosicion FK: {rpar.fkpos}\nLargo FK: {rpar.fklen}\n")
    print(f"FK apunta a {rpar.fkArchivo}\nRegistro: {rpar.registro}\n")
    print(f"Valor PK: {rpar.pk}\n")

comandos = {
    "crear": parsing_crear,
    "insertar": parsing_insertar,
    "borrar": parsing_borrar,
    "leer": parsing_leer,
    "mostrar": parsing_mostrar,
    "cambiar": parsing_cambiar,
}

errores = {
    None: None,
    1: "comando desconocido",
    2: "numero de argumentos de comando incorrecto",
    3: "token PK= no encontrado",
    4: "token coma de separacion no encontrado",
    5: "no hay espacio suficiente para almacenar numero",
    6: "se encontraron caracteres no numericos en donde deberia haber numeros",
    7: "token LRECL= no encontrado",
    8: "token FK= no encontrado",
    9: "token REG= no encontrado",
    10: "PK con largo incorrecto"
}

main()