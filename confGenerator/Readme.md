# Config Map Generator for the Subnet Visualisation Tool


## How to use it 

- Install gcloud sdk and python 3
- Install dependency mentioned in requirements.txt
- run 'gcloud beta auth application-default login'
- Although this project can generate config file for all the project to which you have access but it takes more than 1 hour becaue there are more than 73 projects and data generated is too much. 
- it is advisied to replace the project id for your projject in line 91 inside the main function
- Run python3 configGenerator.py 
- The above commanad will generate the configFile