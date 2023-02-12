# modelling all the different news sources
from bertopic import BERTopic
import datetime
from topic_modeller import TopicModeller

#data_selectors = {'guardian' : 'guardian_*.csv', 'mirror' : 'mirror_*.csv', 'telegraph': 'telegraph_*.csv', 
    # 'sun' : 'sun_*.csv', 'mail' : 'mail_*.csv', 'metro' : 'metro_*.csv', 'express' : 'express_*.csv'}
    # mail may be causing memory issues, will exclude and come back to

class MultiSourceModeller:
    def __init__(self, data_selectors = {'metro' : 'metro_*.csv', 'express' : 'express_*.csv'}, min_topic_size = 70):
        self.data_selectors = data_selectors
        self.min_topic_size = min_topic_size

    def model_all_sources(self):
        # getting topic models for each newspaper including saving
        for source_name in self.data_selectors.keys():
            # for each:
            # - create model and save
            topic_modeller = TopicModeller(self.data_selectors.get(source_name), min_topic_size = self.min_topic_size)
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
    modeller = MultiSourceModeller({'mirror' : 'mirror_*.csv', 'sun' : 'sun_*.csv', 'mail' : 'mail_*.csv'})
    modeller.run()