import socket
import time
import re
import random

class packet:
    host = '169.254.3.52'
    port = random.randrange(5000,20000) #random not used port

    server = ('169.254.3.52', 5678) #localhost + server port

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while(true):
        try:
            s.bind((host, port))
            break;
        except:
            port +=1
            s.bind((host, port))

    L = 0
    max = 0
    czy_ktos_zgadl = False
    #-------------------------------------------------------
    operacja = 0
    czas = ''
    id = ''
    odpowiedz = ''
    final_packet = ''
    ack = ''

    #-------------------------------------------------------
    def stworz_pakiet(self):
        self.final_packet = "Czas>"+self.czas+"<Identyfikator>"+self.id+"<Operacja>"+str(self.operacja)+"<Odpowiedz>"+self.odpowiedz+"<Ack>"+self.ack+"<"

    def decode_packet(self):
        data, addr = self.s.recvfrom(1024)
        data = data.decode('utf-8')
        result = re.findall('>(.*?)<', data)
        self.czas = result[0]
        self.id = result[1]
        self.operacja = int(result[2])
        self.odpowiedz = result[3]
        self.ack = result[4]
        self.stworz_pakiet()
        print('Odebrano: '+self.final_packet)


    def send_packet(self):
        self.czas = time.ctime(time.time())
        self.stworz_pakiet()
        self.s.sendto(self.final_packet.encode('utf-8'), self.server)  # send to server
        print('Wysłano: '+self.final_packet)

    def proceed(self):
        self.send_packet()
        self.decode_packet()
        self.decode_packet()
        self.ack = "Potwierdzenie"
        self.send_packet()
        self.ack = ""


    def proceed1(self):
        try:
            self.L = int(input("Podaj L: "))
        except:
            print("Podałeś nieprawidłową wartość!")
            self.L = input("Podaj L: ")
        self.operacja = self.L
        self.ack = ""
        self.send_packet()
        self.decode_packet()
        self.decode_packet()
        self.ack = "Potwierdzenie"
        self.send_packet()
        self.ack = ""
        self.max = self.operacja
        print("Masz {} prób/y \n Wylosowana liczb jest z przedziału <1;9>".format(self.operacja))

    def guess(self):
        try:
            self.odpowiedz = int(input("Zgadnij liczbę: "))
        except:
            print("Podałeś nieprawidłową wartość!")
            self.odpowiedz= int(input("Zgadnij liczbę: "))
        self.odpowiedz = str(self.odpowiedz)
        self.proceed()
        if(self.odpowiedz == 'Win'):
            print("Wygrałeś!!! :)")
            self.max = 0
        elif(self.odpowiedz == "Opponent first"):
            print("Przeciwnik był pierwszy :(")
            self.czy_ktos_zgadl = True
        elif(self.odpowiedz == "Wrong"):
            print("Błedna odpowiedź")

def Main():
    p = packet()
    p.proceed()
    p.proceed1()
    while p.max != 0:
        if(p.czy_ktos_zgadl):
            break;
        p.max -= 1
        p.guess()



if __name__ == '__main__':
    Main()
