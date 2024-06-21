# Unknown Face Classifier

**프로젝트는 Anaconda 가상 환경에서 이루어졌습니다**  

<br/>

- 파일이나 웹캠에서 비디오 읽기
- 프레임 안의 얼굴 감지
- 얼굴을 인코딩
- 인코딩을 이전에 저장된 얼굴과 비교
- 어떤 사람과 비슷한 인코딩일아면 그 사람의 얼굴을 저장
- 인코딩을 알 수 없는 얼굴과 유사할 경우 새 인물을 생성한다.

<br/>

* face_classifier.py - 웹캠 작동 확인
* person_db.py - 인식된 얼굴 데이터베이스 관련 코드

<br/><br/>

## ✔️코드 작동 방법
```
웹캠 버전 ( 웹 캠 작동 O )
$ python face_classifier.py 0 -d -s 0

비디오 버전 ( -i, -c 등과 같은 명령어에 오류 발생 )
$ python face_classifier.py -i <비디오 파일 경로> -t 0.4 -c -s 0.5
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
*conda install -c conda-forge 라이브러리_이름*
- opencv
- dlib
- face_recognition
- imutils
  
<br/>
## 🐹실행 결과
웹 캠을 통해 얼굴 인식 성공 시
* result 파일에 인식된 얼굴 폴더 생성 -> 폴더 이름 변경시 웹캠에 이름 변경되어 표시됨
* montage 이름의 사진 파일 생성  
![KakaoTalk_20240621_093550829](https://github.com/Florakimm2/OpensourceTeamProject/assets/63054274/73e05e37-69ad-4db2-8724-bc9f7f296d8b)
![image](https://github.com/Florakimm2/OpensourceTeamProject/assets/63054274/d33fc5eb-6a6c-4b1b-bd1c-046e39d31b53)




<br/><br/><br/>

사용한 깃허브 (https://github.com/ukayzm/opencv/tree/master/unknown_face_classifier) 
참고 : (https://ukayzm.github.io/python-face-recognition/)




