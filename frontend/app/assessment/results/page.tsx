'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ScoreResult, getScoreColor, getVulnerabilityColor } from '@/lib/scoring';

export default function ResultsPage() {
  const router = useRouter();
  const [results, setResults] = useState<{ assessment: any; score: ScoreResult } | null>(null);

  useEffect(() => {
    const savedResults = localStorage.getItem('vi-spdat-results');
    if (savedResults) {
      setResults(JSON.parse(savedResults));
    } else {
      router.push('/assessment');
    }
  }, [router]);

  if (!results) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your results...</p>
        </div>
      </div>
    );
  }

  const { score } = results;

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Assessment Complete</h1>
          <p className="text-gray-600">Thank you for completing the VI-SPDAT assessment</p>
        </div>

        {/* Score Card */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
          <div className="text-center mb-6">
            <div className="inline-block">
              <div className={`text-6xl font-bold ${getScoreColor(score.totalScore)}`}>
                {score.totalScore}
              </div>
              <div className="text-sm text-gray-500 mt-1">out of {score.maxScore} points</div>
            </div>
          </div>

          <div className="flex justify-center mb-6">
            <span className={`px-4 py-2 rounded-full text-sm font-medium ${getVulnerabilityColor(score.vulnerability)}`}>
              {score.vulnerability.charAt(0).toUpperCase() + score.vulnerability.slice(1)} Vulnerability
            </span>
          </div>

          <div className="border-t border-gray-200 pt-6">
            <h2 className="text-xl font-bold text-gray-900 mb-3">Recommendation</h2>
            <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
              <p className="text-lg font-semibold text-blue-900 mb-2">
                {score.recommendation}
              </p>
              <p className="text-blue-800">
                {score.recommendationDescription}
              </p>
            </div>
          </div>
        </div>

        {/* Score Breakdown */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Score Breakdown</h3>
          <div className="space-y-3">
            {Object.entries(score.sectionScores).map(([section, sectionScore]) => {
              const maxScores: Record<string, number> = {
                presurvey: 1,
                sectionA: 2,
                sectionB: 4,
                sectionC: 4,
                sectionD: 6
              };
              const sectionNames: Record<string, string> = {
                presurvey: 'Pre-Survey (Age)',
                sectionA: 'Housing History',
                sectionB: 'Risks',
                sectionC: 'Daily Functioning',
                sectionD: 'Wellness'
              };
              
              return (
                <div key={section} className="flex items-center justify-between">
                  <span className="text-gray-700">{sectionNames[section]}</span>
                  <div className="flex items-center gap-3">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${(sectionScore / maxScores[section]) * 100}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium text-gray-900 w-12 text-right">
                      {sectionScore}/{maxScores[section]}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Next Steps */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Next Steps</h3>
          <div className="space-y-3">
            <div className="flex items-start">
              <div className="flex-shrink-0 h-6 w-6 rounded-full bg-blue-100 flex items-center justify-center mr-3 mt-0.5">
                <span className="text-blue-600 text-sm font-bold">1</span>
              </div>
              <div>
                <p className="font-medium text-gray-900">A caseworker will review your assessment</p>
                <p className="text-sm text-gray-600">They will contact you within 2-3 business days</p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 h-6 w-6 rounded-full bg-blue-100 flex items-center justify-center mr-3 mt-0.5">
                <span className="text-blue-600 text-sm font-bold">2</span>
              </div>
              <div>
                <p className="font-medium text-gray-900">Keep your contact information current</p>
                <p className="text-sm text-gray-600">Make sure we can reach you at the location you provided</p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 h-6 w-6 rounded-full bg-blue-100 flex items-center justify-center mr-3 mt-0.5">
                <span className="text-blue-600 text-sm font-bold">3</span>
              </div>
              <div>
                <p className="font-medium text-gray-900">Attend your scheduled appointments</p>
                <p className="text-sm text-gray-600">This helps us connect you with housing faster</p>
              </div>
            </div>
          </div>
        </div>

        {/* Resources */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
          <h3 className="text-lg font-bold text-green-900 mb-3">Immediate Resources</h3>
          <div className="space-y-2 text-sm">
            <p className="text-green-800">
              <strong>Long Beach Multi-Service Center:</strong> (562) 570-4500
            </p>
            <p className="text-green-800">
              <strong>24/7 Crisis Line:</strong> 988 (Suicide & Crisis Lifeline)
            </p>
            <p className="text-green-800">
              <strong>Domestic Violence Hotline:</strong> 1-800-978-3600
            </p>
            <p className="text-green-800">
              <strong>Emergency Shelter:</strong> Call 211 for availability
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={() => window.print()}
            className="flex-1 px-6 py-3 bg-white border border-gray-300 rounded-md hover:bg-gray-50 font-medium"
          >
            Print Results
          </button>
          <button
            onClick={() => router.push('/')}
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium"
          >
            Return to Home
          </button>
        </div>

        {/* Privacy Notice */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Your information is confidential and protected by federal privacy laws.</p>
          <p className="mt-1">Assessment ID: {Date.now().toString(36).toUpperCase()}</p>
        </div>
      </div>
    </div>
  );
}
