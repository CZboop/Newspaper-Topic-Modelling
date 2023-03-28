import React from 'react';
import pieChart from './graph_data/news_source_ratios.json';
import Plot from 'react-plotly.js';

// importing combined plots
import polarityOverTime from './graph_data/combined/all_polarity_over_time.json';
import polarityRatio from './graph_data/combined/all_polarity_ratio.json';
import subjectivityPlot from './graph_data/combined/all_subjectivity_box_plot.json';
import subjectivityOverTime from './graph_data/combined/all_subjectivity_over_time.json';

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
        <p>The total number of headlines analysed was around 3.05 million.</p>
        <p>Ratios by source differed greatly, as can be seen above. The number of headlines for the biggest dataset (The Daily Mail) was around 1.89 million, and for the smallest dataset (The Guardian) was around 43,000.</p>
        <p>Headlines that form the data were published between November 2019 and early January 2023. The number of articles over time can be seen below.</p>
        {/* INSERT GRAPH HERE */}
        <Plot data={polarityOverTime.data} layout={polarityOverTime.layout}/>
        <p>Polarity is a measure of how positive or negative the language used in a text or set of texts is. Above is a graph showing the average polarity across all headlines from all news sources for each month. Polarity in this case goes from a maximum of 1 (very positive) to -1 (very negative).</p>
        <p>Headlines tended to be neutral to slightly positive on average across large samples. Considering the possible range, polarity was fairly stable across the years in the data. However, there are two notable dips where headlines became more negative - the end of 2020 into the start of 2021, and the end of 2022 into the start of 2023.</p>
        <Plot data={polarityRatio.data} layout={polarityRatio.layout}/>
        <p>The graph above shows the ratio of all headlines that were mostly positive, mostly negative or neutral. Here, a headline is only neutral if it scored 0 on polarity. The plurality of headlines were still neutral (43%), positive headlines were next most common at 34%, and the remaining 23% of headline were negative.</p>
        <Plot data={subjectivityPlot.data} layout={subjectivityPlot.layout}/>
        <p>Subjectivity represents how objective or subjective language used is, ranging from 0 (maximally objective) to 1 (maximally subjective).</p>
        <p>The box plot above shows that the data included headlines that were at both limits of subjectivity, but most headlines were more objective, including a significant number (at least a quarter) that were completely objective based on this way of measuring linguistic objectivity.</p>
        <p>Median subjectivity was around 0.29, and around a quarter of all headlines were more subjective than objective.</p>
        <Plot data={subjectivityOverTime.data} layout={subjectivityOverTime.layout}/>
        <p>The line graph above shows the average (mean) subjectivity for each month across all news sources.</p>
        <p>We see that across the months, headlines averaged around 0.32 - more objective than not, but with a fair amount of subjectivity.</p>
        <p>Subjectivity was decreasing slightly over time until April 2021 when it began to increase over time slightly. However, the most notable trend was a sharp decline in subjectivity around November 2022.</p>
        <h3>Data Limitations</h3>
        <p>The data is not completely comparable across sources. One key difference is that for the Daily Mail, the Daily Express and the Metro, a complete or near-complete dataset of all article headlines was initially collected. For the Daily Mail, due to the very high number of articles, several topics were actively filtered out before analysis - 'wires' (these were republications of articles from other sources such as Reuters and AP), as well as sport, showbiz and 'femail' (lifestyle articles targeted at women). This was done based on the topics as classified by the newspaper itself.</p>
        <p>The number and ratio of headlines above is after filtering, so reflects the headlines that were analysed rather than the starting dataset.</p>
        <p>On the other hand, for the other sources, headlines were collected from major news topics such as UK politics, world news, and health. These remaining sources should have a near-complete collection of those news topics but would exclude most coverage of areas such as showbiz, TV news, sports and other miscellaneous topics.</p>

    </div>
  )
}

export default Intro