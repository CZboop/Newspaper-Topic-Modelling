import './App.css';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import Intro from './components/Intro.js';
import Navbar from './components/Navbar.js';
import NewspaperPage from './components/NewspaperPage.js';

// IMPORTING GRAPHS AND TEXT DATA TO PASS INTO PAGE COMPONENTS //

// importing guardian plots and text content //
import guardianTopics from './components/graph_data/guardian/guardian_topics.json';
import guardianOverTime from './components/graph_data/guardian/guardian_over_time.json';
import guardianPolarityTime from './components/graph_data/guardian/guardian_polarity_over_time.json';
import guardianPolarityRatio from './components/graph_data/guardian/guardian_polarity_ratio.json';
import guardianSubjectivityPlot from './components/graph_data/guardian/guardian_subjectivity_box_plot.json';
import guardianSubjectivityTime from './components/graph_data/guardian/guardian_subjectivity_over_time.json';
import guardianText from './components/text_data/guardian_text.json';

// importing sun plots and text content //
import sunTopics from './components/graph_data/sun/sun_topics.json';
import sunOverTime from './components/graph_data/sun/sun_over_time.json';
import sunPolarityTime from './components/graph_data/sun/sun_polarity_over_time.json';
import sunPolarityRatio from './components/graph_data/sun/sun_polarity_ratio.json';
import sunSubjectivityPlot from './components/graph_data/sun/sun_subjectivity_box_plot.json';
import sunSubjectivityTime from './components/graph_data/sun/sun_subjectivity_over_time.json';
import sunText from './components/text_data/sun_text.json';

// importing metro plots and text content //
import metroTopics from './components/graph_data/metro/metro_topics.json';
import metroOverTime from './components/graph_data/metro/metro_over_time.json';
import metroPolarityTime from './components/graph_data/metro/metro_polarity_over_time.json';
import metroPolarityRatio from './components/graph_data/metro/metro_polarity_ratio.json';
import metroSubjectivityPlot from './components/graph_data/metro/metro_subjectivity_box_plot.json';
import metroSubjectivityTime from './components/graph_data/metro/metro_subjectivity_over_time.json';
import metroText from './components/text_data/metro_text.json';

// importing mail plots and text content //
import mailTopics from './components/graph_data/mail/mail_topics.json';
import mailOverTime from './components/graph_data/mail/mail_over_time.json';
import mailPolarityTime from './components/graph_data/mail/mail_polarity_over_time.json';
import mailPolarityRatio from './components/graph_data/mail/mail_polarity_ratio.json';
import mailSubjectivityPlot from './components/graph_data/mail/mail_subjectivity_box_plot.json';
import mailSubjectivityTime from './components/graph_data/mail/mail_subjectivity_over_time.json';
import mailText from './components/text_data/mail_text.json';

function App() {
  return (
    <div className="App">
        <BrowserRouter>
        <Navbar />
          <Routes>
          <Route path='intro' element={<Intro />}/>
          <Route path='guardian' element={<NewspaperPage name='The Guardian' topic_intro={guardianText.topic_intro} topic_plot={guardianTopics} time_plot={guardianOverTime} polarity_time={guardianPolarityTime} polarity_ratio={guardianPolarityRatio} subjectivity_box={guardianSubjectivityPlot} subjectivity_over_time={guardianSubjectivityTime} polarity_comments={guardianText.polarity_comments} subjectivity_comments={guardianText.subjectivity_comments} extra_info={guardianText.extra_info} />}/>
          <Route path='mirror' element={<NewspaperPage name='The Mirror' intro='lorem ipsum' extra_info='lorem ipsum' />}/>
          <Route path='metro' element={<NewspaperPage name='Metro' topic_intro={metroText.topic_intro} topic_plot={metroTopics} time_plot={metroOverTime} polarity_time={metroPolarityTime} polarity_ratio={metroPolarityRatio} subjectivity_box={metroSubjectivityPlot} subjectivity_over_time={metroSubjectivityTime} polarity_comments={metroText.polarity_comments} subjectivity_comments={metroText.subjectivity_comments} extra_info={metroText.extra_info}/>}/>
          <Route path='mail' element={<NewspaperPage name='The Daily Mail' topic_intro={mailText.topic_intro} topic_plot={mailTopics} time_plot={mailOverTime} polarity_time={mailPolarityTime} polarity_ratio={mailPolarityRatio} subjectivity_box={mailSubjectivityPlot} subjectivity_over_time={mailSubjectivityTime} polarity_comments={mailText.polarity_comments} subjectivity_comments={mailText.subjectivity_comments} extra_info={mailText.extra_info}/>}/>
          <Route path='telegraph' element={<NewspaperPage name='The Telegraph' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          <Route path='sun' element={<NewspaperPage name='The Sun' topic_intro={sunText.topic_intro} topic_plot={sunTopics} time_plot={sunOverTime} polarity_time={sunPolarityTime} polarity_ratio={sunPolarityRatio} subjectivity_box={sunSubjectivityPlot} subjectivity_over_time={sunSubjectivityTime} polarity_comments={sunText.polarity_comments} subjectivity_comments={sunText.subjectivity_comments} extra_info={sunText.extra_info}/>}/>
          <Route path='express' element={<NewspaperPage name='The Express' intro='lorem ipsum' extra_info='lorem ipsum'/>}/>
          </Routes>
        </BrowserRouter>
      
    </div>
  );
}

export default App;
