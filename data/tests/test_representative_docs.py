import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
import src
from src.representative_docs import RepresentativeDocsRepresenter
import os
from pathlib import Path
import pandas as pd
import pandas.testing as pd_testing
import shutil
import json

# NOTE: the class being tested simply adds representative docs to an existing plot
# getting representative docs is built in to BERTopic, used in the topic modeller class within this project, and doesn't need to be tested here
class TestRepresentativeDocs(unittest.TestCase):

    maxDiff = None

    # setup before the test suite run
    @classmethod
    def setUpClass(self):
        # create temp directory for files with test data
        self.test_dir_name = 'temp_test_files'
        self.temp_within_current_dir = f'{Path(__file__).parent}/{self.test_dir_name}'
        Path(self.temp_within_current_dir).mkdir(parents=True, exist_ok=True)

        # also for this class, writing to existing relative path for plots so will create that too
        self.temp_plot_path_parent = f'{Path(__file__).parent}/plots'
        self.temp_plot_path_full = f'{Path(__file__).parent}/plots/plots_with_examples'
        Path(self.temp_plot_path_full).mkdir(parents=True, exist_ok=True)

    # helper function to write files with data to be used in tests
    def setup_write_test_json_file(self, data, filename):
        with open(f'{self.test_dir_name}/{filename}', 'w') as file_:
            json.dump(data, file_)

    def test_reading_in_data(self):
        # given - a fresh instance of the representative docs class and json files with a simplified topic plotly plot and a list of representative docs for the topics on that plot
        test_data_plot = {"data" : [{"customdata" : [[0, "cluster | title | but | fake", 100], [1, "a | different | test | topic", 100], [2, "cluster | title | once | again", 100], [3, "the | words | of | cluster", 100], [4, "topic | definition | but | testing", 100], [5, "a | topic | in | test", 100], [6, "name | of | the | group", 100], [7, "a | bag | of | docs", 100], [8, "chunks | of | data | here", 100], [9, "some | words | in | group", 100]],"hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}"}]}
        self.setup_write_test_json_file(test_data_plot, 'test_topics.json')

        test_data_docs = {"2" : ["example 1 group 2", "example 2 group 2"], "4" : ["example 1 group 4", "example 2 group 4", "example 3 group 4"], "6" : ["example 1 group 6"], "8" : ["example 1 group 8", "example 2 group 8"], "1" : ["example 1 group 1", "example 2 group 1"], "3" : ["example 1 group 3", "example 1 group 3"], "5" : ["example 1 group 5"], "7" : ["example 1 group 7", "example 2 group 7"], "9" : ["example 1 group 9", "example 2 group 9", "example 3 group 9"]}
        self.setup_write_test_json_file(test_data_docs, 'test.json')

        undertest_class = RepresentativeDocsRepresenter(path_to_plot = 'temp_test_files', path_to_repr_docs = 'temp_test_files', sources=['test'])

        # when - the read data method is called for the given source
        undertest_class._read_data(source='test')

        # then - the two json plots are added as new class properties
        self.assertTrue(hasattr(undertest_class, "plot"))
        self.assertTrue(hasattr(undertest_class, "repr_docs"))

    def test_adding_representative_docs_to_plot(self):
        # given - a fresh instance of the representative docs class and json files with a simplified topic plotly plot and a list of representative docs for the topics on that plot, where data has been read in
        test_data_plot = {"data" : [{"customdata" : [[0, "cluster | title | but | fake", 100], [1, "a | different | test | topic", 100], [2, "cluster | title | once | again", 100], [3, "the | words | of | cluster", 100], [4, "topic | definition | but | testing", 100], [5, "a | topic | in | test", 100], [6, "name | of | the | group", 100], [7, "a | bag | of | docs", 100], [8, "chunks | of | data | here", 100], [9, "some | words | in | group", 100]],"hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}"}]}
        self.setup_write_test_json_file(test_data_plot, 'test_topics.json')

        test_data_docs = {"0" : ["example 1 group 0", "example 2 group 0"], "2" : ["example 1 group 2", "example 2 group 2"], "4" : ["example 1 group 4", "example 2 group 4", "example 3 group 4"], "6" : ["example 1 group 6"], "8" : ["example 1 group 8", "example 2 group 8"], "1" : ["example 1 group 1", "example 2 group 1"], "3" : ["example 1 group 3", "example 1 group 3"], "5" : ["example 1 group 5"], "7" : ["example 1 group 7", "example 2 group 7"], "9" : ["example 1 group 9", "example 2 group 9", "example 3 group 9"]}
        self.setup_write_test_json_file(test_data_docs, 'test.json')

        undertest_class = RepresentativeDocsRepresenter(path_to_plot = 'temp_test_files', path_to_repr_docs = 'temp_test_files', sources=['test'])
        undertest_class._read_data(source="test")

        # when - the add representative docs method is called for the given source
        actual = undertest_class.add_repr_docs(source="test")

        # then - a new json plot is returned with the first representative doc added based on topic number not order
        expected = {"data" : [{"customdata" : [[0, "cluster | title | but | fake", 100, "example 1 group 0"], [1, "a | different | test | topic", 100, "example 1 group 1"], [2, "cluster | title | once | again", 100, "example 1 group 2"], [3, "the | words | of | cluster", 100, "example 1 group 3"], [4, "topic | definition | but | testing", 100, "example 1 group 4"], [5, "a | topic | in | test", 100, "example 1 group 5"], [6, "name | of | the | group", 100, "example 1 group 6"], [7, "a | bag | of | docs", 100, "example 1 group 7"], [8, "chunks | of | data | here", 100, "example 1 group 8"], [9, "some | words | in | group", 100, "example 1 group 9"]],"hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}<br>Example: %{customdata[3]}"}]}

        self.assertEqual(actual, expected)

    def test_running_for_all_sources(self):
        # given - an instance of the undertest class with multiple sources
        for i in range(3):
            test_data_plot = {"data" : [{"customdata" : [[0, "cluster | title | but | fake", 100], [1, "a | different | test | topic", 100], [2, "cluster | title | once | again", 100], [3, "the | words | of | cluster", 100], [4, "topic | definition | but | testing", 100], [5, "a | topic | in | test", 100], [6, "name | of | the | group", 100], [7, "a | bag | of | docs", 100], [8, "chunks | of | data | here", 100], [9, "some | words | in | group", 100]],"hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}"}]}
            self.setup_write_test_json_file(test_data_plot, f'test{i}_topics.json')

            test_data_docs = {"0" : ["example 1 group 0", "example 2 group 0"], "2" : ["example 1 group 2", "example 2 group 2"], "4" : ["example 1 group 4", "example 2 group 4", "example 3 group 4"], "6" : ["example 1 group 6"], "8" : ["example 1 group 8", "example 2 group 8"], "1" : ["example 1 group 1", "example 2 group 1"], "3" : ["example 1 group 3", "example 1 group 3"], "5" : ["example 1 group 5"], "7" : ["example 1 group 7", "example 2 group 7"], "9" : ["example 1 group 9", "example 2 group 9", "example 3 group 9"]}
            self.setup_write_test_json_file(test_data_docs, f'test{i}.json')

        undertest_class = RepresentativeDocsRepresenter(path_to_plot = 'temp_test_files', path_to_repr_docs = 'temp_test_files', sources=['test0', 'test1', 'test2'])        

        # when - the run for all sources method is called
        actual = undertest_class.run_for_all_sources()

        # then - as many updated plots as sources are returned
        expected = [{"data" : [{"customdata" : [[0, "cluster | title | but | fake", 100, "example 1 group 0"], [1, "a | different | test | topic", 100, "example 1 group 1"], [2, "cluster | title | once | again", 100, "example 1 group 2"], [3, "the | words | of | cluster", 100, "example 1 group 3"], [4, "topic | definition | but | testing", 100, "example 1 group 4"], [5, "a | topic | in | test", 100, "example 1 group 5"], [6, "name | of | the | group", 100, "example 1 group 6"], [7, "a | bag | of | docs", 100, "example 1 group 7"], [8, "chunks | of | data | here", 100, "example 1 group 8"], [9, "some | words | in | group", 100, "example 1 group 9"]],"hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}<br>Example: %{customdata[3]}"}]}, {"data" : [{"customdata" : [[0, "cluster | title | but | fake", 100, "example 1 group 0"], [1, "a | different | test | topic", 100, "example 1 group 1"], [2, "cluster | title | once | again", 100, "example 1 group 2"], [3, "the | words | of | cluster", 100, "example 1 group 3"], [4, "topic | definition | but | testing", 100, "example 1 group 4"], [5, "a | topic | in | test", 100, "example 1 group 5"], [6, "name | of | the | group", 100, "example 1 group 6"], [7, "a | bag | of | docs", 100, "example 1 group 7"], [8, "chunks | of | data | here", 100, "example 1 group 8"], [9, "some | words | in | group", 100, "example 1 group 9"]],"hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}<br>Example: %{customdata[3]}"}]}, {"data" : [{"customdata" : [[0, "cluster | title | but | fake", 100, "example 1 group 0"], [1, "a | different | test | topic", 100, "example 1 group 1"], [2, "cluster | title | once | again", 100, "example 1 group 2"], [3, "the | words | of | cluster", 100, "example 1 group 3"], [4, "topic | definition | but | testing", 100, "example 1 group 4"], [5, "a | topic | in | test", 100, "example 1 group 5"], [6, "name | of | the | group", 100, "example 1 group 6"], [7, "a | bag | of | docs", 100, "example 1 group 7"], [8, "chunks | of | data | here", 100, "example 1 group 8"], [9, "some | words | in | group", 100, "example 1 group 9"]],"hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}<br>Example: %{customdata[3]}"}]}]

        self.assertEqual(actual, expected)

    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.temp_within_current_dir)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')
        try:
            shutil.rmtree(self.temp_plot_path_parent)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')

if __name__ == "__main__":
    unittest.main()