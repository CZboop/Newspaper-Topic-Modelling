# modelling all the different news sources
from bertopic import BERTopic
import datetime
from topic_modeller import TopicModeller

class MultiSourceModeller:
    def __init__(self, data_selectors = {'guardian' : 'guardian_*.csv', 'mirror' : 'mirror_*.csv', 'telegraph': 'telegraph_*.csv', 
    'sun' : 'sun_*.csv', 'mail' : 'mail_*.csv', 'metro' : 'metro_*.csv', 'express' : 'express_*.csv'}):
        self.data_selectors = data_selectors

    def model_all_sources(self):
        # getting topic models for each newspaper including saving
        for source_name in self.data_selectors.keys():
            # for each:
            # - create model and save
            model = TopicModeller(self.data_selectors.get(source_name)).model_topics()
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
    modeller = MultiSourceModeller()
    modeller.run()