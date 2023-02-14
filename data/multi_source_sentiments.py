# a wee class to get all sentiment (polarity and subjectivity) info and graphs for sources
from sentiment import SentimentAnalyser
from data_processor import DataProcessor

class SentimentGetter:
    def __init__(self, selectors = {'guardian' : 'guardian_*.csv', 'mirror' : 'mirror_*.csv', 'telegraph': 'telegraph_*.csv', 
    'sun' : 'sun_*.csv', 'mail' : 'mail_*.csv', 'metro' : 'metro_*.csv', 'express' : 'express_*.csv', 'all': '*.csv'}):
        self.selectors = selectors

    def run(self):
        for name, selector in self.selectors.items():
            self._source_sent(name, selector)

    # running all analysis, plotting and saving for an individual data source
    def _source_sent(self, name, selector):
        sentiment_analyser = SentimentAnalyser(DataProcessor('../../uk_news_scraping/data', ['headline', 'date'], selector), name)
        polarity_over_time = sentiment_analyser.get_polarity_over_time()
        sentiment_analyser.plot_polarity_over_time(polarity_over_time)
        sentiment_analyser.plot_polarity_ratio(sentiment_analyser.get_polarity_ratio())
        subjectivity_over_time = sentiment_analyser.get_subjectivity_over_time()
        sentiment_analyser.plot_subjectivity()
        sentiment_analyser.plot_subjectivity_over_time(subjectivity_over_time)

if __name__ == "__main__":
    sentiment_getter = SentimentGetter(selectors = {'metro' : 'metro_*.csv', 'express' : 'express_*.csv', 'all': '*.csv', 'mail' : 'mail_*.csv'})
    sentiment_getter.run()