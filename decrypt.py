en_map = {
    "E": 12.02,
    "T": 9.1,
    "A": 8.12,
    "O": 7.68,
    "I": 7.31,
    "N": 6.95,
    "S": 6.28,
    "R": 6.02,
    "H": 5.92,
    "D": 4.32,
    "L": 3.98,
    "U": 2.88,
    "C": 2.71,
    "M": 2.61, # M 
    "F": 2.3,  # W 
    "Y": 2.11, # F
    "W": 2.09, # G
    "G": 2.03, # Y
    "P": 1.82, # P
    "B": 1.49,
    "V": 1.11,
    "K": 0.69, 
    "X": 0.17, # J
    "Q": 0.11, # X
    "J": 0.10, # Q
    "Z": 0.07
}

def decrypt(text, lan_map):
    # remove white space or empty string
    raw_text = ""
    for i in text.split():
        raw_text += i

    # count frequency
    time_occurs = {}

    for key in lan_map:
        time_occurs[key] = raw_text.count(key)

    # for key in raw_text:
    #     time_occurs[key] += 1
    
    for key in time_occurs:
        time_occurs[key] = round(time_occurs[key] / len(raw_text) * 100, 2)

    time_occurs = dict(sorted(time_occurs.items(), key=lambda x: x[1], reverse=True))

    temp1 = [i for i in lan_map]
    temp2 = [i for i in time_occurs]

    result = ""
    for key in text:
        count = False
        for i in range(len(temp2)):
            if temp2[i] == key:
                result += temp1[i]
                count = True
        if not count:  
            result += key

    return result


text = "YIFQFMZRWQFYVECFMDZPCVMRZWNMDZVEJBTXCDDUMJ \
NDIFEFMDZCDMQZKCEYFCJMYRNCWJCSZREXCHZUNMXZ \
NZUCDRJXYYMTMEYIFZWDYVZVYFZUMRZCRWNZDZJT \
XZWGCHSMRNMDHNCMFQCHZJMXJZWIEJYUCFWDINZDIR"


print(decrypt(text, en_map))
