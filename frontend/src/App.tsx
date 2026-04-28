import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import LeadForm from './pages/LeadForm';
import Confirmation from './pages/Confirmation';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/form" element={<LeadForm />} />
        <Route path="/confirmation" element={<Confirmation />} />
        {/* Fallback for undefined routes */}
        <Route path="*" element={<Landing />} />
      </Routes>
    </Router>
  );
}

export default App;
