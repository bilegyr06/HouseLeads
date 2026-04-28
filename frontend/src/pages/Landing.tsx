import { useNavigate } from 'react-router-dom';
import { ArrowRight, Zap, Shield } from 'lucide-react';

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="text-2xl font-bold text-blue-600">HomeLeads</div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
        <div className="max-w-2xl w-full">
          {/* Main Headline */}
          <div className="text-center mb-8">
            <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4 leading-tight">
              Find a house in Lagos <br className="hidden sm:inline" />
              without agent stress
            </h1>
            <p className="text-lg sm:text-xl text-gray-600 mb-8">
              Tell us what you need and we'll connect you with serious agents fast.
            </p>
          </div>

          {/* CTA Button */}
          <div className="flex justify-center mb-12">
            <button
              onClick={() => navigate('/form')}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors inline-flex items-center gap-2 text-lg shadow-lg"
            >
              Get Started <ArrowRight size={20} />
            </button>
          </div>

          {/* Subtext */}
          <p className="text-center text-gray-500 text-sm mb-12">
            Takes less than 30 seconds
          </p>

          {/* Benefit Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {/* Card 1: Fast Response */}
            <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-600">
              <div className="flex items-start gap-4">
                <Zap className="text-blue-600 mt-1 flex-shrink-0" size={24} />
                <div>
                  <h3 className="font-bold text-lg text-gray-900 mb-2">Fast response</h3>
                  <p className="text-gray-600">
                    We match your criteria and get agents reaching out within minutes, not days.
                  </p>
                </div>
              </div>
            </div>

            {/* Card 2: Serious Agents Only */}
            <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-600">
              <div className="flex items-start gap-4">
                <Shield className="text-blue-600 mt-1 flex-shrink-0" size={24} />
                <div>
                  <h3 className="font-bold text-lg text-gray-900 mb-2">Serious agents only</h3>
                  <p className="text-gray-600">
                    We vet every agent to ensure they are professional and reliable.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-200 py-6">
        <div className="max-w-6xl mx-auto px-4 text-center text-gray-600 text-sm">
          <p>© 2026 HomeLeads. Connecting serious tenants with trusted agents.</p>
        </div>
      </footer>
    </div>
  );
}
