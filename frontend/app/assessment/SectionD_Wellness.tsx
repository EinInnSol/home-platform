import React, { useState, useEffect } from 'react';

interface SectionDData {
  physicalHealthEviction: string;
  chronicHealth: string;
  hivAidsInterest: string;
  physicalDisability: string;
  avoidsHelp: string;
  pregnant: string;
  substanceEviction: string;
  substanceHousingDifficulty: string;
  mentalHealthEviction: string;
  headInjury: string;
  learningDisability: string;
  mentalHealthNeed: string;
  notTakingMeds: string;
  misusingMeds: string;
  abuseTrauma: string;
}

interface SectionDProps {
  onNext: (data: SectionDData) => void;
  onBack: () => void;
  initialData?: Partial<SectionDData>;
  currentStep: number;
  totalSteps: number;
  gender?: string;
}

const SectionD_Wellness: React.FC<SectionDProps> = ({
  onNext,
  onBack,
  initialData = {},
  currentStep,
  totalSteps,
  gender
}) => {
  const [formData, setFormData] = useState<SectionDData>({
    physicalHealthEviction: initialData.physicalHealthEviction || '',
    chronicHealth: initialData.chronicHealth || '',
    hivAidsInterest: initialData.hivAidsInterest || '',
    physicalDisability: initialData.physicalDisability || '',
    avoidsHelp: initialData.avoidsHelp || '',
    pregnant: initialData.pregnant || '',
    substanceEviction: initialData.substanceEviction || '',
    substanceHousingDifficulty: initialData.substanceHousingDifficulty || '',
    mentalHealthEviction: initialData.mentalHealthEviction || '',
    headInjury: initialData.headInjury || '',
    learningDisability: initialData.learningDisability || '',
    mentalHealthNeed: initialData.mentalHealthNeed || '',
    notTakingMeds: initialData.notTakingMeds || '',
    misusingMeds: initialData.misusingMeds || '',
    abuseTrauma: initialData.abuseTrauma || ''
  });

  const [errors, setErrors] = useState<Partial<Record<keyof SectionDData, string>>>({});

  useEffect(() => {
    localStorage.setItem('vi-spdat-section-d', JSON.stringify(formData));
  }, [formData]);

  const handleChange = (field: keyof SectionDData, value: string) => {
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
    const newErrors: Partial<Record<keyof SectionDData, string>> = {};
    
    Object.keys(formData).forEach(key => {
      const field = key as keyof SectionDData;
      // Skip pregnancy question if not female
      if (field === 'pregnant' && gender !== 'female') return;
      
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
    field: keyof SectionDData,
    question: string,
    questionNumber: string,
    skip?: boolean
  ) => {
    if (skip) return null;
    
    return (
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
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium">Section {currentStep} of {totalSteps}</span>
            <span className="text-sm text-gray-500">Wellness</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(currentStep / totalSteps) * 100}%` }} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-2xl font-bold mb-2">Section D: Wellness</h2>
          <p className="text-gray-600">These questions help us connect you with appropriate health services.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Physical Health Section */}
          <div className="bg-blue-50 border-l-4 border-blue-600 p-4">
            <h3 className="font-semibold text-blue-900">Physical Health</h3>
          </div>

          {renderYesNoQuestion(
            'physicalHealthEviction',
            'Have you ever had to leave an apartment, shelter program, or other place you were staying because of your physical health?',
            '15'
          )}

          {renderYesNoQuestion(
            'chronicHealth',
            'Do you have any chronic health issues with your liver, kidneys, stomach, lungs or heart?',
            '16'
          )}

          {renderYesNoQuestion(
            'hivAidsInterest',
            'If there was space available in a program that specifically assists people that live with HIV or AIDS, would that be of interest to you?',
            '17'
          )}

          {renderYesNoQuestion(
            'physicalDisability',
            'Do you have any physical disabilities that would limit the type of housing you could access, or would make it hard to live independently because you\'d need help?',
            '18'
          )}

          {renderYesNoQuestion(
            'avoidsHelp',
            'When you are sick or not feeling well, do you avoid getting help?',
            '19'
          )}

          {renderYesNoQuestion(
            'pregnant',
            'Are you currently pregnant?',
            '20',
            gender !== 'female'
          )}

          {/* Substance Use Section */}
          <div className="bg-orange-50 border-l-4 border-orange-600 p-4">
            <h3 className="font-semibold text-orange-900">Substance Use</h3>
          </div>

          {renderYesNoQuestion(
            'substanceEviction',
            'Has your drinking or drug use led you to being kicked out of an apartment or program where you were staying in the past?',
            '21'
          )}

          {renderYesNoQuestion(
            'substanceHousingDifficulty',
            'Will drinking or drug use make it difficult for you to stay housed or afford your housing?',
            '22'
          )}

          {/* Mental Health Section */}
          <div className="bg-purple-50 border-l-4 border-purple-600 p-4">
            <h3 className="font-semibold text-purple-900">Mental Health</h3>
          </div>

          {renderYesNoQuestion(
            'mentalHealthEviction',
            'Have you ever had trouble maintaining your housing, or been kicked out of a place because of a mental health issue or concern?',
            '23a'
          )}

          {renderYesNoQuestion(
            'headInjury',
            'Have you ever had trouble maintaining your housing, or been kicked out of a place because of a past head injury?',
            '23b'
          )}

          {renderYesNoQuestion(
            'learningDisability',
            'Have you ever had trouble maintaining your housing, or been kicked out of a place because of a learning disability, developmental disability, or other impairment?',
            '23c'
          )}

          {renderYesNoQuestion(
            'mentalHealthNeed',
            'Do you have any mental health or brain issues that would make it hard for you to live independently because you\'d need help?',
            '24'
          )}

          {/* Medications Section */}
          <div className="bg-green-50 border-l-4 border-green-600 p-4">
            <h3 className="font-semibold text-green-900">Medications</h3>
          </div>

          {renderYesNoQuestion(
            'notTakingMeds',
            'Are there any medications that a doctor said you should be taking that, for whatever reason, you are not taking?',
            '25'
          )}

          {renderYesNoQuestion(
            'misusingMeds',
            'Are there any medications like painkillers that you don\'t take the way the doctor prescribed or where you sell the medication?',
            '26'
          )}

          {/* Abuse & Trauma Section */}
          <div className="bg-red-50 border-l-4 border-red-600 p-4">
            <h3 className="font-semibold text-red-900">Abuse & Trauma</h3>
          </div>

          {renderYesNoQuestion(
            'abuseTrauma',
            'Has your current period of homelessness been caused by an experience of emotional, physical, psychological, sexual, or other type of abuse, or by any other trauma you have experienced?',
            '27'
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

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500">
            If you need immediate help, please call the National Suicide Prevention Lifeline: 988
          </p>
        </div>
      </div>
    </div>
  );
};

export default SectionD_Wellness;
