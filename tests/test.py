import sys
import os
import pandas as pd

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

import kakaotalk_msg_preprocessor

file_path_list =[TEST_DIR + "/datasets/KakaoTalk_export_file_exmple_window_kr.txt",
                TEST_DIR + "/datasets/KakaoTalk_export_file_exmple_android_kr.txt",
                TEST_DIR + "/datasets/KakaoTalk_export_file_exmple_android_en.txt",
                ]

if __name__ == '__main__':
    for file_path in file_path_list:
        print(f"------------{file_path} test start-------------------")
        file_type = kakaotalk_msg_preprocessor.check_export_file_type(file_path)
        print(file_type)
        
        messages = kakaotalk_msg_preprocessor.parse(file_type, file_path)
        print(messages)

        url_messages = kakaotalk_msg_preprocessor.url_msg_extract(file_type, messages)
        print(url_messages)

        input_df = pd.DataFrame.from_dict(url_messages)[['datetime', 'url']]
        input_df.rename(columns = {'datetime' : 'clip_at'}, inplace = True)
        print(input_df)