#!/bin/bash

set -ex

# 进入脚本所在目录
cd "$(dirname "$0")"

# 检查证书是否存在
if [ ! -f "./cert/server.crt" ] || [ ! -f "./cert/server.key" ]; then
    echo "证书不存在，正在生成自签名证书..."
    mkdir -p cert
    openssl req -x509 -newkey rsa:2048 -nodes \
      -keyout cert/server.key \
      -out cert/server.crt \
      -days 3650 \
      -subj "/CN=localhost" \
      -addext "subjectAltName=DNS:localhost,DNS:*.local,IP:127.0.0.1"
    echo "证书生成完成"
fi

# 启动 Docker Compose
docker compose up -d

echo "Nginx 已启动"
echo "访问 https://localhost 测试"
echo "（浏览器会提示不安全，点击高级→继续访问即可）"