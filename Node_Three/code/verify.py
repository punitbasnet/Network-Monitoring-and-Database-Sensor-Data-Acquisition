import hashlib
import hmac

#Files made after execution of this module are hmaclog_date.txt, vreadings_date.txt and badreadings.txt

def verify(thefile):
    datetxt = thefile[-14:]
    date=datetxt.strip('.txt')
    #datetime.datetime.now().strftime("%Y-%m-%d")
    Loc = "Baker"
    bLoc=Loc.encode()
    LocID = "39.326265,-82.103506"
    bLocID = LocID.encode()
    pwd=b"sensor"
    readhr=[]
    f=open(thefile, 'r')
    for line in f:
        datablock = line.encode()
        salt=bLoc+bLocID
        keylength = 12
        NumKDHashes = 10000
        key = hashlib.pbkdf2_hmac('sha256', pwd, salt, NumKDHashes, dklen=keylength)
        ourHMAC=hmac.new(key, datablock, hashlib.sha256)
        hmac_string = ourHMAC.hexdigest()
        hmac_string = hmac_string + '\n'
        readhr.append(hmac_string)
    f.close()
    hmacs=open('/home/sysop/repository/incoming/hmacreadings_{}'.format(datetxt),'r')
    f=open(thefile, 'r')
    readhs=hmacs.readlines()
    read=f.readlines()
    lhs = len(readhs)
    lhr = len(readhr)
    badreads=0
    count = 0
    hmaclog='hmaclog_{}'.format(datetxt)
    vreadings='vreadings_{}'.format(datetxt)
    breadings = 'breadings_{}'.format(datetxt)
    g=open(hmaclog, 'w')
    h=open(vreadings, 'w')
    i=open(breadings, 'w')
    if (lhs != lhr):
        g.write("The readings from {} had INCONSISTENT NUMBER OF ENTRIES".format(date))
        h.write("Empty")
        while (count != lhr):
            i.write(read[count])
            count +=1
    else:
        while (count != lhs):
            a = read[count].split()
            try:
                if (a[0] != 'Conductivity'):
                    float(a[4])
                    float(a[6])
                if (readhs[count] != readhr[count]):
                    badreads = badreads + 1
                    g.write(read[count])
                    i.write(read[count])
                else:
                    h.write(read[count])            
            except ValueError:
                badreads = badreads + 1
                g.write(read[count])
                i.write(read[count])
            count +=1
        if (badreads == 0):
            g.write("All the values were VERIFIED for the readings from {}".format(date))
        else:
            g.write("The {} value(s) BELOW FAILED VERIFICATION in the readings from {}".format(badreads, date))
    f.close()
    g.close()
    h.close()
    i.close()
    return(datetxt)
