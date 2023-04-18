# a wee class to get all sentiment (polarity and subjectivity) info and graphs for sources
from src.sentiment import SentimentAnalyser
from src.data_processor import DataProcessor

class SentimentGetter:
    def __init__(self, selectors = {'guardian' : {'selector': 'guardian_*.csv'}, 'mirror' : {'selector': 'mirror_*.csv'}, 
    'telegraph': {'selector':'telegraph_*.csv'}, 'sun' : {'selector': 'sun_*.csv'}, 'metro' : {'selector': 'metro_*.csv'}, 
    'express' : {'selector': 'express_*.csv'}, 'mail' : {'selector': 'mail_*.csv', 'cols': ['headline', 'date', 'url'], 'topics_to_remove': ['wires','femail', 'sport', 'showbiz']}
    }, with_save = False):
        self.selectors = selectors
        self.with_save = with_save

    def run(self):
        for name, selector in self.selectors.items():
            self._source_sent(name, selector)

    # running all analysis, plotting and saving for an individual data source
    def _source_sent(self, name, selector):
        selector_string = selector.get('selector')
        selector_cols = selector.get('cols', ['headline', 'date']) # if has key cols use that else default to ['headline', 'date']
        selector_topics_to_remove = selector.get('topics_to_remove', None)

        sentiment_analyser = SentimentAnalyser(DataProcessor('../../uk_news_scraping/data', selector_cols, selector_string, topics_to_remove = selector_topics_to_remove), name)
        # TODO: currently just getting initial values with save to csv, can adjust if still memory issues
        if self.with_save == True:
            sentiment_analyser._get_subjectivity_polarity_with_csv()
        polarity_over_time = sentiment_analyser.get_polarity_over_time()
        
        sentiment_analyser.plot_polarity_over_time(polarity_over_time)
        sentiment_analyser.plot_polarity_ratio(sentiment_analyser.get_polarity_ratio())

        subjectivity_over_time = sentiment_analyser.get_subjectivity_over_time()

        sentiment_analyser.plot_subjectivity()
        sentiment_analyser.plot_subjectivity_over_time(subjectivity_over_time)

if __name__ == "__main__":
    sentiment_getter = SentimentGetter({'all' : {'selector': '*.csv', 'cols': ['headline', 'date', 'url'], 'topics_to_remove': ['wires','femail', 'sport', 'showbiz']}}, with_save = True)
    sentiment_getter.run()