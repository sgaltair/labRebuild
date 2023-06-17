Temp readme:

Runs once per minute

Useage:

```
docker run --name vhostPop -d -v /path/to/containers:/app/containers \
    -v /path/to/vhost.d:/app/containers/nginx/vhost.d \
    -v /path/to/vhostPopConfig.py:/app/vhostPop/vhostPopConfig.py \
    isame\vhostProp
```
