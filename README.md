# ochestration_for_docker

* **목적** **:** 엣지 디바이스에의 docker container image 설치를 지원하는 
   서버 - 클라이언트 어플리케이션 작성 (서버 1종, 클라이언트 1종)

* **제약** **:** NAT Traversal issue로부터 자유로울 것

* **방법** **:** MQTT + Flask socket io 사용



   **클라이언트** **-** **서버** **프로로콜** **상세**

1. 클라이언트는 엣지 노드에서 실행시 MQTT Topic에 자기 자신 등록

2. 서버는 엣지 노드로부터 전달된 등록 요청에 의거하여 기기 정보 DB에 저장

3. 서버는 엣지 노드에 hello-world 컨테이너 설치를 요청. 이 때 서버는 클라이언트에 컨테이너 URL 및 설치 명령만 전송.

4.클라이언트는 명령에 의거하여 docker run … 명령을 로컬에서 실행

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

#### Python Library

```sh
$ pip install paho-mqtt

```