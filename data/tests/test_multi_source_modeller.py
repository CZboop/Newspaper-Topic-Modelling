import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
import src
from src.multi_source_modeller import MultiSourceModeller
from src.topic_modeller import TopicModeller
import os
import glob
from pathlib import Path
import pandas as pd
import datetime
import shutil
from bertopic import BERTopic
import plotly
import json
from itertools import chain

# @unittest.skip('skipping for speed while still writing other new tests')
class TestMultiSourceModeller(unittest.TestCase):

    maxDiff = None

    # setup before the test suite run
    @classmethod
    def setUpClass(self):
        # create temp directory for files with test data
        self.test_dir_name = 'temp_test_files'
        self.temp_within_current_dir = f'{Path(__file__).parent}/{self.test_dir_name}'
        Path(self.temp_within_current_dir).mkdir(parents=True, exist_ok=True)

    def setup_write_test_csv_file(self, dataframe, name):
        dataframe.to_csv(f'{self.temp_within_current_dir}/{name}')

    def test_save_model_creates_model_file(self):
        # given - a single bertopic model created by TopicModeller class and an instance of the MultiSourceModeller class
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(10):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        topic_modeller = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir, n_neighbours=2)
        test_topic_model = topic_modeller.model_topics()

        undertest_class = MultiSourceModeller(data_selectors = {'test' : {'selector': 'test*.csv'}}, save_path = self.test_dir_name, data_dir = self.test_dir_name)

        # when - we call the internal save model method, passing in a model and name for the file
        undertest_class._save_model(test_topic_model, 'test_model')        

        # then - the expected test model file is created
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/models/test_model')
        self.assertTrue(test_file_path.is_file())

    def test_save_model_creates_model_that_can_be_loaded(self):
        # given - a single bertopic model and an instance of the MultiSourceModeller class
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(10):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        topic_modeller = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir, n_neighbours=2)
        test_topic_model = topic_modeller.model_topics()

        undertest_class = MultiSourceModeller(data_selectors = {'test' : {'selector': 'test*.csv'}}, save_path = self.test_dir_name, data_dir = self.test_dir_name)

        # when - we call the internal save model method, passing in a model and name for the file, then load it back in with built in bertopic load
        undertest_class._save_model(test_topic_model, 'test_model')
        actual_loaded_model = BERTopic.load(f'{self.test_dir_name}/models/test_model')

        # then - loaded in is an instance of a bertopic model
        self.assertTrue(isinstance(actual_loaded_model, BERTopic))

    def test_run_with_multiple_sources_sets_models_as_class_properties_for_all_sources(self):
        # given - data for multiple sources and a multi source modeller undertest instance with matching list of sources passed in
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : list(chain.from_iterable(headline_list_of_lists)), 'date' : list(chain.from_iterable(date_list_of_lists)), 'url' : ['www.test-url.com/123'] * len(list(chain.from_iterable(headline_list_of_lists))), 'source' : [f'test{i}'] * len(list(chain.from_iterable(headline_list_of_lists)))})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceModeller(data_selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, save_path = self.temp_within_current_dir, data_dir = self.test_dir_name, min_topic_size= 3, n_neighbours=2)

        # when - we call the run method of the undertest class
        undertest_class.run()

        # then - the undertest instance has a _model property for every source passed in via selectors
        self.assertTrue(hasattr(undertest_class, 'test0_model'))
        self.assertTrue(hasattr(undertest_class, 'test1_model'))
        self.assertTrue(hasattr(undertest_class, 'test2_model'))
        self.assertTrue(hasattr(undertest_class, 'test3_model'))
        self.assertTrue(hasattr(undertest_class, 'test4_model'))

    def test_run_with_multiple_sources_saves_cluster_plots_for_all_sources(self):
        # given - data for multiple sources and an instance of the multi source modeller class with matching selectors for the sources
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : list(chain.from_iterable(headline_list_of_lists)), 'date' : list(chain.from_iterable(date_list_of_lists)), 'url' : ['www.test-url.com/123'] * len(list(chain.from_iterable(headline_list_of_lists))), 'source' : [f'test{i}'] * len(list(chain.from_iterable(headline_list_of_lists)))})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceModeller(data_selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, save_path = self.temp_within_current_dir, data_dir = self.test_dir_name, min_topic_size= 3, n_neighbours=2)

        # when - we call the run method of the undertest class
        undertest_class.run()

        # then - a topic cluster plot file has been saved for each source
        topic_plot0_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test0_topics.json')
        topic_plot1_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test1_topics.json')
        topic_plot2_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test2_topics.json')
        topic_plot3_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test3_topics.json')
        topic_plot4_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test4_topics.json')

        self.assertTrue(topic_plot0_file.is_file())
        self.assertTrue(topic_plot1_file.is_file())
        self.assertTrue(topic_plot2_file.is_file())
        self.assertTrue(topic_plot3_file.is_file())
        self.assertTrue(topic_plot4_file.is_file())

    def test_run_with_multiple_sources_saves_over_time_plots_for_all_sources(self):
        # given - data for multiple sources and an instance of the multi source modeller class with matching selectors for the sources
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : list(chain.from_iterable(headline_list_of_lists)), 'date' : list(chain.from_iterable(date_list_of_lists)), 'url' : ['www.test-url.com/123'] * len(list(chain.from_iterable(headline_list_of_lists))), 'source' : [f'test{i}'] * len(list(chain.from_iterable(headline_list_of_lists)))})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceModeller(data_selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, save_path = self.temp_within_current_dir, data_dir = self.test_dir_name, min_topic_size= 3, n_neighbours=2)

        # when - we call the run method of the undertest class 
        undertest_class.run()

        # then - there are topic over time plots saved for each source
        over_time_plot0_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test0_over_time.json')
        over_time_plot1_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test1_over_time.json')
        over_time_plot2_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test2_over_time.json')
        over_time_plot3_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test3_over_time.json')
        over_time_plot4_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test4_over_time.json')

        self.assertTrue(over_time_plot0_file.is_file())
        self.assertTrue(over_time_plot1_file.is_file())
        self.assertTrue(over_time_plot2_file.is_file())
        self.assertTrue(over_time_plot3_file.is_file())
        self.assertTrue(over_time_plot4_file.is_file())

    def test_run_creates_representative_doc_files_for_all_sources(self):
        # given - data for multiple sources and an instance of the multi source modeller class with matching selectors for the sources
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : list(chain.from_iterable(headline_list_of_lists)), 'date' : list(chain.from_iterable(date_list_of_lists)), 'url' : ['www.test-url.com/123'] * len(list(chain.from_iterable(headline_list_of_lists))), 'source' : [f'test{i}'] * len(list(chain.from_iterable(headline_list_of_lists)))})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceModeller(data_selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, save_path = self.temp_within_current_dir, data_dir = self.test_dir_name, min_topic_size= 3, n_neighbours=2)

        # when - we call the run method of the undertest class 
        undertest_class.run()

        # then - representative doc files are create for each source
        example_docs0_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/topic_doc_examples/test0.json')
        example_docs1_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/topic_doc_examples/test1.json')
        example_docs2_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/topic_doc_examples/test2.json')
        example_docs3_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/topic_doc_examples/test3.json')
        example_docs4_file = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/topic_doc_examples/test4.json')

        self.assertTrue(example_docs0_file.is_file())
        self.assertTrue(example_docs1_file.is_file())
        self.assertTrue(example_docs2_file.is_file())
        self.assertTrue(example_docs3_file.is_file())
        self.assertTrue(example_docs4_file.is_file())

    # teardown after all tests run to delete temporary files used in tests
    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.temp_within_current_dir)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')

if __name__ == "__main__":
    unittest.main()