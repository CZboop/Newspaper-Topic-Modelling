import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import Navbar from '../../components/Navbar';

// smoke test checking navbar renders without throwing/crashing 
it('Navbar renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<BrowserRouter><Navbar /></BrowserRouter>, div);
});