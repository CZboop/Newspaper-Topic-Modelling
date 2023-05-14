from src.data_processor import DataProcessor
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
import datetime
import plotly.io as pio
from pathlib import Path
import json
import pandas as pd

# class to run topic analysis and related operations for a single source using bertopic
class TopicModeller:
    # constructor takes in args for data selection and processing as well as parameters for the bertopic model
    def __init__(self, data_selector, start_date=datetime.date(2019, 12, 1), end_date=datetime.date(2023, 1, 5), 
    data_dir = '../../uk_news_scraping/data', data_cols = ['headline', 'date'], min_topic_size = 70, topics_to_remove = None,
    n_neighbours = 15, n_components = 5, min_dist = 0.0, metric = 'cosine', random_state = 42, diversity = 0.75, top_n_words = 4,
    language = 'english', calculate_probabilities = True, global_tuning = True, evolution_tuning = True, nr_bins = 10, 
    save_path = Path(__file__).parent
    ):
        # creating data processor object with args passed in to constructor to select relevant data
        self.data_processor = DataProcessor(data_dir, data_cols, data_selector, topics_to_remove = topics_to_remove)

        # properties for data selection and processing/preprocessing
        self.data_selector = data_selector # file name pattern to select csvs we want to analyse, using glob
        self.start_date = start_date # datetime object, first/earliest date to analyse
        self.end_date = end_date # datetime object, last/latest date to analyse
        self.stopwords_list = STOP_WORDS # SpaCy stop words to ignore/remove
        self.topics_to_remove = topics_to_remove # optional topics to disregard from analysis within data files, requires url column in data_cols and csv data

        # hyperparams for topic modelling - umap
        self.min_topic_size = min_topic_size # minimum documents/articles making up each cluster
        self.n_neighbours = n_neighbours # 15 as default, can lower to narrow and increase to broaden (with expected pros and cons for each)
        self.n_components = n_components # dimensions of data passed in to cluster - umap will reduce dimensions to this
        self.min_dist = min_dist # minimum distance of points/embeddings together, for clustering zero so can group nicely and overlap
        self.metric = metric # distance calculated with cosine
        self.random_state = random_state # specify random seed, otherwise results will differ each time for the same input

        # hyperparams for topic modelling - topic modelling
        self.diversity = diversity # uses mmr algo to increase/decrease synonyms or diff ways of saying same thing
        self.top_n_words = top_n_words # how many of the top words used to describe/define each cluster
        self.language = language # the default is english but specifying and can change
        self.calculate_probabilities = calculate_probabilities # calculate probability of document being in all clusters and assign to highest prob
        
        # hyperparams for topics over time
        self.global_tuning = global_tuning # boolean, topics over time influenced by overall/global representation
        self.evolution_tuning = evolution_tuning # boolean, topics over time influence by previous time step representation
        self.nr_bins = nr_bins # int, number of bins in terms of time e.g. if 12 months of data and 12 bins will get every month
        
        # default save path will be based on the parent of this file, but can pass in another path
        self.save_path = save_path

        # getting the data source name based on selector, in most cases this can be overridden but need to be automatically passed in to get examples of each topic
        self.source_name = ''.join(letter for letter in self.data_selector.split('.')[0] if letter.isalnum())
        self._preprocess()

    # cleaning up the data in place within the text columns of df in self.data
    def _preprocess(self):
        # filtering and processing within the data processor object then getting the data out of the object
        self.data_processor.read_and_concat_data_files()
        self.data_processor.remove_duplicates_and_nones()
        self.data_processor.filter_dates()
        # optionally removing topics if these have been passed in in the constructor
        if self.data_processor.topics_to_remove:
            self.data_processor.filter_topics()
        self.data = self.data_processor.combined_data

        # lowercasing and removing stopwords
        self.data['headline'] = self.data['headline'].apply(lambda x: self._clean_text(x))
        self.data['date'] = self.data['date'].apply(lambda x: str(x))

    # to apply to a pandas df column within lambda func
    def _clean_text(self, text):
        return ' '.join([str(word) for word in str(text).lower().split() if word not in (self.stopwords_list)])

    # main topic modeller class, also calls internal cluster examples method
    def model_topics(self):
        # umap to reduce dimensions of vector repr
        self.umap = UMAP(n_neighbors = self.n_neighbours, 
            n_components = self.n_components, 
            min_dist = self.min_dist, 
            metric = self.metric, 
            random_state = self.random_state)

        # count vectorizer for c tf idf
        self.count_vectoriser = CountVectorizer(stop_words = self.stopwords_list)

        # bertopic model taking in hyperparameters from constructor and umap/vectorizer created above
        self.topic_model = BERTopic(umap_model = self.umap,
            vectorizer_model = self.count_vectoriser,
            diversity = self.diversity, 
            min_topic_size = self.min_topic_size, 
            top_n_words = self.top_n_words, 
            language = self.language, 
            calculate_probabilities = self.calculate_probabilities
        )

        # fitting the model and saving returned topics as property of object
        self.topics, probs = self.topic_model.fit_transform(list(self.data['headline'].apply(lambda x: str(x))))
        # calling cluster examples method now model has topics
        self._cluster_examples(self.source_name)
        # getting topic info, printing and returning topic model
        self.topic_model.get_topic_info()
        print(self.topic_model.get_topic_info())
        return self.topic_model

    # get topics over time using method built in to bertopic
    def get_topics_over_time(self):
        # calling method this relies on if not already
        if not hasattr(self, 'topic_model'):
            self.model_topics()
        # calling .topics_over_time() of the bertopic model, storing in a property of this object
        self.data.reset_index(inplace = True,drop = True)
        self.topics_over_time = self.topic_model.topics_over_time(
            self.data['headline'].apply(lambda x: str(x)), # documents, may need to actively cast to str again
            self.data['date'].apply(lambda x: str(x)), # dates
            global_tuning = self.global_tuning, # averaging specific time with overall for that topic
            evolution_tuning = self.evolution_tuning, # different averaging within that short period of time like rolling average
            nr_bins = self.nr_bins # number of date snapshots, recommended under 50, can think how many months total and sample each n months
        )
        print(self.topics_over_time.head)
        # returns a pd df with the topic (similar to initial topic model -1, 0, 1 by overall freq but words separated, freq as own column and then timestamp as own column)
        return self.topics_over_time
        
    # using builtin bertopic method to visualise topics over time
    def visualise_over_time_builtin(self):
        # running method this depends on if not run already
        if not hasattr(self, 'topics_over_time'):
            self.get_topics_over_time()
        # calling method to get topics over time viualisation, return and store in a property of the object
        self.visualised_over_time = self.topic_model.visualize_topics_over_time(self.topics_over_time, top_n_topics = 10) 
        return self.visualised_over_time

    # saving all plots created (topic clusters and topics over time) as json files
    def save_as_json(self, name):
        # running methods that this depends on if not already run and creating plots
        if not hasattr(self, 'topic_model'):
            self.model_topics()
        if not hasattr(self, 'topics_over_time'):
            self.get_topics_over_time()
        topic_figure = self.topic_model.visualize_topics()
        time_figure = self.visualise_over_time_builtin()

        # setting to have transparent background and white text
        topic_figure.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_font_color="rgba(255,255,255,1)", title_font_color="rgba(255,255,255,1)", font=dict(color="rgba(255,255,255,1)"))
        time_figure.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_font_color="rgba(255,255,255,1)", title_font_color="rgba(255,255,255,1)", font=dict(color="rgba(255,255,255,1)"))

        # creating plots directory if it doesn't exist
        Path(f'{self.save_path}/plots').mkdir(parents=True, exist_ok=True)
        # saving based on path passed in to constructor
        path = self.save_path
        topic_figure.write_json(f'{path}/plots/{name}_topics.json')
        time_figure.write_json(f'{path}/plots/{name}_over_time.json')

    # getting representative examples of each topic
    def _cluster_examples(self, name):
        if hasattr(self, 'topic_model'):
            num_topics = max(self.topic_model.topics_)
            example_docs = self.topic_model.get_representative_docs()

            # creating plots and topic examples directory if it doesn't exist
            Path(f'{self.save_path}/plots').mkdir(parents=True, exist_ok=True)
            Path(f'{self.save_path}/plots/topic_doc_examples').mkdir(parents=True, exist_ok=True)
            # have to explicitly cast to int, otherwise type is int32 (presumably numpy) and causes issues dumping into json file
            example_docs_cast = {int(x):example_docs[x] for x in example_docs.keys()}
            with open(f'{self.save_path}/plots/topic_doc_examples/{name}.json', 'w') as file_:
                json.dump(example_docs_cast, file_)
            # returned as a dict with topic # int : [list of docs, more docs, for each topic]
            # note lack of order so would want to iterate explicitly by key to get right order
            # also note the returned docs won't be the exact headline due to preprocessing

            return example_docs
        else:
            raise Exception('Topic model not found, run .model_topics() to create the topic model and get examples')