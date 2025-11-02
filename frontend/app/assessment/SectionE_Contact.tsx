import React, { useState, useEffect } from 'react';

interface SectionEData {
  bestLocation: string;
  bestTime: string;
  phone: string;
  email: string;
  photoConsent: string;
}

interface SectionEProps {
  onNext: (data: SectionEData) => void;
  onBack: () => void;
  initialData?: Partial<SectionEData>;
  currentStep: number;
  totalSteps: number;
}

const SectionE_Contact: React.FC<SectionEProps> = ({
  onNext,
  onBack,
  initialData = {},
  currentStep,
  totalSteps
}) => {
  const [formData, setFormData] = useState<SectionEData>({
    bestLocation: initialData.bestLocation || '',
    bestTime: initialData.bestTime || '',
    phone: initialData.phone || '',
    email: initialData.email || '',
    photoConsent: initialData.photoConsent || ''
  });

  const [errors, setErrors] = useState<Partial<Record<keyof SectionEData, string>>>({});

  useEffect(() => {
    localStorage.setItem('vi-spdat-section-e', JSON.stringify(formData));
  }, [formData]);

  const handleChange = (field: keyof SectionEData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof SectionEData, string>> = {};
    
    if (!formData.bestLocation.trim()) {
      newErrors.bestLocation = 'Please provide a location';
    }
    
    if (!formData.photoConsent) {
      newErrors.photoConsent = 'Please select an option';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onNext(formData);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium">Section {currentStep} of {totalSteps}</span>
            <span className="text-sm text-gray-500">Contact Information</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(currentStep / totalSteps) * 100}%` }} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-2xl font-bold mb-2">Section E: Contact Information</h2>
          <p className="text-gray-600">
            This information helps us follow up with you about housing opportunities.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <label htmlFor="bestLocation" className="block text-lg font-medium mb-4">
              On a regular day, where is it easiest to find you? <span className="text-red-500">*</span>
            </label>
            <p className="text-sm text-gray-600 mb-3">
              For example: "Outside the library on 5th Street" or "At the park near Main St"
            </p>
            <textarea
              id="bestLocation"
              value={formData.bestLocation}
              onChange={(e) => handleChange('bestLocation', e.target.value)}
              placeholder="Describe the location..."
              rows={3}
              className="w-full px-4 py-3 border rounded-md focus:ring-2 focus:ring-blue-500"
            />
            {errors.bestLocation && (
              <p className="mt-2 text-sm text-red-600">{errors.bestLocation}</p>
            )}
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <label htmlFor="bestTime" className="block text-lg font-medium mb-4">
              What time of day is easiest to find you there?
            </label>
            <input
              id="bestTime"
              type="text"
              value={formData.bestTime}
              onChange={(e) => handleChange('bestTime', e.target.value)}
              placeholder="e.g., Morning around 9am, Afternoon, Evening..."
              className="w-full px-4 py-3 border rounded-md focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <label htmlFor="phone" className="block text-lg font-medium mb-4">
              Is there a phone number where someone can safely reach you or leave a message?
            </label>
            <p className="text-sm text-gray-600 mb-3">Optional - only if you have access to a phone</p>
            <input
              id="phone"
              type="tel"
              value={formData.phone}
              onChange={(e) => handleChange('phone', e.target.value)}
              placeholder="(555) 123-4567"
              className="w-full px-4 py-3 border rounded-md focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <label htmlFor="email" className="block text-lg font-medium mb-4">
              Is there an email address where someone can safely reach you?
            </label>
            <p className="text-sm text-gray-600 mb-3">Optional - only if you have access to email</p>
            <input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              placeholder="your.email@example.com"
              className="w-full px-4 py-3 border rounded-md focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <label className="block text-lg font-medium mb-4">
              May we take your picture to make it easier to find you and confirm your identity in the future? <span className="text-red-500">*</span>
            </label>
            <p className="text-sm text-gray-600 mb-4">
              This photo would only be used internally by staff to help locate you for housing opportunities.
            </p>
            <div className="space-y-3">
              {[
                { value: 'yes', label: 'Yes, you may take my photo' },
                { value: 'no', label: 'No, please do not take my photo' },
                { value: 'refused', label: 'I prefer not to answer right now' }
              ].map((option) => (
                <div key={option.value} className="flex items-start">
                  <input
                    type="radio"
                    id={`photo-${option.value}`}
                    name="photoConsent"
                    value={option.value}
                    checked={formData.photoConsent === option.value}
                    onChange={(e) => handleChange('photoConsent', e.target.value)}
                    className="mt-1 h-4 w-4 text-blue-600"
                  />
                  <label htmlFor={`photo-${option.value}`} className="ml-3 text-base cursor-pointer">
                    {option.label}
                  </label>
                </div>
              ))}
            </div>
            {errors.photoConsent && (
              <p className="mt-2 text-sm text-red-600">{errors.photoConsent}</p>
            )}
          </div>

          <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-blue-800">
                  <strong>Privacy Notice:</strong> All information provided is confidential and will only be used to connect you with housing services. You can update your contact information at any time.
                </p>
              </div>
            </div>
          </div>

          <div className="flex gap-4 pt-6">
            <button type="button" onClick={onBack} className="flex-1 px-6 py-3 bg-white border rounded-md hover:bg-gray-50">
              Back
            </button>
            <button type="submit" className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700">
              Complete Assessment
            </button>
          </div>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500">
            You're almost done! Click "Complete Assessment" to see your results.
          </p>
        </div>
      </div>
    </div>
  );
};

export default SectionE_Contact;
