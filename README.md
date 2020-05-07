# ochestration_for_docker

#### docker daemon

```sh
$ sudo gedit /etc/systemd/system/multi-user.target.wants/docker.service

# 내용 수정
.
.
.
# ExecStart=/usr/bin/dockerd -H fd:// # 변경 전
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375 # 변경 후
.
.
.

$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
$ docker -H 서버IP:포트 명령어
```





#### mongoDB start

```sh
$ sudo systemctl start mongod

```

