import React from 'react';
import ReactDOM from 'react-dom';
import App from '../App';

// smoke test checking renders without throwing/crashing 
it('App component renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App/>, div);
});
