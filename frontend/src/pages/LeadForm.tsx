import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, ArrowLeft, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { LeadFormData, TenantLeadRequest } from '../types/types';
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

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-2xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-blue-600">HomeLeads</h1>
        </div>
      </header>

      {/* Form Container */}
      <main className="flex-1 flex items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
        <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
          {/* Step Indicator */}
          <div className="mb-8">
            <div className="flex justify-between mb-4">
              {STEPS.map((step, index) => (
                <div
                  key={index}
                  className={`flex-1 text-center ${
                    index < STEPS.length - 1 ? 'pr-2' : ''
                  }`}
                >
                  <div
                    className={`inline-flex items-center justify-center w-10 h-10 rounded-full font-semibold text-sm ${
                      index === currentStep
                        ? 'bg-blue-600 text-white'
                        : index < currentStep
                        ? 'bg-green-500 text-white'
                        : 'bg-gray-200 text-gray-600'
                    }`}
                  >
                    {index < currentStep ? <CheckCircle size={20} /> : index + 1}
                  </div>
                </div>
              ))}
            </div>
            <p className="text-center text-sm text-gray-600">
              Step {currentStep + 1} of {STEPS.length}
            </p>
          </div>

          {/* Step Header */}
          <div className="mb-8">
            <h2 className="text-center text-sm font-bold text-gray-500 tracking-wide uppercase mb-2">
              LET'S FIND YOU A HOUSE FAST
            </h2>
            <h3 className="text-center text-2xl font-bold text-gray-900">
              {currentStep === 0 && 'Where are you looking to rent?'}
              {currentStep === 1 && 'What type of property do you need?'}
              {currentStep === 2 && 'What's your budget?'}
              {currentStep === 3 && 'When do you want to move in?'}
              {currentStep === 4 && 'Tell us how to reach you'}
            </h3>
          </div>

          {/* Error Message */}
          {apiError && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
              <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
              <p className="text-red-700 text-sm">{apiError}</p>
            </div>
          )}

          {/* Step Content */}
          <div className="mb-8">
            {/* Step 0: Location */}
            {currentStep === 0 && (
              <div className="space-y-3">
                {LOCATIONS.map((location) => (
                  <button
                    key={location.name}
                    onClick={() => handleLocationToggle(location.name)}
                    className={`w-full p-4 rounded-lg border-2 transition-all text-left ${
                      formData.locations.includes(location.name)
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 bg-white hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-semibold text-gray-900">
                          {location.name}
                        </p>
                        <p className="text-sm text-gray-600">{location.type}</p>
                      </div>
                      <div
                        className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                          formData.locations.includes(location.name)
                            ? 'bg-blue-600 border-blue-600'
                            : 'border-gray-300'
                        }`}
                      >
                        {formData.locations.includes(location.name) && (
                          <CheckCircle size={16} className="text-white" />
                        )}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            )}

            {/* Step 1: Property Type */}
            {currentStep === 1 && (
              <div className="space-y-3">
                {PROPERTY_TYPES.map((type) => (
                  <button
                    key={type}
                    onClick={() =>
                      setFormData((prev) => ({
                        ...prev,
                        propertyType: type,
                      }))
                    }
                    className={`w-full p-4 rounded-lg border-2 transition-all text-left ${
                      formData.propertyType === type
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 bg-white hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <p className="font-semibold text-gray-900">{type}</p>
                      <div
                        className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                          formData.propertyType === type
                            ? 'bg-blue-600 border-blue-600'
                            : 'border-gray-300'
                        }`}
                      >
                        {formData.propertyType === type && (
                          <CheckCircle size={16} className="text-white" />
                        )}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            )}

            {/* Step 2: Budget */}
            {currentStep === 2 && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Minimum Budget (Optional)
                  </label>
                  <input
                    type="number"
                    placeholder="e.g., 350,000"
                    value={formData.budgetMin}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        budgetMin: e.target.value,
                      }))
                    }
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">₦ NGN</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Maximum Budget *
                  </label>
                  <input
                    type="number"
                    placeholder="e.g., 550,000"
                    value={formData.budgetMax}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        budgetMax: e.target.value,
                      }))
                    }
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">₦ NGN (minimum ₦100,000)</p>
                </div>
              </div>
            )}

            {/* Step 3: Move-in Date */}
            {currentStep === 3 && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  When do you want to move in?
                </label>
                <input
                  type="date"
                  value={formData.moveInDate}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      moveInDate: e.target.value,
                    }))
                  }
                  min={new Date().toISOString().split('T')[0]}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none"
                />
              </div>
            )}

            {/* Step 4: Contact Info */}
            {currentStep === 4 && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    placeholder="e.g., Chioma Okonkwo"
                    value={formData.fullName}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        fullName: e.target.value,
                      }))
                    }
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    WhatsApp/Phone Number *
                  </label>
                  <input
                    type="tel"
                    placeholder="e.g., +234 812 345 6789"
                    value={formData.phoneNumber}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        phoneNumber: e.target.value,
                      }))
                    }
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none text-lg font-semibold"
                  />
                  <p className="text-xs text-gray-500 mt-1">Nigerian number format</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email (Optional)
                  </label>
                  <input
                    type="email"
                    placeholder="e.g., chioma@example.com"
                    value={formData.email}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        email: e.target.value,
                      }))
                    }
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none"
                  />
                </div>
              </div>
            )}
          </div>

          {/* Navigation Buttons */}
          <div className="flex gap-4">
            <button
              onClick={handleBack}
              disabled={currentStep === 0 || isLoading}
              className="flex-1 py-3 px-4 rounded-lg border border-gray-300 text-gray-700 font-semibold hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2"
            >
              <ArrowLeft size={20} />
              Back
            </button>

            <button
              onClick={handleNext}
              disabled={isLoading}
              className="flex-1 py-3 px-4 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition-colors disabled:bg-blue-400 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <Loader2 size={20} className="animate-spin" />
                  Submitting...
                </>
              ) : (
                <>
                  {currentStep === STEPS.length - 1 ? 'Submit' : 'Continue'}
                  <ArrowRight size={20} />
                </>
              )}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
