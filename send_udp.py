#!/usr/bin/env python

import math, socket, struct

# prepare UDP packet
#packetsize = 928
packetsize = 159
message = [ 0 for i in range( packetsize ) ]
#message = map(lambda x: struct.pack('>B',x), message)

host = '127.0.0.1'
#host = '10.130.3.129'
#host = '10.130.3.62'
#host = '10.130.3.44'
#port = 4000
port = 50000
#port = 51001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# init values
start_byte = 0
start_bit = 7
length = 16
factor = 1
offset = 0

def setdata( data_value, start_byte, start_bit, length, msg ):

    data_value = data_value << (start_bit+1)
    nbytes =  int( math.ceil((length + (start_bit+1))/8.0) )
    byte_mask = (2**length - 1) << (start_bit+1)

    for i in range(0, nbytes):
        j = nbytes - i - 1
        dat = (((2**8 - 1) << j*8) & data_value ) >> j*8 
        nmask = (((2**8 - 1) << j*8) & ~byte_mask ) >> j*8
        msg[start_byte + i] = (msg[start_byte + i] & nmask) | dat

    return msg

msg_data = message[:]
counter = 0

# loop
while True:

    print "\n** setup **************************************"
    try:
        msg = "start_byte("+str(start_byte)+") ="
        val = input( msg )
        start_byte = val
    except:
        pass

    if start_byte < 0:
        break

    try:
        msg = "start_bit("+str(start_bit)+") ="
        val = input( msg )
        start_bit = val
    except:
        pass

    if start_bit < 0:
        break
    try:
        msg = "length("+str(length)+") ="
        val = input( msg )
        length = val
    except:
        pass

    if length < 0:
        break

    try:
        msg = "factor("+str(factor)+") ="
        val = input( msg )
        factor = val
    except:
        pass

    try:
        msg = "offset("+str(offset)+") ="
        val = input( msg )
        offset = val
    except:
        pass

    print "***********************************************"

    while True:
        try:
            value = input( "\nvalue?" )
        except:
            break

        data = (value-offset) / factor
      #  print "data value="+str(data)

     #   print start_byte, value, data

        if length == 16: 
            packed = struct.pack('>H', data)
        elif length == 32: 
            packed = struct.pack('>I', data)

        packet = []
        packet_str = []

        for i in packed:
            packet_str.append( ord(struct.unpack('c',i)[0]) )
            packet.append( struct.unpack('c',i)[0] )

        #DEBUG
     #   print start_byte, packet_str
       # msg_data = "".join(packet)
        #print message,len(message) 

    #    msg_data = message
     #     for i in range(0, len(packet)):
     #       #  print start_byte+i, i, packet_str[i]
     #         msg_data[start_byte + i] = packet[i]

      #  msg_data = message   # ** incorrect **   see ref<1>

        message[56] = 0x00
        message[57] = 0xEE
#        message[58] = int(counter / 0x10) / 0x10
#        message[59] = counter % 0x100
        
        counter += 1 
        if counter > 0xffff:
          counter = 0

        message = setdata( value, start_byte, start_bit, length, message )

        #print message
        message_hex =  map(lambda x: hex(x), message)
      #  print message_hex
        message_dev =  [message_hex[i:i+10] for i in range(0, len(message), 8)]
      #  print message_dev
        for i,dat in enumerate(message_dev):
          print '{:03d}'.format(i*10), map(lambda x: '{:02x}'.format(int(x,16)), dat)


        msg_data = map(lambda x: struct.pack('>B',x), message)
        msg_data = "".join(msg_data)

        #print msg_data

        sock.sendto(msg_data, (host, port))

print "\nEND."


#references:
#<1> http://qiita.com/utgwkk/items/5ad2527f19150ae33322
