## 用 docker 打软件包的 Dockerfile 仓库

### 基本使用方式
```sh
docker build --build-arg foo=doo --output 'type=local,dest=./dist/' 
```