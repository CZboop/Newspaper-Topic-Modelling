# running some basic positive/negative sentiment analysis on the different news sources
# and subjectivity analyis
# comparing over time
from data_processor import DataProcessor
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd

class SentimentAnalyser:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.data_processor.read_and_concat_data_files()
        # passing in a data processor object to handle reading data instead of repeating logic
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe('spacytextblob')

    def analyse_sentiment_and_subjectivity(self):
        # init will create .combined_data within the self.data_processor
        self.data_df = self.data_processor.combined_data
        headlines = self.data_df['headline'][:50]
        sentiment_and_subjectivity = headlines.apply(lambda x: self.nlp(str(x))) # returns an object with sent, subj, etc. info
        print(sentiment_and_subjectivity)
        # TODO: extract the individual pieces of data into own columns in df, avoid running expensive processes twice
        # ._.blob.polarity and ._.blob.subjectivity
        # self.data_df['sentiment'], self.data_df['subjectivity'] =
        # return self.data_df['sentiment']

    def get_sentiment_ratio(self):
        pass

    def plot_ratios(self):
        pass

    def get_sentiment_over_time(self):
        pass

    def plot_sent_over_time(self):
        pass

    def save_as_json(self):
        pass


if __name__ == "__main__":
    sentiment_analyser = SentimentAnalyser(DataProcessor('../../uk_news_scraping/data', ['headline', 'date'], 'guardian*.csv'))
    sentiment_analyser.analyse_sentiment_and_subjectivity()