import React from 'react';
import ReactDOM from 'react-dom';
import InfoIcon from '../../components/InfoIcon';

// smoke test checking renders without throwing/crashing 
it('Info icon renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<InfoIcon />, div);
});