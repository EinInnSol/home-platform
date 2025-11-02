'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import SectionA_HousingHistory from './SectionA_HousingHistory';
import SectionB_Risks from './SectionB_Risks';
import SectionC_DailyFunctioning from './SectionC_DailyFunctioning';
import SectionD_Wellness from './SectionD_Wellness';
import SectionE_Contact from './SectionE_Contact';
import { AssessmentData, calculateVISPDATScore } from '@/lib/scoring';

export default function AssessmentPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [assessmentData, setAssessmentData] = useState<Partial<AssessmentData>>({});

  const totalSteps = 5;

  const handleSectionComplete = (sectionData: any) => {
    const updatedData = { ...assessmentData, ...sectionData };
    setAssessmentData(updatedData);
    
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    } else {
      // Calculate score and redirect to results
      const score = calculateVISPDATScore(updatedData as AssessmentData);
      localStorage.setItem('vi-spdat-results', JSON.stringify({
        assessment: updatedData,
        score
      }));
      router.push('/assessment/results');
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    } else {
      router.push('/');
    }
  };

  return (
    <>
      {currentStep === 1 && (
        <SectionA_HousingHistory
          onNext={handleSectionComplete}
          onBack={handleBack}
          initialData={assessmentData}
          currentStep={currentStep}
          totalSteps={totalSteps}
        />
      )}
      
      {currentStep === 2 && (
        <SectionB_Risks
          onNext={handleSectionComplete}
          onBack={handleBack}
          initialData={assessmentData}
          currentStep={currentStep}
          totalSteps={totalSteps}
        />
      )}
      
      {currentStep === 3 && (
        <SectionC_DailyFunctioning
          onNext={handleSectionComplete}
          onBack={handleBack}
          initialData={assessmentData}
          currentStep={currentStep}
          totalSteps={totalSteps}
        />
      )}
      
      {currentStep === 4 && (
        <SectionD_Wellness
          onNext={handleSectionComplete}
          onBack={handleBack}
          initialData={assessmentData}
          currentStep={currentStep}
          totalSteps={totalSteps}
        />
      )}
      
      {currentStep === 5 && (
        <SectionE_Contact
          onNext={handleSectionComplete}
          onBack={handleBack}
          initialData={assessmentData}
          currentStep={currentStep}
          totalSteps={totalSteps}
        />
      )}
    </>
  );
}
