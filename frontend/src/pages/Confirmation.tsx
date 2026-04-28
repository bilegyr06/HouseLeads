import { useLocation, useNavigate } from 'react-router-dom';
import { CheckCircle, MessageSquare, Share2 } from 'lucide-react';
import type { TenantLeadResponse } from '../types/types';

export default function Confirmation() {
  const location = useLocation();
  const navigate = useNavigate();
  const lead = location.state?.lead as TenantLeadResponse;

  // Fallback if no lead data (should not happen in normal flow)
  if (!lead) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center px-4">
        <div className="text-center">
          <p className="text-red-600 mb-4">Error: No lead data found.</p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white py-2 px-6 rounded-lg hover:bg-blue-700"
          >
            Go Back Home
          </button>
        </div>
      </div>
    );
  }

  const handleShareForm = () => {
    if (navigator.share) {
      navigator.share({
        title: 'Find a House in Lagos - HomeLeads',
        text: 'I just used HomeLeads to find a house in Lagos without agent stress. Check it out!',
        url: window.location.origin,
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.origin);
      alert('Link copied to clipboard!');
    }
  };

  const handleWhatsAppClick = () => {
    // Placeholder for WhatsApp group link
    // In production, replace with actual WhatsApp group/channel URL
    window.open('https://whatsapp.com', '_blank');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="text-2xl font-bold text-blue-600">HomeLeads</div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
        <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8 sm:p-12">
          {/* Checkmark Icon */}
          <div className="flex justify-center mb-8">
            <div className="bg-blue-100 rounded-full p-4">
              <CheckCircle className="text-blue-600" size={64} />
            </div>
          </div>

          {/* Headline */}
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 text-center mb-6">
            Your Request Has Been Received!
          </h1>

          {/* Body Text */}
          <div className="bg-blue-50 rounded-lg p-6 mb-8 text-center">
            <p className="text-gray-700 text-lg leading-relaxed">
              We are now matching your requirements with verified agents and landlords who have suitable properties in Lagos. You will be contacted via WhatsApp or phone by serious agents shortly. We only work with screened agents (CAC and LASRERA verified) to reduce scams and agent wahala.
            </p>
          </div>

          {/* Summary Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 font-medium">Location</p>
              <p className="text-lg font-semibold text-gray-900 mt-1">
                {lead.location_preference}
              </p>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 font-medium">Property Type</p>
              <p className="text-lg font-semibold text-gray-900 mt-1">
                {lead.property_type}
              </p>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 font-medium">Budget</p>
              <p className="text-lg font-semibold text-gray-900 mt-1">
                ₦{lead.budget_max.toLocaleString()}
                {lead.budget_min && ` - ₦${lead.budget_max.toLocaleString()}`}
              </p>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 font-medium">Move-in Date</p>
              <p className="text-lg font-semibold text-gray-900 mt-1">
                {new Date(lead.move_in_date).toLocaleDateString('en-NG', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
            {/* WhatsApp Button */}
            <button
              onClick={handleWhatsAppClick}
              className="bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors inline-flex items-center justify-center gap-2"
            >
              <MessageSquare size={20} />
              Join Our WhatsApp Updates
            </button>

            {/* Share Button */}
            <button
              onClick={handleShareForm}
              className="bg-white hover:bg-gray-50 text-gray-900 font-semibold py-3 px-6 rounded-lg border-2 border-gray-300 transition-colors inline-flex items-center justify-center gap-2"
            >
              <Share2 size={20} />
              Share Form With Friends
            </button>
          </div>

          {/* Trust Note */}
          <div className="border-t pt-6 text-center">
            <p className="text-gray-600 text-sm">
              <span className="text-green-600 font-bold">✓</span> We match serious tenants with trusted agents based on your exact needs. No upfront fees for tenants.
            </p>
          </div>

          {/* Contact Confirmation */}
          <div className="mt-6 p-4 bg-green-50 rounded-lg text-center">
            <p className="text-green-700 text-sm">
              <strong>Contact Details:</strong>
              <br />
              {lead.full_name}
              <br />
              {lead.phone_number}
              {lead.email && (
                <>
                  <br />
                  {lead.email}
                </>
              )}
            </p>
          </div>

          {/* Back to Home */}
          <div className="mt-8 text-center">
            <button
              onClick={() => navigate('/')}
              className="text-blue-600 hover:text-blue-700 font-semibold underline"
            >
              ← Back to Home
            </button>
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
