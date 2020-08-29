
## login
```
az login
```

# create resource group
```
az group create --location westeurope --resource-group PruebasMarcial
az group list
```

## monitoring plugin
Needed for `--enable-addons monitoring` on the cluster
```
az provider register --namespace Microsoft.OperationsManagement
az provider register --namespace Microsoft.OperationalInsights
```

### check
```
az provider show -n Microsoft.OperationalInsights
az provider show -n Microsoft.OperationalInsights -o table
az provider show -n Microsoft.OperationsManagement -o table
```

# create acr
```
az acr create --resource-group PruebasMarcial --name ACRMarcial --sku Basic
az acr login --name ACRMarcial
```

# create cluster
```
az aks create --resource-group PruebasMarcial --name ClusterMarcial --node-count 1 --enable-addons monitoring --generate-ssh-keys  # --attach-acr <acrName>
```

## update current aks with acr integration
```
az aks update -n ClusterMarcial -g PruebasMarcial --attach-acr ACRMarcial
```


## get creds
```
az login
az aks get-credentials --resource-group PruebasMarcial --name ClusterMarcial
```

## get nodes
```
kubectl get nodes
```

# setting the app

## app local (compose)
https://docs.microsoft.com/es-es/azure/aks/tutorial-kubernetes-deploy-application

```
create images with docker-compse build
docker-compose up -d

docker images

docker-compose down
```
Needs the images names to create the tags for acr.

## tag images
Get name acr login server with:
```
az acr list --resource-group PruebasMarcial --query "[].{acrLoginServer:loginServer}" --output table
```

Use it:
```
docker tag dummy-project_app acrmarcial.azurecr.io/test-sep-app:v1
docker images

>   REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
>   acrmarcial.azurecr.io/test-sep-app   v1                  16e1421d442e        42 minutes ago      95.3MB
>   dummy-project_app                    latest              16e1421d442e        42 minutes ago      95.3MB
```

## push images to acr
```
docker push acrmarcial.azurecr.io/test-sep-app:v1
az acr repository list --name ACRMarcial --output table
# az acr repository show-tags --name ACRMarcial --repository test-sep-app --output table
>   Result
>   ------------
>   test-sep-app
```

## delete repository
```
az acr repository delete --name ACRMarcial --repository test_sep_app
```

## update manifest with the acr loginserver
use the login server (acrmarcial.azurecr.io/test-sep-app) in the yaml file.

## apply
```
kubectl apply -f azure-app.yaml
```

## check launch
```
kubectl get service test-sep-app --watch
```