# -*- coding: utf-8 -*-
"""Sentiment Analysis Models

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FOBTi5HK3ipfLMXNDm_yA5Ybjqix79wU

**Sentiment Analysis Using Vader Model**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')

import nltk

df = pd.read_csv('/content/random_tweets.csv')
print(df.shape)
df = df.head(500)
print(df.shape)

df.head()

ax = df['Retweets'].value_counts().sort_index() \
    .plot(kind='bar',
          title='Retweets for each tweets',
          figsize=(100, 30))
ax.set_xlabel('Retweets Count')
plt.show()

example = df['Text'][50]
print(example)

nltk.download('punkt')

nltk.download('averaged_perceptron_tagger')

nltk.download('maxent_ne_chunker')
nltk.download('words')

nltk.download('vader_lexicon')

tokens = nltk.word_tokenize(example)
tokens[:10]

tokens = nltk.word_tokenize(example)
tokens[:10]

tagged = nltk.pos_tag(tokens)
tagged[:10]

entities = nltk.chunk.ne_chunk(tagged)
entities.pprint()

from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm

sia = SentimentIntensityAnalyzer()

sia.polarity_scores('Today was such a beautiful day, I feel so blessed.')

sia.polarity_scores("Had a terrible day at work, can't wait to go home and forget about it")

sia.polarity_scores(example)

# Run the polarity score on the entire dataset
res = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    text = row['Text']
    myid = row['Tweet ID']
    res[myid] = sia.polarity_scores(text)

vaders = pd.DataFrame(res).T
vaders = vaders.reset_index().rename(columns={'index': 'Tweet ID'})
vaders = vaders.merge(df, how='left')

vaders.head()

import seaborn as sns
import matplotlib.pyplot as plt

# Divide Likes column by 1
vaders['Likes'] = vaders['Likes'] // 1

# Create count plot
ax = sns.countplot(data=vaders, x='Likes', hue='compound', palette='coolwarm', edgecolor='black')

# Set title and labels
ax.set_title('Count of compound sentiment score for each like')
ax.set_xlabel('Likes')
ax.set_ylabel('Count')
ax.legend(title='Compound', loc='upper right')

# Show plot
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Divide Likes column by 1
vaders['Likes'] = vaders['Likes'] // 1

# Create count plot
ax = sns.countplot(data=vaders, x='Likes', hue='pos', palette='coolwarm', edgecolor='black')

# Set title and labels
ax.set_title('Count of positive sentiment score for each like')
ax.set_xlabel('Likes')
ax.set_ylabel('Count')
ax.legend(title='pos', loc='upper right')

# Show plot
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Divide Likes column by 1
vaders['Likes'] = vaders['Likes'] // 1

# Create count plot
ax = sns.countplot(data=vaders, x='Likes', hue='neg', palette='coolwarm', edgecolor='black')

# Set title and labels
ax.set_title('Count of negetive sentiment score for each like')
ax.set_xlabel('Likes')
ax.set_ylabel('Count')
ax.legend(title='neg', loc='upper right')

# Show plot
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Divide Likes column by 1
vaders['Likes'] = vaders['Likes'] // 1

# Create count plot
ax = sns.countplot(data=vaders, x='Likes', hue='neu', palette='coolwarm', edgecolor='black')

# Set title and labels
ax.set_title('Count of neutral sentiment score for each like')
ax.set_xlabel('Likes')
ax.set_ylabel('Count')
ax.legend(title='neu', loc='upper right')

# Show plot
plt.show()





"""**Sentiment Analysis Using Roberta Model**"""

!pip install transformers
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

print(example)
sia.polarity_scores(example)

# Run for Roberta Model
encoded_text = tokenizer(example, return_tensors='pt')
output = model(**encoded_text)
scores = output[0][0].detach().numpy()
scores = softmax(scores)
scores_dict = {
    'roberta_neg' : scores[0],
    'roberta_neu' : scores[1],
    'roberta_pos' : scores[2]
}
print(scores_dict)

def polarity_scores_roberta(example):
    encoded_text = tokenizer(example, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_dict = {
        'roberta_neg' : scores[0],
        'roberta_neu' : scores[1],
        'roberta_pos' : scores[2]
    }
    return scores_dict

res = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    try:
        text = row['Text']
        myid = row['Tweet ID']
        vader_result = sia.polarity_scores(text)
        vader_result_rename = {}
        for key, value in vader_result.items():
            vader_result_rename[f"vader_{key}"] = value
        roberta_result = polarity_scores_roberta(text)
        both = {**vader_result_rename, **roberta_result}
        res[myid] = both
    except RuntimeError:
        print(f'Broke for id {myid}')

results_df = pd.DataFrame(res).T
results_df = results_df.reset_index().rename(columns={'index': 'Tweet ID'})
results_df = results_df.merge(df, how='left')



"""**Compare Scores between models**"""

results_df.columns

"""**Combine and compare**"""

import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))

sns.pairplot(data=results_df,
             vars=['vader_neg', 'vader_neu', 'vader_pos',
                  'roberta_neg', 'roberta_neu', 'roberta_pos'],
            hue='Likes',
            palette='tab10')
plt.show()



"""**The Transformers Pipeline**"""

from transformers import pipeline

sent_pipeline = pipeline("sentiment-analysis")

sent_pipeline('Feeling like a failure today, nothing seems to be going right.')

sent_pipeline('Feeling optimistic about the future, so many exciting things ahead!')

sent_pipeline("Enjoying a lazy Sunday at home, sometimes it's nice to do nothing.")