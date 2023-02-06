import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Intro from './components/Intro.js';
import Navbar from './components/Navbar.js';

function App() {
  return (
    <div className="App">
      <header className="Heading">
        <h1>UK News Topic Modelling</h1>
        <BrowserRouter>
        <Navbar />
          <Routes>
          <Route path='intro' element={<Intro />}/>
          </Routes>
        </BrowserRouter>
      </header>
    </div>
  );
}

export default App;
