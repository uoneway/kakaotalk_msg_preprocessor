# kakaotalk_msg_preprocessor

카카오톡 대화창에서 `대화 내보내기`를 통해 export한 txt파일에 들어있는 메시지를 전처리해주는 라이브러리입니다.

주요 기능은 다음과 같습니다.

- 카카오톡에서 export한 txt파일로부터 메시지를 파싱하여 



## Guide

### Usage

````python
import kakaotalk_msg_tokenizer
````

#### 카카오톡 메시지 파싱하기

```python
# get the device type and language of kakaotalk_export_file
file_type = kakaotalk_msg_preprocessor.check_export_file_type(file_path)
print(file_type)

#  Parsing the text from a kaotalk_export_file
messages = kakaotalk_msg_preprocessor.parser(file_type, file_path)
print(messages)
```

예시 결과

```
window_ko
[{'datetime': datetime.datetime(2020, 6, 28, 1, 1), 'user_name': '김한길', 'text': '사진'}, {'datetime': datetime.datetime(2020, 6, 28, 1, 3), 'user_name': '김한길', 'text': '공부하기'}, 
{'datetime': datetime.datetime(2020, 8, 11, 2, 41), 'user_name': '김한길', 'text': '화 19:30-22:30\n\n\n자유석권(선착순)\n오후 6시 녹화장 앞 번호표대로 줄서기, 6시 50분부터 입장\n- 번호표 배부 : 녹화일 9:00 ~ 18:20까지 (입장순서가 부여된 방청권 선착순 배부)\n- 입장시간: 18시까지 녹화장 앞에서 번호표대로 줄서기(번호표 지참), 18:50부터 입장\n- 번호표 배부는 오후 6시 20분에 마감. 마감 이후에 오신 분들은 별도로 통제합니다'}, 
{'datetime': datetime.datetime(2020, 8, 11, 12, 3), 'user_name': '김한길', 'text': 'https://www.youtube.com'}]
```



#### 카카오톡 메시지에서 URL만 추출하기

```
url_messages = kakaotalk_msg_preprocessor.url_msg_extractor(file_type, messages)
print(url_messages)
```

예시 결과

```
[{'datetime': datetime.datetime(2020, 8, 11, 12, 3), 'url': 'https://www.youtube.com'}]
```



## 지원 export 파일 종류

카카오톡은 카카오톡 앱 실행 환경에 따라 상이한 형식의 txt파일을 export합니다.

현재 정상작동이 확인된 환경은 다음과 같습니다.

- 윈도우(OS언어: 한글)
- 안드로이드(OS언어: 한글)
- 안드로이드(OS언어: 영어)

