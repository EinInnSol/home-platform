import React, { useState, useEffect } from 'react';

interface SectionBData {
  erVisits: number | string;
  ambulance: number | string;
  hospitalized: number | string;
  crisisServices: number | string;
  policeInteractions: number | string;
  incarceration: number | string;
  attacked: string;
  selfHarm: string;
  legalIssues: string;
  forced: string;
  riskyBehaviors: string;
}

interface SectionBProps {
  onNext: (data: SectionBData) => void;
  onBack: () => void;
  initialData?: Partial<SectionBData>;
  currentStep: number;
  totalSteps: number;
}

const SectionB_Risks: React.FC<SectionBProps> = ({
  onNext,
  onBack,
  initialData = {},
  currentStep,
  totalSteps
}) => {
  const [formData, setFormData] = useState<SectionBData>({
    erVisits: initialData.erVisits || '',
    ambulance: initialData.ambulance || '',
    hospitalized: initialData.hospitalized || '',
    crisisServices: initialData.crisisServices || '',
    policeInteractions: initialData.policeInteractions || '',
    incarceration: initialData.incarceration || '',
    attacked: initialData.attacked || '',
    selfHarm: initialData.selfHarm || '',
    legalIssues: initialData.legalIssues || '',
    forced: initialData.forced || '',
    riskyBehaviors: initialData.riskyBehaviors || ''
  });

  const [errors, setErrors] = useState<Partial<Record<keyof SectionBData, string>>>({});

  useEffect(() => {
    localStorage.setItem('vi-spdat-section-b', JSON.stringify(formData));
  }, [formData]);

  const handleChange = (field: keyof SectionBData, value: string | number) => {
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
    const newErrors: Partial<Record<keyof SectionBData, string>> = {};
    
    // Validate all Yes/No questions have been answered
    const yesNoFields: (keyof SectionBData)[] = ['attacked', 'selfHarm', 'legalIssues', 'forced', 'riskyBehaviors'];
    yesNoFields.forEach(field => {
      if (!formData[field]) {
        newErrors[field] = 'Please select an option';
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
    field: keyof SectionBData,
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
            <span className="text-sm text-gray-500">Risks</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(currentStep / totalSteps) * 100}%` }} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-2xl font-bold mb-2">Section B: Risks</h2>
          <p className="text-gray-600">These questions help us understand your safety and wellbeing.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* B4: Emergency Service Use */}
          <div className="bg-white rounded-lg shadow p-6">
            <label className="block text-lg font-medium mb-4">
              4. In the past 6 months, how many times have you...
            </label>
            
            <div className="space-y-4">
              <div>
                <label className="block text-base mb-2">a) Received health care at an emergency department/room?</label>
                <input
                  type="number"
                  min="0"
                  value={formData.erVisits}
                  onChange={(e) => handleChange('erVisits', e.target.value)}
                  placeholder="Enter number..."
                  className="w-full px-4 py-2 border rounded-md"
                />
              </div>

              <div>
                <label className="block text-base mb-2">b) Taken an ambulance to the hospital?</label>
                <input
                  type="number"
                  min="0"
                  value={formData.ambulance}
                  onChange={(e) => handleChange('ambulance', e.target.value)}
                  placeholder="Enter number..."
                  className="w-full px-4 py-2 border rounded-md"
                />
              </div>

              <div>
                <label className="block text-base mb-2">c) Been hospitalized as an inpatient?</label>
                <input
                  type="number"
                  min="0"
                  value={formData.hospitalized}
                  onChange={(e) => handleChange('hospitalized', e.target.value)}
                  placeholder="Enter number..."
                  className="w-full px-4 py-2 border rounded-md"
                />
              </div>

              <div>
                <label className="block text-base mb-2">d) Used a crisis service (mental health crisis, domestic violence, suicide prevention)?</label>
                <input
                  type="number"
                  min="0"
                  value={formData.crisisServices}
                  onChange={(e) => handleChange('crisisServices', e.target.value)}
                  placeholder="Enter number..."
                  className="w-full px-4 py-2 border rounded-md"
                />
              </div>

              <div>
                <label className="block text-base mb-2">e) Talked to police (witnessed crime, victim, alleged perpetrator, or told to move)?</label>
                <input
                  type="number"
                  min="0"
                  value={formData.policeInteractions}
                  onChange={(e) => handleChange('policeInteractions', e.target.value)}
                  placeholder="Enter number..."
                  className="w-full px-4 py-2 border rounded-md"
                />
              </div>

              <div>
                <label className="block text-base mb-2">f) Stayed in a holding cell, jail or prison?</label>
                <input
                  type="number"
                  min="0"
                  value={formData.incarceration}
                  onChange={(e) => handleChange('incarceration', e.target.value)}
                  placeholder="Enter number..."
                  className="w-full px-4 py-2 border rounded-md"
                />
              </div>
            </div>
          </div>

          {renderYesNoQuestion('attacked', 'Have you been attacked or beaten up since you became homeless?', '5')}
          {renderYesNoQuestion('selfHarm', 'Have you threatened to or tried to harm yourself or anyone else in the last year?', '6')}
          {renderYesNoQuestion('legalIssues', 'Do you have any legal stuff going on that may result in jail, fines, or make it harder to rent?', '7')}
          {renderYesNoQuestion('forced', 'Does anybody force or trick you to do things you don\'t want to do?', '8')}
          {renderYesNoQuestion('riskyBehaviors', 'Do you ever do risky things like exchange sex for money, run drugs, have unprotected sex with strangers, or share needles?', '9')}

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

export default SectionB_Risks;
