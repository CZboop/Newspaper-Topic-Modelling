from data_processor import DataProcessor
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
import datetime
import plotly.io as pio
from pathlib import Path

# TODO: refactor to take multiple data sources
class TopicModeller:
    def __init__(self, data_selector, start_date=datetime.date(2019, 12, 1), end_date=datetime.date(2023, 1, 5), data_dir = '../../uk_news_scraping/data', data_cols = ['headline', 'date']):
        self.data = DataProcessor(data_dir, data_cols, data_selector).read_and_concat_data_files()
        self.start_date = start_date
        self.end_date = end_date
        self.stopwords_list = STOP_WORDS

    # clean up the data in place within the text columns of df in self.data
    # note this could get slow as data expands, may need mitigation/some kind of checkpointing
    def _preprocess(self):
        self.data.remove_duplicates()
        self.data.filter_dates(start_date, end_date)
        self.data['headline'] = self.data['headline'].apply(lambda x: self._clean_text(x))
        self.data['subheading'] = self.data['subheading'].apply(lambda x: self._clean_text(x))
        self.data['text'] = self.data['text'].apply(lambda x: self._clean_text(x))

    # to apply to a pandas df column within lambda func
    # TODO: further clean eg remove special chars (currently lowercases and removes stopwords)
    def _clean_text(self, text):
        return ' '.join([word for word in str(text).lower().split() if word not in (self.stopwords_list)])

    # TODO: refactor to handle more than one model at once? or no need to save as object property if saving model
    def model_topics(self, min_topic_size = 50):
        # umap way of reducing dimensions of vector repr
        self.umap = UMAP(n_neighbors = 15, # this is default, can lower to narrow and increase to broaden (with expected pros and cons for each)
            n_components = 5, # dimensions of data passed in to cluster - umap will reduce dimensions to this
            min_dist = 0.0, # minimum distance of points/embeddings together, for clustering zero so can group nicely and overlap
            metric = 'cosine', # distance calculated with cosine
            random_state = 42) # specify random seed, otherwise results will differ each time for the same input
        
        self.count_vectoriser = CountVectorizer(stop_words = self.stopwords_list)

        self.topic_model = BERTopic(umap_model = self.umap,
            vectorizer_model = self.count_vectoriser,
            diversity = 0.75, # uses mmr algo to increase/decrease synonyms or diff ways of saying same thing
            min_topic_size = min_topic_size, # minimum documents/articles making up each cluster
            top_n_words = 4, # how many of the top words used to describe/define each cluster
            language = 'english', # the default is english but specifying
            calculate_probabilities = True # calculate probability of document being in all clusters and assign to highest prob
        )

        self.topics = self.topic_model.fit_transform(list(self.data['headline'].apply(lambda x: str(x))))

        self.topic_model.get_topic_info()
        print(self.topic_model.get_topic_info())
        return self.topic_model

    # prob want couple of these methods and above to do for different data e.g. headlines subheadings and article text
    def get_topics_over_time(self):
        self.topics_over_time = self.topic_model.topics_over_time(
            self.data['headline'].apply(lambda x: str(x)), # documents, may need to actively cast to str again
            self.data['date'].apply(lambda x: str(x)), # dates
            global_tuning = True, # averaging specific time with overall for that topic
            evolution_tuning = True, # different averaging within that short period of time like rolling average
            nr_bins = 10 # number of date snapshots, recommended under 50, can think how many months total and sample each n months
        )
        print(self.topics_over_time.head)
        # returns a pd df with the topic (similar to initial topic model -1, 0, 1 by overall freq but words separated, freq as own column and then timestamp as own column)

    def visualise_over_time_builtin(self):
        if not hasattr(self, 'topics_over_time'):
            self.get_topics_over_time()
        # ie the built in method that BERTopic has for visualising, thinking could take the time topic df and do own visualisation
        self.visualised_over_time = self.topic_model.visualize_topics_over_time(self.topics_over_time, top_n_topics = 10) # shows if run in a notebook
        return self.visualised_over_time

    def html_plot(self, name):
        plot = self.topic_model.visualize_topics()
        path = Path(__file__).parent
        plot.write_html(f'{path}/plots/{name}.html')

    def save_as_json(self, name):
        topic_figure = self.topic_model.visualize_topics()
        time_figure = self.visualise_over_time_builtin()
        # setting to have transparent background
        topic_figure.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_font_color="rgba(255,255,255,1)", title_font_color="rgba(255,255,255,1)", font=dict(color="rgba(255,255,255,1)"))
        time_figure.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_font_color="rgba(255,255,255,1)", title_font_color="rgba(255,255,255,1)", font=dict(color="rgba(255,255,255,1)"))
        
        # saving by getting relative path as absolute path
        path = Path(__file__).parent
        topic_figure.write_json(f'{path}/plots/{name}_topics.json')
        time_figure.write_json(f'{path}/plots/{name}_over_time.json')

    def cluster_examples(self):
        # trying to get a representative example of each cluster
        pass

if __name__ == "__main__":
    # guardian_topic_modeller = TopicModeller('guardian_*.csv')
    # # guardian_topic_modeller._preprocess()
    # guardian_topic_modeller.model_topics()
    # # guardian_topic_modeller.get_topics_over_time()
    # guardian_topic_modeller.html_plot('guardian_topic_plot')
    guardian_topic_modeller = TopicModeller('guardian*.csv')
    guardian_topic_modeller.model_topics(min_topic_size = 80)
    guardian_topic_modeller.save_as_json('guardian')
