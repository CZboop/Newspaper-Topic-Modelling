import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import Home from '../../components/Home';

// smoke test checking renders without throwing/crashing - wrapping in browser router as component contains link from router
it('Home component renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<BrowserRouter><Home /></BrowserRouter>, div);
});

// testing the expected headings render as part of homepage component
test('Homepage component renders paragraph about the data', () => {
  render(<Home />, {wrapper: MemoryRouter});
  const dataElement = screen.getByText(/The Data 📈/i);
  expect(dataElement).toBeInTheDocument();
});

test('Homepage component renders paragraph about the analysis', () => {
    render(<Home />, {wrapper: MemoryRouter});
    const dataElement = screen.getByText(/The Analysis 🔎/i);
    expect(dataElement).toBeInTheDocument();
});

test('Homepage component renders paragraph about the tech', () => {
    render(<Home />, {wrapper: MemoryRouter});
    const dataElement = screen.getByText(/The Tech 💻/i);
    expect(dataElement).toBeInTheDocument();
});