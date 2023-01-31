# getting a basic idea of the data from the different sources
from data_processor import DataProcessor
import plotly.express as px
import pandas as pd
from pathlib import Path
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class GeneralAnalyser:
    def __init__(self, data_selectors = {'guardian' : 'guardian_*.csv', 'mirror' : 'mirror_*.csv', 'telegraph': 'telegraph_*.csv', 
    'sun' : 'sun_*.csv', 'mail' : 'mail_*.csv', 'metro' : 'metro_*.csv', 'express' : 'express_*.csv'}):
        self.data_selectors = data_selectors

    def compare_ratio_of_docs(self):
        # total number of records all
        all_records = DataProcessor(selector = '*.csv', path_to_dir = '../uk_news_scraping/data', cols = ['headline', 'date']).read_and_concat_data_files().shape[0] # get the number of rows in returned dataframe
        # number per each source
        record_numbers = {}
        for paper in self.data_selectors.keys():
            record_nums = DataProcessor(selector = self.data_selectors.get(paper), path_to_dir = '../uk_news_scraping/data', cols = ['headline', 'date']).read_and_concat_data_files().shape[0]
            record_numbers[paper] = record_nums
        # percentage of each
        record_percentages = {}
        for paper in record_numbers.keys():
            percentage = round(record_numbers.get(paper) / all_records * 100, 2)
            record_percentages[paper] = percentage
        return all_records, record_numbers, record_percentages

    def visualise_percentages(self, percentages): # percentages as dict e.g. coming from compare_ratio_of_docs method
        # values into df
        percent_df = pd.DataFrame(percentages.items(), columns=['source', 'percentage'])
        # df into plotly pie chart
        fig = px.pie(percent_df, values='percentage', names='source', title='Ratio of articles by news source')
        # save as html
        self.save_as_html(fig, 'news_source_ratios')

    def save_as_html(self, figure, name):
        path = Path(__file__).parent
        figure.write_html(f'{path}/plots/{name}.html')
    
    def compare_num_of_docs_over_time(self, start_date=datetime.date(2019, 12, 1), end_date=datetime.date(2023, 1, 5)):
        # iterate over each month and get number of articles in that month for each source and total
        # TODO: for this and other analysis, may need to revisit based on hugely disproportionate daily mail number of articles that may filter/have option to ignore
        month_year = start_date
        docs_by_month_total = {}
        docs_by_month_source = {}
        while month_year <= end_date:
            doc_num_list = {}
            for source in self.data_selectors.keys():
                article_df = DataProcessor(selector = self.data_selectors.get(source), path_to_dir = '../uk_news_scraping/data', cols = ['headline', 'date']).read_and_concat_data_files()
                articles_in_range = article_df['date'].loc[lambda x: (pd.DatetimeIndex(x).month == month_year.month) & (pd.DatetimeIndex(x).year == month_year.year)]
                doc_num_list[source] = len(list(articles_in_range))
            docs_by_month_source[month_year] = doc_num_list
            complete_df = DataProcessor(selector = '*.csv', path_to_dir = '../uk_news_scraping/data', cols = ['headline', 'date']).read_and_concat_data_files()
            docs_by_month_total[month_year] = len(list(complete_df['date'].loc[lambda x: (pd.DatetimeIndex(x).month == month_year.month) & (pd.DatetimeIndex(x).year == month_year.year)]))
            month_year -= relativedelta(months = 1)
        
        return docs_by_month_source, docs_by_month_total
    
    def visualise_number_over_time(self, data):
        pass

if __name__ == "__main__":
    # below to create pie chart of ratios across each news source (total articles/documents)
    # analyser = GeneralAnalyser()
    # print(analyser.compare_ratio_of_docs())
    # analyser.visualise_percentages(analyser.compare_ratio_of_docs()[2])
    # below to get how many articles by each month
    analyser = GeneralAnalyser()
    print(analyser.compare_num_of_docs_over_time())