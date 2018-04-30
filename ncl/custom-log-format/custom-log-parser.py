import os
import sys
import datetime
import ipaddress
with open("Custom File Format.sky", "rb") as raw:
    raw.seek(0)
    header={}
    header['magic']=raw.read(8).hex()
    header['ver']=int.from_bytes(raw.read(1), byteorder='big')
    header['created']=datetime.datetime.utcfromtimestamp(int.from_bytes(raw.read(4), byteorder='big'))
    host_len=int.from_bytes(raw.read(4), byteorder='big')
    header['hostname']=raw.read(host_len).decode('utf-8')
    flag_len=int.from_bytes(raw.read(4), byteorder='big')
    header['flag']=raw.read(flag_len).decode('utf-8')

    data=[]
    entries=int.from_bytes(raw.read(4), byteorder='big')
    for entry in range(0, entries):
        event={}
        event['src-addr']=ipaddress.IPv4Address(raw.read(4))
        event['dst-addr']=ipaddress.IPv4Address(raw.read(4))
        event['time']=datetime.datetime.utcfromtimestamp(int.from_bytes(raw.read(4), byteorder='big'))
        event['bytes']=int.from_bytes(raw.read(4), byteorder='big')
        data.append(event)

with open('header.txt', 'w') as HeadOut:
    for field in header.keys():
        if field == 'created':
            HeadOut.write(field+" : "+datetime.datetime.strftime(header[field], "%Y-%m-%d %H:%M:%S")+"\n")
        else:
            HeadOut.write(field+" : "+str(header[field])+"\n")

total=0
ipData={}
dayData={}
with open('body.csv', 'w') as body:
    body.write("src,dst,time,bytes\n")
    for event in data:
        body.write(str(event['src-addr'])+',')
        body.write(str(event['dst-addr'])+',')
        body.write(datetime.datetime.strftime(event['time'], "%Y-%m-%d %H:%M:%S")+',')
        body.write(str(event['bytes'])+"\n")
        total=total+event['bytes']
        if str(event['src-addr']) in ipData.keys():
            ipData[str(event['src-addr'])]+=event['bytes']
        else:
            ipData[str(event['src-addr'])]=event['bytes']
        if datetime.datetime.strftime(event['time'], "%Y-%m-%d") in dayData.keys():
            dayData[datetime.datetime.strftime(event['time'], "%Y-%m-%d")]+=event['bytes']
        else:
            dayData[datetime.datetime.strftime(event['time'], "%Y-%m-%d")]=event['bytes']

print(total)
with open("ip-totals.csv", 'w') as data:
    data.write("addr,bytes\n")
    for addr in ipData.keys():
        data.write(addr+","+str(ipData[addr])+"\n")

with open("date-totals.csv", 'w') as data:
    data.write("date,bytes\n")
    for day in dayData.keys():
        data.write(day+","+str(dayData[day])+"\n")