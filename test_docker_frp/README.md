# 内网穿透案例

## frps

使用 `theanony/frp` 镜像，它包含多用户管理的插件

```
cd frps
docker compose up -d
```

在 `frps/tokens` 中增减授权的用户

## frpc

可以使用 `fatedier/frpc` 镜像，它支持多种平台

```
cd frpc
docker compose up -d
```
