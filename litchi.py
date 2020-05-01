# Thursday, April 30, 2020
# Author:nianhua
# Blog:https://github.com/nian-hua/

from bluepy.btle import *
import sys,getopt

deviceCount = 0
argv = sys.argv[1:]
DEVICE = None
SERVICE = None
CHARAS = None
MESSAG = None
TIME = 10

def GetOptions(argv):
    global DEVICE,SERVICE,CHARAS,MESSAG,TIME
    try:
        opts,args = getopt.getopt(argv,"hT:D:S:C:M:",["time","device=","server=","charas","messag"])
    except getopt.GetoptError:
        print('Litchi.py -T 10 -D 68:9e:19:03:68:ea -S 9fdc9c81-fffe-51a1-e511-5a38c414c2f9 -C ac7bc836-6b69-74b6-d64c-451cc52b476e -M 140000000000000000000007290801ff002000000280')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("LITCHI - Litchi 1.0 (2020 April 30, compiled April 30 2020 04:10:35)\n")
            print("parameter:")
            print("\t-T : Set Scan time.")
            print("\t-D : Set The ID of the connected device.")
            print("\t-S : Set The service of the connected device.")
            print("\t-C : Set The characteristic of the connected service.")
            print("\t-M : Set The Message to Device >> type:Hex.")
            sys.exit()
        elif opt in ("-T", "--time"):
            TIME = int(arg)
        elif opt in ("-D", "--device"):
            DEVICE = arg
        elif opt in ("-S", "--service"):
            SERVICE = arg
        elif opt in ("-C", "--charas"):
            CHARAS = arg
        elif opt in ("-M", "--messag"):
            MESSAG = arg

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        global deviceCount
        if isNewDev:
            deviceCount += 1
        elif isNewData:
            deviceCount += 0


def ScanDevice():
    global DEVICE,TIME
    if DEVICE != None:
        return 0
    else:
        print("------------scaning devices------------")
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(TIME)
        print("End of Scan , %s devices found."%(deviceCount))
        num = 0
        devices_list = []
        for dev in devices:
            num += 1
            devices_list.append(dev)
            print("[%s] Device %s <%s>\tRSSI = %d dB |" %(num,dev.addr,dev.addrType,dev.rssi),end="")
            for (adtype,desc,value) in dev.getScanData():
                if "Complete" in desc:
                    print("%s = %s | "%(desc,value),end='')
            print('')
        choice = int(input("please input number:"))
        dev = devices_list[choice - 1]
        DEVICE = dev.addr

GetOptions(argv)
ScanDevice()

def SelectService():
    
    global SERVICE
    peridevice = Peripheral(DEVICE)
    print("connected %s success!"%(DEVICE))
    services = list(peridevice.getServices())
    if SERVICE != None:
        pass
    else:
        for i in range(len(services)):
            print("[%s] %s" %(i+1,services[i]))
        choice = int(input("please input number:"))
        SERVICE = str(services[choice - 1])
    for i in range(len(services)):
        if SERVICE in str(services[i]):
            service = services[i]
    return service

service = SelectService()

def SelectCharas(service):
    global CHARAS
    print("select %s success!"%(service))
    charas = list(service.getCharacteristics())
    if CHARAS != None:
        pass
    else:
        for i in range(len(charas)):
            print("[%s] %s"%(i+1,charas[i]))
        choice = int(input("please input number:"))
        CHARAS = str(charas[choice - 1])
    for i in range(len(charas)):
        if CHARAS in str(charas[i]):
            chara = charas[i]
    return chara

chara = SelectCharas(service)

def SendMessage(chara):
    global MESSAG
    print("select % success"%(chara))
    if MESSAG != None:
        pass
    else:
        MESSAG = str(input('please input send data:'))
    MESSAG = bytearray.fromhex(MESSAG)
    chara.write(MESSAG,True)
    print("Send Message Success!!!")
SendMessage(chara)
