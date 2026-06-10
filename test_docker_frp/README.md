# 内网穿透案例

## frps

```
# 启动容器
docker run -d --name=frps \
  --restart=always \
  --network host \
  -v /etc/frp/frps.toml:/etc/frp/frps.toml \
  snowdreamtech/frps
```

## frpc

```
docker run -d --name=frpc-b \
  --restart=always \
  --network host \
  -v /etc/frp/frpc-b.toml:/etc/frp/frpc.toml \
  snowdreamtech/frpc
```