from Carta import Carta
from Mazo import Mazo
from Jugador import Jugador
from IA import IA
from PAT import jugadaValida

import os

estado = True
update = False
turno = 0
tiro = ""

"""Funcion encarga de mostrar los detalles del juego en el formato CLI"""
def Draw(UNO,Tablero,IA,P1):
    #os.system("cls")

    global turno

    print("======================= U N O ! =========================")

    print("== Turno {}:  ==".format(turno))

    print("========  En la mesa... : ==========".format(Tablero.getName()))
    #print(Tablero.mano[len(Tablero.mano)-1].mostrar())
    Tablero.mostrarMano()
    print("\n")

    print("========  Cartas de {}:  ========".format(IA.getName()))
    IA.mostrarMano()
    print("\n")

    print("========  Cartas de {}:  ========".format(P1.getName()))
    P1.mostrarMano()
    print("\n")

    if(UNO):
        print("=================== CPU UNO ===================")

    print("\n")


    return 0

"""

Funcion encargada de coordinar el turno de la computadora
Requiere de parametros el objeto IA (jugador CPU), tablero donde se juega y el mazo de 
cartas todavia disponible

"""
def IAPiensa(IA,tablero, mazo):

    global turno
    global tiro

    #Empezamos checando que la carta jugada anteriormente no sea un comodin que salte el 
    #juego del CPU o lo haga tomar cartas
    if(tablero.getUltimaCarta().getEfecto()=="+2" and tiro=="jugador"):
        IA.tomarCarta(mazo)
        IA.tomarCarta(mazo)
        return 0

    elif(tablero.getPenultimaCarta().getEfecto()=="Comodin +4" and tiro=="jugador"):
        IA.tomarCarta(mazo)
        IA.tomarCarta(mazo)
        IA.tomarCarta(mazo)
        IA.tomarCarta(mazo)
        return 0

    elif(tablero.getUltimaCarta().getEfecto()=="Salto" and tiro=="jugador"):
        return 0

    elif(tablero.getUltimaCarta().getEfecto()=="Reversa" and tiro=="jugador"):
        return 0


    else:
        #Una vez checado que no hay comodin checamos si segun las ordenes de la computadora es conveniente dejar un
        #comodin +4 en caso de tenerlo
        carta = IA.ifDejaMasCuatro()
        if(carta[0]==False):

            #En caso de no dejar un +4 checamos lo mismo con un comodin de cambio de color
            carta = IA.ifDejaComodinColor()

            if(carta[0] == False):

                #Buscamos que el CPU deje una carta siguiendo las reglas del juego
                carta= IA.dejaCarta()
                #En caso de no tener una el CPU tomara una carta hatsa que la jugada ya sea valida
                while(carta==False):
                    print("IA TOMO UNA CARTA")
                    IA.tomarCarta(mazo)
                    IA.mostrarMano()
                    carta= IA.dejaCarta()
                tablero.recibeCarta(carta)
                print("Carta jugada = ",end="")
                carta.mostrar()

            else:

                #En caso de que si elejimos un comodin de cambio de color indicamos cual se jugo e indicamos a que color se cambio
                print("Carta jugada = ",end="")
                carta[0].mostrar()
                tablero.recibeCarta(carta[0])
                carta = Carta("",carta[1],"")
                tablero.recibeCarta(carta)
                print("Carta jugada = ",end="")
                carta.mostrar()

        else:

            #En caso de que si elejimos un comodin +4 indicamos cual se jugo e indicamos a que color se cambio
            print("Carta jugada = ",end="")
            carta[0].mostrar()
            tablero.recibeCarta(carta[0])
            nuevaCarta = Carta("",carta[1],"")
            tablero.recibeCarta(nuevaCarta)
            print("Carta jugada = ",end="")
            nuevaCarta.mostrar()
    tiro="IA"


"""

Funcion encargada de coordinar el turno del jugador
Requiere de parametros el objeto IA (jugador CPU), tablero donde se juega y el mazo de 
cartas todavia disponible

"""
def juegaJugador(jugador, tablero, mazo):

    global tiro

    #Empezamos checando que la carta jugada anteriormente no sea un comodin que salte el 
    #juego del jugador o lo haga tomar cartas
    if(tablero.getUltimaCarta().getEfecto()=="+2" and tiro=="IA"):
        for i in range(0,2):
            jugador.tomarCarta(mazo)
        return

    elif(tablero.getPenultimaCarta().getEfecto()=="Comodin +4" and tiro=="IA"):
        for i in range(0,4):
            jugador.tomarCarta(mazo)
        return

    elif(tablero.getUltimaCarta().getEfecto()=="Salto" and tiro=="IA"):
        return

    elif(tablero.getUltimaCarta().getEfecto()=="Reversa" and tiro=="IA"):
        return 0

    #En caso de que pueda jugar empezamos por preguntarle al usuario si quiere tomar una carta o jugar
    valido = False
    while(valido == False):
        P1.mostrarMano()
        yes = input("Va a tomar carta? [Y/n]\n$ ")
        carta = None
        #En caso de tomar una carta se repite el proceso hasta que el jugador deje una
        while(yes == "Y" or yes == "y"):
            jugador.tomarCarta(mazo)
            P1.mostrarMano()
            yes = input("Va a tomar carta? [Y/n]\n$ ")
    
        #En caso de no tomar carta se procede a que el usuario elija una
        jugador.mostrarMano()
        i = int(input("ingrese carta a dejar\n$ "))
        #Buscamos que el valor de indice ingresado exista
        if(i >= len(jugador.getMano())):
            print("Numero ingresado erroneo")
            juegaJugador(jugador, tablero, mazo)

        carta = jugador.getCarta(i)

        #Revisamos que no sea comodin la carta dejada, los comodines se pueden dejar sin importar del caso anterior
        if(carta.getEfecto() != "Comodin" and carta.getEfecto() != "Comodin +4" and tablero.getUltimaCarta() != "Comodin" and tablero.getUltimaCarta() != "Comodin +4"):
            #Mediante el metodo jugadaValida que implementa PAT checamos que sea valida
            valido = jugadaValida([tablero.getPenultimaCarta(),tablero.getUltimaCarta(),carta])
            print(valido)

            if(valido == False):
                print("Jugada invalida")

        else:
            valido = True


    #Ya que la jugada es valida la extraemos de la mano del usuario
    carta = jugador.dejaCarta(i)
    print(carta.toString())
    tablero.recibeCarta(carta)
    tiro="jugador"

    #En caso de haber dejado un comodin +4 o cambio de color le pedimos al usuario que indique a que color cambia
    if(carta.getEfecto()=="Comodin" or carta.getEfecto()=="Comodin +4"):
        print("Escoja el color de la siguiente carta")
        opciones = ["Azul","Rojo","Amarillo","Verde"]
        iter = 0
        for i in opciones:
            print(str(iter)+")"+ i)
            iter = iter + 1
        i = int(input("Ingrese numero correspondiente al color\n$ "))
        nuevaCarta = Carta("",opciones[i],"")
        tablero.recibeCarta(nuevaCarta)

while ( estado ):

    #Inicio del Juego
    if(turno == 0):
        #Se inicializan el mazo junto a los jugadores
        mazo = Mazo()
        P1 = Jugador("Pedrito")
        Tablero = Jugador("Tablero")
        IA = IA("PC",mazo,Tablero)

        #Se revuelve el mazo
        mazo.revolver()


        Tablero.tomarCarta(mazo)
        #Repartir las 7 Cartas iniciales
        for i in range(0,7):
            IA.tomarCarta(mazo)
            P1.tomarCarta(mazo)

        #Se toma una carta del Mazo para iniciar el juego:
        comodin = True
        while(comodin):
            if(Tablero.getUltimaCarta().getEfecto()!=""):
                Tablero.tomarCarta(mazo)
            else:
                comodin = False
        update = True
        turno = turno + 1
        if (update):
            Draw(False,Tablero,IA,P1)
            update = False


    #Logica del Juego
    #Inicia jugando el usuario
    turno = turno + 1
    juegaJugador(P1, Tablero, mazo)
    IA.setContador(len(P1.getMano()))
    IAPiensa(IA,Tablero,mazo)

    #Por reglas del juego la computadora debe de indicar cuando le queda una sola carta
    UNO=False
    if(len(IA.getMano())==1):
        UNO=True

    
    Draw(UNO,Tablero,IA,P1)

    if(len(IA.getMano())==0):
        print("Lo sentimos, gano la computadora")
        estado = False
    if(len(P1.getMano())==0):
        print("Felicidades, usted ("+P1.getName()+") a ganado")
        estado = False

    


