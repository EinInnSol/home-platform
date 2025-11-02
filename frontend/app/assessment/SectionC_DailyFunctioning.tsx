import React, { useState, useEffect } from 'react';

interface SectionCData {
  oweMoney: string;
  hasIncome: string;
  meaningfulActivities: string;
  selfCare: string;
  relationshipCause: string;
}

interface SectionCProps {
  onNext: (data: SectionCData) => void;
  onBack: () => void;
  initialData?: Partial<SectionCData>;
  currentStep: number;
  totalSteps: number;
}

const SectionC_DailyFunctioning: React.FC<SectionCProps> = ({
  onNext,
  onBack,
  initialData = {},
  currentStep,
  totalSteps
}) => {
  const [formData, setFormData] = useState<SectionCData>({
    oweMoney: initialData.oweMoney || '',
    hasIncome: initialData.hasIncome || '',
    meaningfulActivities: initialData.meaningfulActivities || '',
    selfCare: initialData.selfCare || '',
    relationshipCause: initialData.relationshipCause || ''
  });

  const [errors, setErrors] = useState<Partial<Record<keyof SectionCData, string>>>({});

  useEffect(() => {
    localStorage.setItem('vi-spdat-section-c', JSON.stringify(formData));
  }, [formData]);

  const handleChange = (field: keyof SectionCData, value: string) => {
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
    const newErrors: Partial<Record<keyof SectionCData, string>> = {};
    
    Object.keys(formData).forEach(key => {
      if (!formData[key as keyof SectionCData]) {
        newErrors[key as keyof SectionCData] = 'Please select an option';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onNext(formData);
    }
  };

  const renderYesNoQuestion = (
    field: keyof SectionCData,
    question: string,
    questionNumber: string
  ) => (
    <div className="bg-white rounded-lg shadow p-6">
      <label className="block text-lg font-medium mb-4">
        {questionNumber}. {question} <span className="text-red-500">*</span>
      </label>
      <div className="space-y-3">
        {['yes', 'no', 'refused'].map((value) => (
          <div key={value} className="flex items-center">
            <input
              type="radio"
              id={`${field}-${value}`}
              name={field}
              value={value}
              checked={formData[field] === value}
              onChange={(e) => handleChange(field, e.target.value)}
              className="h-4 w-4 text-blue-600"
            />
            <label htmlFor={`${field}-${value}`} className="ml-3 text-base cursor-pointer">
              {value === 'yes' ? 'Yes' : value === 'no' ? 'No' : 'Prefer not to answer'}
            </label>
          </div>
        ))}
      </div>
      {errors[field] && <p className="mt-2 text-sm text-red-600">{errors[field]}</p>}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium">Section {currentStep} of {totalSteps}</span>
            <span className="text-sm text-gray-500">Daily Functioning</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(currentStep / totalSteps) * 100}%` }} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-2xl font-bold mb-2">Section C: Socialization & Daily Functioning</h2>
          <p className="text-gray-600">These questions help us understand your daily life and needs.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {renderYesNoQuestion(
            'oweMoney',
            'Is there any person, past landlord, business, bookie, dealer, or government group like the IRS that thinks you owe them money?',
            '10'
          )}

          {renderYesNoQuestion(
            'hasIncome',
            'Do you get any money from the government, a pension, an inheritance, working under the table, a regular job, or anything like that?',
            '11'
          )}

          {renderYesNoQuestion(
            'meaningfulActivities',
            'Do you have planned activities, other than just surviving, that make you feel happy and fulfilled?',
            '12'
          )}

          {renderYesNoQuestion(
            'selfCare',
            'Are you currently able to take care of basic needs like bathing, changing clothes, using a restroom, getting food and clean water?',
            '13'
          )}

          {renderYesNoQuestion(
            'relationshipCause',
            'Is your current homelessness caused by a relationship that broke down, an unhealthy or abusive relationship, or because family or friends caused you to become evicted?',
            '14'
          )}

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

export default SectionC_DailyFunctioning;
