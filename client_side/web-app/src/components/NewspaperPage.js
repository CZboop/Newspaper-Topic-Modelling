import React from 'react';
import Plot from 'react-plotly.js';
import { useResizeDetector } from 'react-resize-detector';
import './NewspaperPage.css';
import { useState, useCallback, useEffect } from "react";

// importing image - svg icon as component
import InfoIcon from './InfoIcon.js';

function NewspaperPage({name, topic_intro, topic_plot, time_plot, polarity_time, polarity_ratio, subjectivity_box, subjectivity_over_time, extra_info, polarity_comments, subjectivity_comments}) {
  // using resize detector npm module to get height and width to resize graphs with window size
  // using debounce so updates once per second at most, no glitching
  const { width, height, ref } = useResizeDetector({ 
    refreshMode: 'debounce', 
    refreshRate: 1000
  })
  // getting array of plot names to use in dynamic adding of line breaks in graph titles based on window size
  const plotArray = [topic_plot, time_plot, polarity_time, polarity_ratio, subjectivity_box, subjectivity_over_time];
  const [titles, setTitles] = useState({});
  
  const handleTitles = useCallback(() => {
    let plotKeyArray = ["topic_plot", "time_plot", "polarity_time", "polarity_ratio", "subjectivity_box", "subjectivity_over_time"]
    let titlesArray = plotArray.map(name => name.layout.title.text);
    if ( width <= 600 ) {
      titlesArray = titlesArray.map(title => title.match(/[\w:-]+(?:[^\w\n]+[\w:-]+){0,2}\b/g).join("<br>"))
    }
    else if ( width <= 800 ) {
      titlesArray = titlesArray.map(title => title.match(/[\w:-]+(?:[^\w\n]+[\w:-]+){0,5}\b/g).join("<br>"))
    }
    let titlesObj = {};
    // quick fix for regex missing starting < in <b> for bold titles, 
    for (let i = 0 ; i < titlesArray.length; i++) {
      if (titlesArray[i].startsWith("b>")) {
        titlesArray[i] = titlesArray[i].replace("b>","<b>")
      }
    }
    for (let i = 0 ; i < titlesArray.length; i++) {
      titlesObj[plotKeyArray[i]] = titlesArray[i];
    }
    setTitles(titlesObj);
  }, [plotArray, width])

  // setting width as dependency is key to make sure titles change when width changes
  useEffect(() => {handleTitles();
  }, [setTitles, width]);

  return (
    <div className='newspaper-container page-content'>
        <h2>{name}</h2>
        <div className="comment text-module">
        <h3>Topics</h3>
        <p>{topic_intro}</p>
        </div>
        <div className="boilerplate text-module">
        <InfoIcon />
        <p>An interactive plot of the topics can be seen below.</p>
        <p>You can mouse over each topic to see the summary of the words that define it, as well as its number which corresponds to how many headlines form the cluster. Topic 0 will be the biggest group with most articles.</p>
        <p>Hovering over each topic will also show a representative example of a headline from the group. These differ from the original headline in that stopwords and capitalisation have been removed.</p>
        <p>There are pan and zoom options available from the top right of the plot, and the slider along the bottom cycles through the topics one by one, highlighting each one on the graph.</p>
        </div>
        <div ref={ref} class="graph-container">
        {/* using spread operator so adding to layout with resonsive height width in one line keeping it as single object */}
        <Plot data={topic_plot.data} layout={{...topic_plot.layout, ...{width: width, height: height, legend:{font:{size: '2%'}}}, title: {text: titles["topic_plot"]}}} config = {{responsive: true}}/>
        </div>
        <div className="boilerplate text-module">
        <InfoIcon />
        <p>An interactive plot of topics over time can be found below.</p>
        <p>You can select or deselect different topics to show, hide or isolate them for clarity.</p>
        </div>
        {
        // some of the graphs have legend overlap or hard to read on smaller screens, using legend settings below to prevent this if width less than 800
        width <= 800 ?
        <div ref={ref} class="graph-container">
        <Plot data={time_plot.data} layout={{...time_plot.layout, ...{width: width, showlegend: true, legend: {x: 0, y:-1.8, xanchor:"left", yanchor:"bottom"}, title: {text: titles["time_plot"]}}}}/>
        </div>
        :
        <div ref={ref} class="graph-container">
        <Plot data={time_plot.data} layout={{...time_plot.layout, ...{width: width}, title: {text: titles["time_plot"]}}}/>
        </div>
        }
        <div className="boilerplate text-module">
        <InfoIcon />
        <h3>Polarity</h3>
        <p>Polarity is a measure of how positive or negative language is. In this instance, this goes from -1 which is the most negative, or 1 which is the most positive. 0 is completely neutral in terms of polarity.</p>
        <p>The pie chart below shows the ratio of headlines which are positive, negative, or completely neutral according to the polarity analysis run.</p>
        </div>
        {
        // again setting legend position based on screen size when the graph looks off because of legend
        width <= 600 ?
        <div ref={ref} class="graph-container">
        <Plot data={polarity_ratio.data} layout={{...polarity_ratio.layout, ...{width: width, showlegend: true, legend: {x: 0, y:-0.5, xanchor:"left", yanchor:"bottom"}, title: {text: titles["polarity_ratio"]}}}}/>
        </div>
        :
        <div ref={ref} class="graph-container">
        <Plot data={polarity_ratio.data} layout={{...polarity_ratio.layout, ...{width: width, height: height, title: {text: titles["polarity_ratio"]}}}}/>
        </div>
        }
        <div className="boilerplate text-module">
        <InfoIcon />
        <p>The line graph below shows the polarity over time, where the polarity was averaged for each month.</p>    
        </div>    
        <div ref={ref} class="graph-container">
        <Plot data={polarity_time.data} layout={{...polarity_time.layout, ...{width: width, height: height, title: {text: titles["polarity_time"]}}}}/>
        </div>
        <div className="comment text-module">
        <p>{polarity_comments}</p>
        </div>
        <div className="boilerplate text-module">
        <InfoIcon />
        <h3>Subjectivity</h3>
        <p>Subjectivity is a measure of subjective (opinionated) or objective (factual) language is. In this instance, this goes from 0 which is the most objective, to 1 which is the most subjective. We could think of 0.5 as an equal mix of fact and opinion.</p>
        <p>The box plot below shows the minimum and maximum subjectivity for this news source, as well as the quartiles.</p>
        </div>
        <div ref={ref} class="graph-container">
        <Plot data={subjectivity_box.data} layout={{...subjectivity_box.layout, ...{width: width, height: height, title: {text: titles["subjectivity_box"]}}}}/>
        </div>
        <div className="boilerplate text-module">
        <InfoIcon />
        <p>The line graph below shows the subjectivity over time, where the subjectivity was averaged for each month.</p>
        </div>
        <div ref={ref} class="graph-container">
        <Plot data={subjectivity_over_time.data} layout={{...subjectivity_over_time.layout, ...{width: width, height: height, title: {text: titles["subjectivity_over_time"]}}}}/>
        </div>
        <div className="boilerplate text-module">
        <InfoIcon />
        <p>{subjectivity_comments}</p>
        </div>
        <p className='extra-info'>{extra_info}</p>
        {/* TODO: potentially hide the extra info if it's falsy or remove if not used in any anyway*/}

    </div>
  )
}

export default NewspaperPage;