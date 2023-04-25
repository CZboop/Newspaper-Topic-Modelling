import React from 'react';
import ReactDOM from 'react-dom';
import TextWindow from '../../components/TextWindow';

// smoke test checking renders without throwing/crashing 
it('Text window component renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<TextWindow textArray={['Some text', 'Some more text']} title='Test Title' pageTitle={false}/>, div);
});