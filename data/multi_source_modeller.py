# modelling all the different news sources
from bertopic import BERTopic
import datetime
from topic_modeller import TopicModeller

class MultiSourceModeller:
    def __init__(self, data_selectors = {'guardian' : {'selector': 'guardian_*.csv'}, 'mirror' : {'selector': 'mirror_*.csv'}, 'telegraph': {'selector':'telegraph_*.csv'}, 
    'sun' : {'selector': 'sun_*.csv'}, 'mail' : {'selector': 'mail_*.csv', 'cols': ['headline', 'date', 'url'], 'topics_to_remove': ['wires','femail', 'sport', 'showbiz']}, 
    'metro' : {'selector': 'metro_*.csv'}, 'express' : {'selector': 'express_*.csv'}}, min_topic_size = 70):
        self.data_selectors = data_selectors
        self.min_topic_size = min_topic_size

    def model_all_sources(self):
        # getting topic models for each newspaper including saving
        for source_name, selector_dict in self.data_selectors.items():
            # for each:
            # - create model and save
            # data_cols, topics_to_remove
            topic_modeller = TopicModeller(selector_dict.get('selector'), min_topic_size = self.min_topic_size, data_cols = selector_dict.get('cols', ['headline', 'date']), topics_to_remove = selector_dict.get('topics_to_remove', None))
            # topic_modeller._preprocess()
            model = topic_modeller.model_topics()
            topic_modeller.save_as_json(source_name)
            model_name = f'{source_name}_model'
            setattr(self, model_name, model)
            print(self._save_model(model, model_name))
            # - get over time
            # - visualise

    def _save_model(self, model, name):
        try:
            model.save(f'models/{name}')
        except:
            raise Exception(f'Error while attempting to save model \'{model}\' as file name \'{name}\'')

    def _load_model(self, name):
        try:
            model = BERTopic.load(name)
            return model
        except:
            raise Exception(f'Error while attempting to load model {name}')

    def run(self):
        # running everything
        # load or create based on whether models already there in expected location
        self.model_all_sources()

if __name__ == "__main__":
    # currently not running all at once 
    modeller = MultiSourceModeller(data_selectors = {'metro' : {'selector': 'metro_*.csv'}, 'express' : {'selector': 'express_*.csv'}})
    modeller.run()