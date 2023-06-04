import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
from topic_modeller import TopicModeller
import os
import glob
from pathlib import Path
import pandas as pd
import datetime
import shutil
from bertopic import BERTopic
import plotly
import json

# @unittest.skip('skipping for speed while still writing other new tests')
class TestTopicModeller(unittest.TestCase):

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

    # NOTE: this is done by preprocess method which is mostly calling methods of the data processor class that have been separately tested
    def test_constructor_adds_data_as_property_of_topic_modeller(self):
        # given - some data in csv files 
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        # when - we create an instance of the topic modeller class
        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], save_path=self.temp_within_current_dir)

        # then - the topic modeller class has a data property added by constuctor
        self.assertTrue(hasattr(undertest_class, 'data'))

    def test_constructor_adds_data_as_property_of_topic_modeller_which_is_all_lowercase(self):
        # given - some data in csv files with mixed case
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'A TESTING headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a TEST']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        # when - we create an instance of the topic modeller class where preprocess is called in the constructor
        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], save_path=self.temp_within_current_dir)
        actual_headlines = list(undertest_class.data['headline'])

        actual_headlines_lowercased = [i.lower() for i in actual_headlines]

        # then - the topic modeller headline data is all lowercase, sense checking the preprocessing has been applied
        self.assertListEqual(sorted(actual_headlines), sorted(actual_headlines_lowercased))

    def test_model_topics_returns_bertopic_model(self):
        # given - some data for one source passed into a topic modeller instance, with enough data to get some clusters with the parameters
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir)
        
        # when - we call the model topics method of the undertest topic modeller
        actual_model_returned = undertest_class.model_topics()

        # then - an instance of a bertopic model is returned
        actual_model_class = actual_model_returned.__class__
        expected_model_class = BERTopic

        self.assertEqual(actual_model_class, expected_model_class)

    def test_model_topics_adds_topics_property(self):
        # given - some data for one source passed into a topic modeller instance, with enough data to get some clusters with the parameters
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir)
        
        # when - we call the model topics method of the undertest topic modeller
        undertest_class.model_topics()

        # then - the undertest topic modeller now has a topics property
        self.assertTrue(hasattr(undertest_class, 'topics'))
    
    def test_model_topics_adds_topics_df_with_expected_columns(self):
        # given - some data for one source passed into a topic modeller instance, with enough data to get some clusters with the parameters
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir)
        
        # when - we call the model topics method of the undertest topic modeller and call get topic info on the resulting model
        undertest_class.model_topics()
        actual_topics = undertest_class.topic_model.get_topic_info()
        actual_columns = actual_topics.columns.tolist()

        # then - topic info shows expected columns for topic count and name
        expected_columns = ['Topic', 'Count', 'Name']
        self.assertListEqual(sorted(actual_columns), sorted(expected_columns))

    def test_get_topics_over_time_adds_topics_over_time_property(self):
        # given - some headline data passed into an instance of the topic modeller class
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir)

        # when - we call the get topics over time method of the undertest topic modeller
        undertest_class.get_topics_over_time()

        # then - the topic modeller instance has a topics over time property
        self.assertTrue(hasattr(undertest_class, 'topics_over_time'))

    def test_get_topics_over_time_adds_topics_over_time_df_with_expected_columns(self):
        # given - some headline data passed into an instance of the topic modeller class
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir)

        # when - we call the get topics over time method of the undertest topic modeller
        undertest_class.get_topics_over_time()
        actual_topics_over_time = undertest_class.topics_over_time
        actual_columns = actual_topics_over_time.columns.tolist()

        # then - the topic modeller's topics_over_time property has the expected columns
        expected_columns = ['Topic', 'Words', 'Frequency', 'Timestamp']
        self.assertListEqual(sorted(actual_columns), sorted(expected_columns))

    def test_visualise_over_time_returns_plot(self):
        # given - some headline data passed into an instance of the topic modeller class
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir)

        # when - we call the visualise over time builtin (this is calling a bertopic method) method of the undertest topic modeller
        actual_plot = undertest_class.visualise_over_time_builtin() 

        # then - a plotly plot is returned
        self.assertTrue(isinstance(actual_plot, plotly.graph_objects.Figure))

    def test_save_as_json_saves_topic_cluster_graph(self):
        # given - some headline data passed into an instance of the topic modeller class
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(10):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir, n_neighbours=2)

        # when - we call the save as json method of the undertest class
        undertest_class.save_as_json('test')

        # then - the expected json file for the topic cluster graph is there
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test_topics.json')
        self.assertTrue(test_file_path.is_file())

    def test_save_as_json_saves_topics_over_time_graph(self):
        # given - some headline data passed into an instance of the topic modeller class
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(10):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir, n_neighbours=2)

        # when - we call the save as json method of the undertest class
        undertest_class.save_as_json('test')

        # then - the expected json file for the topics over time graph is there
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test_over_time.json')
        self.assertTrue(test_file_path.is_file())

    def test_cluster_examples_saves_expected_json_file(self):
        # given - some headline data passed into an instance of the topic modeller class
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(10):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir, n_neighbours=2)

        # when - we call the model topics method where the internal method to cluster topics is run from
        undertest_class.model_topics()

        # then - a json file with the cluster examples is created with a name based on the selector
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/topic_doc_examples/test.json')
        self.assertTrue(test_file_path.is_file())
    
    def test_cluster_examples_creates_same_length_obj_as_topics(self):
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(10):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = TopicModeller(data_selector="test*.csv", data_dir = f'./{self.test_dir_name}', data_cols = ['headline', 'date'], min_topic_size= 3, save_path=self.temp_within_current_dir, n_neighbours=2)

        # when - we call the model topics method where the internal method to cluster topics is run from, and load in the resulting file
        undertest_class.model_topics()
        topic_list = undertest_class.topic_model.get_topic_info() 

        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/topic_doc_examples/test.json')
        with open(test_file_path) as f:
            file_data = json.load(f)
        
        # note, -1 because topic list includes the category for everything that didnt fit into clusters, which representative docs file doesn't
        num_topics_from_topic_list = len(topic_list) - 1 
        num_topics_from_file = len(list(file_data.keys()))

        # then - the number of topics in the representative docs file matches total topics for the model
        self.assertEqual(num_topics_from_file, num_topics_from_topic_list)

    # teardown after all tests run to delete temporary files used in tests
    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.temp_within_current_dir)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')

if __name__ == "__main__":
    unittest.main()