## 用 docker 打软件包的 Dockerfile 仓库

### 基本使用方式
```sh
docker build --build-arg foo=doo --output 'type=local,dest=./dist/' .
```

## QA
- Q: Centos7报 `14: curl#6 - "Could not resolve host: mirrorlist.centos.org; Unknown error"` 怎么办？  
  A: 一些Dockerfile里面包含了加载repos文件夹的命令，如果没有可以自己加
