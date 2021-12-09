import re
import sys
import pandas as pd
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob
import pysentiment as ps
from datetime import datetime

def preprocess_word(word):
    # Remove punctuation
    word = word.strip('\'"?!,.():;')
    # Convert more than 2 letter repetitions to 2 letter
    # funnnnny --> funny
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - & '
    word = re.sub(r'(-|\')', '', word)
    return word


def is_valid_word(word):
    '''
    判断是否是英文单词/英文字母打头
    '''
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)


def handle_emojis(tweet):
    '''
    处理tweet中字符表情
    '''
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return tweet


def preprocess_tweet(tweet):
    '''
    处理tweet中文本
    '''
    processed_tweet = []
    # 转小写
    tweet = tweet.lower()
    # 替换所有URL
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', tweet)
    # @
    tweet = re.sub(r'@[\S]+', 'USER_MENTION', tweet)
    # tag#
    tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
    # 转发
    tweet = re.sub(r'\brt\b', '', tweet)
    # 逗号
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # 引号
    tweet = tweet.strip(' "\'')
    # 字符表情
    tweet = handle_emojis(tweet)
    # 空格缩进
    tweet = re.sub(r'\s+', ' ', tweet)
    words = tweet.split()

    for word in words:
        word = preprocess_word(word)
        if is_valid_word(word):
            # 同根词 去掉单词后缀
            # word = str(porter_stemmer.stem(word))
            processed_tweet.append(word)

    return ' '.join(processed_tweet)


def analyze_sentiment_LM(text):
    '''
    LM字典返回情感分
    '''
    #初始化LM字典
    lm = ps.LM()
    #分词得到词语列表tokens
    words = lm.tokenize(text)
    #将词语列表words传入lm.get_score，得到得分score
    score = lm.get_score(words)
    return score

def analyze_sentiment_textblob(text):
    '''
    textblob返回情感分
    '''
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def preprocess_csv(csv_file_name, processed_file_name, df):
    '''
    读取csv提取文本并存储df中
    '''
    save_to_file = open(processed_file_name, 'w')

    with open(csv_file_name, 'r') as csv:
        lines = csv.readlines()
        i = 0
        while i < len(lines):
            line = lines[i]

            parameters = line.split(";")
            # print("读取第 %d行" %i)
            # print(line)
            # print(len(parameters))
            for index in range(len(parameters)):
                if index > 8:
                    parameters[8] = parameters[8] + " " + parameters[index]
            del parameters[9:]
            t = 1
            flag = False
            while True:
                # if (lines[i+t]) == ",,,,,\n":
                #     t += 1
                #     continue
                # print(lines[i+t])
                if i+t >= len(lines):
                    break;
                if len(lines[i+t].split(";")) < 9:
                    parameters[8] += lines[i+t]
                    t = t + 1
                    flag = True
                else:
                    break;

            if flag is True:
                i = i + t - 1
            # print(parameters)
            # print(len(parameters))
            # print("***********************")

            i += 1
            parameters[8] = preprocess_tweet(parameters[8])
            SA = analyze_sentiment_textblob(parameters[8])
            # SA = analyze_sentiment_LM(parameters[8])
            new = pd.DataFrame({'time': parameters[4],
                  'id': parameters[0],
                  'replies': parameters[5],
                  'likes': parameters[6],
                  'retweets': parameters[7],
                  'body': parameters[8],
                  'SA':SA['Polarity']}, index=[1])
            df = df.append(new, ignore_index=True)   # ignore_index=True,表示不按原来的索引，从0开始自动递增

    save_to_file.close()
    return df


if __name__ == '__main__':
    csv_file_name = "Tsample.csv"
    processed_file_name = "Tresult.csv"
    porter_stemmer = PorterStemmer()
    df = pd.DataFrame([], columns=['time','id','replies','likes','retweets','body','SA'])
    df = preprocess_csv(csv_file_name, processed_file_name, df)
    df = df.drop(0,axis=0,inplace=False)

    # df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d')
    df['time'] = pd.to_datetime(df['time']).dt.date
    print(df)
    df = df.sort_values(by='time')
    data_group = df.groupby(['time']).sum()
    print(data_group)
    df.to_csv("Tresult2.csv", index=False)
