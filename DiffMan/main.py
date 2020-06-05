hexadecimalcontrast = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111',
}


def HexToBin(string):
    "Convert sixteen to binary"

    Binstring = ""
    string = string.lower()
    for i in string:
        try:
            Binstring += hexadecimalcontrast[i]
        except:
            return -1
    return Binstring


def BinToStr(strbin):
    "Turn the binary string to a ASCII string"

    strten = ""
    for i in range(len(strbin) // 8):
        num = 0
        test = strbin[i * 8:i * 8 + 8]
        for j in range(8):
            num += int(test[j]) * (2**(7 - j))
        strten += chr(num)
    return strten


def StrToHex(string):
    "Converts a string to HEX"

    hexStr = ''
    for i in string:
        tmp = str(hex(ord(i)))
        if len(tmp) == 3:
            hexStr += tmp.replace('0x', '0')
        else:
            hexStr += tmp.replace('0x', '')
    return hexStr


def Binxor(string1, string2):
    "If the length is different, only the short one is returned."

    strlen = 0
    xorstr = ""
    if len(string1) > len(string2):
        strlen = len(string2)
    else:
        strlen = len(string1)
    for i in range(strlen):
        if string1[i] == string2[i]:
            xorstr += '0'
        else:
            xorstr += '1'
    return xorstr


def EnManchOn(strbin):
    clockline = ''
    prepareda = ''
    for i in strbin:
        prepareda += i * 2
        clockline += '0' + '1'
    return Binxor(clockline, prepareda)


def DeManchOn(strbin):
    clockline = ''
    string = ''
    for i in range(len(strbin) // 2):
        clockline += '0' + '1'
    prepareda = Binxor(clockline, strbin)
    for i in range(len(prepareda) // 2):
        if prepareda[i * 2] == prepareda[i * 2 + 1]:
            string += prepareda[i * 2]
    return string


def EnManchOff(strbin):
    clockline = ''
    prepareda = ''
    for i in strbin:
        prepareda += i * 2
        clockline += '1' + '0'
    return Binxor(clockline, prepareda)


def DeManchOff(strbin):
    clockline = ''
    string = ''
    for i in range(len(strbin) // 2):
        clockline += '1' + '0'
    prepareda = Binxor(clockline, strbin)
    for i in range(len(prepareda) // 2):
        if prepareda[i * 2] == prepareda[i * 2 + 1]:
            string += prepareda[i * 2]
    return string


def EndSeqCon(strbin):
    string = ''
    for i in range(len(strbin) // 8):
        string += strbin[i * 8:i * 8 + 8][::-1]
    return string


def EndEnd(hexstr):
    string = ""
    for i in range(len(hexstr) // 2):
        string += hexstr[2 * i:2 * i + 2][::-1]
    return string


def EnDiffMan(strbin):
    string = ""
    lastda = '01'
    for i in strbin:
        if lastda == '01':
            if i == '1':
                string += '10'
                lastda = '10'
            else:
                string += '01'
                lastda = '01'
        else:
            if i == '1':
                string += '01'
                lastda = '01'
            else:
                string += '10'
                lastda = '10'
    return string

def DeDiffMan(strbin):
    string = ""
    strbin = '1' + strbin
    for i in range(len(strbin)//2):
    	ps = strbin[i*2:i*2+2]
    	if ps[0] == ps[1]:
    		string += '1'
    	else:
    		string += '0'
    return string


def ManchesterBig(data):

	return EndEnd(StrToHex(BinToStr(DeManchOn(EndSeqCon(HexToBin(data))))))

def ManchesterSmall(data):

	return StrToHex(BinToStr(DeManchOff(HexToBin(data))))


def DifferentialManchester(data):

	return StrToHex(BinToStr(DeDiffMan(HexToBin(data))))


print ManchesterSmall('5555555595555A65556AA696AA6666666955')
print ManchesterBig('5555555595555A65556AA696AA6666666955')
print DifferentialManchester('295965569a596696995a9aa969996a6a9a669965656969996959669566a5655699669aa5656966a566a56656')





