#gcloud compute networks subnets list > subnets.txt
#Fetching all the subnet details with the help of Gcloud SDK
range=($(gcloud compute networks subnets list | awk '{print $4}'  | tail -n+2))
vpc=($(gcloud compute networks subnets list | awk '{print $3}'  | tail -n+2))
regions=($(gcloud compute networks subnets list | awk '{print $2}'  | tail -n+2))
name=($(gcloud compute networks subnets list | awk '{print $1}'  | tail -n+2))

python3 yamlCreation.py "${range[@]}" "${vpc[@]}" "${regions[@]}" "${name[@]}"