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



### Mosquitto using docker

```sh
$ sudo docker pull ansi/mosquitto
$ sudo docker run -p 1883:1883 --name mosquitto -d ansi/mosquitto
```



#### mongoDB start

```sh
$ ps aux | grep -i uwsgi
$ sudo netstat -tulpn | grep LISTEN
$ sudo kill -9 {number}
$ sudo systemctl start mongod
```



#### Ngrox start

```sh
# ngrok 위치로 가서
$ ./ngrok http 8080

```

