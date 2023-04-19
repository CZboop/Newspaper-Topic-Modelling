# getting a basic idea of the data from the different sources
from src.data_processor import DataProcessor
import plotly.express as px
import pandas as pd
from pathlib import Path
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class GeneralAnalyser:
    def __init__(self, data_selectors = {'guardian' : {'selector': 'guardian_*.csv'}, 'mirror' : {'selector': 'mirror_*.csv'}, 
    'telegraph': {'selector':'telegraph_*.csv'}, 'sun' : {'selector': 'sun_*.csv'}, 'metro' : {'selector': 'metro_*.csv'}, 
    'express' : {'selector': 'express_*.csv'}, 'mail' : {'selector': 'mail_*.csv', 'cols': ['headline', 'date', 'url'], 'topics_to_remove': ['wires','femail', 'sport', 'showbiz']}}, path_to_dir='../../uk_news_scraping/data'):
        self.data_selectors = data_selectors
        self.path_to_dir = path_to_dir

    def compare_ratio_of_docs(self):
        # total number of records all
        all_records = 0
        # number per each source
        record_numbers = {}
        for paper in self.data_selectors.keys():
            record_nums = DataProcessor(selector = self.data_selectors.get(paper).get('selector'), path_to_dir = self.path_to_dir, cols = self.data_selectors.get(paper).get('cols'), topics_to_remove = self.data_selectors.get(paper).get('topics_to_remove', None)).read_and_concat_data_files().shape[0]
            record_numbers[paper.title()] = record_nums
            all_records += record_nums
        # percentage of each
        record_percentages = {}
        for paper in record_numbers.keys():
            percentage = round(record_numbers.get(paper) / all_records * 100, 2)
            record_percentages[paper] = percentage

        return all_records, record_numbers, record_percentages

    def visualise_percentages(self, percentages): # percentages as dict e.g. coming from compare_ratio_of_docs method
        # values into df
        percent_df = pd.DataFrame(percentages.items(), columns=['Source', 'Percentage'])
        # df into plotly pie chart
        fig = px.pie(percent_df, values='Percentage', names='Source', title='Ratio of Articles by News Source')
        # save as json
        self.save_as_json(fig, 'news_source_ratios')
        return fig
    
    def save_as_json(self, figure, name):
        # setting to have transparent background
        figure.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_font_color="rgba(255,255,255,1)", title_font_color="rgba(255,255,255,1)", font=dict(color="rgba(255,255,255,1)"))
        # saving by getting relative path as absolute path
        # path = Path(__file__).parent
        # note the above gets the path of this script, so if running this script from elsewhere could cause issues and not save relative to where running from which is what goal is
        figure.write_json(f'{self.path_to_dir}/plots/{name}.json')
    
    def compare_num_of_docs_over_time(self, start_date=datetime.date(2019, 12, 1), end_date=datetime.date(2023, 1, 5)):
        # iterate over each month and get number of articles in that month for each source and total
        month_year = start_date
        docs_by_month_total = {}
        docs_by_month_source = []
        # how to store data for multiple sources...
        # picture df
        # will explicitly have eac column as key and what would be cell value as value
        while month_year <= end_date:
            doc_num_list = [month_year]
            combined_total_by_month = 0
            for source in self.data_selectors.keys():
                article_df = DataProcessor(selector = self.data_selectors.get(source).get('selector'), path_to_dir = self.path_to_dir, cols = self.data_selectors.get(source).get('cols'), topics_to_remove = self.data_selectors.get(source).get('topics_to_remove', None)).read_and_concat_data_files()
                articles_in_range = article_df['date'].loc[lambda x: (pd.DatetimeIndex(x).month == month_year.month) & (pd.DatetimeIndex(x).year == month_year.year)]
                num_articles_in_range = len(list(articles_in_range))
                # doc_num_list[source] = num_articles_in_range
                combined_total_by_month += num_articles_in_range
                doc_num_list.append(num_articles_in_range)
            docs_by_month_source.append(doc_num_list)
            docs_by_month_total[month_year] = combined_total_by_month
            month_year += relativedelta(months = 1)
        print(docs_by_month_source)
        return docs_by_month_source, docs_by_month_total
    
    def visualise_number_over_time(self, data, single = False, source_name= None): # single kwarg is for whether it's one data source per graph or not
        filename = 'articles_over_time' if source_name == None else f'articles_over_time_{source_name}'
        if single:
            data_df = pd.DataFrame(data.items(), columns=['Month', 'Articles'])
            fig = px.line(data_df, x= 'Month', y= 'Articles', title=f'{source_name} - Article Number Over Time')
            self.save_as_json(fig, filename)
        else:
            sources_list = list(self.data_selectors.keys()) # dict keys data type needs to be cast to list to concat later, not enough to be iterable
            data_df = pd.DataFrame(data, columns=['Month'] + sources_list)
            fig = px.line(data_df, x= 'Month', y= sources_list, title=f'{source_name} - Article Number Over Time')
            self.save_as_json(fig, filename)

    def run(self):
        self.visualise_percentages(self.compare_ratio_of_docs()[2])
        number_by_source, number_total = self.compare_num_of_docs_over_time()
        self.visualise_number_over_time(number_by_source, source_name = "All Sources")
        self.visualise_number_over_time(number_total, single = True, source_name = "Combined Sources")

if __name__ == "__main__":
    # below to create pie chart of ratios across each news source (total articles/documents)
    analyser = GeneralAnalyser()
    analyser.run()
    # print(analyser.compare_ratio_of_docs())
    # analyser.visualise_percentages(analyser.compare_ratio_of_docs()[2])
    # # below to get how many articles by each month
    # # analyser = GeneralAnalyser()
    # print(analyser.compare_num_of_docs_over_time())
    # analyser.visualise_number_over_time(analyser.compare_num_of_docs_over_time())