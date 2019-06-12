#!/usr/bin/python3
# coding: utf-8

import subprocess
import os
import time

###################################################################
###################################################################


def Main():

    
    while True:
   
        rectangle_vert = "<div id='rectangle_vert'>"
        rectangle_orange = "<div id='rectangle_orange'>"
        rectangle_rouge = "<div id='rectangle_rouge'>"
        lignehtml_cpu = ""
        lignehtml_ram = ""

        #ICI On rentre la commande SNMP
        out_cpu = subprocess.getoutput(["snmpget -v2c -c public 192.168.10.251 .1.3.6.1.4.1.2021.11.9.0"])
        out_ram_used = subprocess.getoutput(["snmpget -v2c -c public 192.168.10.251 .1.3.6.1.4.1.2021.4.11.0"])
        out_ram_total = subprocess.getoutput(["snmpget -v2c -c public 192.168.10.251 .1.3.6.1.4.1.2021.4.5.0"])

        #ICI on coupe la réponse à partir du mot 'INTEGER: '
        valeurCPU = out_cpu.split('INTEGER: ')
        valeurRAMused = out_ram_used.split('INTEGER: ')
        valeurRAMtotal = out_ram_total.split('INTEGER: ')

        #ICI on prend la valeur du dictionnaire créé par la coupure du split ci-dessus
        valeurCPU = valeurCPU[1]
        valeurRAMused = valeurRAMused[1]
        valeurRAMtotal = valeurRAMtotal[1]


        #ICI on transforme le résultat en integer pour le comparer avec nos cofdition if
        valeurCPU = int(valeurCPU)
        valeurRAMused = int(valeurRAMused)
        valeurRAMtotal = int(valeurRAMtotal)
        valeurRAMpercent = int((valeurRAMused / valeurRAMtotal) * 100)
        #ICI on vérifier la valeur de la charge CPU

        if(valeurCPU <= 50):
            #On estime que 50% d'utilisation c'est peu donc rectangle vert et charge envoyée
            lignehtml_cpu = rectangle_vert + str(valeurCPU) + ''.join('%</div>\n')
        
        if(valeurRAMpercent <= 50):
            lignehtml_ram = rectangle_vert + str(valeurRAMpercent) + ''.join('%</div>\n')

        if(valeurCPU >= 51 and valeurCPU <= 84):
            #entre 51 et 84 % utilisation d'un rectangle orange
            lignehtml_cpu = rectangle_orange + str(valeurCPU) + ''.join('%</div>\n')
        
        if(valeurRAMpercent >= 51 and valeurRAMpercent <= 84):
            lignehtml_ram = rectangle_orange + str(valeurRAMpercent) + ''.join('%</div>\n')

        if(valeurCPU >= 85):
            #On estime que au dessus de 85% c'est un rectangle rouge
            lignehtml_cpu = rectangle_rouge + str(valeurCPU) + ''.join('%</div>\n')

        if(valeurRAMpercent >= 85):
            lignehtml_ram = rectangle_rouge + str(valeurRAMpercent) + ''.join('%</div>\n')

        f = open('/var/www/template.html', 'r')
        f2= open('/var/www/html/index.html', 'w')

        line=1
        for l in f:
            if line == 10:
                f2.write(l.replace(l, lignehtml_cpu))
            elif line == 13:
                f2.write(l.replace(l,lignehtml_ram))
            else:
                f2.write(l)
            line+=1    
        f.close()
        f2.close()

        time.sleep(5)

###################################################################
###################################################################

if __name__=="__main__":
   Main()

###################################################################
###################################################################
