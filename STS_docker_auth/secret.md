
SECRET:

If you are using Kubernetes, and you need it for creating the registry password just run:

kubectl create secret docker-registry --dry-run=true docker-regcred \
--docker-server=https://index.docker.io/v1/ \
--docker-username=xxx \
--docker-password=xxx \
--docker-email=yourmail@yourdomain.com \
--namespace=xxx \
-o yaml > docker-secret.yaml

This will create docker-secret.yaml with your JSON there. if you dont include --dry-run and -o yaml > docker-secret.yaml It will create the k8s secret.




