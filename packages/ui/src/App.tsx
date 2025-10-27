import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ObjectivesPage from './pages/ObjectivesPage';
import ObjectiveDetailPage from './pages/ObjectiveDetailPage';
import ChatPage from './pages/ChatPage';

function App() {
  return (
    <Router>
      <div>
        <header className="header">
          <div className="container">
            <h1>KETA - Knowledge Extract & Talk Agent</h1>
            <nav className="nav">
              <Link to="/">Objectives</Link>
              <Link to="/about">About</Link>
            </nav>
          </div>
        </header>

        <main className="container">
          <Routes>
            <Route path="/" element={<ObjectivesPage />} />
            <Route path="/objectives/:objectiveId" element={<ObjectiveDetailPage />} />
            <Route path="/chat/:sessionId" element={<ChatPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function AboutPage() {
  return (
    <div className="card">
      <h2>About KETA</h2>
      <p>
        KETA (Knowledge Extract & Talk Agent) is a multi-agent POC that enables users to:
      </p>
      <ul>
        <li>Define objectives for knowledge extraction</li>
        <li>Provide text documents as sources</li>
        <li>Extract structured knowledge into a graph database</li>
        <li>Chat with a knowledge-aware agent that can query the extracted knowledge</li>
      </ul>
      <p style={{ marginTop: '20px' }}>
        <strong>Version:</strong> 0.1.0 (POC)
      </p>
    </div>
  );
}

export default App;
