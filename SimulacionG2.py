#!/usr/bin/python
# -*- coding: utf-8 -*-
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.node import OVSBridge
from mininet.log import setLogLevel, info
from mininet.link import TCLink #Con esta libreria se puede ajustar parametros de retraso, ancho de banda
import sys

def startNetwork():
  
  net = Mininet(switch=OVSBridge , link=TCLink)# hay que agregar los tipos de enlaces
  # Hosts / Sensores
  Dispositivos = ["CamMovi","SensAud","Velocimet","stnMlogica","SenPeso","CamSeg","PtoRecol"]
  # Switch / Antena
  net.addSwitch("S1")
  # Se crean los hosts y se conectan al switch
  for i in range(len(Dispositivos)):
    # Se crean los hosts 
    net.addHost(Dispositivos[i],ip="10.0.0."+str(i+1)+"/24")
    # Se vinculan los host al switch con los parametros predefinidos
    #net.addLink(Dispositivos[i],"S1", bw=100, delay='5ms', loss=0.01) # 5G
    net.addLink(Dispositivos[i],"S1", bw=100, delay='5ms', loss=0.01)
  net.start()
  
  #["stnMlogica","50K","250K","u"],
  PruebasPing = [
  ["CamMovi","50M","8192K","u","3"],
  ["SensAud","300","800","u","1"],
  ["Velocimet","10M","16K","t","2"],
  ["SenPeso","5M","80K","t","1"],
  ["CamSeg","150M","8192K","u","1"]]

  IP_dest = str(net.get("PtoRecol").IP())
  option=0
  while option != 1:
    info('\n=========================================')
    info('\n |-> 1 - LINEA DE COMANDOS MININET')
    info('\n |-> 2 - Comprobar conectivad total (pingall)')
    info('\n |-> 3 - Imprimir hosts')
    info('\n |-> 4 - IPERF')
    info('\n |-> 5 - PRUEBAS')
    info('\n |-> 6 - SALIR')
    info('\n==========================================\n')
    
    opt = input('DIGITE UNA option: ')
    if opt.isdigit(): option = int(opt)
    #===================================================
    if option == 2:
      net.pingAll()
      option = 0
    #===================================================
    if option == 3:
      print(net.hosts)
      option = 0
    #===================================================
    if option == 4:
      net.iperf((net.get("CamMovi"), net.get("PtoRecol")), l4Type='TCP', seconds=5)
      option = 0
    #===================================================
    if option == 5:
      net.get("PtoRecol").cmd("iperf -s > /dev/null 2>&1 & iperf -s -u -p 5002 > /dev/null 2>&1 &") # Escucha el servidor con un puerto TCP y otro en UDP
      #net.get("PtoRecol").cmd("iperf -s -u -p 5002> /dev/null 2>&1 &")
      
      for host in range(len(PruebasPing)):
        if PruebasPing[host][3] == "u":# Simula dispositivos UDP
          print("Prueba del sensor: ",PruebasPing[host][0],"##########################################################################################")
          client_output = net.get(PruebasPing[host][0]).cmd("iperf -u -c " + IP_dest + " -n "+PruebasPing[host][1]+" -b "+PruebasPing[host][2]+" -p 5002 > /tmp/h1.txt &")  # Cliente con sus parametros
          print(client_output)
        else:# Simula dispositivos TCP
          print("Prueba del sensor: ",PruebasPing[host][0],"##########################################################################################")
          client_output = net.get(PruebasPing[host][0]).cmd("iperf -c " + IP_dest + " -n "+PruebasPing[host][1]+" -l "+PruebasPing[host][2]," -i 1")  # Cliente con sus parametros
          print(client_output)
      option = 0
    #===================================================
    elif option == 6:
      net.stop()
      sys.exit()
  CLI( net )
#////////////////////////////////////////////////////////////
if __name__ == '__main__':
  setLogLevel('info')
  startNetwork()