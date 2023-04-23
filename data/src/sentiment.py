# running some basic positive/negative sentiment analysis on the different news sources
# and subjectivity analyis
# comparing over time
from src.data_processor import DataProcessor
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
import plotly.express as px
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
import os

class SentimentAnalyser:
    # note, the data processor is passed in as an object already but lots can be controlled depending on what the data processor is given e.g. filtering
    def __init__(self, data_processor, source_name = None, save_path = None):
        self.data_processor = data_processor
        self.data_processor.read_and_concat_data_files()
        if save_path == None:
            self.save_path = '.'
        else:
            self.save_path = save_path
        if source_name != None:
            self.source_name = source_name
        else:
            self.source_name = self.data_processor.selector.split('*')[0].title()
        # passing in a data processor object to handle reading data instead of repeating logic
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe('spacytextblob')
        self._preprocess()

    def _preprocess(self):
        self.data_processor.read_and_concat_data_files()
        self.data_processor.remove_duplicates_and_nones()
        self.data_processor.filter_dates()
        # optionally removing topics if these have been passed in in the constructor
        if self.data_processor.topics_to_remove:
            self.data_processor.filter_topics()
        # self.data_processor.combined_data['headlines'] = self.data_processor._clean_text(self.data_processor.combined_data['headlines'])

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
        
        positive_percent = len(self.positive) / total * 100
        negative_percent = len(self.negative) / total * 100
        neutral_percent = len(self.neutral) / total * 100

        return {'positive': positive_percent, 'negative': negative_percent, 'neutral': neutral_percent}

    def plot_polarity_ratio(self, ratios): # ratio result of calling get_polarity_ratio, name of data source to use in title
        percentage_df = pd.DataFrame(ratios.items(), columns=['Polarity', 'Percentage'])
        fig = px.pie(percentage_df, values='Percentage', names='Polarity', title=f'{self.source_name} - Percentages of Positive, Negative and Neutral Headlines')
        self.save_as_json(fig, f'{self.source_name}_polarity_ratio')
        return fig

    def get_polarity_over_time(self, start_date=datetime.date(2019, 12, 1), end_date=datetime.date(2023, 1, 5)):
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()

        # calculate average polarity by month?
        # using datetimes to step through months and slice the df
        current_date = end_date
        month_polarity = {}
        while current_date >= start_date:
            # slice df
            current_month_polarity = self.data_df.loc[lambda df: (pd.DatetimeIndex(df['date']).month == current_date.month) & (pd.DatetimeIndex(df['date']).year == current_date.year)]['polarity']
            # get avg 
            avg_polarity = current_month_polarity.mean()
            # assign to dict
            month_polarity[current_date] = avg_polarity
            # decrement current month
            current_date -= relativedelta(months=1)
        return month_polarity

    def plot_polarity_over_time(self, overtime_data):
        overtime_polarity_df = pd.DataFrame(overtime_data.items(), columns=['Date', 'Polarity'])
        fig = px.line(overtime_polarity_df, x="Date", y="Polarity", title=f'{self.source_name} - Polarity of Headlines Over Time')
        self.save_as_json(fig, f'{self.source_name}_polarity_over_time')
        return fig

    def get_subjectivity_info(self):
        # get median, mean, but mostly will pass in to plotly to do a box plot 
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()
        median_subjectivity = self.data_df['subjectivity'].median()
        mean_subjectivity = self.data_df['subjectivity'].mean()
        return {'median': median_subjectivity, 'mean': mean_subjectivity}

    def plot_subjectivity(self):
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()
        box_plot = px.box(self.data_df, y= 'subjectivity', title= f'{self.source_name} - Subjectivity of Headlines')
        self.save_as_json(box_plot, f'{self.source_name}_subjectivity_box_plot')
        return box_plot

    def get_subjectivity_over_time(self, start_date=datetime.date(2019, 12, 1), end_date=datetime.date(2023, 1, 5)):
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()

        current_date = end_date
        month_subjectivity = {}
        while current_date >= start_date:
            # slice df
            current_month_subjectivity = self.data_df.loc[lambda df: (pd.DatetimeIndex(df['date']).month == current_date.month) & (pd.DatetimeIndex(df['date']).year == current_date.year)]['subjectivity']
            # get avg subjectivity
            avg_subjectivity = current_month_subjectivity.mean()
            # assign to dict
            month_subjectivity[current_date] = avg_subjectivity
            # decrement current month
            current_date -= relativedelta(months= 1)
        return month_subjectivity

    def plot_subjectivity_over_time(self, overtime_data):
        overtime_subjectivity_df = pd.DataFrame(overtime_data.items(), columns=['Date', 'Subjectivity'])
        fig = px.line(overtime_subjectivity_df, x="Date", y="Subjectivity", title=f'{self.source_name} - Subjectivity of Headlines Over Time')
        self.save_as_json(fig, f'{self.source_name}_subjectivity_over_time')
        return fig

    def save_as_json(self, fig, name):
        # creating plots directory if it doesn't exist
        Path(f'{self.save_path}/plots').mkdir(parents=True, exist_ok=True)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_font_color="rgba(255,255,255,1)", title_font_color="rgba(255,255,255,1)", font=dict(color="rgba(255,255,255,1)"))
        fig.write_json(f'{self.save_path}/plots/{name}.json')

if __name__ == "__main__":
    sentiment_analyser = SentimentAnalyser(DataProcessor('../../uk_news_scraping/data', ['headline', 'date', 'url'], '*.csv', topics_to_remove = ['wires','femail', 'sport', 'showbiz']), source_name='all')
    # sentiment_analyser.plot_polarity_ratio(sentiment_analyser.get_polarity_ratio()) #NOTE: still need to run this fully to save result
    polarity_over_time = sentiment_analyser.get_polarity_over_time()
    sentiment_analyser.plot_polarity_over_time(polarity_over_time)
    sentiment_analyser.plot_polarity_ratio(sentiment_analyser.get_polarity_ratio())
    subjectivity_over_time = sentiment_analyser.get_subjectivity_over_time()
    sentiment_analyser.plot_subjectivity()
    sentiment_analyser.plot_subjectivity_over_time(subjectivity_over_time)