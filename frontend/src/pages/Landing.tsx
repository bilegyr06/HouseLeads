import { useNavigate } from 'react-router-dom';
import { ArrowRight, Zap, Shield } from 'lucide-react';

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-4 py-12">
      {/* Logo */}
      <div className="mb-12 text-center">
        <div className="inline-block">
          <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mb-4">
            <span className="text-white font-bold text-xl">HL</span>
          </div>
        </div>
        <h2 className="text-xl font-bold text-blue-600">HomeLeads</h2>
      </div>

      {/* Main Container */}
      <div className="max-w-2xl w-full">
      {/* Main Headline */}
      <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6 leading-tight text-center">
        Find a house in Lagos without agent stress
      </h1>

      {/* Subheadline */}
      <p className="text-lg sm:text-xl text-gray-600 mb-8 text-center leading-relaxed">
        Tell us what you need and we'll connect you with serious agents fast.
      </p>

      {/* CTA Button */}
      <div className="flex justify-center mb-3">
        <button
          onClick={() => navigate('/form')}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-10 rounded-lg transition-colors inline-flex items-center gap-2 text-lg shadow-lg"
        >
          Get Started <ArrowRight size={22} />
        </button>
      </div>

      {/* Subtext under button */}
      <p className="text-center text-gray-500 text-sm mb-12 font-medium">
        Takes less than 30 seconds
      </p>

      {/* Benefit Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {/* Card 1: Fast Response */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-600 hover:shadow-lg transition-shadow">
          <div className="flex items-start gap-4 mb-3">
            <Zap className="text-blue-600 flex-shrink-0" size={28} />
            <h3 className="font-bold text-lg text-gray-900">Fast response</h3>
          </div>
          <p className="text-gray-700 text-sm leading-relaxed">
            We match your criteria and get agents reaching out within minutes, not days.
          </p>
        </div>

        {/* Card 2: Serious Agents Only */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-600 hover:shadow-lg transition-shadow">
          <div className="flex items-start gap-4 mb-3">
            <Shield className="text-blue-600 flex-shrink-0" size={28} />
            <h3 className="font-bold text-lg text-gray-900">Serious agents only</h3>
          </div>
          <p className="text-gray-700 text-sm leading-relaxed">
            We vet every agent to ensure they are professional and reliable.
          </p>
        </div>
      </div>
    </div>
    </div>
  );
}
