import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className='page-content'>
        <div className="comment text-module">
      <div className="window-title">
        <h2>Welcome!</h2>
          <div>
            <button className="module-button">-</button>
            <button className="module-button">X</button>
            </div>
          
        </div>
        {/* <div className="comment text-module"> */}
        <p>This web page serves to present the results of a data collection and analysis project, looking at the topics that different newspapers cover, as well as their subjectivity and sentiment polarity.</p>
        <p>All of the newspapers are based in the UK and are among the most popular with readers in the United Kingdom.</p>
        <p>This site is designed to work on both desktop and mobile, but some of the data visualisations will be clearer on larger screens.</p>
        </div>
        {/* </div> */}
        <div className="comment text-module">
        <div className="window-title">
        <h3>The Data 📈</h3>
          <div>
            <button className="module-button">-</button>
            <button className="module-button">X</button>
            </div>
          </div>
        
        <p>The data used for the analysis consisted of headlines, collected using web scraping with a limited number of requests per minute. Data was collected using Python, primarily using Beautiful Soup and httplib.</p>
        <p>Headlines were from articles that were all published online between late November 2019 and early January 2023.</p>
        <p>The <Link to='/intro'>[Introduction]</Link> page provides more details on the data, including the relative number from each newspaper and the number of articles over time.</p>
        <p>The dataset that the analysis was based on is not public.</p>
        <p>Below are links to the newspapers that were analysed. This web page's navigation menu (above) can be used to to go the data analysis for each newspaper.</p>
        <ul>
            <li className='highlighted-link'><a href='https://www.theguardian.com/'>The Guardian</a></li>
            <li className='highlighted-link'><a href='https://www.mirror.co.uk/'>The Mirror</a></li>
            <li className='highlighted-link'><a href='https://metro.co.uk/'>Metro</a></li>
            <li className='highlighted-link'><a href='https://www.dailymail.co.uk/home/index.html'>The Daily Mail</a></li>
            <li className='highlighted-link'><a href='https://www.telegraph.co.uk/'>The Telegraph</a></li>
            <li className='highlighted-link'><a href='https://www.thesun.co.uk/'>The Sun</a></li>         
            <li className='highlighted-link'><a href='https://www.express.co.uk/'>The Daily Express</a></li>
        </ul>
        </div>
        <div className="comment text-module">
        <div className="window-title">
        <h3>The Analysis 🔎</h3>
          <div>
            <button className="module-button">-</button>
            <button className="module-button">X</button>
            </div>
          </div>
        
        <p>Analysis was performed using BERTopic for topic modelling, and TextBlob via spaCy for sentiment analysis in the form of polarity and subjectivity analysis.</p>
        <p>The resulting topic cluster graphs are visible on the web page for each newspaper, in their entirety. There is also a line graph of the top 10 topics over time for each newspaper.</p>
        <p>Some thoughts were added on these top topics and anything that seemed interesting such as groups of topics, individuals who appear in the topics or comparisons to other papers.</p>
        <p>The topic cluster graph also shows a representative example of the headlines that make up each cluster when hovered over, which was added by me combining built in methods from BERTopic to get these examples and visualise the topics, by manipulation the resulting json plot from the visualisation.</p>
        <br/>
        <p>Polarity and subjectivity was calculated using built in methods from the spaCy TextBlob pipeline.</p>
        <p>Pandas and Plotly within Python were then used to process the data and extract key information into visualisations. This included the ratios of positive, negative and neutral headlines, as well as how these metrics changed over time.</p>
        <p>Some comments were also added to explain and provide comment on the subjectivity and polarity.</p>
        </div>
        <div className="comment text-module">
            <div className="window-title">
            <h3>The Tech 💻</h3>
            <div>
            <button className="module-button">-</button>
            <button className="module-button">X</button>
            </div>
          </div>
        
        <h4>Data Side</h4>
        <p>The scraping and data analysis was done using Python. Libraries used included:</p> 
        <ul>
            <li>BERTopic (including UMAP, HDBSCAN and sci-kit learn) - for topic modelling</li>
            <li>SpaCy (including TextBlob) - for sentiment analysis and stopword removal</li>
            <li>Pandas - for a range of data processing tasks</li>
            <li>Plotly - for visualising data</li>
            <li>Beautiful Soup - for scraping data</li>
            <li>httplib - for making requests to collect data</li>
            <li>Glob - for handling data across different files</li>
            <li>Datetime and Dateutil - for selecting data from different ranges and iterating over time deltas</li>
        </ul>

        <h4>Web Side</h4>
        <p>This website was made with JavaScript, using React.</p>
        </div>
    </div>
  )
}

export default Home;