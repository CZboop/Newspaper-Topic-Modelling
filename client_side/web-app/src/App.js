import './App.css';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import Intro from './components/Intro.js';
import Navbar from './components/Navbar.js';
import NewspaperPage from './components/NewspaperPage.js';

import guardianTopics from './components/graph_data/guardian_topics.json';
import guardianOverTime from './components/graph_data/guardian_over_time.json';

function App() {
  return (
    <div className="App">
        <BrowserRouter>
        <Navbar />
          <Routes>
          <Route path='intro' element={<Intro />}/>
          <Route path='guardian' element={<NewspaperPage name='The Guardian' intro='lorem ipsum' topic_plot={guardianTopics} time_plot={guardianOverTime} extra_info='lorem ipsum' />}/>
          <Route path='mirror' element={<NewspaperPage name='The Mirror' intro='lorem ipsum' extra_info='lorem ipsum' />}/>
          <Route path='metro' element={<NewspaperPage name='Metro' intro='lorem ipsum' extra_info='lorem ipsum' />}/>
          <Route path='mail' element={<NewspaperPage name='The Daily Mail' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          <Route path='telegraph' element={<NewspaperPage name='The Telegraph' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          <Route path='sun' element={<NewspaperPage name='The Sun' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          <Route path='express' element={<NewspaperPage name='The Express' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          </Routes>
        </BrowserRouter>
      
    </div>
  );
}

export default App;
