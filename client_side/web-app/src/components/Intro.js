import React from 'react';
import Graph from './Graph.js';
import pieChart from './graph_data/news_source_ratios.json';
import Plot from 'react-plotly.js';

function Intro() {
  return (
    <div className='Intro'>
        <h2>Introduction</h2>
        <p></p>
        <Plot data={pieChart.data} layout={pieChart.layout}/>
    </div>
  )
}

export default Intro