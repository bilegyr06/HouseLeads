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
      <div className="min-h-screen bg-white flex items-center justify-center px-4">
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
        text: 'HomeLeads helps serious tenants in Lagos find houses fast with verified agents only. No scams, no inspection fee runs, no upfront fees.',
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
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-4 py-8 sm:py-12">
      {/* Main Container */}
      <div className="w-full max-w-md bg-white">
        {/* Checkmark Icon - Centered */}
        <div className="flex justify-center mb-8">
          <div className="bg-blue-100 rounded-full p-5 flex items-center justify-center">
            <CheckCircle className="text-blue-600" size={80} strokeWidth={1.5} />
          </div>
        </div>

        {/* Headline */}
        <h1 className="text-3xl sm:text-3xl font-bold text-gray-900 text-center mb-6 leading-tight">
          Your Request Has Been Received!
        </h1>

        {/* Body Text */}
        <p className="text-gray-700 text-center mb-8 leading-relaxed text-sm sm:text-base">
          We are now matching your requirements with verified agents and landlords who have suitable properties in Lagos. You will be contacted via WhatsApp or phone by serious agents shortly. We only work with screened agents (CAC and LASRERA verified) to reduce scams and agent wahala.
        </p>

        {/* Action Buttons */}
        <div className="space-y-3 mb-8">
          {/* WhatsApp Button */}
          <button
            onClick={handleWhatsAppClick}
            className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg transition-colors inline-flex items-center justify-center gap-2 text-base"
          >
            <MessageSquare size={20} />
            Join Our WhatsApp Updates
          </button>

          {/* Share Button */}
          <button
            onClick={handleShareForm}
            className="w-full bg-white hover:bg-gray-50 text-gray-900 font-bold py-3 px-6 rounded-lg border-2 border-gray-300 transition-colors inline-flex items-center justify-center gap-2 text-base"
          >
            <Share2 size={20} />
            Share Form With Friends
          </button>
        </div>

        {/* Trust Note */}
        <div className="border-t border-gray-200 pt-6 text-center">
          <p className="text-gray-700 text-xs sm:text-sm leading-relaxed">
            <span className="text-green-600 font-bold text-lg">✓</span> We match serious tenants with trusted agents based on your exact needs. No upfront fees for tenants.
          </p>
        </div>
      </div>
    </div>
  );
}
