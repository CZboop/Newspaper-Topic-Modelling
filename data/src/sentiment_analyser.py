from data_processor import DataProcessor
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
import plotly.express as px
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
import os

# running some basic positive/negative sentiment analysis on the different news sources, and subjectivity analyis, cmparing over time
class SentimentAnalyser:
    # note, the data processor is passed in as a whole object but lots can be controlled depending on what args data processor is given
    def __init__(self, data_processor, source_name = None, save_path = None, start_date = datetime.date(2019, 12, 1), end_date = datetime.date(2023, 1, 5)):
        self.data_processor = data_processor # instance of DataProcessor class from data_processor.py
        self.data_processor.read_and_concat_data_files() # calling method to read data into the data processor instance
        # saving into current path if none given, else setting from constructor args
        if save_path == None:
            self.save_path = '.'
        else:
            self.save_path = save_path
        # setting source name from args or data processor
        if source_name != None:
            self.source_name = source_name
        else:
            self.source_name = self.data_processor.selector.split('*')[0].title()

        self.start_date = start_date # start and end date for getting sentiment over time
        self.end_date = end_date

        # setting some more properties that should always have these values, spacy text blob to be used for sentiment analysis
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe('spacytextblob')

        # preprocessing before any other method called
        self._preprocess()

    # reusing methods of the data processor to preprocessor the data within it
    def _preprocess(self):
        # removing duplicates and none, filtering to given date range
        self.data_processor.remove_duplicates_and_nones()
        self.data_processor.filter_dates()
        # optionally removing topics if these have been passed in in the constructor
        if self.data_processor.topics_to_remove:
            self.data_processor.filter_topics()

    # getting polarity and subjectivity for each headline
    def _get_polarity_subjectivity(self):
        # init will create .combined_data with all headlines within the self.data_processor
        self.data_df = self.data_processor.combined_data
        headlines = self.data_df['headline']
        # applying main method of spacy text blob to each element in the headliness column/series from above dataframe
        sentiment_docs = headlines.apply(lambda x: self.nlp(str(x))) # returns an object with sent, subj, etc. info
        # adding polarity and subjectivity column to main dataframe
        self.data_df['polarity'] = sentiment_docs.apply(lambda x: x._.blob.polarity)
        self.data_df['subjectivity'] = sentiment_docs.apply(lambda x: x._.blob.subjectivity)

    # calculating percentage of headlines with negative, positive or neutral polarity
    def get_polarity_ratio(self):
        # using just 0.00 as neutral rather than a range, sense check shows a lot of documents are at exactly 0
        # running method this depends on if not already run
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()

        total = len(self.data_df)
        # selecting from dataframe positive negative and neutral polarities
        self.positive = self.data_df.loc[self.data_df['polarity'] > 0]
        self.negative = self.data_df.loc[self.data_df['polarity'] < 0]
        self.neutral = self.data_df.loc[self.data_df['polarity'] == 0]
        
        # calculating positive negative and neutral as percentages
        positive_percent = len(self.positive) / total * 100 
        negative_percent = len(self.negative) / total * 100
        neutral_percent = len(self.neutral) / total * 100

        # returning a dict with percentages of positive, negative and neutral documents
        return {'positive': positive_percent, 'negative': negative_percent, 'neutral': neutral_percent}

    # saving polarity ratios as pie chart, takes in ratios result of calling get_polarity_ratio
    def plot_polarity_ratio(self, ratios):
        # creating dataframe from ratios dict
        percentage_df = pd.DataFrame(ratios.items(), columns=['Polarity', 'Percentage'])
        # creating plotly express pie chart with above dataframe data
        fig = px.pie(percentage_df, values='Percentage', names='Polarity', title=f'{self.source_name} - Percentages of Positive, Negative and Neutral Headlines')
        # saving in json format
        self.save_as_json(fig, f'{self.source_name}_polarity_ratio')
        return fig

    # calculating polarity over time within date range passed in with start_date before end_date
    def get_polarity_over_time(self):
        # running method this depends on if not run already
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()

        # using datetimes to step through months and slice the df
        current_date = self.end_date
        month_polarity = {}
        while current_date >= self.start_date:
            # slice df by month
            current_month_polarity = self.data_df.loc[lambda df: (pd.DatetimeIndex(df['date']).month == current_date.month) & (pd.DatetimeIndex(df['date']).year == current_date.year)]['polarity']
            # calculate average polarity for that month
            avg_polarity = current_month_polarity.mean()
            # assign to dict
            month_polarity[current_date] = avg_polarity
            # decrement current month
            current_date -= relativedelta(months=1)

        # returns dict where key = date and value = mean polarity
        return month_polarity

    # saving plotly line graph showing polarity over time, takes in overtime_data, dict in format returned by .get_polarity_over_time()
    def plot_polarity_over_time(self, overtime_data):
        # creating pandas dataframe from overtime_data dict
        overtime_polarity_df = pd.DataFrame(overtime_data.items(), columns=['Date', 'Polarity'])
        # creating plotly express line graph using above dataframe as data
        fig = px.line(overtime_polarity_df, x="Date", y="Polarity", title=f'{self.source_name} - Polarity of Headlines Over Time')
        # saving plot in json format and returning the plot/figure that was saved
        self.save_as_json(fig, f'{self.source_name}_polarity_over_time')
        return fig

    # getting subjectivity averages, mean and median
    def get_subjectivity_info(self):
        # running method this depends on if not already run
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()
        # calculating and returning median and mean subjectivity
        median_subjectivity = self.data_df['subjectivity'].median()
        mean_subjectivity = self.data_df['subjectivity'].mean()
        return {'median': median_subjectivity, 'mean': mean_subjectivity}

    # saving subjectivity box plot
    def plot_subjectivity(self):
        # running method this depends on if not already run
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()
        # creating plotly box plot taking in subjectivity column of main data dataframe
        box_plot = px.box(self.data_df, y= 'subjectivity', title= f'{self.source_name} - Subjectivity of Headlines')
        # saving plot in json format, and returning the same plot
        self.save_as_json(box_plot, f'{self.source_name}_subjectivity_box_plot')
        return box_plot

    # calculating subjectivity over time, taking in date range as start_date and end_date where start date is before end date
    def get_subjectivity_over_time(self):
        # running method this depends on if not run already
        if not hasattr(self, 'data_df'):
            self._get_polarity_subjectivity()

        # using datetimes to step through months and slice the df
        current_date = self.end_date
        month_subjectivity = {}
        while current_date >= self.start_date:
            # slice df by month
            current_month_subjectivity = self.data_df.loc[lambda df: (pd.DatetimeIndex(df['date']).month == current_date.month) & (pd.DatetimeIndex(df['date']).year == current_date.year)]['subjectivity']
            # get avg subjectivity for that month
            avg_subjectivity = current_month_subjectivity.mean()
            # assign to dict
            month_subjectivity[current_date] = avg_subjectivity
            # decrement current month
            current_date -= relativedelta(months= 1)

        # returns dict where key = date and value = mean subjectivity
        return month_subjectivity

    # saving plot of subjectivity over time, takes in dict in format returned by .get_subjectivity_over_time()
    def plot_subjectivity_over_time(self, overtime_data):
        # creating dataframe of data in overtime_date
        overtime_subjectivity_df = pd.DataFrame(overtime_data.items(), columns=['Date', 'Subjectivity'])
        # creating plotly line with data from above dataframe
        fig = px.line(overtime_subjectivity_df, x="Date", y="Subjectivity", title=f'{self.source_name} - Subjectivity of Headlines Over Time')
        # saving plotly figure in json format and returning the same figure/plot
        self.save_as_json(fig, f'{self.source_name}_subjectivity_over_time')
        return fig

    # saving plots in json format, takes in fig = plotly plot, name = name to be used in saved file name
    def save_as_json(self, fig, name):
        # creating plots directory if it doesn't exist
        Path(f'{self.save_path}/plots').mkdir(parents=True, exist_ok=True)
        # updating layout to have transparent background and white text
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_font_color="rgba(255,255,255,1)", title_font_color="rgba(255,255,255,1)", font=dict(color="rgba(255,255,255,1)"))
        # writing json file with plot
        fig.write_json(f'{self.save_path}/plots/{name}.json')