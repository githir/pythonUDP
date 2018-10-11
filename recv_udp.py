#!/usr/bin/env python

#from __future__ import print_function
import socket, struct
from contextlib import closing

def main():
  host = '127.0.0.1'
  #host = '10.130.3.44'
#  port = 4000
  port = 50000
  bufsize = 4096

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  with closing(sock):
    sock.bind((host, port))
    while True:
      data = sock.recv(bufsize)
      data = map( lambda x: struct.unpack('>B',x)[0], data)
      print data
 #     print(sock.recv(bufsize))
  return

if __name__ == '__main__':
  main()


#references:
# http://memo.saitodev.com/home/python_network_programing/#udp
