import React from 'react';
import Plot from 'react-plotly.js';

function NewspaperPage({name, topic_intro, topic_plot, time_plot, polarity_time, polarity_ratio, subjectivity_box, subjectivity_over_time, extra_info, polarity_comments, subjectivity_comments}) {
  return (
    <div className='newspaper-container'>
        <h2>{name}</h2>
        <h3>Topics</h3>
        <p>{topic_intro}</p>
        <p>An interactive plot of the topics can be seen below.</p>
        <p>You can mouse over each topic to see the summary of the words that define it, as well as its number which corresponds to how many headlines form the cluster. Topic 0 will be the biggest group with most articles.</p>
        <p>There are pan and zoom options available from the top right of the plot, and the slider along the bottom cycles through the topics one by one, highlighting each one on the graph.</p>
        <Plot data={topic_plot.data} layout={topic_plot.layout}/>
        <p>An interactive plot of topics over time can be found below.</p>
        <p>You can select or deselect different topics to show, hide or isolate them for clarity.</p>
        <Plot data={time_plot.data} layout={time_plot.layout}/>
        <h3>Polarity</h3>
        <p>Polarity is a measure of how positive or negative language is. In this instance, this goes from -1 which is the most negative, or 1 which is the most positive. 0 is completely neutral in terms of polarity.</p>
        <p>The pie chart below shows the ratio of headlines which are positive, negative, or completely neutral according to the polarity analysis run.</p>
        <Plot data={polarity_ratio.data} layout={polarity_ratio.layout}/>
        <p>The line graph below shows the polarity over time, where the polarity was averaged for each month.</p>
        <Plot data={polarity_time.data} layout={polarity_time.layout}/>
        <p>{polarity_comments}</p>
        <h3>Subjectivity</h3>
        <p>Subjectivity is a measure of subjective (opinionated) or objective (factual) language is. In this instance, this goes from 0 which is the most objective, to 1 which is the most subjective. We could think of 0.5 as an equal mix of fact and opinion.</p>
        <p>The box plot below shows the minimum and maximum subjectivity for this news source, as well as the quartiles.</p>
        <Plot data={subjectivity_box.data} layout={subjectivity_box.layout}/>
        <p>The line graph below shows the subjectivity over time, where the subjectivity was averaged for each month.</p>
        <Plot data={subjectivity_over_time.data} layout={subjectivity_over_time.layout}/>
        <p>{subjectivity_comments}</p>
        <p className='extra-info'>{extra_info}</p>
        {/* potentially hide the extra info if it's falsy */}

    </div>
  )
}

export default NewspaperPage;