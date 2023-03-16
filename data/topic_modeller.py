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
import json
import pandas as pd

class TopicModeller:
    def __init__(self, data_selector, start_date=datetime.date(2019, 12, 1), end_date=datetime.date(2023, 1, 5), data_dir = '../../uk_news_scraping/data', data_cols = ['headline', 'date'], min_topic_size = 70, topics_to_remove = None):
        self.data_processor = DataProcessor(data_dir, data_cols, data_selector)
        self.data_selector = data_selector
        self.start_date = start_date
        self.end_date = end_date
        self.stopwords_list = STOP_WORDS
        self.min_topic_size = min_topic_size
        self.topics_to_remove = topics_to_remove
        # getting the data source name based on selector, in most cases this can be overridden but need to be automatically passed in to get examples of each topic
        self.source_name = ''.join(letter for letter in self.data_selector.split('.')[0] if letter.isalnum())
        self._preprocess()

    # clean up the data in place within the text columns of df in self.data
    # note this could get slow as data expands, may need mitigation/some kind of checkpointing
    def _preprocess(self):
        # filtering and processing within the data processor object then getting the data out of the object
        self.data_processor.read_and_concat_data_files()
        self.data_processor.remove_duplicates_and_nones()
        self.data_processor.filter_dates()
        # optionally removing topics if these have been passed in in the constructor
        if self.data_processor.topics_to_remove:
            self.data_processor.filter_topics(self.topics_to_remove)
        self.data = self.data_processor.combined_data

        self.data['headline'] = self.data['headline'].apply(lambda x: self._clean_text(x))
        self.data['date'] = self.data['date'].apply(lambda x: str(x))

    # to apply to a pandas df column within lambda func
    # TODO: further clean eg remove special chars (currently lowercases and removes stopwords)
    def _clean_text(self, text):
        return ' '.join([str(word) for word in str(text).lower().split() if word not in (self.stopwords_list)])

    # TODO: refactor to handle more than one model at once? or no need to save as object property if saving model
    def model_topics(self):
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
            min_topic_size = self.min_topic_size, # minimum documents/articles making up each cluster
            top_n_words = 4, # how many of the top words used to describe/define each cluster
            language = 'english', # the default is english but specifying
            calculate_probabilities = True # calculate probability of document being in all clusters and assign to highest prob
        )

        self.topics = self.topic_model.fit_transform(list(self.data['headline'].apply(lambda x: str(x))))
        self._cluster_examples(self.source_name)
        self.topic_model.get_topic_info()
        print(self.topic_model.get_topic_info())
        return self.topic_model

    # prob want couple of these methods and above to do for different data e.g. headlines subheadings and article text
    def get_topics_over_time(self):
        self.data.reset_index(inplace = True,drop = True)
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

    def _cluster_examples(self, name):
        # TODO: have this handle large datasets by saving in chunks 
        # getting representative examples for each cluster/topic in the model
        if hasattr(self, 'topic_model'):
            num_topics = max(self.topic_model.topics_)
            if num_topics > 150:
                # save with csv if over certain num of topics else get all at once
                # note, .topics_ gives array of ints and -1, can try getting the max and using as range
                print(num_topics)
                current_path = Path(__file__).parent
                temp_csv_path = f'{current_path}/temp/temp_repesentative_docs_{self.source_name}.csv'
                example_topics = []
                example_docs = []
                for i in range(num_topics):
                    if i % 19 == 0:
                        temp_df = pd.DataFrame()
                        temp_df['topic'] = example_topics
                        temp_df['docs'] = example_docs
                        # save append to csv, no headers or index
                        temp_df.reset_index(drop=True)
                        temp_df.to_csv(temp_csv_path, mode='a', header= False, index = False)

                        example_topics = []
                        example_docs = []
                    example_topics.append(i)
                    example_docs.append(self.topic_model.get_representative_docs(i))
                    
                # then load back in and assign to dataframe
                full_df = pd.read_csv(temp_csv_path, names = ['topic', 'docs'], header = None)
                # example_docs = self.topic_model.get_representative_docs() # may not save as property if this is unnecessary use of memory
                path = Path(__file__).parent
                
                example_docs_cast = dict(full_df.values)
                with open(f'{path}/plots/topic_doc_examples/{name}.json', 'w') as file_:
                    json.dump(example_docs_cast, file_)
            else:
                example_docs = self.topic_model.get_representative_docs()
                path = Path(__file__).parent
                # have to explicitly cast to int, otherwise type is int32 (presumably numpy) and causes issues dumping into json file
                example_docs_cast = {int(x):example_docs[x] for x in example_docs.keys()}
                with open(f'{path}/plots/topic_doc_examples/{name}.json', 'w') as file_:
                    json.dump(example_docs_cast, file_)
                # returned as a dict with topic # int : [list of docs, more docs, for each topic]
                # note lack of order so would want to iterate explicitly by key to get right order
                # also note the returned docs won't be the exact headline due to preprocessing

                return example_docs

            # os.remove(temp_csv_path)
            # TODO: how to save these and then show them
            # saving as json for now, can either import into where showing results as a separate thing
            # or try and look at ways of incorporating into existing visualisations
            # path = Path(__file__).parent
            # have to explicitly cast to int, otherwise type is int32 (presumably numpy) and causes issues dumping into json file
            # example_docs_cast = {int(x):example_docs[x] for x in example_docs.keys()}
            # print(example_docs_cast)
            # UNCOMMENT BELOW 2 LINES vvvv
            # with open(f'{path}/plots/topic_doc_examples/{name}.json', 'w') as file_:
            #     json.dump(example_docs_cast, file_)
            # returned as a dict with topic # int : [list of docs, more docs, for each topic]
            # note lack of order so would want to iterate explicitly by key to get right order
            # also note the returned docs won't be the exact headline due to preprocessing
            
            return example_docs
        else:
            raise Exception('Topic model not found, run .model_topics() to create the topic model and get examples')

    # TODO: slightly different process to run all sources together as classes to compare - by joint broad categories as defined by the newspapers
    # potential shared categories - uk news, world news, health, money, politics, royals?, education?, environment?
    # note might not be able to get any categories for - metro, express (maybe with getting data again slight change), 
    def multi_class_model(self, topic):
        # TODO: add a check for if the data has everything you need e.g. columns have the source to use as class and something to get the category 
        # TODO: class will need to add to the df based on the file name - first word after splitting by underscores
        # have added classes as 'source' column at the data processor stage
        self.umap = UMAP(n_neighbors = 15,
            n_components = 5,
            min_dist = 0.0,
            metric = 'cosine',
            random_state = 42)
        
        self.count_vectoriser = CountVectorizer(stop_words = self.stopwords_list)

        self.topic_model = BERTopic(umap_model = self.umap,
            vectorizer_model = self.count_vectoriser,
            diversity = 0.75,
            min_topic_size = self.min_topic_size,
            top_n_words = 4,
            language = 'english',
            calculate_probabilities = True
        )

        self.topics = self.topic_model.fit_transform(list(self.data['headline'].apply(lambda x: str(x))))
        classes = self.data['']
        # example from the docs below - 
        # data = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))
        # docs = data["data"]
        # classes = [data["target_names"][i] for i in data["target"]]

        # # Create topic model and calculate topics per class
        # topic_model = BERTopic()
        # topics, probs = topic_model.fit_transform(docs)
        # topics_per_class = topic_model.topics_per_class(docs, classes=classes)

        self.topic_model.get_topic_info()
        print(self.topic_model.get_topic_info())
        return self.topic_model

if __name__ == "__main__":
    # guardian_topic_modeller = TopicModeller('guardian_*.csv')
    # guardian_topic_modeller.model_topics()

    # note, preprocessing not called separately anymore, done by default on init
    # guardian_topic_modeller._preprocess()
    # 
    # # guardian_topic_modeller.get_topics_over_time()
    # guardian_topic_modeller.html_plot('guardian_topic_plot')
    # ['wires','femail', 'sport', 'showbiz']
    
    # mail_topic_modeller.save_as_json('mail_topics')
    
    mail_topic_modeller = TopicModeller('mail*.csv', data_cols = ['headline', 'date', 'url'], topics_to_remove = ['wires','femail', 'sport', 'showbiz'])
    mail_topic_modeller.model_topics()