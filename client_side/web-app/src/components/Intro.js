import React from 'react';
import pieChart from './graph_data/news_source_ratios.json';
import Plot from 'react-plotly.js';
import { useResizeDetector } from 'react-resize-detector';
import { useState, useCallback, useEffect } from "react";

// importing combined plots
import polarityOverTime from './graph_data/combined/all_polarity_over_time.json';
import polarityRatio from './graph_data/combined/all_polarity_ratio.json';
import subjectivityPlot from './graph_data/combined/all_subjectivity_box_plot.json';
import subjectivityOverTime from './graph_data/combined/all_subjectivity_over_time.json';
import articlesOverTimeAll from './graph_data/combined/articles_over_time_All Sources.json';
import articlesOverTimeCombined from './graph_data/combined/articles_over_time_Combined Sources.json';

// importing text components
import TextInfo from './TextInfo.js';
import TextWindow from './TextWindow';

function Intro() {
  const { width, height, ref } = useResizeDetector({ 
    refreshMode: 'debounce', 
    refreshRate: 1000
  })
  // getting array of plot names to use in dynamic adding of line breaks in graph titles based on window size
  const plotArray = [pieChart, polarityOverTime, polarityRatio, subjectivityPlot, subjectivityOverTime, articlesOverTimeAll, articlesOverTimeCombined];
  const [titles, setTitles] = useState({})

  const handleTitles = useCallback(() => {
    let plotKeyArray = ["pieChart", "polarityOverTime", "polarityRatio", "subjectivityPlot", "subjectivityOverTime", "articlesOverTimeAll", "articlesOverTimeCombined"];
    let titlesArray = plotArray.map(name => name.layout.title.text);
    if ( width <= 600 ) {
      titlesArray = titlesArray.map(title => title.match(/[\w:-]+(?:[^\w\n]+[\w:-]+){0,2}\b/g).join("<br>"))
    }
    else if ( width <= 800 ) {
      titlesArray = titlesArray.map(title => title.match(/[\w:-]+(?:[^\w\n]+[\w:-]+){0,5}\b/g).join("<br>"))
    }
    let titlesObj = {};
    for (let i = 0 ; i < titlesArray.length; i++) {
      if (titlesArray[i].startsWith("b>")){
        titlesArray[i] = titlesArray[i].replace("b>","<b>");
      }
      if (!titlesArray[i].startsWith("<b>")){
        titlesArray[i] = "<b>" + titlesArray[i];
      }
      titlesObj[plotKeyArray[i]] = titlesArray[i];
    }
    setTitles(titlesObj);
  }, [plotArray, width])

  // setting width as dependency is key to make sure titles change when width changes
  useEffect(() => {handleTitles();
  }, [setTitles, width]);

  return (
    <div className='Intro page-content'>
      <TextWindow title={"Introduction"} textArray={[""]} pageTitle={true}/>
        <div className="comment text-module">
        <div className="window-title">
        <h3>Data Summary</h3>
          <div>
            <button className="module-button">-</button>
            <button className="module-button">X</button>
            </div>
          </div>
        
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
        </div>
        <div className="comment text-module">
        <div className="window-title">
        <h3>Documents by Source</h3>
          <div>
            <button className="module-button">-</button>
            <button className="module-button">X</button>
            </div>
          </div>
        <p>The percentages of articles from each news source can be seen below. You can click on the sources in the legend to remove or add them from the chart, for example to better compare document numbers between certain sources.</p>
        {
        // different legend position so chart more vertical if small screen as can squeeze the chart too small otherwise on smaller screens
        width <= 600 ?
        <div ref={ref} className="graph-container no-border">
        <Plot data={pieChart.data} layout={{...pieChart.layout, ...{title: {text: titles["pieChart"], font: {color: "white"}}, width: width, height: height, legend:{x: -0.4, y:-0.5, xanchor:"left", yanchor:"bottom", font:{size: '2%', color: "white"}}}}} config = {{responsive: true}}/>
        </div>
        :
        <div ref={ref} className="graph-container no-border">
        <Plot data={pieChart.data} layout={{...pieChart.layout, ...{title: {text: titles["pieChart"], font: {color: "white"}}, width: width, height: height, legend:{font:{color: "white"}}}}} config = {{responsive: true}}/>
        </div>
        }
        <p>The total number of headlines analysed was around 3.05 million.</p>
        <p>Ratios by source differed greatly, as can be seen above. The number of headlines for the biggest dataset (The Daily Mail) was around 1.89 million, and for the smallest dataset (The Guardian) was around 43,000.</p>
        </div>
      <TextWindow title={"Articles Over Time"} textArray={["Headlines that form the data were published between November 2019 and early January 2023. The number of articles over time can be seen below. The dip in the last month is most likely due to the fact that data was incomplete for this month - only from the start of the month not the whole of it.","As the graph below shows, the number of articles over time was relatively stable overall, with a significant dip at the end due to only part of the month being in the dataset. However, this is likely due to the disproportionate influence of the larger Daily Mail dataset, which ends up being very similar in shape to the combined data."]} pageTitle={false}/>
        <div ref={ref} className="graph-container">
        <Plot data={articlesOverTimeCombined.data} layout={{...articlesOverTimeCombined.layout, ...{title: {text: titles["articlesOverTimeCombined"], font: {color: "white"}}, width: width, height: height, legend:{font:{size: '2%', color: "white"}}}}} config = {{responsive: true}}/>
        </div>
      <TextWindow title={"Over Time by Source"} textArray={["The Daily Mail had quite similar numbers of articles over time. The Sun and the Metro showed a trend of generally less articles over time.", "The Telegraph also had less articles over time, but this seemed to be in two stages rather than an overall trend - in mid-2021 there was a dip in article numbers and they stayed similarly low since then.", "The Guardian showed a slight increase in average article numbers over time, as did the Express.", "The Mirror showed the biggest change in articles each month, with a very clear trend of increasing articles over time, especially since 2021.", "For the Mirror, average articles were around 3000 per month, rising to over double this at the end of 2022."]} pageTitle={false}/>
        {
        // different legend position for small screens more vertical
        width <= 600 ?
        <div ref={ref} className="graph-container">
        <Plot data={articlesOverTimeAll.data} layout={{...articlesOverTimeAll.layout, ...{title: {text: titles["articlesOverTimeAll"], font: {color: "white"}}, width: width, height: height, legend:{tracegroupgap: 1 ,x: -0.4, y:-1.5, xanchor:"left", yanchor:"bottom", font:{size: '2%', color: "white"}}}}} config = {{responsive: true}}/>
        </div>
        :
        <div ref={ref} className="graph-container">
        <Plot data={articlesOverTimeAll.data} layout={{...articlesOverTimeAll.layout, ...{title: {text: titles["articlesOverTimeAll"], font: {color: "white"}}, width: width, height: height, legend:{font:{size: '2%', color: "white"}}}}} config = {{responsive: true}}/>
        </div>
        }
        <TextInfo title={null} textArray={["Click on a source name from the key to show or hide the line for that newspaper. Double-click to isolate one news source."]}/>
        <div ref={ref} className="graph-container">
        <Plot data={polarityOverTime.data} layout={{...polarityOverTime.layout, ...{title: {text: titles["polarityOverTime"], font: {color: "white"}}, width: width, height: height, legend:{font:{size: '2%', color: "white"}}}}} config = {{responsive: true}}/>
        </div>
        <TextInfo title={null} textArray={["Polarity is a measure of how positive or negative the language used in a text or set of texts is. Above is a graph showing the average polarity across all headlines from all news sources for each month. Polarity in this case goes from a maximum of 1 (very positive) to -1 (very negative)."]}/>
        <TextWindow title={"Polarity"} textArray={["Headlines tended to be neutral to slightly positive on average across large samples. Considering the possible range, polarity was fairly stable across the years in the data. However, there are two notable dips where headlines became more negative - the end of 2020 into the start of 2021, and the end of 2022 into the start of 2023."]} pageTitle={false}/>
        {
        // different legend position for small screens more vertical
        width <= 600 ?
        <div ref={ref} className="graph-container">
        <Plot data={polarityRatio.data} layout={{...polarityRatio.layout, ...{title: {text: titles["polarityRatio"], font: {color: "white"}}, width: width, height: height, legend:{x: -0.3, y:-0.2, xanchor:"left", yanchor:"bottom", font:{size: '2%', color: "white"}}}}} config = {{responsive: true}}/>
        </div>
        :
        <div ref={ref} className="graph-container">
        <Plot data={polarityRatio.data} layout={{...polarityRatio.layout, ...{title: {text: titles["polarityRatio"], font: {color: "white"}},width: width, height: height, legend:{font:{size: '2%', color: "white"}}}}} config = {{responsive: true}}/>
        </div>
        }
        <TextWindow title={"Polarity Ratio"} textArray={["The graph above shows the ratio of all headlines that were mostly positive, mostly negative or neutral. Here, a headline is only neutral if it scored 0 on polarity. The plurality of headlines were still neutral (43%), positive headlines were next most common at 34%, and the remaining 23% of headline were negative."]} pageTitle={false}/>
      <TextInfo title={null} textArray={["Subjectivity represents how objective or subjective language used is, ranging from 0 (maximally objective) to 1 (maximally subjective)."]}/>
      <div ref={ref} className="graph-container">
        <Plot data={subjectivityPlot.data} layout={{...subjectivityPlot.layout, ...{title: {text: titles["subjectivityPlot"], font: {color: "white"}},width: width, height: height, legend:{font:{size: '2%', color: "white"}}}}} config = {{responsive: true}}/>
        </div>
      <TextWindow title={"Overall Subjectivity"} textArray={["The box plot above shows that the data included headlines that were at both limits of subjectivity, but most headlines were more objective, including a significant number (at least a quarter) that were completely objective based on this way of measuring linguistic objectivity.","Median subjectivity was around 0.29, and around a quarter of all headlines were more subjective than objective."]} pageTitle={false}/>
        <div ref={ref} className="graph-container">
        <Plot data={subjectivityOverTime.data} layout={{...subjectivityOverTime.layout, ...{title: {text: titles["subjectivityOverTime"], font: {color: "white"}},width: width, height: height, legend:{font:{size: '2%', color: "white"}}}}} config = {{responsive: true}}/>
        </div>
      <TextWindow title={"Subjectivity Over Time"} textArray={["The line graph above shows the average (mean) subjectivity for each month across all news sources.","We see that across the months, headlines averaged around 0.32 - more objective than not, but with a fair amount of subjectivity.","Subjectivity was decreasing slightly over time until April 2021 when it began to increase over time slightly. However, the most notable trend was a sharp decline in subjectivity around November 2022."]} pageTitle={false}/>
      <TextInfo title={"Data Limitations"} textArray={["The data is not completely comparable across sources. One key difference is that for the Daily Mail, the Daily Express and the Metro, a complete or near-complete dataset of all article headlines was initially collected. For the Daily Mail, due to the very high number of articles, several topics were actively filtered out before analysis - 'wires' (these were republications of articles from other sources such as Reuters and AP), as well as sport, showbiz and 'femail' (lifestyle articles targeted at women). This was done based on the topics as classified by the newspaper itself, and had the effect of removing around 800,000 headlines.","The number and ratio of headlines above is after filtering, so reflects the headlines that were analysed rather than the starting dataset.","On the other hand, for the other sources, headlines were collected from major news topics such as UK politics, world news, and health. These remaining sources should have a near-complete collection of those news topics but would exclude most coverage of areas such as showbiz, TV news, sports and other miscellaneous topics."]}/>
    </div>
  )
}

export default Intro;