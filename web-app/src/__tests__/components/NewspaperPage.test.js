import React from 'react';
import ReactDOM from 'react-dom';
import NewspaperPage from '../../components/NewspaperPage';

// mocking resize observer for purpose of testing
const { ResizeObserver } = window;

beforeEach(() => {
  delete window.ResizeObserver;
  window.ResizeObserver = jest.fn().mockImplementation(() => ({
    observe: jest.fn(),
    unobserve: jest.fn(),
    disconnect: jest.fn(),
  }));
});

afterEach(() => {
  window.ResizeObserver = ResizeObserver;
  jest.restoreAllMocks();
});

// smoke test checking newspaper page renders without throwing/crashing 
it('Newspaper page component renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<NewspaperPage name='Test Component' topic_intro='Test Intro' topic_plot='placeholder' time_plot='placeholder' polarity_time='placeholder' polarity_ratio='placeholder' subjectivity_box='placeholder' subjectivity_over_time='placeholder' polarity_comments='Test Comments Polarity' subjectivity_comments='Test Comments Subjectivity'/>, div);
});