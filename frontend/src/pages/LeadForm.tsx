import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, ArrowLeft, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import type { LeadFormData, TenantLeadRequest } from '../types/types';
import { submitTenantLead } from '../services/api';

const STEPS = [
  'Location',
  'Property Type',
  'Budget',
  'Move-in Date',
  'Contact Info',
];

const LOCATIONS = [
  { name: 'Lekki', type: 'Island' },
  { name: 'Yaba', type: 'Mainland' },
  { name: 'Ikeja', type: 'Mainland' },
  { name: 'Ajah', type: 'Island' },
  { name: 'Surulere', type: 'Mainland' },
];

const PROPERTY_TYPES = ['1 bedroom', '2 bedroom', 'Self-contain', 'Studio'];

export default function LeadForm() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const [formData, setFormData] = useState<LeadFormData>({
    fullName: '',
    phoneNumber: '',
    email: '',
    locations: [],
    propertyType: '',
    budgetMin: '',
    budgetMax: '',
    moveInDate: '',
  });

  const handleLocationToggle = (location: string) => {
    setFormData((prev) => ({
      ...prev,
      locations: prev.locations.includes(location)
        ? prev.locations.filter((loc) => loc !== location)
        : [...prev.locations, location],
    }));
    setApiError(null);
  };

  const validateStep = (): boolean => {
    setApiError(null);

    switch (currentStep) {
      case 0:
        if (formData.locations.length === 0) {
          setApiError('Please select at least one location');
          return false;
        }
        return true;

      case 1:
        if (!formData.propertyType) {
          setApiError('Please select a property type');
          return false;
        }
        return true;

      case 2:
        if (!formData.budgetMax || Number(formData.budgetMax) < 100000) {
          setApiError('Maximum budget must be at least ₦100,000');
          return false;
        }
        if (
          formData.budgetMin &&
          Number(formData.budgetMax) < Number(formData.budgetMin)
        ) {
          setApiError('Maximum budget must be greater than or equal to minimum budget');
          return false;
        }
        return true;

      case 3:
        if (!formData.moveInDate) {
          setApiError('Please select a move-in date');
          return false;
        }
        // Validate that date is not in the past
        const selectedDate = new Date(formData.moveInDate);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        if (selectedDate < today) {
          setApiError('Move-in date must be in the future');
          return false;
        }
        return true;

      case 4:
        if (!formData.fullName || formData.fullName.trim().length < 2) {
          setApiError('Please enter a valid name (at least 2 characters)');
          return false;
        }
        if (!formData.phoneNumber || formData.phoneNumber.trim().length < 10) {
          setApiError('Please enter a valid phone number');
          return false;
        }
        return true;

      default:
        return true;
    }
  };

  const handleNext = () => {
    if (validateStep()) {
      if (currentStep < STEPS.length - 1) {
        setCurrentStep(currentStep + 1);
      } else {
        handleSubmit();
      }
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
      setApiError(null);
    }
  };

  const handleSubmit = async () => {
    if (!validateStep()) return;

    setIsLoading(true);
    setApiError(null);

    try {
      // Convert form data to API format
      const budgetMin = formData.budgetMin ? parseInt(formData.budgetMin) : undefined;
      const budgetMax = parseInt(formData.budgetMax);
      const phoneNumber = normalizePhoneNumber(formData.phoneNumber);

      const payload: TenantLeadRequest = {
        full_name: formData.fullName,
        phone_number: phoneNumber,
        email: formData.email || undefined,
        location_preference: formData.locations.join(','),
        budget_min: budgetMin,
        budget_max: budgetMax,
        property_type: formData.propertyType,
        move_in_date: formData.moveInDate,
      };

      const result = await submitTenantLead(payload);

      if (result.success && result.data) {
        // Navigate to confirmation page with lead data
        navigate('/confirmation', { state: { lead: result.data } });
      } else {
        setApiError(
          result.error?.message || 'Failed to submit form. Please try again.'
        );
        setIsLoading(false);
      }
    } catch (error) {
      setApiError('An error occurred. Please try again.');
      setIsLoading(false);
    }
  };

  const normalizePhoneNumber = (phone: string): string => {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.startsWith('234')) {
      return '+' + cleaned;
    }
    if (cleaned.startsWith('0')) {
      return '+234' + cleaned.slice(1);
    }
    return '+234' + cleaned;
  };

  const progressPercent = ((currentStep + 1) / STEPS.length) * 100;

  return (
    <div className="stitch-shell">
      <div className="stitch-phone">
        <header className="form-topbar">
          <button
            type="button"
            className="form-back"
            aria-label="Go back"
            onClick={() => (currentStep > 0 ? handleBack() : navigate('/'))}
            disabled={isLoading}
          >
            <ArrowLeft size={18} />
          </button>
          <p className="form-step-text">
            Step {currentStep + 1} of {STEPS.length}
          </p>
        </header>
        <div className="form-progress" aria-hidden="true">
          <div className="form-progress-fill" style={{ width: `${progressPercent}%` }} />
        </div>
        <div className="stitch-content">
          <p className="form-eyebrow">LET'S FIND YOU A HOUSE FAST</p>
          <h1 className="form-title">
            {currentStep === 0 && 'Where are you looking to rent?'}
            {currentStep === 1 && 'What type of property do you need?'}
            {currentStep === 2 && "What's your budget?"}
            {currentStep === 3 && 'When do you want to move in?'}
            {currentStep === 4 && 'Tell us how to reach you'}
          </h1>
          <p className="form-subtitle">
            {currentStep === 0 && "Choose areas you're open to"}
            {currentStep === 1 && 'Pick your space'}
            {currentStep === 2 && "Choose with your pocket in mind"}
            {currentStep === 3 && 'Set that date!'}
            {currentStep === 4 && "We want to keep up communication"}
          </p>

          {apiError && (
            <div className="form-error" role="alert">
              <AlertCircle size={16} />
              <span>{apiError}</span>
            </div>
          )}

          {currentStep === 0 && (
            <section className="option-grid" aria-label="Locations">
              {LOCATIONS.map((location) => {
                const selected = formData.locations.includes(location.name);

                return (
                  <button
                    type="button"
                    key={location.name}
                    onClick={() => handleLocationToggle(location.name)}
                    className={`option-card ${selected ? 'selected' : ''} ${location.name === 'Surulere' ? 'full' : ''}`}
                  >
                    <div>
                      <p className="option-name">{location.name}</p>
                      <p className="option-type">{location.type}</p>
                    </div>
                    <span className={`option-check ${selected ? 'checked' : ''}`}>
                      {selected && <CheckCircle size={12} />}
                    </span>
                  </button>
                );
              })}
            </section>
          )}

          {currentStep === 1 && (
            <section className="option-grid" aria-label="Property Types">
              {PROPERTY_TYPES.map((type) => {
                const selected = formData.propertyType === type;

                return (
                  <button
                    type="button"
                    key={type}
                    onClick={() =>
                      setFormData((prev) => ({
                        ...prev,
                        propertyType: type,
                      }))
                    }
                    className={`option-card ${selected ? 'selected' : ''}`}
                  >
                    <div>
                      <p className="option-name">{type}</p>
                    </div>
                    <span className={`option-check ${selected ? 'checked' : ''}`}>
                      {selected && <CheckCircle size={12} />}
                    </span>
                  </button>
                );
              })}
            </section>
          )}

          {currentStep === 2 && (
            <section className="form-fields" aria-label="Budget">
              <div>
                <label className="form-label" htmlFor="budgetMin">
                  Minimum Budget (Optional)
                </label>
                <input
                  id="budgetMin"
                  type="number"
                  placeholder="e.g., 350000"
                  value={formData.budgetMin}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      budgetMin: e.target.value,
                    }))
                  }
                  className="form-input"
                />
                <p className="form-help">NGN</p>
              </div>

              <div>
                <label className="form-label" htmlFor="budgetMax">
                  Maximum Budget *
                </label>
                <input
                  id="budgetMax"
                  type="number"
                  placeholder="e.g., 550000"
                  value={formData.budgetMax}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      budgetMax: e.target.value,
                    }))
                  }
                  className="form-input"
                />
                <p className="form-help">Minimum 100000 NGN</p>
              </div>
            </section>
          )}

          {currentStep === 3 && (
            <section className="form-fields" aria-label="Move-in Date">
              <div>
                <label className="form-label" htmlFor="moveInDate">
                  When do you want to move in?
                </label>
                <input
                  id="moveInDate"
                  type="date"
                  value={formData.moveInDate}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      moveInDate: e.target.value,
                    }))
                  }
                  min={new Date().toISOString().split('T')[0]}
                  className="form-input"
                />
              </div>
            </section>
          )}

          {currentStep === 4 && (
            <section className="form-fields" aria-label="Contact Info">
              <div>
                <label className="form-label" htmlFor="fullName">
                  Full Name *
                </label>
                <input
                  id="fullName"
                  type="text"
                  placeholder="e.g., Chioma Okonkwo"
                  value={formData.fullName}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      fullName: e.target.value,
                    }))
                  }
                  className="form-input"
                />
              </div>

              <div>
                <label className="form-label" htmlFor="phoneNumber">
                  WhatsApp/Phone Number *
                </label>
                <input
                  id="phoneNumber"
                  type="tel"
                  placeholder="e.g., +234 812 345 6789"
                  value={formData.phoneNumber}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      phoneNumber: e.target.value,
                    }))
                  }
                  className="form-input"
                />
                <p className="form-help">Nigerian number format</p>
              </div>

              <div>
                <label className="form-label" htmlFor="email">
                  Email (Optional)
                </label>
                <input
                  id="email"
                  type="email"
                  placeholder="e.g., chioma@example.com"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      email: e.target.value,
                    }))
                  }
                  className="form-input"
                />
              </div>
            </section>
          )}

          <div className="form-actions">
            <button onClick={handleNext} disabled={isLoading} className="stitch-primary-btn">
              {isLoading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  Submitting...
                </>
              ) : (
                <>
                  {currentStep === STEPS.length - 1 ? 'Submit' : 'Continue'}
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
