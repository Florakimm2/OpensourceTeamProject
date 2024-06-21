# 오픈소스프로그래밍 현민수팀  

## ✔️참고  

**논문**  
https://viewer.dcollection.net/originalViewer.jsp?streamdocsId=72059310428674398&mode=011

**참고한 사이트 및 깃허브**  
주요 참고 깃허브 :  
[[https://github.com/Ohhyeonseo/opencv.git](https://github.com/ukayzm/opencv.git)]

<br/>

**그 외 참고**  
- https://medium.com/@jongdae.lim/%EA%B8%B0%EA%B3%84-%ED%95%99%EC%8A%B5-machine-learning-%EC%9D%80-%EC%A6%90%EA%B2%81%EB%8B%A4-part-4-63ed781eee3c
- https://magicode.tistory.com/72

<br/>

### 📂파일별 설명 요약  

  
#### 😊face_recognition
- camera.py : 웹캠 작동 가능 여부를 확인하는 코드 파일
- face_recog.py : 웹캠 실행을 통해 knowns 파일에 있는 사람 얼굴을 인식해 얼굴에 표시하는 코드 파일
- live_streaming.py : 웹캠을 서버에 전송하는 코드파일로 face_recog에서 보여준 화면을 서버에서 보여준다.

  
#### ❓unknown_face_classifier
- face_classifier.py : 모르는 사람을 인식하고 한 번 인식된 사람은 아는 사람으로 재인식할 수 있도록 한다.

#### 🤖visitor_alarm_telegram_bot
- web cam에서 인식된 얼굴을 텔레그램 봇을 통해 인식된 얼굴 정보를 사용자에게 전달하는 코드가 들어있다.

<br/>

각 파일 README에 더 상세하게 기술해 놓았습니다. 

*학기 종료 후 사진파일은 삭제 예정*
