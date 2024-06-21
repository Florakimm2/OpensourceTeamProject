# Face Recognition

**프로젝트는 Anaconda 가상 환경에서 이루어졌습니다**  

<br/>

웹캠 비디오를 실시간으로 인식하여 사람 이름과 함께 표시한다.

* camera.py - 웹캠 작동 확인
* face_recog.py - 웹캠으로 얼굴을 인식한다.
* live_streaming.py - http://IP_addr:5000/ 를 통해 비디오 전송  

<br/><br/>

## ✔️코드 작동 방법
```
$ python camera.py
$ python face_recog.py
$ python live_streaming.py
```  
<br/><br/>

## 📂필요 라이브러리
* opencv-python
* opencv-contrib-python
* dlib (CMake 다운로드가 필요합니다.)
* face_recognition
* flask  

<br/><br/>

### ✊Anaconda 가상 환경에서 오류 발생시 라이브러리 다운
opencv-python과 opencv-contrib-python은 적용되지 않아 pip install로 다운 받아야함  

<br/>

**그 외 conda install을 사용해야하는 라이브러리**
###### pip install로 진행하니 오류가 발생해서 다른 방법을 찾아본 결과 conda install로 진행

<br/>

*conda install -c conda-forge 라이브러리_이름*
- opencv
- dlib
- face_recognition
- flask  

<br/><br/>

## 💻코드 수정 : face_recog
##### 발생 오류 : RuntimeError: Unsupported image type, must be 8bit gray or RGB image.

**해결 방법**
```
28번째 줄에 추가
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

49번째 줄 수정
rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
```
<br/>
**실행 결과**  

![face_recog2](https://github.com/Florakimm2/OpensourceTeamProject/assets/63054274/673c7633-7d4d-440d-82c1-7d74c892560b)

<br/><br/>

###### 제대로 수정한 것인지 확실하지는 않지만 얼굴 인식은 잘 이루어졌음

<br/>

사용한 깃허브 [https://github.com/ukayzm/opencv/tree/master/face_recognition]  
참고 : (https://ukayzm.github.io/python-face-recognition/)
