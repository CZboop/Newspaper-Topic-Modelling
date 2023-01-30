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
        for source_name in self.data_sources.keys():
            # for each:
            # - create model and save
            model = TopicModeller(self.data_sources.get(source_name))
            model_name = f'{source_name}_model'
            setattr(self, model_name, model)
            self._save_model(model, model_name)
            # - get over time
            # - visualise

    def _save_model(self, model, name):
        try:
            model.save(name)
            return 1
        except:
            return -1

    def _load_model(self, name):
        model = BERTopic.load(name)
        return model

    def run(self):
        # running everything
        # load or create based on whether models already there in expected location
        pass

if __name__ == "__main__":
    modeller = MultiSourceModeller()
    modeller.run()