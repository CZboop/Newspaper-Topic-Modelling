import React from 'react';
import ReactDOM from 'react-dom';
import {render, screen} from '@testing-library/react'
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from '../App';

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

// smoke test checking renders without throwing/crashing 
it('App component renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App/>, div);
});

// testing navigation within full app
test('Able to navigate to intro page', async () => {
  const div = document.createElement('div');
  render(<App />, div);
  const user = userEvent.setup();

  // verify home page content / starting at web page - note as tests progress won't be able to assume starting at home page
  expect(screen.getByText(/This web page serves to present/i)).toBeInTheDocument();

  // verify intro page content
  await user.click(screen.getByRole('link', { name: 'Introduction' }));
  expect(screen.getByText(/Data Summary/i)).toBeInTheDocument();
})

test('Able to navigate to Guardian page', async () => {
  const div = document.createElement('div');
  render(<App />, div);
  const user = userEvent.setup();

  // verify guardian page content appears on clicking its nav link
  await user.click(screen.getByRole('link', { name: 'Guardian' }));
  expect(screen.getByText(/The Guardian's biggest topic clusters concerned/i)).toBeInTheDocument();
})

test('Able to navigate to Mirror page', async () => {
  const div = document.createElement('div');
  render(<App />, div);
  const user = userEvent.setup();

  // verify mirror page content appears on clicking its nav link
  await user.click(screen.getByRole('link', { name: 'Mirror' }));
  expect(screen.getByText(/The Mirror's top topic was the war in Ukraine/i)).toBeInTheDocument();
})

test('Able to navigate to Metro page', async () => {
  const div = document.createElement('div');
  render(<App />, div);
  const user = userEvent.setup();

  // verify metro page content appears on clicking its nav link
  await user.click(screen.getByRole('link', { name: 'Metro' }));
  expect(screen.getByText(/Metro's top topics focused less on politics than other newspapers/i)).toBeInTheDocument();
})

test('Able to navigate to Daily Mail page', async () => {
  const div = document.createElement('div');
  render(<App />, div);
  const user = userEvent.setup();

  // verify daily mail page content appears on clicking its nav link
  await user.click(screen.getByRole('link', { name: 'Daily Mail' }));
  expect(screen.getByText(/The Daily Mail had a very large quantity of data and lots of clusters/i)).toBeInTheDocument();
})

test('Able to navigate to Telegraph page', async () => {
  const div = document.createElement('div');
  render(<App />, div);
  const user = userEvent.setup();

  // verify telegraph page content appears on clicking its nav link
  await user.click(screen.getByRole('link', { name: 'Telegraph' }));
  expect(screen.getByText(/The Telegraph's top 10 topics were dominated by UK politics/i)).toBeInTheDocument();
})

test('Able to navigate to Sun page', async () => {
  const div = document.createElement('div');
  render(<App />, div);
  const user = userEvent.setup();

  // verify sun page content appears on clicking its nav link
  await user.click(screen.getByRole('link', { name: 'Sun' }));
  expect(screen.getByText(/Within the Sun data, the largest topic was around /i)).toBeInTheDocument();
})

test('Able to navigate to Express page', async () => {
  const div = document.createElement('div');
  render(<App />, div);
  const user = userEvent.setup();

  // verify express page content appears on clicking its nav link
  await user.click(screen.getByRole('link', { name: 'Express' }));
  expect(screen.getByText(/The Express had a very high number of clusters/i)).toBeInTheDocument();
})

test('Able to navigate to back to home page', async () => {
  const div = document.createElement('div');
  render(<App />, div);
  const user = userEvent.setup();

  // verify not already on home page - query instead of get to prevent error when not found
  expect(screen.queryByText(/This web page serves to present the results/i)).not.toBeInTheDocument();

  // verify home page content appears on clicking its nav link
  await user.click(screen.getByRole('link', { name: '📰 UK News Topic Modelling' }));
  expect(screen.getByText(/This web page serves to present the results/i)).toBeInTheDocument();
})