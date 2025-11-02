'use client';

import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-600 rounded-full mb-6">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Welcome to H.O.M.E.
          </h1>
          <p className="text-xl text-gray-700 mb-2">
            Housing Opportunity Management Engine
          </p>
          <p className="text-lg text-gray-600">
            City of Long Beach Homeless Services
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Housing Assessment
          </h2>
          <p className="text-gray-700 mb-6">
            This assessment helps us understand your situation and connect you with the housing resources that best fit your needs. 
            It takes about 10-15 minutes to complete.
          </p>

          <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-blue-800">
                  <strong>Your privacy is protected.</strong> All information is confidential and used only to help connect you with housing services.
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-4 mb-8">
            <h3 className="font-semibold text-gray-900">What to expect:</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="flex items-start">
                <div className="flex-shrink-0 h-6 w-6 rounded-full bg-green-100 flex items-center justify-center mr-3">
                  <svg className="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-gray-900">5 Simple Sections</p>
                  <p className="text-sm text-gray-600">Housing history, risks, daily life, wellness, and contact info</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0 h-6 w-6 rounded-full bg-green-100 flex items-center justify-center mr-3">
                  <svg className="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-gray-900">Mobile Friendly</p>
                  <p className="text-sm text-gray-600">Works on any smartphone or tablet</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0 h-6 w-6 rounded-full bg-green-100 flex items-center justify-center mr-3">
                  <svg className="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-gray-900">Save Your Progress</p>
                  <p className="text-sm text-gray-600">You can pause and come back anytime</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0 h-6 w-6 rounded-full bg-green-100 flex items-center justify-center mr-3">
                  <svg className="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-gray-900">Immediate Results</p>
                  <p className="text-sm text-gray-600">Get your housing recommendation right away</p>
                </div>
              </div>
            </div>
          </div>

          <button
            onClick={() => router.push('/assessment')}
            className="w-full py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
          >
            Start Assessment
          </button>
        </div>

        {/* Help Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h3 className="font-bold text-gray-900 mb-4">Need Help Right Now?</h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div>
              <p className="font-medium text-gray-900">Long Beach Multi-Service Center</p>
              <p className="text-gray-600">(562) 570-4500</p>
              <p className="text-gray-500 text-xs">Mon-Fri 8am-4pm</p>
            </div>
            <div>
              <p className="font-medium text-gray-900">24/7 Crisis Line</p>
              <p className="text-gray-600">988 (Call or Text)</p>
              <p className="text-gray-500 text-xs">Available anytime</p>
            </div>
            <div>
              <p className="font-medium text-gray-900">Emergency Shelter</p>
              <p className="text-gray-600">Call 211</p>
              <p className="text-gray-500 text-xs">For available beds</p>
            </div>
            <div>
              <p className="font-medium text-gray-900">Domestic Violence</p>
              <p className="text-gray-600">1-800-978-3600</p>
              <p className="text-gray-500 text-xs">Confidential support</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-gray-600">
          <p>Powered by H.O.M.E. Platform | City of Long Beach</p>
          <p className="mt-2">© 2025 Einharjer Innovative Solutions</p>
        </div>
      </div>
    </div>
  );
}
