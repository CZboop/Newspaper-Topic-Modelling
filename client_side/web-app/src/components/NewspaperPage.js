import React from 'react';
import Plot from 'react-plotly.js';

function NewspaperPage({name, intro, topic_plot, time_plot, extra_info}) {
  return (
    <div className='newspaper-container'>
        <h2>{name}</h2>
        <p>{intro}</p>
        <p>An interactive plot of the topics can be seen below.</p>
        <p>You can mouse over each topic to see the summary of the words that define it, as well as its number which corresponds to how many headlines form the cluster. Topic 0 will be the biggest group with most articles.</p>
        <p>There are pan and zoom options available from the top right of the plot, and the slider along the bottom cycles through the topics one by one, highlighting each one on the graph.</p>
        <Plot data={topic_plot.data} layout={topic_plot.layout}/>
        <p>An interactive plot of topics over time can be found below.</p>
        <p>You can select or deselect different topics to show, hide or isolate them for clarity.</p>
        <Plot data={time_plot.data} layout={time_plot.layout}/>
        <p className='extra-info'>{extra_info}</p>
        {/* potentially hide the extra info if it's falsy */}

    </div>
  )
}

export default NewspaperPage;