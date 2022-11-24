import sys

def init_header(fobj):
    fobj.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    fobj.write('<configuration>\n\n')
    fobj.write('\t<scope>\n')
    fobj.write('\t\t<scope id="1" experiment="*" test="*" step="*"/>\n')
    fobj.write('\t</scope>\n\n')
    return
    
    
filename = 'myconfig.xml'
fobj = open(filename,'w')
init_header(fobj)
mframe='f001'
sframe='1'
gmetricid=1
fno=230
mno=20

fobj.write('\t<frames>\n')
for i in range(fno):
    fobj.write('\t\t<mainframe id="{}" type="FREQUENCY" scope="1">\n'.format(hex(int(mframe,16))))
    mframe = hex(int(mframe,16)+1)
    fobj.write('\t\t\t<subframe id="{}">\n'.format(hex(int(sframe,16))))
    for j in range(mno):
        pos=j*2
        fobj.write('\t\t\t\t<metric name="参数{}" id="{}">\n'.format(gmetricid,j+1))
        fobj.write('\t\t\t\t\t<input byteSeq="{}" byteLength="2" dataType="UINT16" byteOrder="LWLB" sequenceValue=""/>\n'.format(pos))
        fobj.write('\t\t\t\t\t<formula expression="" outVariable="" updateFlag=""/>\n')
        fobj.write('\t\t\t\t\t<bound upper="" lower=""/>\n')
        fobj.write('\t\t\t\t\t<output dataType="INT32" unit="" referenceValue="" property="ANALOG"/>\n')
        fobj.write('\t\t\t\t</metric>\n')
        gmetricid += 1
    fobj.write('\t\t\t</subframe>\n')
    fobj.write('\t\t</mainframe>\n')
fobj.write('\t</frames>\n')
fobj.write('</configuration>')

fobj.close()