#routine to get RPi serial number
def getserial():
    # extract serial from cupinfo file
    cpuserial = "00000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERR0000000000"
    return cpuserial

myserial = getserial()
print(myserial)