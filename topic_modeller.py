from data_processor import DataProcessor
import nltk
from nltk.corpus import stopwords

class TopicModeller:
    def __init__(self, data_dir, data_cols, data_selector):
        self.data = DataProcessor(data_dir, data_cols, data_selector).read_and_concat_data_files()
        self.stopwords_list = stopwords.words('english')

    # clean up the data in place within the text columns of df in self.data
    # note this could get slow as data expands, may need mitigation/some kind of checkpointing
    def _preprocess(self):
        self.data['headline'] = self.data['headline'].apply(lambda x: self._clean_text(x))
        self.data['subheading'] = self.data['subheading'].apply(lambda x: self._clean_text(x))
        self.data['text'] = self.data['text'].apply(lambda x: self._clean_text(x))

    # to apply to a pandas df column within lambda func
    # TODO: further clean eg remove special chars (currently lowercases and removes stopwords)
    def _clean_text(self, text):
        return ' '.join([word for word in str(text).lower().split() if word not in (self.stopwords_list)])

if __name__ == "__main__":
    topic_modeller = TopicModeller('../uk_news_scraping/data', ['headline', 'subheading', 'text', 'date'], 'guardian_*.csv')
    topic_modeller._preprocess()
