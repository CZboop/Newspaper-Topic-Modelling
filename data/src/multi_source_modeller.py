# modelling all the different news sources
from bertopic import BERTopic
import datetime
from src.topic_modeller import TopicModeller
from pathlib import Path

class MultiSourceModeller:
    def __init__(self, data_selectors = {'guardian' : {'selector': 'guardian_*.csv'}, 'mirror' : {'selector': 'mirror_*.csv'}, 'telegraph': {'selector':'telegraph_*.csv'}, 'sun' : {'selector': 'sun_*.csv'}, 'mail' : {'selector': 'mail_*.csv', 'cols': ['headline', 'date', 'url'], 
    'topics_to_remove': ['wires','femail', 'sport', 'showbiz']}, 'metro' : {'selector': 'metro_*.csv'}, 
    'express' : {'selector': 'express_*.csv'}}, min_topic_size = 70, n_neighbours = 15, 
    n_components = 5, min_dist = 0.0, metric = 'cosine', random_state = 42, diversity = 0.75, top_n_words = 4,
    language = 'english', calculate_probabilities = True, global_tuning = True, evolution_tuning = True, nr_bins = 10,
    save_path = Path(__file__).parent, data_dir = '../../uk_news_scraping/data'):
        self.data_selectors = data_selectors
        self.min_topic_size = min_topic_size
        self.n_neighbours = n_neighbours
        self.n_components = n_components
        self.min_dist = min_dist
        self.metric = metric
        self.random_state = random_state
        self.diversity = diversity
        self.top_n_words = top_n_words
        self.language = language
        self.calculate_probabilities = calculate_probabilities
        self.global_tuning = global_tuning
        self.evolution_tuning = evolution_tuning
        self.nr_bins = nr_bins
        self.save_path = save_path
        self.data_dir = data_dir
    
    # run is equivalent of running topic modelling for all sources from selectors
    def run(self):
        # getting topic models for each newspaper including saving
        for source_name, selector_dict in self.data_selectors.items():
            # for each:
            # create modeller (this includes preprocessing)
            topic_modeller = TopicModeller(
                selector_dict.get('selector'), 
                min_topic_size = self.min_topic_size, 
                data_cols = selector_dict.get('cols', ['headline', 'date']), 
                topics_to_remove = selector_dict.get('topics_to_remove', None), 
                n_neighbours = self.n_neighbours,
                n_components = self.n_components,
                min_dist = self.min_dist,
                metric = self.metric,
                random_state = self.random_state,
                diversity = self.diversity,
                top_n_words = self.top_n_words,
                language = self.language,
                calculate_probabilities = self.calculate_probabilities,
                global_tuning = self.global_tuning,
                evolution_tuning = self.evolution_tuning,
                nr_bins = self.nr_bins,
                data_dir = self.data_dir,
                save_path = self.save_path
            )
            # model topics and return the model
            model = topic_modeller.model_topics()
            # save plots
            # note, save as json is doing a lot of work saves all the resulting graphs from topic modeller (cluster graph and top over time)
            topic_modeller.save_as_json(source_name)
            # save the model
            model_name = f'{source_name}_model'
            setattr(self, model_name, model)
            print(self._save_model(model, model_name))

    def _save_model(self, model, name):
        # create models directory if not exists
        Path(f'{self.save_path}/models').mkdir(parents=True, exist_ok=True)
        try:
            model.save(f'{self.save_path}/models/{name}')
        except Exception as exception:
            raise Exception(f'Error while attempting to save model \'{model}\' as file name \'{name}\' - {exception.strerror}')

if __name__ == "__main__":
    modeller = MultiSourceModeller()
    modeller.run()