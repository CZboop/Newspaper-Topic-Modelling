# Newspaper Topic Modelling 📰 🔍 

NLP topic modelling of UK newspapers, with analysis of topics over time, as well as sentiment analysis of polarity and subjectivity of language used.

## Project Summary

## Tools Used
### Languages:
* [Python](https://www.python.org/) - for data analysis
* [JavaScript](https://www.javascript.com/) - for front-end web app

### Libraries/Frameworks:
#### Front-End
* [React JSX](https://react.dev/) - primary framework for creating the web app
* [React Router](https://reactrouter.com/en/main) - to create multiple routes/pages within the app
* [React Plotly JS](https://plotly.com/javascript/react/) - to represent and manipulate Plotly graphs within the web app
* [React Resize Detector](https://www.npmjs.com/package/react-resize-detector) - to handle page resize including altering page content dependent on size
* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) (including media queries) - for web styling, and handling mobile/screen size responsiveness

##### Testing (Front End)
* [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) including [Jest DOM](https://testing-library.com/docs/ecosystem-jest-dom/) - to render components and select elements from the page, and create tests (primarily smoke tests as there is little user interaction with the page)

#### Data
* [BERTopic](https://maartengr.github.io/BERTopic/index.html) (including [UMAP](https://umap-learn.readthedocs.io/en/latest/), [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/) and [sci-kit learn](https://scikit-learn.org/stable/)) - for topic modelling and many elements of analysis such as:
    * Finding topics (including in order of frequency, with count of occurence)
    * Creation of topic cluster and topics over time visualisations
    * Getting representative documents per topic
    * Getting topics over time
* [SpaCy](https://spacy.io/) (including [SpaCy TextBlob](https://spacy.io/universe/project/spacy-textblob)) - for stopword removal and polarity/subjectivity analysis
* [Pandas](https://pandas.pydata.org/) - for creation of dataframes to store and manipulate data
* [Plotly](https://plotly.com/python/) - for saving and adjusting the plots created by BERTopic
* [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) - for scraping data to be analysed
* [httplib2](https://pypi.org/project/httplib2/) - for making requests as part of data scraping
* [Glob](https://docs.python.org/3/library/glob.html) - for pattern based file and path selection (to read in data stored across multiple files)
* [Datetime](https://docs.python.org/3/library/datetime.html) and [Dateutil](https://dateutil.readthedocs.io/en/stable/) - to select data from time ranges and iterate over time deltas
* [Pathlib](https://docs.python.org/3/library/pathlib.html), [sys](https://docs.python.org/3/library/sys.html), [shutil](https://docs.python.org/3/library/shutil.html) and [os](https://docs.python.org/3/library/os.html) - for selecting, creating and deleting files and directories
* [Json](https://docs.python.org/3/library/json.html) - for encoding and decoding json files and data

##### Testing (Data)
* [Unittest](https://docs.python.org/3/library/unittest.html) - primary unit test framework, with test suites created as class of type unittest.TestCase
* [Pytest](https://docs.pytest.org/en/7.3.x/) - to run tests from the command line
* [Pandas testing](https://pandas.pydata.org/docs/reference/testing.html) - to assert dataframe equality

## Dataset

## How to Install and Run

## How to Use
