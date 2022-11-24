import socket  # for little Endian encoding
import binascii
from binascii import unhexlify,hexlify
from crcmod import mkCrcFun
import time

def hex_to_little_endian(hex_string):
    little_endian_hex = bytearray.fromhex(hex_string)[::-1]
    return little_endian_hex

# generate crc code
def get_crc(s):
    data = s.replace(' ', '')
    crc_out = crc16_xmodem(unhexlify(data))
    cv = hex(socket.ntohs(crc_out))[2:].upper().rjust(4,'0')  # convert to little Endian encoding
    return cv

def ls2send(s):  # calculate crc, merge msg+crc and send out
    crc_value = get_crc(s)
    bmsg = unhexlify(s+crc_value)
    sock.sendto(bmsg, (UDP_IP, UDP_PORT))

max_frames = 3000000
sleep_duration = 1  # milliseconds
sleep_every_msgs = 20  # sleep after given number of messages sent 

UDP_IP = "127.0.0.1"  # lingshu2 server IP address
UDP_PORT = 10100  # lingshu2 server listening UDP port
crc16_xmodem = mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)  # initialize crc16-xmodem function via mkCrcFun

ts_start=time.time()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

fobj = open('start','r')
msg = fobj.readline()
fobj.close()
ls2send(msg)  # fire off first line - start experiment
bytes_sent = len(msg)/2+2

frame_count = 10    # initial frame_count
metrics = 20  # all metrics are uint16 ANALOG
num_of_frames = 345
frame_length = hex(socket.ntohs(133+2*metrics))[2:].upper()
counter = '01'
confirmation = '00'
initial_mframe = '0xf001'
mframe = initial_mframe
sframe = '0x1'

bdatatype ='40'
sframe = hex(socket.ntohl(int(sframe,16)))[2:].upper()  # little Endian encoding for 32bits integer
sframe = sframe.rjust(8,'0')
datasource = '0'*200
datalen = hex(socket.ntohs(2*metrics))[2:]    # little Endian encoding for 16bits integer
datablock = '0'*2*2*metrics
blkstatus = '0000'
# tmstampl32 = 'E8DD686484010000'
# tmstamph16 = '0000'
# tmstampl32fly = 'E8DD686484010000'
# tmstamph16fly = '0000'

for i in range(max_frames):
    fc_little_endian = hex(socket.ntohl(frame_count))[2:].upper()  # little Endian encoding for 32bits integer
    fc_little_endian = fc_little_endian.rjust(8,'0')  # add '0' to left if length less than 8 digits
    msg='0100'+frame_length+fc_little_endian+counter+confirmation  # communication frame head,  10 Bytes
    
    mf = hex(socket.ntohl(int(mframe,16)))[2:].upper()
    mf = mf.rjust(8,'0')
    
    ms = hex(int(time.time()*1000))[2:].upper().rjust(16,'0')  
    us = hex(int(str(time.time_ns())[-6:-3]))[2:].upper().rjust(4,'0')  # acquire microsecond and transfer to hex
    
    tmstampl32 = hexlify(hex_to_little_endian(ms)).decode('utf-8')
    tmstamph16 = hexlify(hex_to_little_endian(us)).decode('utf-8')
    tmstampl32fly = tmstampl32
    tmstamph16fly = tmstamph16
    
    msg += bdatatype+mf+sframe+datasource+datalen+datablock+blkstatus+tmstampl32+tmstamph16+tmstampl32fly+tmstamph16fly
    ls2send(msg)  # fire off payload
    bytes_sent += len(msg)/2+2
    
    frame_count += 1
    mframe = hex(int(mframe,16)+1)
    if i % num_of_frames == 0:
        mframe = initial_mframe
    if i % sleep_every_msgs == 0:
        time.sleep(sleep_duration/1000)

fobj = open('end','r')
msg = fobj.readline()
fobj.close()
ls2send(msg)  # fire off last line - ending experiment
bytes_sent += len(msg)/2+2

sock.close()
ts_end=time.time()

print('Frames sent: {}    Bytes sent: {}'.format(max_frames+2, bytes_sent))
print('Time cost: ',ts_end-ts_start)
