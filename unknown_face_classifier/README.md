# Unknown Face Classifier

**프로젝트는 Anaconda 가상 환경에서 이루어졌습니다**  

<br/>

- 파일이나 웹캠에서 비디오 읽기
- 프레임 안의 얼굴 감지
- 얼굴을 인코딩
- 인코딩을 이전에 저장된 얼굴과 비교
- 어떤 사람과 비슷한 인코딩일아면 그 사람의 얼굴을 저장
- 인코딩을 알 수 없는 얼굴과 유사할 경우 새 인물을 생성한다.
- 

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
* imutils 

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
- imutils


<br/>

사용한 깃허브 (https://github.com/ukayzm/opencv/tree/master/unknown_face_classifier) 
참고 : (https://ukayzm.github.io/python-face-recognition/)




