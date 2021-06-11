import yaml
import pprint
import sys
import os
"""
The objective of this script is to generate a yaml file for network configurations of Gcloud

A sample test value
ip=['10.231.0.0/16','10.239.128.0/17']
names=['a','b']
vpc=['a','b']
region=["us","asia"]

"""
#Fetching the network details from the gcloudShell script
networksDetails=(sys.argv)[1:]

#Splitting  the input into correct lists

lenSplit=len(networksDetails)

ip=networksDetails[0:lenSplit//4]
vpc=networksDetails[lenSplit//4:lenSplit//2]
region=networksDetails[lenSplit//2:3*(lenSplit//4)]
names=networksDetails[3*(lenSplit//4):]

# Creating the appropriate dict in python

targetsTen={}
targetsOneSevenTwo={}
targetsOneNineTwo={}
for i in range(0,len(ip)):
    ipRanges={}
    ipRanges["name"]=names[i]
    ipRanges["vpc"]=vpc[i]
    ipRanges["region"]=region[i]
    if ip[i].startswith('10.'):
        targetsTen[ip[i]]=ipRanges
    elif ip[i].startswith('172.'):
        targetsOneSevenTwo[ip[i]]=ipRanges
    else :
        targetsOneNineTwo[ip[i]]=ipRanges

finalDictOne={}
finalDictOne["root"]="10.0.0.0/8"
finalDictOne["display_attributes"]=["name","vpc","region"]
finalDictOne["targets"]=targetsTen

finalDictTwo={}
finalDictTwo["root"]="172.16.0.0/12"
finalDictTwo["display_attributes"]=["name","vpc","region"]
finalDictTwo["targets"]=targetsOneSevenTwo

finalDictThree={}
finalDictThree["root"]="192.168.0.0/16"
finalDictThree["display_attributes"]=["name","vpc","region"]
finalDictThree["targets"]=targetsOneNineTwo



#Generation of yaml from Dictionary
#print(yaml.dump(finalDict))

#Creating yaml files for all private subnets

file=open("ConfigOne.yaml","w")
yaml.dump(finalDictOne, file)
file.close()

file=open("ConfigTwo.yaml","w")
yaml.dump(finalDictTwo, file)
file.close()

file=open("ConfigThree.yaml","w")
yaml.dump(finalDictThree, file)
file.close()