import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Intro from './components/Intro.js';
import Home from './components/Home.js';
import Navbar from './components/Navbar.js';
import NewspaperPage from './components/NewspaperPage.js';

// ==== IMPORTING GRAPHS AND TEXT DATA TO PASS INTO PAGE COMPONENTS ==== //

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

// importing telegraph plots and text content //
import telegraphTopics from './components/graph_data/telegraph/telegraph_topics.json';
import telegraphOverTime from './components/graph_data/telegraph/telegraph_over_time.json';
import telegraphPolarityTime from './components/graph_data/telegraph/telegraph_polarity_over_time.json';
import telegraphPolarityRatio from './components/graph_data/telegraph/telegraph_polarity_ratio.json';
import telegraphSubjectivityPlot from './components/graph_data/telegraph/telegraph_subjectivity_box_plot.json';
import telegraphSubjectivityTime from './components/graph_data/telegraph/telegraph_subjectivity_over_time.json';
import telegraphText from './components/text_data/telegraph_text.json';

// importing express plots and text content //
import expressTopics from './components/graph_data/express/express_topics.json';
import expressOverTime from './components/graph_data/express/express_over_time.json';
import expressPolarityTime from './components/graph_data/express/express_polarity_over_time.json';
import expressPolarityRatio from './components/graph_data/express/express_polarity_ratio.json';
import expressSubjectivityPlot from './components/graph_data/express/express_subjectivity_box_plot.json';
import expressSubjectivityTime from './components/graph_data/express/express_subjectivity_over_time.json';
import expressText from './components/text_data/express_text.json';

// importing mirror plots and text content //
import mirrorTopics from './components/graph_data/mirror/mirror_topics.json';
import mirrorOverTime from './components/graph_data/mirror/mirror_over_time.json';
import mirrorPolarityTime from './components/graph_data/mirror/mirror_polarity_over_time.json';
import mirrorPolarityRatio from './components/graph_data/mirror/mirror_polarity_ratio.json';
import mirrorSubjectivityPlot from './components/graph_data/mirror/mirror_subjectivity_box_plot.json';
import mirrorSubjectivityTime from './components/graph_data/mirror/mirror_subjectivity_over_time.json';
import mirrorText from './components/text_data/mirror_text.json';

// ==== THE APP - PUTTING TOGETHER COMPONENTS WITH PROPS AND RETURNING ==== //

function App() {
  return (
    <div className="App">
        <BrowserRouter>
        <Navbar />
          <Routes>
          <Route index path='home' element={<Home/>}/>
          <Route path='' element={ <Navigate to="/home" /> }/>
          <Route path='intro' element={<Intro />}/>
          <Route path='guardian' element={<NewspaperPage name='The Guardian' topic_intro={guardianText.topic_intro} topic_plot={guardianTopics} time_plot={guardianOverTime} polarity_time={guardianPolarityTime} polarity_ratio={guardianPolarityRatio} subjectivity_box={guardianSubjectivityPlot} subjectivity_over_time={guardianSubjectivityTime} polarity_comments={guardianText.polarity_comments} subjectivity_comments={guardianText.subjectivity_comments}  />}/>
          <Route path='mirror' element={<NewspaperPage name='The Mirror' topic_intro={mirrorText.topic_intro} topic_plot={mirrorTopics} time_plot={mirrorOverTime} polarity_time={mirrorPolarityTime} polarity_ratio={mirrorPolarityRatio} subjectivity_box={mirrorSubjectivityPlot} subjectivity_over_time={mirrorSubjectivityTime} polarity_comments={mirrorText.polarity_comments} subjectivity_comments={mirrorText.subjectivity_comments} />}/>
          <Route path='metro' element={<NewspaperPage name='Metro' topic_intro={metroText.topic_intro} topic_plot={metroTopics} time_plot={metroOverTime} polarity_time={metroPolarityTime} polarity_ratio={metroPolarityRatio} subjectivity_box={metroSubjectivityPlot} subjectivity_over_time={metroSubjectivityTime} polarity_comments={metroText.polarity_comments} subjectivity_comments={metroText.subjectivity_comments} />}/>
          <Route path='mail' element={<NewspaperPage name='The Daily Mail' topic_intro={mailText.topic_intro} topic_plot={mailTopics} time_plot={mailOverTime} polarity_time={mailPolarityTime} polarity_ratio={mailPolarityRatio} subjectivity_box={mailSubjectivityPlot} subjectivity_over_time={mailSubjectivityTime} polarity_comments={mailText.polarity_comments} subjectivity_comments={mailText.subjectivity_comments} />}/>
          <Route path='telegraph' element={<NewspaperPage name='The Telegraph' topic_intro={telegraphText.topic_intro} topic_plot={telegraphTopics} time_plot={telegraphOverTime} polarity_time={telegraphPolarityTime} polarity_ratio={telegraphPolarityRatio} subjectivity_box={telegraphSubjectivityPlot} subjectivity_over_time={telegraphSubjectivityTime} polarity_comments={telegraphText.polarity_comments} subjectivity_comments={telegraphText.subjectivity_comments} />}/>
          <Route path='sun' element={<NewspaperPage name='The Sun' topic_intro={sunText.topic_intro} topic_plot={sunTopics} time_plot={sunOverTime} polarity_time={sunPolarityTime} polarity_ratio={sunPolarityRatio} subjectivity_box={sunSubjectivityPlot} subjectivity_over_time={sunSubjectivityTime} polarity_comments={sunText.polarity_comments} subjectivity_comments={sunText.subjectivity_comments} />}/>
          <Route path='express' element={<NewspaperPage name='The Express' topic_intro={expressText.topic_intro} topic_plot={expressTopics} time_plot={expressOverTime} polarity_time={expressPolarityTime} polarity_ratio={expressPolarityRatio} subjectivity_box={expressSubjectivityPlot} subjectivity_over_time={expressSubjectivityTime} polarity_comments={expressText.polarity_comments} subjectivity_comments={expressText.subjectivity_comments} />}/>
          <Route path='*' element={<Navigate to="/home" />}/> 
          {/* above redirecting to home if invalid path, could always add a dedicated error page and route there instead */}
          </Routes>
        </BrowserRouter>
      <div className="background">
      </div>
    </div>
  );
}

export default App;
