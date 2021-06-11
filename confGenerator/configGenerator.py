from pprint import pprint
from sys import stderr
import yaml
import os

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# Global Color Index
globalIndex=["lightblue","DarkOrange","indianred","MediumSpringGreen","green","MediumAquaMarine","SpringGreen","YellowGreen","LawnGreen"]
colorIndex=0
# Global VPC Hashmap

globalVPC={}


def getProjects():
    projects=[]
    credentials = GoogleCredentials.get_application_default()
    service=discovery.build('cloudresourcemanager','v1',credentials=credentials)

    request =service.projects().list()
    response=request.execute()

    for project in response.get('projects', []):
            projects.append(project["projectId"])

    return projects

def getRegions(project: str):
    regions =[] 
    credentials = GoogleCredentials.get_application_default()
    service=discovery.build('compute','v1',credentials=credentials)

    request =service.regions().list(project=project)

    while request is not None:
        try:
            response=request.execute()

            for region in response['items']:
                regions.append(region['name'])
        
            request =service.regions().list_next(previous_request=request,previous_response=response)
        except:
            return []

    return regions

def getSubnets(project: str, region: str):
    targets={}
    credentials = GoogleCredentials.get_application_default()
    service=discovery.build('compute','v1',credentials=credentials)

    request =service.subnetworks().list(project=project, region=region)

    while request is not None:
        try:
            response=request.execute()
            for subnetwork in response['items']:
                temp={}
                #temp.push(subnetwork["ipCidrRange"])
                temp["Network"]=subnetwork["network"].split("networks/")[1]
                temp["Selflink"]=subnetwork["selfLink"]
                targets[subnetwork["ipCidrRange"]]=temp
            request = service.subnetworks().list_next(previous_request=request, previous_response=response)
        except:
            return {}
        return targets

def mergeDict(x, y):
    return {**x, **y}

def createYaml(fileName,dict):
    file=open(fileName,"w")
    yaml.dump(dict, file)
    file.close()


if __name__=="__main__":

    finalDict={}
    subnetDetails={}
    """
    Uncomment the following line is you want to run it across all projects
    projects=getProjects()
    """
    """
    Replace the project-id in the following list for which you want to generate config list
    """
    projects=['dev-ops-now']
    
    for project in projects:
        regions=getRegions(project)
        for region in regions:
            subnetDetails=mergeDict(getSubnets(project,region),subnetDetails)
    #pprint(subnetDetails['10.182.0.0/20']["Network"])
    
    for x in subnetDetails:
        if  subnetDetails[x]["Network"] in globalVPC.keys():
            subnetDetails[x]["color"]=globalVPC[subnetDetails[x]["Network"]]
        else:
            #global colorIndex
            subnetDetails[x]["color"]=globalIndex[colorIndex]
            globalVPC[subnetDetails[x]["Network"]]=subnetDetails[x]["color"]
            colorIndex=(colorIndex+1)%len(globalIndex)
    finalDict["root"]="0.0.0.0/0"
    finalDict["display_attributes"]=["Network","Selflink"]
    finalDict["targets"]=subnetDetails
    #pprint(globalVPC)


    createYaml("ConfigNewDemo.yaml",finalDict)
    