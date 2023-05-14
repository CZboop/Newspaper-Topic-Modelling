from src.sentiment import SentimentAnalyser
from src.data_processor import DataProcessor

# getting sentiment (polarity and subjectivity) info and graphs for all sources
class SentimentGetter:
    # constructor taking in selectors dict with info for each source (name as key, dict value with info needed for data processor object) 
    def __init__(self, selectors = {'guardian' : {'selector': 'guardian_*.csv'}, 'mirror' : {'selector': 'mirror_*.csv'}, 
    'telegraph': {'selector':'telegraph_*.csv'}, 'sun' : {'selector': 'sun_*.csv'}, 'metro' : {'selector': 'metro_*.csv'}, 
    'express' : {'selector': 'express_*.csv'}, 'mail' : {'selector': 'mail_*.csv', 'cols': ['headline', 'date', 'url'], 'topics_to_remove': ['wires','femail', 'sport', 'showbiz']}
    }):
        self.selectors = selectors

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
        sentiment_analyser = SentimentAnalyser(DataProcessor('../../uk_news_scraping/data', selector_cols, selector_string, topics_to_remove = selector_topics_to_remove), name)
        
        # getting and plotting polarity over time and polarity ratio
        polarity_over_time = sentiment_analyser.get_polarity_over_time()
        sentiment_analyser.plot_polarity_over_time(polarity_over_time)
        sentiment_analyser.plot_polarity_ratio(sentiment_analyser.get_polarity_ratio())

        # getting and plotting subjectivity over time and subjectivity box plot
        subjectivity_over_time = sentiment_analyser.get_subjectivity_over_time()
        sentiment_analyser.plot_subjectivity()
        sentiment_analyser.plot_subjectivity_over_time(subjectivity_over_time)