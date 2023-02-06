import React from 'react';
import Plot from 'react-plotly.js';

function Graph({data}) {
  return (
    <Plot data={data} />
  )
}

export default Graph