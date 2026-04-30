import { useNavigate } from 'react-router-dom';
import { ArrowRight, Zap, Verified } from 'lucide-react';

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="stitch-shell">
      <div className="stitch-phone">
        <div className="stitch-content">
          <div className="brand-row">
            <div className="brand-icon">HL</div>
            <p className="brand-name">HomeLeads</p>
          </div>

          <h1 className="hero-title">Find a house in Lagos without agent stress</h1>
          <p className="hero-subtitle">
            Tell us what you need and we&apos;ll connect you with serious agents fast.
          </p>

          <button onClick={() => navigate('/form')} className="stitch-primary-btn">
            Get Started <ArrowRight size={16} />
          </button>
          <p className="micro-note">Takes less than 30 seconds</p>

          <div className="feature-list">
            <article className="feature-card">
              <div className="feature-icon">
                <Zap size={25} strokeWidth={0} fill='#0052ff'/>
              </div>
              <h2 className="feature-title">Fast response</h2>
              <p className="feature-body">
                We match your criteria and get agents reaching out within minutes, not days.
              </p>
            </article>

            <article className="feature-card">
              <div className="feature-icon">
                <Verified size={25} strokeWidth={2} stroke='#ffffff' fill='#0052ff'/>
              </div>
              <h2 className="feature-title">Serious agents only</h2>
              <p className="feature-body">
                We vet every agent to ensure they are professional and reliable.
              </p>
            </article>
          </div>
        </div>
      </div>
    </div>
  );
}
