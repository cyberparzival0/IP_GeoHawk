def padIPv6s(ip: str):
    #print(ip)
    if ":" in ip:
        final = ""
        chunks = ip.split(":")
        middle = 8 - (len(chunks) - 1)
        ptr = 0

        while ptr != len(chunks):
            lengthChunk = len(chunks[ptr])
            chunk = chunks[ptr]

            if lengthChunk == 0:
                final += "0000:" * middle
            else:
                while lengthChunk != 4:
                    chunk = "0" + chunk
                    lengthChunk += 1
                final += chunk
                if ptr != len(chunks) - 1:
                    final += ":"
            ptr += 1
        #print(final)
        return final
                    
    else:
        return ip

#print(padIPv6s('2606:4700::6810:f9f'))
#print(padIPv6s('2606:4700:0:0:0:0:6810:f9f'))
