import React, { useState, useEffect } from 'react';

interface SectionAData {
  sleepingLocation: string;
  sleepingLocationOther?: string;
  lengthHomeless: string;
  homelessEpisodes: number | string;
}

interface SectionAProps {
  onNext: (data: SectionAData) => void;
  onBack: () => void;
  initialData?: Partial<SectionAData>;
  currentStep: number;
  totalSteps: number;
}

const SectionA_HousingHistory: React.FC<SectionAProps> = ({
  onNext,
  onBack,
  initialData = {},
  currentStep,
  totalSteps
}) => {
  const [formData, setFormData] = useState<SectionAData>({
    sleepingLocation: initialData.sleepingLocation || '',
    sleepingLocationOther: initialData.sleepingLocationOther || '',
    lengthHomeless: initialData.lengthHomeless || '',
    homelessEpisodes: initialData.homelessEpisodes || ''
  });

  const [errors, setErrors] = useState<Partial<Record<keyof SectionAData, string>>>({});

  // Auto-save to localStorage
  useEffect(() => {
    localStorage.setItem('vi-spdat-section-a', JSON.stringify(formData));
  }, [formData]);

  const sleepingOptions = [
    { value: 'shelters', label: 'Shelters' },
    { value: 'transitional', label: 'Transitional Housing' },
    { value: 'safe-haven', label: 'Safe Haven' },
    { value: 'outdoors', label: 'Outdoors' },
    { value: 'other', label: 'Other (please specify)' },
    { value: 'refused', label: 'Prefer not to answer' }
  ];

  const handleChange = (field: keyof SectionAData, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof SectionAData, string>> = {};
    if (!formData.sleepingLocation) {
      newErrors.sleepingLocation = 'Please select where you sleep most frequently';
    }
    if (formData.sleepingLocation === 'other' && !formData.sleepingLocationOther) {
      newErrors.sleepingLocationOther = 'Please specify your sleeping location';
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
            <span className="text-sm text-gray-500">Housing History</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(currentStep / totalSteps) * 100}%` }}/>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-2xl font-bold mb-2">Section A: Housing History</h2>
          <p className="text-gray-600">These questions help us understand your situation.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <label className="block text-lg font-medium mb-4">
              1. Where do you sleep most frequently? <span className="text-red-500">*</span>
            </label>
            <div className="space-y-3">
              {sleepingOptions.map((option) => (
                <div key={option.value} className="flex items-start">
                  <input
                    type="radio"
                    id={`sleeping-${option.value}`}
                    name="sleepingLocation"
                    value={option.value}
                    checked={formData.sleepingLocation === option.value}
                    onChange={(e) => handleChange('sleepingLocation', e.target.value)}
                    className="mt-1 h-4 w-4 text-blue-600"
                  />
                  <label htmlFor={`sleeping-${option.value}`} className="ml-3 text-base cursor-pointer">
                    {option.label}
                  </label>
                </div>
              ))}
            </div>
            {formData.sleepingLocation === 'other' && (
              <input
                type="text"
                value={formData.sleepingLocationOther}
                onChange={(e) => handleChange('sleepingLocationOther', e.target.value)}
                placeholder="Please specify..."
                className="mt-4 w-full px-4 py-2 border rounded-md"
              />
            )}
            {errors.sleepingLocation && <p className="mt-2 text-sm text-red-600">{errors.sleepingLocation}</p>}
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <label className="block text-lg font-medium mb-4">
              2. How long since you had permanent stable housing?
            </label>
            <input
              type="text"
              value={formData.lengthHomeless}
              onChange={(e) => handleChange('lengthHomeless', e.target.value)}
              placeholder="e.g., 2 years, 6 months..."
              className="w-full px-4 py-3 border rounded-md"
            />
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <label className="block text-lg font-medium mb-4">
              3. In the last 3 years, how many times homeless?
            </label>
            <input
              type="number"
              value={formData.homelessEpisodes}
              onChange={(e) => handleChange('homelessEpisodes', e.target.value)}
              placeholder="Enter number..."
              min="0"
              className="w-full px-4 py-3 border rounded-md"
            />
          </div>

          <div className="flex gap-4 pt-6">
            <button type="button" onClick={onBack} className="flex-1 px-6 py-3 bg-white border rounded-md hover:bg-gray-50">
              Back
            </button>
            <button type="submit" className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700">
              Continue
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SectionA_HousingHistory;
