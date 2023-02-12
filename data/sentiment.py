# running some basic positive/negative sentiment analysis on the different news sources
# and subjectivity analyis
# comparing over time
from data_processor import DataProcessor
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
import plotly.express as px

class SentimentAnalyser:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.data_processor.read_and_concat_data_files()
        # passing in a data processor object to handle reading data instead of repeating logic
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe('spacytextblob')

    def _get_polarity_subjectivity(self):
        # init will create .combined_data within the self.data_processor
        self.data_df = self.data_processor.combined_data
        headlines = self.data_df['headline']
        sentiment_docs = headlines.apply(lambda x: self.nlp(str(x))) # returns an object with sent, subj, etc. info
        self.data_df['polarity'] = sentiment_docs.apply(lambda x: x._.blob.polarity)
        self.data_df['subjectivity'] = sentiment_docs.apply(lambda x: x._.blob.subjectivity)

    def get_polarity_ratio(self):
        # using just 0.00 as neutral rather than a range, initial sense check shows a lot of documents exactly 0
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()

        total = len(self.data_df)
        self.positive = self.data_df.loc[self.data_df['polarity'] > 0]
        self.negative = self.data_df.loc[self.data_df['polarity'] < 0]
        self.neutral = self.data_df.loc[self.data_df['polarity'] == 0]
        print(positive)
        positive_percent = len(self.positive) / total * 100
        negative_percent = len(self.negative) / total * 100
        neutral_percent = len(self.neutral) / total * 100

        return {'positive': positive_percent, 'negative': negative_percent, 'neutral': neutral_percent}

    def plot_polarity_ratio(self, ratios, name): # ratio result of calling get_polarity_ratio, name of data source to use in title
        perentage_df = DataFrame(ratios.items(), columns=['Polarity', 'Percentage'])
        fig = px.pie(percentage_df, values='Percentage', names='Polarity', title=f'{name} - Percentages of Positive, Negative and Neutral Headlines')
        self.save_as_json(fig, f'{name}_polarity_ratio')

    def get_polarity_over_time(self):
        pass

    def plot_polarity_over_time(self):
        pass

    def save_as_json(self, fig, name):
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_font_color="rgba(255,255,255,1)", title_font_color="rgba(255,255,255,1)", font=dict(color="rgba(255,255,255,1)"))
        # saving by getting relative path as absolute path
        path = Path(__file__).parent
        fig.write_json(f'{path}/plots/{name}.json')

if __name__ == "__main__":
    sentiment_analyser = SentimentAnalyser(DataProcessor('../../uk_news_scraping/data', ['headline', 'date'], 'guardian*.csv'))
    sentiment_analyser.get_polarity_ratio()