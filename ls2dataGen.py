import socket  # for little Endian encoding
import time

filename = 'mysampledata'
fobj = open(filename,'w')
ts_start=time.time()

frame_count = 10    # initial frame_count
frame_length = hex(socket.ntohs(173))[2:].upper()
counter = '01'
confirmation = '00'

initial_mframe = '0xf001'
mframe = initial_mframe
sframe = '0x1'
metrics = 20
max_frames = 1000
num_of_frames = 230

bdatatype ='40'
sframe = hex(socket.ntohl(int(sframe,16)))[2:].upper()
sframe = sframe.rjust(8,'0')
datasource = '0'*200
datalen = hex(socket.ntohs(2*metrics))[2:]    # little Endian encoding for 16bits integer
datablock = '0'*2*2*metrics
blkstatus = '0000'
tmstampl32 = 'E8DD686484010000'
tmstamph16 = '0000'
tmstampl32fly = 'E8DD686484010000'
tmstamph16fly = '0000'

for i in range(max_frames):
    fc_little_endian = hex(socket.ntohl(frame_count))[2:].upper()  # little Endian encoding for 32bits integer
    fc_little_endian = fc_little_endian.rjust(8,'0')  # add '0' to left if length less than 8 digits
    fobj.write('0100{}{}{}{}'.format(frame_length,fc_little_endian,counter,confirmation))
    
    mf = hex(socket.ntohl(int(mframe,16)))[2:].upper()
    mf = mf.rjust(8,'0')
    fobj.write('{}{}{}{}{}{}{}{}{}{}{}\n'.format(bdatatype,mf,sframe,datasource,datalen,datablock,blkstatus,tmstampl32,tmstamph16,tmstampl32fly,tmstamph16fly))
    
    frame_count += 1
    mframe = hex(int(mframe,16)+1)
    if i % num_of_frames == 0:
        mframe = initial_mframe

ts_end=time.time()
print('Time cost: ',ts_end-ts_start)
fobj.close()