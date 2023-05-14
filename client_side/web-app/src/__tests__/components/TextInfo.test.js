import React from 'react';
import ReactDOM from 'react-dom';
import TextInfo from '../../components/TextInfo';

// smoke test checking textinfo renders without throwing/crashing 
it('Text info component renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<TextInfo textArray={['Some text', 'Some more text']} title='Test Title' />, div);
});