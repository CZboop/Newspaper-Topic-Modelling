from src.data_processor import DataProcessor
import plotly.express as px
import pandas as pd
from pathlib import Path
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# getting basic info about the data, ratios and volumes from different sources and times
class GeneralAnalyser:
    def __init__(self, data_selectors = {'guardian' : {'selector': 'guardian_*.csv'}, 'mirror' : {'selector': 'mirror_*.csv'}, 
    'telegraph': {'selector':'telegraph_*.csv'}, 'sun' : {'selector': 'sun_*.csv'}, 'metro' : {'selector': 'metro_*.csv'}, 
    'express' : {'selector': 'express_*.csv'}, 'mail' : {'selector': 'mail_*.csv', 'cols': ['headline', 'date', 'url'], 'topics_to_remove': ['wires','femail', 'sport', 'showbiz']}}, path_to_data='../../uk_news_scraping/data', path_to_save= Path(__file__).parent):
        self.data_selectors = data_selectors # dict with source name as key and another dict as value containing args to pass in to data processor for that source
        self.path_to_data = path_to_data # path to data source, same for all sources
        self.path_to_save = path_to_save # path to save plots, defaults to parent directory of current file

    # comparing the number and percentage of individual documents/headlines for each data source
    def compare_ratio_of_docs(self):
        # initialising total number of records all, will be added to as iterate over different sources
        all_records = 0
        # initialising dict to store number per each source
        record_numbers = {}
        # iterating over sources using .data_selector dict keys
        for paper in self.data_selectors.keys():
            # getting record numbers from data processor dataframe shape, storing in record_numbers dict
            record_nums = DataProcessor(selector = self.data_selectors.get(paper).get('selector'), path_to_dir = self.path_to_data, cols = self.data_selectors.get(paper).get('cols'), topics_to_remove = self.data_selectors.get(paper).get('topics_to_remove', None)).read_and_concat_data_files().shape[0]
            record_numbers[paper.title()] = record_nums
            all_records += record_nums
        
        # initialising dict to store percentage of documents from each source, calculating below
        record_percentages = {}
        for paper in record_numbers.keys():
            percentage = round(record_numbers.get(paper) / all_records * 100, 2)
            record_percentages[paper] = percentage

        # returns:
            # all_records - int total number of documents across all sources
            # record_numbers - dict with string key (source name) and int value (number of documents)
            # record_percentages - dict with string key (source name) and int value (percentage of total documents from that source)
        return all_records, record_numbers, record_percentages

    # visualising percentages of data from each source in a pie chart
    # taking in percentages as dict in same format returned by .compare_ratio_of_docs() method
    def visualise_percentages(self, percentages):
        # creating dataframe from percentages dict
        percent_df = pd.DataFrame(percentages.items(), columns=['Source', 'Percentage'])
        # turning df into plotly pie chart
        fig = px.pie(percent_df, values='Percentage', names='Source', title='Ratio of Articles by News Source')
        # saving as json using .save_as_json() method of this class
        self.save_as_json(fig, 'news_source_ratios')
        return fig
    
    # saving plotly figure as json file
    def save_as_json(self, figure, name):
        # creating plots directory if it doesn't exist
        Path(f'{self.path_to_save}/plots').mkdir(parents=True, exist_ok=True)

        # setting to have transparent background and white text
        figure.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_font_color="rgba(255,255,255,1)", title_font_color="rgba(255,255,255,1)", font=dict(color="rgba(255,255,255,1)"))
        # using plotly method to save in json format
        figure.write_json(f'{self.path_to_save}/plots/{name}.json')
    
    # calculating the number of documents (individual headlines) per month
    def compare_num_of_docs_over_time(self, start_date=datetime.date(2019, 12, 1), end_date=datetime.date(2023, 1, 5)):
        # iterate over each month and get number of articles in that month for each source and overall
        month_year = start_date
        docs_by_month_total = {}
        docs_by_month_source = []
        # iterating by month
        while month_year <= end_date:
            # initialising totals for the month
            doc_num_list = [month_year]
            combined_total_by_month = 0
            # getting data for each source by month
            for source in self.data_selectors.keys():
                article_df = DataProcessor(selector = self.data_selectors.get(source).get('selector'), path_to_dir = self.path_to_data, cols = self.data_selectors.get(source).get('cols'), topics_to_remove = self.data_selectors.get(source).get('topics_to_remove', None)).read_and_concat_data_files()
                articles_in_range = article_df['date'].loc[lambda x: (pd.DatetimeIndex(x).month == month_year.month) & (pd.DatetimeIndex(x).year == month_year.year)]
                num_articles_in_range = len(list(articles_in_range))
                # 
                combined_total_by_month += num_articles_in_range
                doc_num_list.append(num_articles_in_range)
            
            # updating collections with information gathered for that month
            docs_by_month_source.append(doc_num_list)
            docs_by_month_total[month_year] = combined_total_by_month
            month_year += relativedelta(months = 1)

        return docs_by_month_source, docs_by_month_total
    
    def visualise_number_over_time(self, data, single = False, source_name= None): # single kwarg is for whether it's one data source per graph or not
        filename = 'articles_over_time' if source_name == None else f'articles_over_time_{source_name}'
        if single:
            data_df = pd.DataFrame(data.items(), columns=['Month', 'Articles'])
            fig = px.line(data_df, x= 'Month', y= 'Articles', title=f'{source_name} - Article Number Over Time')
            self.save_as_json(fig, filename)
            return fig
        else:
            sources_list = list(self.data_selectors.keys()) # dict keys data type needs to be cast to list to concat later, not enough to be iterable
            data_df = pd.DataFrame(data, columns=['Month'] + sources_list)
            fig = px.line(data_df, x= 'Month', y= sources_list, title=f'{source_name} - Article Number Over Time')
            self.save_as_json(fig, filename)
            return fig

    def run(self):
        self.visualise_percentages(self.compare_ratio_of_docs()[2])
        number_by_source, number_total = self.compare_num_of_docs_over_time()
        self.visualise_number_over_time(number_by_source, source_name = "All Sources")
        self.visualise_number_over_time(number_total, single = True, source_name = "Combined Sources")