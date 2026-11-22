# USB 카메라 연결 및 영상 수신 오류 해결 기록

## 1. 개발 환경

본 프로젝트에서는 Microsoft LifeCam HD-3000 USB 카메라를 사용하여 책상 위 사물을 실시간으로 촬영한다.

개발 환경은 Windows 11과 WSL2 기반 Ubuntu 24.04이며, Ubuntu 환경에서 ROS2 Jazzy와 OpenCV를 이용하여 카메라 영상을 처리하도록 구성하였다.

### 개발 환경 및 장비

| 항목 | 내용 |
|---|---|
| 운영체제 | Windows 11 |
| 가상화 환경 | WSL2 |
| Linux 배포판 | Ubuntu 24.04 LTS |
| ROS2 | Jazzy |
| 카메라 | Microsoft LifeCam HD-3000 |
| 영상 처리 | OpenCV |
| USB 연결 도구 | usbipd-win |
| 카메라 인터페이스 | V4L2 |
| 카메라 장치 | /dev/video0 |

### 전체 카메라 연결 구조

```text
Microsoft LifeCam HD-3000
          |
          v
      Windows 11
          |
          v
       usbipd
          |
          v
        WSL2
          |
          v
   Ubuntu 24.04
          |
          v
   V4L2 (/dev/video0)
          |
          v
       OpenCV
          |
          v
  YOLOv8n + MediaPipe
          |
          v
       ROS2
          |
          v
       SQLite
```

## 2. 최초 발생 문제: Ubuntu에서 USB 카메라 인식 불가

초기 개발 과정에서 Windows에 연결된 USB 카메라가 Ubuntu 환경에서 정상적으로 인식되지 않는 문제가 발생하였다.

Windows와 WSL2는 USB 장치를 자동으로 공유하지 않기 때문에, Windows에 연결된 카메라를 Ubuntu에서 사용하려면 별도의 USB 장치 전달 과정이 필요했다.

### 원인

- Windows와 WSL2 사이에 USB 장치가 자동으로 전달되지 않음.
- Ubuntu에서 카메라 장치 파일(`/dev/video0`)을 확인할 수 없는 상태 발생.
- OpenCV에서 카메라를 열기 전에 USB 장치 연결부터 해결해야 하는 상황이었다.

### 해결 방법

`usbipd-win`을 사용하여 Windows에 연결된 USB 카메라를 WSL2의 Ubuntu로 전달하였다.

Windows PowerShell에서 관리자 권한으로 USB 장치를 공유하였다.

```powershell
usbipd bind --busid 3-3
```

이후 WSL2에 USB 장치를 연결하였다.

```powershell
usbipd attach --wsl --busid 3-3
```

Ubuntu에서 USB 장치 인식 여부를 확인하였다.

```bash
lsusb
```

이후 카메라 장치 파일을 확인하였다.

```bash
ls /dev/video*
```

확인 결과 `/dev/video0`가 실제 영상 캡처 장치로 확인되었다.

이를 통해 WSL2 Ubuntu 환경에서 USB 카메라를 사용할 수 있는 연결 구성을 완료하였다.

## 3. 두 번째 문제: 카메라 영상 수신 속도 및 안정성 저하

USB 카메라가 Ubuntu에서 인식된 이후에도 영상 수신 과정에서 추가적인 문제가 발생하였다.

### 발생 현상

- 프레임 속도를 높게 설정했을 때 실제 영상 수신 속도가 설정값에 도달하지 못함.
- 영상 수신 과정에서 select() timeout 오류 발생.
- Corrupt JPEG data 메시지와 함께 JPEG 데이터 손상 현상 발생.
- 일부 테스트에서는 영상 수신이 중단되는 문제 발생.

### 원인 분석

USB 카메라가 Ubuntu에 연결되는 것과 안정적으로 영상을 수신하는 것은 별개의 문제였다.

특히 WSL2의 USB/IP 전달 환경에서 해상도와 프레임 속도에 따라 영상 수신 성능이 달라지는 것을 확인하였다.

이에 따라 해상도와 영상 포맷을 변경하고, 프레임 속도별 수신 성능을 비교하는 실험을 진행하였다.

## 4. 영상 수신 설정 변경 및 FPS 비교 실험

카메라의 영상 출력 설정을 변경하여 수신 성능과 안정성을 비교하였다.

### 4.1 해상도 및 영상 포맷 변경

초기 640×480 해상도에서 약 2.3 FPS가 측정되어 해상도를 320×240으로 낮추었다.

영상 포맷은 MJPG를 사용하였다.

```bash
v4l2-ctl -d /dev/video0 --set-fmt-video=width=320,height=240,pixelformat=MJPG
```

이후 카메라의 프레임 속도를 10 FPS로 설정하였다.

```bash
v4l2-ctl -d /dev/video0 --set-parm=10
```

설정값은 다음 명령어로 확인하였다.

```bash
v4l2-ctl -d /dev/video0 --get-fmt-video
v4l2-ctl -d /dev/video0 --get-parm
```

### 4.2 V4L2 직접 스트리밍 테스트

OpenCV를 통한 영상 수신뿐만 아니라 V4L2를 이용한 직접 스트리밍 테스트도 진행하였다.

```bash
v4l2-ctl -d /dev/video0 --stream-mmap=3 --stream-count=300 --stream-to=/dev/null
```

초기 10 FPS 설정에서 약 10.1 FPS의 수신
