import React from 'react';
import ReactDOM from 'react-dom';
import Intro from '../../components/Intro';

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

// smoke test checking intro renders without throwing/crashing 
it('Introduction component renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<Intro />, div);
});