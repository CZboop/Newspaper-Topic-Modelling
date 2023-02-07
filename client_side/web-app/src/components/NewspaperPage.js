import React from 'react';
import Plot from 'react-plotly.js';

function NewspaperPage({name, intro, topic_plot, time_plot, extra_info}) {
  return (
    <div className='newspaper-container'>
        <h2>{name}</h2>
        <p>{intro}</p>
        <p>An interactive plot of the topics can be seen below.</p>
        {/* <Plot data={topic_plot.data} layout={topic_plot.layout}/> */}
        <p>An interactive plot of topics over time can be found below.</p>
        {/* <Plot data={time_plot.data} layout={time_plot.layout}/> */}
        <p className='extra-info'>{extra_info}</p>
        {/* potentially hide the extra info if it's falsy */}

    </div>
  )
}

export default NewspaperPage;