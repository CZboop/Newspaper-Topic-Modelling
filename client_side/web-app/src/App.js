import './App.css';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import Intro from './components/Intro.js';
import Navbar from './components/Navbar.js';
import NewspaperPage from './components/NewspaperPage.js';

import guardianTopics from './components/graph_data/guardian/guardian_topics.json';
import guardianOverTime from './components/graph_data/guardian/guardian_over_time.json';
import guardianPolarityTime from './components/graph_data/guardian/guardian_polarity_over_time.json';
import guardianPolarityRatio from './components/graph_data/guardian/guardian_polarity_ratio.json';
import guardianSubjectivityPlot from './components/graph_data/guardian/guardian_subjectivity_box_plot.json';
import guardianSubjectivityTime from './components/graph_data/guardian/guardian_subjectivity_over_time.json';
import guardianText from './components/text_data/guardian_text.json';

import sunTopics from './components/graph_data/sun/sun_topics.json';
import sunOverTime from './components/graph_data/sun/sun_over_time.json';
import sunPolarityTime from './components/graph_data/sun/sun_polarity_over_time.json';
import sunPolarityRatio from './components/graph_data/sun/sun_polarity_ratio.json';
import sunSubjectivityPlot from './components/graph_data/sun/sun_subjectivity_box_plot.json';
import sunSubjectivityTime from './components/graph_data/sun/sun_subjectivity_over_time.json';
import sunText from './components/text_data/sun_text.json';

function App() {
  return (
    <div className="App">
        <BrowserRouter>
        <Navbar />
          <Routes>
          <Route path='intro' element={<Intro />}/>
          <Route path='guardian' element={<NewspaperPage name='The Guardian' topic_intro={guardianText.topic_intro} topic_plot={guardianTopics} time_plot={guardianOverTime} polarity_time={guardianPolarityTime} polarity_ratio={guardianPolarityRatio} subjectivity_box={guardianSubjectivityPlot} subjectivity_over_time={guardianSubjectivityTime} polarity_comments={guardianText.polarity_comments} subjectivity_comments={guardianText.subjectivity_comments} extra_info={guardianText.extra_info} />}/>
          <Route path='mirror' element={<NewspaperPage name='The Mirror' intro='lorem ipsum' extra_info='lorem ipsum' />}/>
          <Route path='metro' element={<NewspaperPage name='Metro' intro='lorem ipsum' extra_info='lorem ipsum' />}/>
          <Route path='mail' element={<NewspaperPage name='The Daily Mail' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          <Route path='telegraph' element={<NewspaperPage name='The Telegraph' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          <Route path='sun' element={<NewspaperPage name='The Sun' topic_intro={sunText.topic_intro} topic_plot={sunTopics} time_plot={sunOverTime} polarity_time={sunPolarityTime} polarity_ratio={sunPolarityRatio} subjectivity_box={sunSubjectivityPlot} subjectivity_over_time={sunSubjectivityTime} polarity_comments={sunText.polarity_comments} subjectivity_comments={sunText.subjectivity_comments} extra_info={sunText.extra_info}/>}/>
          <Route path='express' element={<NewspaperPage name='The Express' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          </Routes>
        </BrowserRouter>
      
    </div>
  );
}

export default App;
