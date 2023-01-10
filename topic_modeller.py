from data_processor import DataProcessor
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

class TopicModeller:
    def __init__(self, data_dir, data_cols, data_selector):
        self.data = DataProcessor(data_dir, data_cols, data_selector).read_and_concat_data_files()
        self.stopwords_list = STOP_WORDS

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

    def model_topics(self):
        # umap way of reducing dimensions of vector repr
        self.umap = UMAP(n_neighbours = 15, # this is default, can lower to narrow and increase to broaden (with expected pros and cons for each)
            n_components = 5, # dimensions of data passed in to cluster
            min_dist = 0.0, # minimum distance of points/embeddings together, for clustering zero so can group nicely and overlap
            metric = cosine, # distance calculated with cosine
            random_state = 42) # specify random seed, otherwise results will differ each time for the same input
        
        self.count_vectoriser = CountVectorizer(stopwords = self.stopwords)

if __name__ == "__main__":
    topic_modeller = TopicModeller('../uk_news_scraping/data', ['headline', 'subheading', 'text', 'date'], 'guardian_*.csv')
    topic_modeller._preprocess()
