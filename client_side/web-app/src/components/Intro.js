import React from 'react';
import pieChart from './graph_data/news_source_ratios.json';
import Plot from 'react-plotly.js';

function Intro() {
  return (
    <div className='Intro'>
        <h2>Introduction</h2>
        <h3>The Shape of the Data</h3>
        <p>Headline data was gathered from seven of the top newspapers in the UK:</p>
        <ul>
            <li className='highlighted-link'><a href='https://www.theguardian.com/'>The Guardian</a></li>
            <li className='highlighted-link'><a href='https://www.mirror.co.uk/'>The Mirror</a></li>
            <li className='highlighted-link'><a href='https://metro.co.uk/'>Metro</a></li>
            <li className='highlighted-link'><a href='https://www.dailymail.co.uk/home/index.html'>The Daily Mail</a></li>
            <li className='highlighted-link'><a href='https://www.telegraph.co.uk/'>The Telegraph</a></li>
            <li className='highlighted-link'><a href='https://www.thesun.co.uk/'>The Sun</a></li>         
            <li className='highlighted-link'><a href='https://www.express.co.uk/'>The Daily Express</a></li>
        </ul>
        <p>The links above will take you to their respective websites, where you can read their reporting and support their work if you are interested.</p>
        <p>The percentages of articles from each news source can be seen below.</p>
        <Plot data={pieChart.data} layout={pieChart.layout}/>
        <p>Headlines that form the data were published between November 2019 and early January 2023. The number of articles over time can be seen below.</p>
        {/* INSERT GRAPH HERE */}
        <p>The total number of headlines was around 3.85 million.</p>
        <h3>Data Limitations</h3>
        <p>The data is not completely comparable across sources. One key difference is that for the Daily Mail, the Daily Express and the Metro, a complete or near-complete dataset of all article headlines was collected. On the other hand, for the other sources, headlines were collected from major news topics such as UK politics, world news, and health. These remaining sources should have a near-complete collection of those news topics but would exclude most coverage of areas such as showbiz, TV news, sports and other miscellaneous topics.</p>

    </div>
  )
}

export default Intro