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
      <div className="stitch-shell">
        <div className="stitch-phone">
          <div className="stitch-content">
            <div className="text-center">
              <p style={{ color: 'var(--stitch-primary)' }} className="mb-4">Error: No lead data found.</p>
              <button
                onClick={() => navigate('/')}
                className="stitch-primary-btn"
              >
                Go Back Home
              </button>
            </div>
          </div>
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
    <div className="stitch-shell">
      <div className="stitch-phone">
        <div className="stitch-content">
          <div className="confirm-icon-wrap">
            <CheckCircle size={32} strokeWidth={2} />
          </div>
          <h1 className="confirm-title">
            Your Request Has Been Received!
          </h1>
          <p className="confirm-body">
            We are now matching your requirements with verified agents and landlords who have suitable properties in Lagos. You will be contacted via WhatsApp or phone by serious agents shortly. We only work with screened agents (CAC and LASRERA verified) to reduce scams and agent wahala.
          </p>
          <div className="confirm-actions">
            <button
              type="button"
              onClick={handleWhatsAppClick}
              className="stitch-secondary-btn stitch-whatsapp-btn"
            >
              <MessageSquare size={16} />
              Join Our WhatsApp Updates
            </button>
            <button
              type="button"
              onClick={handleShareForm}
              className="stitch-secondary-btn"
            >
              <Share2 size={16} />
              Share Form With Friends
            </button>
          </div>
          <div className="confirm-trust">
            <span className="confirm-trust-mark">✓</span>
            <p>
              We match serious tenants with trusted agents based on your exact needs. No upfront fees for tenants.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
