#!/usr/local/bin/python3

import requests
import csv
from bs4 import BeautifulSoup
import time

def read_apns(filename):
    apns=[]
    with open(filename,'r') as f:
        f.readline()
        for line in f:
            apn = line.split(',')[2]
            if apn == '':
                continue
            apns.append(apn)

    return apns

def query_apn(apn):
    res = requests.post('https://payments.sccgov.org/propertytax/Secured', params={'ParcelNumber': apn})
    soup = BeautifulSoup(res.text, features='html.parser')
    tags = soup.find_all(class_='col-sm-1 col-md-1 hidden-sm')

    counter=0
    property_tax=[0,0]
    for el in tags:
        if el.string is None:
            continue

        if '$' in el.string:
            property_tax[counter] = float(el.string.replace('$','').replace(',',''))
            counter += 1

        if counter==2:
            break

    return property_tax

def append_to_csv(f_out, apn, property_tax):
    f_out.write(str(apn))
    f_out.write(',')
    f_out.write(str(property_tax[0]))
    f_out.write(',')
    f_out.write(str(property_tax[1]))
    f_out.write(',')
    f_out.write(str(property_tax[0]+property_tax[1]))
    f_out.write('\n')

def main():
    parcel_filename = 'Santa_Clara_Station_APN.txt'
    output_filename = 'santa_clara_apn_property_tax.csv'

    print('Reading in apns...')
    apns = read_apns(parcel_filename)

    print('Clearing file...')
    with open(output_filename,'w') as f_out:
        f_out.write('')

    with open(output_filename,'a') as f_out:
        for i,apn in enumerate(apns):
            pt = query_apn(apn)
            print(str(i),'of',str(len(apns)),'|', apn, pt)
            append_to_csv(f_out, apn, pt)

if __name__=='__main__':
    main()
