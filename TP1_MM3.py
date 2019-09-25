import numpy as np
import math
import pymysql
import xlsxwriter


def generarTiempo (tasa):
    return -tasa*math.log(np.random.rand())

def calcularMedia ():
    a=0
    s=0
    for x in eventosTodos:
        a += x[2]
    for y in eventosTodos:
        s += y[4]
    obj= (a/len(eventosTodos),s/len(eventosTodos))
    return obj

def queServidorP1():
    #devuelve (el proximo servidor a desocuparse y la posicion dentro del array)
    t = min(tiempoServidores_1)
    servidor = tiempoServidores_1.index(t)
    return (t,servidor)

def queServidorP2():
    #devuelve (el proximo servidor a desocuparse y la posicion dentro del array)
    t = min(tiempoServidores_2)
    servidor = tiempoServidores_2.index(t)
    return (t,servidor)

def generarArribos_1(duracion):
    arribos = []
    id = 0
    tiempoLlegada = 0
    tiempoLlegadaAcum = 0
    tiempoServicio = generarTiempo(tasaServicio_1)
    obj = (id,tiempoLlegada,tiempoLlegadaAcum,tiempoServicio)
    arribos.append(obj)
    while (arribos[-1][2] < duracion):
        id += 1
        tiempoLlegada = generarTiempo(tasaArribo)
        tiempoServicio = generarTiempo(tasaServicio_1)
        tiempoLlegadaAcum+=tiempoLlegada
        obj = (id,tiempoLlegada,tiempoLlegadaAcum,tiempoServicio)
        arribos.append(obj)
    return arribos

def generarArribos_Prioridad(duracion):
    arribos = []
    id = 0
    tiempoLlegada = 0
    tiempoLlegadaAcum = 0
    tiempoServicio = generarTiempo(tasaServicio_1)
    prioridad = False
    global cantClientesConPrioridad
    if (np.random.rand()<=probPrioridad):
        prioridad = True
        cantClientesConPrioridad +=1
    obj = (id,tiempoLlegada,tiempoLlegadaAcum,tiempoServicio,prioridad)
    arribos.append(obj)
    while (arribos[-1][2] < duracion):
        id += 1
        tiempoLlegada = generarTiempo(tasaArribo)
        tiempoServicio = generarTiempo(tasaServicio_1)
        tiempoLlegadaAcum+=tiempoLlegada
        if (np.random.rand()<probPrioridad):
            prioridad = True
            cantClientesConPrioridad+=1
        else:
            prioridad = False
        obj = (id,tiempoLlegada,tiempoLlegadaAcum,tiempoServicio,prioridad)
        arribos.append(obj)
    return arribos

def generarServicios_Prioridad(f):
    indice = 0
    aux = 0
    global NCCD_1
    loEncontre = False
    arribos = f[:]
    aux = []

    while (len(arribos)>0):
        tiempoServidor = queServidorP1()
        for x in range (len(arribos)-1):
            if (arribos[x][2]<= min(min(tiempoServidores_1),arribos[x][2]) and loEncontre == False ):
                cliente = arribos[x]
                loEncontre = True
                del arribos[x]
        if loEncontre == False:
            cliente = arribos[0]
            del arribos[0]
        loEncontre=False
        if (cliente[2] < tiempoServidor[0] ):
            #Tiene demora (los servidores estan ocupados
            demora = tiempoServidor[0] - cliente[2]
            NCCD_1 += 1
            tiempoSalida = demora + cliente[2] + cliente[3]
            servidor = tiempoServidor[1]
            tiempoServidores_1[servidor] += cliente[3]
        else:
            demora = 0
            tiempoSalida = cliente[2] + cliente[3]
            servidor = tiempoServidor[1]
            tiempoServidores_1[servidor] += cliente[3]
        demoras_1.append(demora)
        servicio = (idTirada, cliente[0], cliente[1], cliente[2],cliente[3],demora, servidor+1,tiempoSalida)
        aux.append(servicio)
        indice += 1
        if servidor == 0:
            arribos_4.append(servicio)
        else:
            if servidor == 1:
                arribos_5.append(servicio)
            else:
                arribos_6.append(servicio)
    return aux

def generarServicios_1 (a):
    indice = 0
    aux = []
    global NCCD_1

    while (indice < len(a)):
        
        tiempoServidor = queServidorP1()

        cliente = a[indice]
        if (cliente[2] < tiempoServidor[0] ):
            #Tiene demora (los servidores estan ocupados
            demora = tiempoServidor[0] - cliente[2]
            NCCD_1 += 1
            tiempoSalida = demora + cliente[2] + cliente[3]
            servidor = tiempoServidor[1]
            tiempoServidores_1[servidor] += cliente[3]
        else:
            demora = 0
            tiempoSalida = cliente[2] + cliente[3]
            servidor = tiempoServidor[1]
            tiempoServidores_1[servidor] += cliente[3]
        demoras_1.append(demora)
        servicio = (idTirada, cliente[0], cliente[1], cliente[2],cliente[3],demora, servidor+1,tiempoSalida)
        aux.append(servicio)
        indice += 1
        if servidor == 0:
            arribos_4.append(servicio)
        else:
            if servidor == 1:
                arribos_5.append(servicio)
            else:
                arribos_6.append(servicio)
    return aux

def generarServicios_LIFO (a):
    indice = len(a)-1
    aux = []
    global NCCD_1

    while (indice > 0):
        tiempoServidor = queServidorP1()
        cliente = a[indice]
        if (cliente[2] < tiempoServidor[0] ):
            #Tiene demora (los servidores estan ocupados
            demora = tiempoServidor[0] - cliente[2]
            NCCD_1 += 1
            tiempoSalida = demora + cliente[2] + cliente[3]
            servidor = tiempoServidor[1]
            tiempoServidores_1[servidor] += cliente[3]
        else:
            demora = 0
            tiempoSalida = cliente[2] + cliente[3]
            servidor = tiempoServidor[1]
            tiempoServidores_1[servidor] += cliente[3]
        demoras_1.append(demora)
        servicio = (idTirada, cliente[0], cliente[1], cliente[2], cliente[3],demora, servidor+1,tiempoSalida)
        aux.append(servicio)
        indice -= 1
        if servidor == 0:
            arribos_4.append(servicio)
        else:
            if servidor == 1:
                arribos_5.append(servicio)
            else:
                arribos_6.append(servicio)
    return aux

def generarServicios_2 (a): #Para la mejora
    global NCCD_2
    aux = []
    for x in (a):
        tLlegada_P2 = x[7]
        tiemposservidor = queServidorP2()
        minimoTiempoServidor = tiemposservidor[0]
        servidor = tiemposservidor[1]
        servidor+=1
        if servidor == 1:
            tasa = tasaServicio_4
        if servidor == 2:
            tasa = tasaServicio_5
        if servidor == 3:
            tasa = tasaServicio_6

        if(tLlegada_P2 > minimoTiempoServidor): #hay demora
            demora = minimoTiempoServidor - tLlegada_P2
            NCCD_2 +=1
        else:
            demora = 0
        tiempoServicio = generarTiempo(tasa)
        tSalida = tLlegada_P2 + demora + tiempoServicio
        tiempoServidores_2[servidor-1] += tiempoServicio
        demoras_2.append(demora)

        servicio = (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], tiempoServicio, demora, servidor, tSalida)
        aux.append(servicio)
    return aux

def generarEventos_1 (a):
    eventos = []
    for x in a:
        a = ("ARRIBO", x[1], x[3])
        p = ("PARTIDA", x[1], x[7])
        eventos.append(a)
        eventos.append(p)
    return eventos

def calcularCantClientesEnSistemaYCola(e):
    cantClientesSistema_1 = 0
    cantClientesCola_1 = 0
    acumSistema = 0
    cola = 0
    ultimo = 0
    for x in e:
        if x[0] == "PARTIDA":
            cola += cantClientesCola_1*(x[2]-ultimo)
            acumSistema += cantClientesSistema_1*(x[2]-ultimo)
            cantClientesSistema_1 -=1
            if cantClientesCola_1 != 0:
                cantClientesCola_1 -= 1


        else:
            cola += cantClientesCola_1*(x[2]-ultimo)
            acumSistema += cantClientesSistema_1*(x[2]-ultimo)
            cantClientesSistema_1 +=1
            if cantClientesSistema_1>3:
                cantClientesCola_1+=1

        ultimo=x[2]
    obj = (acumSistema,cola)
    return obj

def calcularCantClientesEnSistemaYCola_2(e):
    cantClientesSistema_2 = 0
    cantClientesCola_2 = 0
    acumSistema = 0
    cola = 0
    ultimo = 0
    maxSistema = 0
    maxCola = 0
    for x in e:
        if x[0] == "ARRIBO":
            cola += cantClientesCola_2*(x[1]-ultimo)
            acumSistema += cantClientesSistema_2*(x[1]-ultimo)
            cantClientesSistema_2 +=1
            if cantClientesSistema_2>5:
                cantClientesCola_2+=1
        else:
            cola += cantClientesCola_2*(x[1]-ultimo)
            acumSistema += cantClientesSistema_2*(x[1]-ultimo)
            cantClientesSistema_2 -=1
            if cantClientesCola_2 != 0:
                cantClientesCola_2 -= 1
        if maxCola < cantClientesCola_2:
            maxCola = cantClientesCola_2
        if maxSistema < cantClientesSistema_2:
            maxSistema = cantClientesSistema_2
        ultimo=x[1]
    obj = (acumSistema,cola, maxSistema, maxCola)
    return obj

def calcMaxTiempoClienteSistema():
    idMaximo = 0
    tiempoMaximo = 0
    for x in servicios_1:
        if tiempoMaximo<x[7]-x[3]:
            tiempoMaximo=x[7]-x[3]
            idMaximo = x[1]
    obj = (idMaximo,tiempoMaximo)
    return obj

def calcCantidadDeTiempoDeClienteEnSistema(s):
    tiempo = 0
    tiempos = []
    for x in s:
        tiempo = x[7]-x[3]
        tiempos.append(tiempo)
    return tiempos

def calcularEstadisticos_1 (s):
    maximaDuracion_1 = eventos_1[-1][2]
    cantArribos_1 = len(arribos_1)
    aux = calcularCantClientesEnSistemaYCola(eventos_1)
    areaClientesEnSistema_1 = aux[0]
    areaClientesEnCola_1 = aux[1]
    aux2 = calcularMedia()
    aux3 = calcMaxTiempoClienteSistema()
    t = calcCantidadDeTiempoDeClienteEnSistema(servicios_1)

    print("Duracion de la simulacion:", maximaDuracion_1)
    print("Cantidad de arribos: ", cantArribos_1)
    print("Area de Cant Clientes en Sistema", areaClientesEnSistema_1)
    print("Area de Cant Clientes en Cola", areaClientesEnCola_1)
    print("Promedio de Clientes en Sistema", areaClientesEnSistema_1/maximaDuracion_1)
    print("Promedio de Clientes en Cola", areaClientesEnCola_1/maximaDuracion_1)
    print("Uso de cada servidor:", tiempoServidores_1)
    print("Factor de utilizacion del servidor 1:", 100*tiempoServidores_1[0]/maximaDuracion_1,"%")
    print("Factor de utilizacion del servidor 2:", 100*tiempoServidores_1[1]/maximaDuracion_1,"%")
    print("Factor de utilizacion del servidor 3:", 100*tiempoServidores_1[2]/maximaDuracion_1,"%")
    print("Media entre Arribos:", aux2[0])
    print("Media entre servicios", aux2[1])
    print("Numero de Clientes que completaron Demora:",NCCD_1)
    if (NCCD_1 != 0):
        print("Promedio de demoras entre los clientes que completaron demora:", sum(demoras_1)/NCCD_1)
    print("Sumatoria de demoras:", sum(demoras_1))
    print("Maximo cantidad de tiempo para un cliente en el sistema: ", aux3[1])
    #print("Cantidad de tiempo por cada cliente en sistema", t)

def generarServicios_S345 (q):
    indice = 0
    demora = 0
    serv = []
    global NCCD_2
    while (indice < len(q)):
        obj = queServidorP2()
        tiempo = obj[0]
        servidor = obj[1]
        cliente = q[indice]
        if servidor == 0:
            tasa = tasaServicio_4
            cuantos[0]+=1
        if servidor == 1:
            tasa = tasaServicio_5
            cuantos[1]+=1
        if servidor == 2:
            tasa = tasaServicio_6
            cuantos[2]+=1
        tiempoServicio = generarTiempo(tasa)
        if (cliente[7]<tiempo):
            demora = tiempo - cliente[7]
            NCCD_2 +=1
        else:
            demora = 0
        tiempoSalida = cliente[7] + demora + tiempoServicio
        tiempoServidores_2[servidor] += tiempoServicio
        demoras_2.append(demora)
        obj = (cliente[0],cliente[1],cliente[2],cliente[3],cliente[4],cliente[5],cliente[6],cliente[7],tiempoServicio,demora,servidor+4,tiempoSalida)
        serv.append(obj)
        indice +=1
    return serv

def generarServicios_S4 (q):
    tiempo = tiempoServidores_2[0]
    indice = 0
    demora = 0
    serv = []
    global NCCD_4
    while (indice < len(q)):
        cliente = q[indice]
        tiempoServicio = generarTiempo(tasaServicio_4)
        if (cliente[7]<tiempoServidores_2[0]):
            demora = tiempoServidores_2[0] - cliente[7]
            NCCD_4 +=1
        else:
            demora = 0
        tiempoSalida = cliente[7] + demora + tiempoServicio
        tiempoServidores_2[0] += tiempoServicio
        demoras_4.append(demora)
        obj = (cliente[0],cliente[1],cliente[2],cliente[3],cliente[4],cliente[5],cliente[6],cliente[7],tiempoServicio,demora,4,tiempoSalida)
        serv.append(obj)
        indice +=1
    return serv

def generarServicios_S5 (q):
    tiempo = tiempoServidores_2[1]
    indice = 0
    demora = 0
    serv = []
    global NCCD_5
    while (indice < len(q)):
        cliente = q[indice]
        tiempoServicio = generarTiempo(tasaServicio_5)
        if (cliente[7]<tiempoServidores_2[1]):
            demora = tiempoServidores_2[1] - cliente[7]
            NCCD_5 +=1
        else:
            demora = 0
        tiempoSalida = cliente[7] + demora + tiempoServicio
        tiempoServidores_2[1] += tiempoServicio
        demoras_5.append(demora)
        obj = (cliente[0],cliente[1],cliente[2],cliente[3],cliente[4],cliente[5],cliente[6],cliente[7],tiempoServicio,demora,5,tiempoSalida)
        serv.append(obj)
        indice +=1
    return serv

def generarServicios_S6 (q):
    tiempo = tiempoServidores_2[2]
    indice = 0
    demora = 0
    serv = []
    global NCCD_6
    while (indice < len(q)):
        cliente = q[indice]
        tiempoServicio = generarTiempo(tasaServicio_6)
        if (cliente[7]<tiempoServidores_2[2]):
            demora = tiempoServidores_2[2] - cliente[7]
            NCCD_6 +=1
        else:
            demora = 0
        tiempoSalida = cliente[7] + demora + tiempoServicio
        tiempoServidores_2[2] += tiempoServicio
        demoras_6.append(demora)
        obj = (cliente[0],cliente[1],cliente[2],cliente[3],cliente[4],cliente[5],cliente[6],cliente[7],tiempoServicio,demora,6,tiempoSalida)
        serv.append(obj)
        indice +=1
    return serv

def calcTiempoPromedioClientesEnSistema (e):
    acum = 0
    max = 0
    for x in e:
        acum += x[11]-x[3]
        if acum > max:
            max = acum
    return acum/len(e)

#Comienza Programa Principal
#Definicion Variables
np.random.seed(0)
cantitdadTiradas=1
duracion = 180
#db = pymysql.connect("localhost","root","damela10","tpSimulacion_6Servers")
#cursor = db.cursor()
#0 => FIFO
#1 => LIFO
#2 => Prioridad
politica = 0
probPrioridad = 0.03
#mejora =1 => unica fila
#mejora=0 => tres files
mejora = 1


tasaArribo = 0.6
tasaServicio_1 = 0.5
tasaServicio_4 = 0.2
tasaServicio_5 = 0.4
tasaServicio_6 = 0.6

numTirada = []
promedio_duracion = []
promedio_cantArribos = []
promedio_AreaClientes = []
promedio_AreaCola = []
promedio_promedioClientesSistema = []
promedio_promedioClientesCola = []
promedio_promedioTiempoClientesEnSistema = []
promedio_usoServidor1 = []
promedio_usoServidor2 = []
promedio_usoServidor3 = []
promedio_usoServidor4 = []
promedio_usoServidor5 = []
promedio_usoServidor6 = []
promedio_mediaEntreArribos = []
promedio_mediaEntreServidios = []
promedio_NCCD1 = []
promedio_demoras1 = []
promedio_NCCD2 = []
promedio_demoras2 = []
promedio_NCCD4 = []
promedio_demoras4 = []
promedio_NCCD5 = []
promedio_demoras5 = []
promedio_NCCD6 = []
promedio_demoras6 = []
promedio_maximaCantidadDeClientesEnSistema = []
promedio_maximaCantidadDeClientesEnCola = []
promedio_clientesPrioridad = []



for tirada in range(cantitdadTiradas):
    numTirada.append(tirada)
    tiempoServidores_1 = [0,0,0]
    tiempoServidores_2 = [0,0,0]
    cuantos = [0,0,0]
    arribos_1 = []
    servicios_1 = []
    eventos_1 = []

    arribos_4 = []
    servicios_4 = []
    arribos_5 = []
    servicios_5 = []
    arribos_6 = []
    servicios_6 = []

    prioridades = []

    #Estadisticos
    demoras_1 = []
    NCCD_1 = 0
    #Para la mejora
    NCCD_2 = 0
    demoras_2 = []

    demoras_4 = []
    NCCD_4 = 0
    demoras_5 = []
    NCCD_5 = 0
    demoras_6 = []
    NCCD_6 =0
    areaClientesEnSistema_1 = 0
    areaClientesEnCola_1 = 0

    maximaDuracion_1 = 0
    cantArribos_1 = 0
    idTirada = tirada

    cantClientesConPrioridad = 0

    if politica == 0:
        arribos_1 = generarArribos_1(duracion)
        servicios_1 = generarServicios_1(arribos_1)
    else:
        if politica ==1 :
            arribos_1 = generarArribos_1(duracion)
            servicios_1 = generarServicios_LIFO(arribos_1)
        else:
            if politica ==2:
                arribos_1 = generarArribos_Prioridad(duracion)

                servicios_1 = generarServicios_Prioridad(arribos_1)





    eventos_1 = generarEventos_1(servicios_1)
    eventos_1.sort(key = lambda x: x[2])

    #Calcula estadisticos de la primer parte del sistema
    #calcularEstadisticos_1(servicios_1)


    eventosTodos = []

    if mejora==0: #sin mejora se generar 3 colas en la segunda mitad del sistema
        servicios_4 = generarServicios_S4(arribos_4)
        servicios_5 = generarServicios_S5(arribos_5)
        servicios_6 = generarServicios_S6(arribos_6)
        for x in servicios_4:
            eventosTodos.append(x)
        for x in servicios_5:
            eventosTodos.append(x)
        for x in servicios_6:
            eventosTodos.append(x)
    else: #Con la mejora generamos una unica cola que luego se distribuye entre los 3 servidores
        eventosTodos = generarServicios_S345(servicios_1)

    eventosTodos.sort(key=lambda x: x[11])


    listaEventosTodos = []
    for x in eventosTodos:
        a = ("ARRIBO", x[3])
        p = ("PARTIDA", x[11])
        listaEventosTodos.append(a)
        listaEventosTodos.append(p)

    listaEventosTodos.sort(key=lambda x: x[1])
    print(listaEventosTodos)


    obj = calcularCantClientesEnSistemaYCola_2(listaEventosTodos)
    areaClientesEnSistema_2 = obj[0]
    areaClientesEnCola_2 = obj[1]

    duracionSimulacion = eventosTodos[-1][11]
    #print("Duracion de la simulacion: ", duracionSimulacion)
    promedio_duracion.append(duracionSimulacion)
    #print("Cantidad de arribos:", len(arribos_1))
    promedio_cantArribos.append(len(arribos_1))
    #print("Area Clientes en Sistema:", areaClientesEnSistema_2)
    promedio_AreaClientes.append(areaClientesEnSistema_2)
    #print("Area Clientes en Cola:", areaClientesEnCola_2)
    promedio_AreaCola.append(areaClientesEnCola_2)
    #print("Promedio de Clientes en Sistema:", areaClientesEnSistema_2/duracionSimulacion)
    promedio_promedioClientesSistema.append(areaClientesEnSistema_2/duracionSimulacion)
    #print("Promedio de Clientes en Cola:", areaClientesEnCola_2/duracionSimulacion)
    promedio_promedioClientesCola.append(areaClientesEnCola_2/duracionSimulacion)
    #print("Tiempo promedio de un cliente en el sistema:",calcTiempoPromedioClientesEnSistema(eventosTodos))
    promedio_promedioTiempoClientesEnSistema.append(calcTiempoPromedioClientesEnSistema(eventosTodos))
    #print("    Servidor 1:",100*tiempoServidores_1[0]/duracionSimulacion,"%")
    promedio_usoServidor1.append(100*tiempoServidores_1[0]/duracionSimulacion)
    #print("    Servidor 2:",100*tiempoServidores_1[1]/duracionSimulacion,"%")
    promedio_usoServidor2.append(100*tiempoServidores_1[1]/duracionSimulacion)
    #print("    Servidor 3:",100*tiempoServidores_1[2]/duracionSimulacion,"%")
    promedio_usoServidor3.append(100*tiempoServidores_1[2]/duracionSimulacion)
    #print("    Servidor 4:",100*tiempoServidores_2[0]/duracionSimulacion,"%")
    promedio_usoServidor4.append(100*tiempoServidores_2[0]/duracionSimulacion)
    #print("    Servidor 5:",100*tiempoServidores_2[1]/duracionSimulacion,"%")
    promedio_usoServidor5.append(100*tiempoServidores_2[1]/duracionSimulacion)
    #print("    Servidor 6:",100*tiempoServidores_2[2]/duracionSimulacion,"%")
    promedio_usoServidor6.append(100*tiempoServidores_2[2]/duracionSimulacion)
    #print("Media entre Arribos:", calcularMedia()[0])
    promedio_mediaEntreArribos.append(calcularMedia()[0])
    #print("Media entre Servicios:", calcularMedia()[1])
    promedio_mediaEntreServidios.append(calcularMedia()[1])

    #print("Demora promedio de un cliente utilizando los servidores 1 y 4:", sum(demoras_1)/len(arribos_1) + sum(demoras_4)/len(arribos_4) )
    #print("Demora promedio de un cliente utilizando los servidores 1 y 5:", sum(demoras_1)/len(arribos_1) + sum(demoras_5)/len(arribos_5) )
    #print("Demora promedio de un cliente utilizando los servidores 1 y 6:", sum(demoras_1)/len(arribos_1) + sum(demoras_5)/len(arribos_6) )





    #print("Numero de Clientes que completaron demora en Cola 1:", NCCD_1)
    promedio_NCCD1.append(NCCD_1)
    promedio_demoras1.append(sum(demoras_1))
    #if NCCD_1 != 0:
        #print("Suma de las demoras en cola 1:", sum(demoras_1))
        #print("Demora promedio de los clientes que completaron demora en cola 1:", sum(demoras_1)/NCCD_1)
        #print("Demora promedio de los clientes (todos) en cola 1:", sum(demoras_1)/len(arribos_1))

    #print("Numero de Clientes que completaron demora en Cola 4:", NCCD_4 )
    promedio_NCCD4.append(NCCD_4)
    promedio_demoras4.append(sum(demoras_4))
    #if NCCD_4 != 0:
        #print("Suma de las demoras en cola 4:", sum(demoras_4))
        #print("Demora promedio de los clientes que completaron demora en cola 4:", sum(demoras_4)/NCCD_4)
        #print("Demora promedio de los clientes (todos) en cola 4:", sum(demoras_4)/len(arribos_4))

    #print("Numero de Clientes que completaron demora en Cola 5:", NCCD_5 )
    promedio_NCCD5.append(NCCD_5)
    promedio_demoras5.append(sum(demoras_5))
    #if NCCD_5 != 0:
        #print("Suma de las demoras en cola 5:", sum(demoras_5))
        #print("Demora promedio de los clientes que completaron demora en cola 5:", sum(demoras_5)/NCCD_5)
        #print("Demora promedio de los clientes (todos) en cola 5:", sum(demoras_5)/len(arribos_5))

    #print("Numero de Clientes que completaron demora en Cola 6:", NCCD_6 )
    promedio_NCCD6.append(NCCD_6)
    promedio_demoras6.append(sum(demoras_6))
    #if NCCD_6 != 0:
        #print("Suma de las demoras en cola 6:", sum(demoras_6))
        #print("Demora promedio de los clientes que completaron demora en cola 6:", sum(demoras_6)/NCCD_6)
        #print("Demora promedio de los clientes (todos) en cola 6:", sum(demoras_6)/len(arribos_6))


    #print("Numero de Clientes que completaron demora en Cola 2:", NCCD_2 )
    promedio_NCCD2.append(NCCD_2)
    promedio_demoras2.append(sum(demoras_2))
    #if NCCD_2 != 0:
        #print("Suma de las demoras en cola 6:", sum(demoras_2))
        #print("Demora promedio de los clientes que completaron demora en cola 6:", sum(demoras_2)/NCCD_2)
        #print("Demora promedio de los clientes (todos) en cola 6:", sum(demoras_2)/len(arribos_1))

    #print("Maxima cantidad de clientes en sistema en un instante t:", obj[2])
    #print("Maxima cantidad de clientes en cola en un instante t:", obj[3])


    #print("Maxima cantidad de clientes en sistema en un instante t:", obj[2])
    #print("Maxima cantidad de clientes en cola en un instante t:", obj[3])
    promedio_maximaCantidadDeClientesEnSistema.append(obj[2])
    promedio_maximaCantidadDeClientesEnCola.append(obj[3])

    #if politica ==2:
        #print("Promedio de clientes que ingresaron con prioridad", cantClientesConPrioridad/len(arribos_1))

    promedio_clientesPrioridad.append(cantClientesConPrioridad/len(arribos_1))


    #sql = "INSERT INTO client_tracking_LIFO_conMejora values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}')".format(tirada,round(duracionSimulacion,3),len(arribos_1), round(areaClientesEnSistema_2,4), round(areaClientesEnCola_2,4), round(calcTiempoPromedioClientesEnSistema(eventosTodos),4), round(tiempoServidores_1[0],4),round(tiempoServidores_1[1],4),round(tiempoServidores_1[2],4), round(tiempoServidores_2[0],4),round(tiempoServidores_2[1],4),round(tiempoServidores_2[2],4), round(calcularMedia()[0],4),round(calcularMedia()[1],4), NCCD_1, NCCD_2, 'null','null',sum(demoras_1), sum(demoras_2), 'null','null',obj[2], obj[3])

    #cursor.execute(sql)
    #db.commit()


print("AREA Cola",promedio_AreaCola)
'''
print(numTirada)
print(promedio_duracion)
print(promedio_cantArribos)
print("AREA sistema",promedio_AreaClientes)
print("AREA Cola",promedio_AreaCola)

print(promedio_promedioClientesSistema)
print(promedio_promedioClientesCola)
print(promedio_promedioTiempoClientesEnSistema)
print(promedio_usoServidor1)
print(promedio_usoServidor2)
print(promedio_usoServidor3)
print(promedio_usoServidor4)
print(promedio_usoServidor5)
print(promedio_usoServidor6)
print(promedio_mediaEntreArribos)
print(promedio_mediaEntreServidios)
'''
print("NCCD1",promedio_NCCD1)
print("PROMEDIO Demoras1",promedio_demoras1)
print("NCCD2",promedio_NCCD2)
print("PROMEDIO Demoras2",promedio_demoras2)
print("NCCD4",promedio_NCCD4)
print("PROMEDIO Demoras4",promedio_demoras4)
print("NCCD5",promedio_NCCD5)
print("PROMEDIO Demoras5",promedio_demoras5)
print("NCCD6",promedio_NCCD6)
print("PROMEDIO Demoras6",promedio_demoras6)
'''
print(promedio_maximaCantidadDeClientesEnSistema)
print(promedio_maximaCantidadDeClientesEnCola)
print(promedio_clientesPrioridad)

#db = pymysql.connect("localhost","root","damela10","Simulacion_TP1")
#cursor = db.cursor()

#for z in range(cantitdadTiradas):
#    sql = "INSERT INTO clientTracking_Prioridad_cMejora values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}','{24}','{25}','{26}','{27}','{28}')".format(numTirada[z],promedio_duracion[z],promedio_cantArribos[z], promedio_AreaClientes[z], promedio_AreaCola[z], promedio_promedioClientesSistema[z],promedio_promedioClientesCola[z], promedio_promedioTiempoClientesEnSistema[z], promedio_usoServidor1[z], promedio_usoServidor2[z], promedio_usoServidor3[z], promedio_usoServidor4[z], promedio_usoServidor5[z], promedio_usoServidor6[z], promedio_mediaEntreArribos[z], promedio_mediaEntreServidios[z], promedio_NCCD1[z], promedio_demoras1[z], promedio_NCCD2[z], promedio_demoras2[z], promedio_NCCD4[z], promedio_demoras4[z], promedio_NCCD5[z], promedio_demoras5[z], promedio_NCCD6[z], promedio_demoras6[z],promedio_maximaCantidadDeClientesEnSistema[z], promedio_maximaCantidadDeClientesEnCola[z], promedio_clientesPrioridad[z] )
#    cursor.execute(sql)
#    db.commit()
'''
