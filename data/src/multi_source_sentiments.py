from sentiment_analyser import SentimentAnalyser
from data_processor import DataProcessor
import datetime

# getting sentiment (polarity and subjectivity) info and graphs for all sources
class MultiSourceSentiments:
    # constructor taking in selectors dict with info for each source (name as key, dict value with info needed for data processor object) 
    def __init__(self, selectors = {'guardian' : {'selector': 'guardian_*.csv'}, 'mirror' : {'selector': 'mirror_*.csv'}, 
    'telegraph': {'selector':'telegraph_*.csv'}, 'sun' : {'selector': 'sun_*.csv'}, 'metro' : {'selector': 'metro_*.csv'}, 
    'express' : {'selector': 'express_*.csv'}, 'mail' : {'selector': 'mail_*.csv', 'cols': ['headline', 'date', 'url'], 'topics_to_remove': ['wires','femail', 'sport', 'showbiz']}
    }, data_path= '../../uk_news_scraping/data', save_path = '.', start_date = datetime.date(2019, 12, 1), end_date = datetime.date(2023, 1, 5)):
        self.selectors = selectors
        self.data_path = data_path # path to directory containing data for all sources to be analysed
        self.save_path = save_path # default to current directory, path to save plots inside
        self.start_date = start_date # start and end dates to pass to sentiment analyser for getting sentiment over time
        self.end_date = end_date

    # running _source_sent() method for each source
    def run(self):
        for name, selector in self.selectors.items():
            # note selector is entire value dict for the source not just the selector part
            self._source_sent(name, selector)

    # running all analysis, plotting and saving for an individual data source
    def _source_sent(self, name, selector):
        # gathering information for each source from the selector dict, with defaults for some if not present
        selector_string = selector.get('selector')
        selector_cols = selector.get('cols', ['headline', 'date']) # if has key cols use that else default to ['headline', 'date']
        selector_topics_to_remove = selector.get('topics_to_remove', None)

        # creating sentiment analyser instance
        sentiment_analyser = SentimentAnalyser(DataProcessor(self.data_path, cols = selector_cols, selector = selector_string, topics_to_remove = selector_topics_to_remove, start_date = self.start_date, end_date = self.end_date), source_name = name, save_path = self.save_path, start_date = self.start_date, end_date = self.end_date)
        
        # getting and plotting polarity over time and polarity ratio
        polarity_over_time = sentiment_analyser.get_polarity_over_time()
        sentiment_analyser.plot_polarity_over_time(polarity_over_time)
        polarity_ratio = sentiment_analyser.get_polarity_ratio()
        sentiment_analyser.plot_polarity_ratio(polarity_ratio)

        # getting and plotting subjectivity over time and subjectivity box plot
        subjectivity_over_time = sentiment_analyser.get_subjectivity_over_time()
        sentiment_analyser.plot_subjectivity()
        sentiment_analyser.plot_subjectivity_over_time(subjectivity_over_time)

        # returning resulting data
        # polarity_over_time: dict where key = date and value = mean polarity
        # polarity_ratio: dict with format {'positive': positive_percent, 'negative': negative_percent, 'neutral': neutral_percent}
        # subjectivity_over_time: dict where key = date and value = mean subjectivity
        return polarity_over_time, polarity_ratio, subjectivity_over_time