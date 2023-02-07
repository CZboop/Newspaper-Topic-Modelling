import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Intro from './components/Intro.js';
import Navbar from './components/Navbar.js';
import NewspaperPage from './components/NewspaperPage.js';

function App() {
  return (
    <div className="App">
      <header className="Heading">
        <h1>UK News Topic Modelling</h1>
        <BrowserRouter>
        <Navbar />
          <Routes>
          <Route path='intro' element={<Intro />}/>
          <Route path='guardian' element={<NewspaperPage name='The Guardian' intro='lorem ipsum' extra_info='lorem ipsum' />}/>
          <Route path='mirror' element={<NewspaperPage name='The Mirror' intro='lorem ipsum' extra_info='lorem ipsum' />}/>
          <Route path='metro' element={<NewspaperPage name='Metro' intro='lorem ipsum' extra_info='lorem ipsum' />}/>
          <Route path='mail' element={<NewspaperPage name='The Daily Mail' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          <Route path='telegraph' element={<NewspaperPage name='The Telegraph' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          <Route path='sun' element={<NewspaperPage name='The Sun' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          <Route path='express' element={<NewspaperPage name='The Express' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          </Routes>
        </BrowserRouter>
      </header>
    </div>
  );
}

export default App;
