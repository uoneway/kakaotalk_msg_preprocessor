import re
from datetime import datetime

# kakaotalk 메시지 중 날짜표현 패턴
# 이를 사용하여 파일이 추출된 소스와 메시지 구분과 
kakaotalk_datetime_pattern_dict = {'window_ko_date': "-{15} [0-9]{4}년 [0-9]{1,2}월 [0-9]{1,2}일 \S요일 -{15}",
                                'window_ko_time': "((\[)([^\[])+(\])) ((\[오)\S [0-9]{1,2}:[0-9]{1,2}(\]))",
                                'android_ko': "([0-9]){4}년 ([0-9]){1,2}월 ([0-9]){1,2}일 오\S ([0-9]){1,2}:([0-9]){1,2}",
                                'android_en': "([A-z])+ ([0-9]){1,2}, ([0-9]){4}, ([0-9]){1,2}:([0-9]){1,2} \SM",
                                    }

def check_export_file_type(file_path,
                            datetime_pattern_dict=kakaotalk_datetime_pattern_dict):
    """
    Check the device type and language of kakaotalk_export_file.
    It is done based on datetime patterns in file
    
    Parameters
    ----------
    file_path: string

    datetime_pattern_dict: dict
        datetime_pattern used i kaotalk_export_file

    Returns
    -------
    file_type: string
        one of among 'window_ko', 'android_ko' or 'android_en'
    """

    # 파일의 두 번째 줄(저장한 날짜 : /Date Saved : ) 부분의 날짜형식으로 구분
    # kakaotalk_include_date_pattern_dict = {'pc_ko': "([0-9]){4}-([0-9]){1,2}-([0-9]){1,2} ([0-9]){1,2}:([0-9]){1,2}",
    #                             'mobile_ko': "([0-9]){4}년 ([0-9]){1,2}월 ([0-9]){1,2}일 오\S ([0-9]){1,2}:([0-9]){1,2}",
    #                             'mobile_en': "([A-z])+ ([0-9]){1,2}, ([0-9]){4}, ([0-9]){1,2}:([0-9]){1,2} \SM",}
    
    with open(file_path, 'r') as f:
        for counter in range(5):
            line = f.readline()
            if not line: break

            for file_type, pattern in datetime_pattern_dict.items():
                if re.search(pattern, line):
                    
                    return '_'.join(file_type.split('_')[:2])
    
    print("Error: Cannot know the device type and language of the file.\n",
          f"Please check the file is a kakaotalk export file or the export enviroment is in among {str(list(kakaotalk_include_date_pattern_dict.keys()))}")



    

def _str_to_datetime(file_type, text):
    kakaotalk_strptime_pattern_dict = {'ko': '%Y년 %m월 %d일 %p %I:%M',
                                        'en': '%B %d, %Y, %I:%M %p',
                                        }

    language = file_type.split('_')[1]
    if language == 'ko':
        text = text.replace('오전', 'AM')
        text = text.replace('오후', 'PM')

    text_dt = datetime.strptime(text, kakaotalk_strptime_pattern_dict[language])
    return text_dt


def parser(file_type, file_path,
                datetime_pattern_dict=kakaotalk_datetime_pattern_dict):
    """
    Parsing the text from a kaotalk_export_file.
    This parser divide messages based on datetime_pattern.
    
    Parameters
    ----------
    file_type: string
        one of among 'window_ko', 'android_ko' or 'android_en'

    file_path: string

    datetime_pattern_dict: dict
        datetime_pattern used i kaotalk_export_file

    Returns
    -------
    msgs: list
        The messages are list of dictionary.
        Each dictionary compose of the informtion of each message.
        And it has keys, 'datetime,'user_name' and 'text'.
    """

                                        
    msgs = []

    if file_type == 'window_ko':     # window
        date_pattern = datetime_pattern_dict['window_ko_date']
        time_pattern = datetime_pattern_dict['window_ko_time']

        with open(file_path) as file: 
            # 줄바꿈되어있는 경우도 묶어주기 위해 buffer 사용
            buffer = ''
            date = ''

            for line in file:
                # window파일의 데이트str(--------------- 2020년 6월 28일 일요일 ---------------)이거나 시간 str([김한길] [오후 2:15] htt)이면
                if re.match(date_pattern, line) or re.match(time_pattern, line):
                    # buffer가 time_pattern으로 시작하는 경우만 추가해주기
                    if re.match(time_pattern, buffer):  
                        buffer_tokens = buffer.split(']', maxsplit=2)
                        user_name = buffer_tokens[0].replace('[', '').strip()
                        time = buffer_tokens[1].replace('[', '').strip()
                        my_datetime = _str_to_datetime(file_type, f"{date} {time}")
                        text = buffer_tokens[2].strip()
                        
                        msgs.append({'datetime': my_datetime,
                                        'user_name': user_name,
                                        'text': text
                        })

                    if re.match(date_pattern, line):  # window파일의 데이트str이면
                        date = line.replace('-', '').strip().rsplit(" ", 1)[0]
                        buffer = ''
                    else:  #  window파일의 시간 str이면
                        buffer = line

                else:
                    buffer += line

    else: # android
        datetime_pattern = datetime_pattern_dict[file_type]
        msg_exist_check_pattern = datetime_pattern + ",.*:"
        
        with open(file_path) as file: 
            # 줄바꿈되어있는 경우도 저장하기 위해 buffer 사용
            buffer=''
            for line in file:
                if re.match(datetime_pattern, line):
                    if re.match(msg_exist_check_pattern, buffer):
                        
                        temp_01_2_tokens = buffer.split(" : ", maxsplit=1)
                        temp_0_1_tokens = temp_01_2_tokens[0].rsplit(",", maxsplit=1)

                        my_datetime = temp_0_1_tokens[0].strip()
                        my_datetime = _str_to_datetime(file_type, my_datetime)
                        user_name = temp_0_1_tokens[1].strip()
                        text = temp_01_2_tokens[1].strip()
                        msgs.append({'datetime': my_datetime,
                                    'user_name': user_name,
                                    'text': text
                        })

                    buffer = line
                else:
                    buffer += line
    
    return msgs


def _url_extractor(text):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = re.findall(regex, text)
    return urls


def url_msg_extractor(file_type, msgs):
    url_msgs = []
    for msg in msgs:
        text = msg['text']

        urls = _url_extractor(text)
        if urls:
            for url in urls:
                url_msgs.append({'datetime': msg['datetime'],
                                'user_name': msg['user_name'],
                                'url': ''.join(url)
                })

    return url_msgs