# Ensure env vars are set



```
set -a # automatically export all variables
source .env
set +a
```


Check:
```
printenv | grep AZURE
```