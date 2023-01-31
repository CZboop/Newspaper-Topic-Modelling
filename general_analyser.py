# getting a basic idea of the data from the different sources
from data_processor import DataProcessor
import plotly.express as px
import pandas as pd
from pathlib import Path

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
    
    def compare_num_of_docs_over_time(self):
        pass
        # iterate over each month
    
    def visualise_number_over_time(self, data):
        pass

if __name__ == "__main__":
    # below to create pie chart of ratios across each news source (total articles/documents)
    # analyser = GeneralAnalyser()
    # print(analyser.compare_ratio_of_docs())
    # analyser.visualise_percentages(analyser.compare_ratio_of_docs()[2])
    pass