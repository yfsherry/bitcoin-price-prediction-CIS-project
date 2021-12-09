import re
import numpy as np
import pandas as pd
from textblob import TextBlob


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

def clean_txtbody(tweet):
    try:
        tweet = BeautifulSoup(tweet, 'lxml')
    except:
        tweet = tweet

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

    return tweet

def analyze_sentiment(tweet):
    '''
    textblob返回情感分
    '''
    analysis = TextBlob(tweet)
    return analysis.sentiment.polarity


def preprocess_csv(csv_file_name, df):
    '''
    读取csv提取文本并存储df中
    '''
    with open(csv_file_name, 'r', encoding='utf-8') as csv:
        lines = csv.readlines()
        i = 1
        while i < len(lines):
            line = lines[i]
            print(line)
    return df

if __name__ == '__main__':
    csv_file_name = 'Rsample.csv'
    df = pd.DataFrame([], columns=['index','date','username','score','body','SA'])
    # dataset = preprocess_csv(csv_file_name, df)

    dataset = pd.read_csv("Rsample.csv")
    columns_to_be_removed = ['subreddit','created_utc','controversiality']
    dataset = dataset.drop(columns_to_be_removed, axis=1, inplace=True)
    dataset = dataset.drop(0,axis=0,inplace=False)
    print(dataset)
    # assert()
    dataset['body'] = dataset['body'].apply(clean_txtbody)
    # dataset['body'] = clean_txtbody(dataset['body'])

    dataset['SA'] = np.array([analyze_sentiment(tweet) for tweet in dataset['body'].astype(str)])

    dataset['date'] = pd.to_datetime(dataset['date'], errors='coerce')
    dataset['date'] = pd.to_datetime(dataset['date']).dt.date

    dataset = dataset.sort_values(by ='date')
    print(dataset)

    data_group = dataset.groupby(['date']).sum()
    print(data_group)
    '''
    按日期排序后相同时间的数据并列显示
    data_group = dataset.groupby(['date'])
    new_data = pd.DataFrame(columns=['date','author','score','body','SA'])
    # 循环拼接
    for key, value in data_group:
        new_data = pd.concat([new_data, value])
    new_data.index = np.arange(len(new_data.index))
    print(new_data)
    '''

    dataset.to_csv("Rresult2.csv", index=False)

