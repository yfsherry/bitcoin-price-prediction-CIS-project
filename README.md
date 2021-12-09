# bitcoin-price-prediction-CIS-project
# Prediction of Bitcoin Prices Using Machine Learning Algorithms and Sentiment Analysis

**ABSTRACT**

We harnessed machine learning to determine if sentiment extracted from Twitter and Reddit can be used as a proxy
for bitcoin price prediction. Our results show 
1) Aggregating sentiment derived from both Reddit and Twitter outperforms either standalone sentiment 
2) Model GRU was shown to be the best model performance with a RMSE of 56.97 
3) Model LSTM+CNN was shown to have unstable prediction performances on datasets with different characteristics.

**KEYWORDS**

Bitcoin price prediction · Sentiment Analysis · Long short-term memory (LSTM) · Gated recurrent unit (GRU) · 
Convolution neural network (CNN) & LSTM


**Introduction**

Publicly available data on Twitter and Reddit make it accessible to gain public moods that can be used to predict
future market trends (Mittal and Goel (2012); Lubitz (2017); Karalevicius et al. (2018)). Some work has showed social
signals have some interdependence with the Bitcoin economy. Garcia et al. (2014) showed a social feedback cycle based on
word-of-mouth effect and a user-driven adoption cycle, which reveals that users’ interest inspirations and some higher social
media activities drive Bitcoin prices up and then feedback on social influence. Li et al. (2019) firstly proved academically
that social media platforms such as Twitter can serve as powerful social signals for predicting price fluctuation in
alternative cryptocurrency market. Prajapati et al. (2020) examined predictive relationships between social media and
Bitcoin returns by considering the relative effect of different social media platforms.

Sentiment analysis (opinion mining) applying natural language processing and machine learning to detect emotional polarity
demonstrated by text is a popular methodology to predict Bitcoin prices based on social signals.APIs are available for sentiment
metrics extraction. Traditional dictionary-based methods may include Valence Aware Dictionary and Sentiment Reasoner (VADER) 
and TextBlob. VADER considers grammatical structures and is developed and tuned specifically for social media text data, 
available with vaderSentiment, which extracts polarity, subjectivity and compound metrics. TextBlob is a more general tool 
rather than merely for media sentiment, effective for extracting polarity and subjectivtity information. Among the most commonly 
used sentiment dictionaries, Loughran and McDonald sentiment divides the vocabulary into six categories, where involves 354 
optimistic words and 2329 pessimistic words. Since LM hardly misses the commonly used positive/negative vocabulary compared to
Henry’s dictionary and categories divided by LM is more rigorous than GI vocabulary's, we finally chose to implement pysentiment 
and TextBlob to extract sentiment polarity & subjectivity from texts with various lengths from whole documents, paragraphs, 
sentences to clauses. 

Moreover, we rebuilt other parameters into weighted moving average transformation. Considering 'retweets' in tweet dataset 
and 'upvotes' & 'downvotes' in reddit dataset, we captured the popularity information into sentiment factors by multiplying sentiment 
to the 'likes' & 'retweets' count and 'upvotes' minus 'downvotes' count. For the final step before tuning our parameters into 
deep learning networks, we implemented LightGBM to left our weak features. 


**Author**

Tong Li · Xi’an Jiaotong University · College of Mathematics and Statistics · litong1812@gmail.com
Pengfei Qiao · Southeast University · College of Computer Science · anesthetisa@gmail.com
Yuxuan Fu · East China Normal University · College of Economic Management · sherry_fu1002@163.com
Jiayi Yan · Qingdao No.2 Middle School · nanabeatrice@163.com

#
**Note**

Here we cited a paper https://arxiv.org/abs/2001.10343 by Pratikkumar Prajapati(2020) for tuning our parameters into LSTM, GRU and 
CNN networks. 

```
@misc{prajapati2020predictive,
    title={Predictive analysis of Bitcoin price considering social sentiments},
    author={Pratikkumar Prajapati},
    year={2020},
    eprint={2001.10343},
    archivePrefix={arXiv},
    primaryClass={cs.IR}
}
```
#
