# Newspaper Topic Modelling 📰 🔍 

NLP topic modelling of UK newspapers, with analysis of topics over time, as well as sentiment analysis of polarity and subjectivity of language used. Python data analysis and React JSX website presenting that analysis, which is live here: [https://czboop.github.io/Newspaper-Topic-Modelling/](https://czboop.github.io/Newspaper-Topic-Modelling/)

## Project Summary
This project uses several techniques within natural language processing to explore seven of the top newspapers in the UK. Data analysed for all sources covered the period from just before the start of the COVID-19 pandemic (late November 2019), until the start of 2023 (early January). The newspapers analysed were:
* The Express
* The Dail Mail
* The Sun
* The Mirror
* The Telegraph
* The Guardian
* Metro

Headlines were used exclusively, rather than the main body of articles, for all sources and all analysis.
BERTopic (a Python package using SBERT, UMAP, HDBSCAN, CountVectorizer and c-TF-IDF to cluster text data into topics) was used to create topic clusters, as well as to perform other topic modelling related analysis. 
SpaCy TextBlob (a SpaCy Universe package implementing TextBlob sentiment analysis with SpaCy) was also used to analyse the subjectivity (level of being factual or opinionated) and polarity (level of being emotionally positive or negative) of different newspapers. 
Plotly was used to create new plots to represent this, as well as to manipulate the plots that are created by BERTopic.

Alongside the Python data analysis, a React web app was also created to present many of the findings from this analysis, and the graphs that visualise the data.

This repository contains a combination of a Python data directory, and a React web app directory used to present some of the findings in a more visual and user friendly way.

Data was scraped from the internet over a period of time, with a limited number of requests per minute. More information on the dataset can be found below. The dataset used as the basis of this analysis is not public and is not intended to be made public. The scraping scripts are not part of this or any other public repository.

## Dataset Details and Limitations
The dataset used was collected from the websites of each of the respective newspapers, with slightly different techniques for some newspapers. Different newspapers had very different numbers of total documents, with The Daily Mail having by far the highest number of documents, and The Guardian having the lowest.  

There were also varying levels of completeness in terms of what percentage of all headlines made it into the dataset, depending on source.  

For the Daily Mail, a complete set of all headlines from this time period was collected. However, the extremely high number of documents from The Daily Mail was intially creating a model that was too large (in terms of memory - around 17GB) so the script would error while trying to fit the model. Due to this, some types of articles were removed from before training and analysis. This included a large chunk of documents that were re-published by The Daily Mail, but came from other sources such as Reuters or the Associated Press. Showbiz, Sport and Lifestyle articles were also removed. The Daily Mail still had by far the most documents even after this filtering.  

Some other newspapers had high level categories limited at the point of data collection, but all of these were then analysed. This applied to The Telegraph, The Guardian, The Mirror and The Sun. These categories were largely based on the main news categories that the each newspaper used for their articles.  

The categories collected and analysed (or not) for these newspapers can be seen in the table below. Note, in some cases absence of a category may mean that the newspaper does not flag articles with this label, while in other cases this may be a gap in the dataset. Categories that are not shown in the table (such as sport) can be assumed to be excluded for all of these sources:

|              |The Sun|The Mirror|The Telegraph|The Guardian|
|--------------|-------|----------|-------------|------------|
|Politics      |✔️ |✔️ |✔️ |✔️ |
|Science       |✔️ |✔️ |✔️ |✔️ |
|Technology    |❌ |✔️ |❌ |✔️ |
|UK News       |✔️ |✔️ |✔️ |❌ |
|World News    |✔️ |✔️ |✔️ |❌ |
|US News       |❌ |✔️ |❌ |❌ |
|Health        |❌ |✔️ |✔️ |❌ |
|Environment   |❌ |❌ |✔️ |✔️ |
|Education     |❌ |❌ |✔️ |✔️ |
|Royal Family  |❌ |✔️ |✔️ |❌ |
|Business      |❌ |❌ |❌ |✔️ |
|Society       |❌ |❌ |❌ |✔️ |
|'More Hopeful'|❌ |✔️ |❌ |❌ |
|Defence       |❌ |❌ |✔️ |❌ |
|Opinion       |✔️ |❌ |❌ |❌ |

On the other hand, the Metro and Daily Express newspapers had what should be a complete set of their headlines both collected and analysed.

## Repository Contents
Some of the key repository contents:

* 📁 data: python files for data analysis
    * 📁 src: main data content
        * 📁 plots: where data visualisations are saved
        * 📄 data_processor.py - a class used within other objects to load in and process data files
        * 📄 general_analyser.py - performs basic analysis on data e.g. ratio of documents by source, number of articles by month
        * 📄 multi_source_modeller.py - performs topic modelling on multiple sources one after the other
        * 📄 multi_source_sentiments.py - performs sentiment analysis on multiple sources one after the other
        * 📄 representative_docs.py - adds representative document to the hover tooltip of json file visualising topics
        * 📄 sentiment.py - analyses subjectivity and polarity, including over time, and creates visualisations of these
        * 📄 topic_modeller.py - finds topics from data and save results as plots
    * 📁 tests: unit tests for the files in the data/src folder
    
* 📁 client_side/web-app: react web app to display analysis results
    * 📁 src: main web app content
        * 📁 \_\_tests__: smoke tests for components rendering and testing the navigation works
        * 📁 components: components used within the web app, including stylesheets for them
            * 📁 graph_data: json files of data visualisations to be imported into components
            * 📁 text_data: json files containing text content to be used in components
    * 📁 public: web app html, icon, manifest and robots files

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
* [Plotly](https://plotly.com/python/) - for saving and adjusting the plots created by BERTopic, as well as creating new plots based on sentiment analysis
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

## How to Install and Run

## How to Use
Checkout out the React website hosted on GitHub Pages, which presents many of the findings of the topic modelling and sentiment analysis, as well as data visualistions. [Link to website](https://czboop.github.io/Newspaper-Topic-Modelling/)
