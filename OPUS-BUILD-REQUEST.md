# COMPREHENSIVE BUILD REQUEST FOR H.O.M.E. PLATFORM
## Feed this entire document to Claude Opus 4.1 in Vertex AI

---

## PROJECT CONTEXT

**Project Name:** H.O.M.E. Platform (Housing Opportunity Management Engine)  
**Client:** City of Long Beach, California  
**Contract Value:** $75,000 pilot program  
**Demo Date:** November 15, 2025 (14 days from now)  
**Current Date:** November 1, 2025

**Mission:** Build a digital intake platform for homeless services that replaces Long Beach's paper-based VI-SPDAT assessment system.

---

## WHAT WE'RE BUILDING

A complete web application with 3 main components:

1. **Client Intake Portal** - Mobile-first assessment form
2. **Caseworker Dashboard** - View and manage assessments  
3. **City Analytics View** - Aggregate statistics and reporting

---

## TECHNICAL STACK

- **Frontend:** Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **State:** React hooks (useState, useEffect)
- **Storage:** localStorage for drafts, Firebase Firestore for persistence
- **Forms:** React Hook Form + Zod validation (optional)
- **Deployment:** Vercel

**Project Structure:**
```
home-platform/
├── frontend/
│   ├── app/
│   │   ├── page.tsx                    # Landing page
│   │   ├── assessment/
│   │   │   ├── page.tsx               # Start assessment
│   │   │   ├── [step]/page.tsx        # Multi-step form router
│   │   │   ├── SectionA_HousingHistory.tsx  ✅ DONE
│   │   │   ├── SectionB_Risks.tsx     ⏳ NEED THIS
│   │   │   ├── SectionC_DailyFunctioning.tsx  ⏳ NEED THIS
│   │   │   ├── SectionD_Wellness.tsx  ⏳ NEED THIS
│   │   │   ├── SectionE_Contact.tsx   ⏳ NEED THIS
│   │   │   └── results/page.tsx       ⏳ NEED THIS
│   │   ├── dashboard/
│   │   │   ├── page.tsx               ⏳ NEED THIS
│   │   │   └── [id]/page.tsx          ⏳ NEED THIS
│   │   └── analytics/
│   │       └── page.tsx               ⏳ NEED THIS
│   ├── components/
│   │   ├── ui/                        # shadcn components
│   │   ├── assessment/
│   │   │   ├── ProgressBar.tsx        ⏳ NEED THIS
│   │   │   └── QuestionCard.tsx       ⏳ NEED THIS
│   │   └── dashboard/
│   │       └── AssessmentCard.tsx     ⏳ NEED THIS
│   ├── lib/
│   │   ├── scoring.ts                 ⏳ NEED THIS
│   │   ├── types.ts                   ⏳ NEED THIS
│   │   └── storage.ts                 ⏳ NEED THIS
```

---

## THE VI-SPDAT ASSESSMENT

### Official Tool Information
- **Name:** Vulnerability Index - Service Prioritization Decision Assistance Tool v2.0
- **Purpose:** Federally-mandated (HEARTH Act) homeless intake assessment
- **Used by:** 1000+ communities nationwide, including Long Beach
- **Scoring:** 0-17 points determines housing intervention level

### Scoring Recommendations
- **0-3 points:** No housing intervention
- **4-7 points:** Assessment for Rapid Re-Housing
- **8+ points:** Assessment for Permanent Supportive Housing/Housing First

---

## SECTION-BY-SECTION REQUIREMENTS

### SECTION A: HOUSING HISTORY (Already Built ✅)
Location: `frontend/app/assessment/SectionA_HousingHistory.tsx`

**Questions:**
1. Where do you sleep most frequently? (Radio: Shelters, Transitional Housing, Safe Haven, Outdoors, Other, Refused)
2. How long since permanent stable housing? (Text input)
3. In last 3 years, how many times homeless? (Number input)

**Scoring:**
- Q1: 1 point if NOT Shelters/Transitional/Safe Haven
- Q2+Q3 combined: 1 point if 1+ consecutive years OR 4+ episodes

**Total Section A Score:** 0-2 points

---

### SECTION B: RISKS (Need to Build)
Location: `frontend/app/assessment/SectionB_Risks.tsx`

**Questions:**

**B4. Emergency Service Use (6 sub-questions)**
In the past 6 months, how many times have you:
- a) Received ER health care? (Number)
- b) Taken ambulance to hospital? (Number)
- c) Been hospitalized as inpatient? (Number)
- d) Used crisis services? (Number)
- e) Talked to police? (Number)
- f) Stayed in jail/holding cell? (Number)

**Scoring:** If total of all 6 ≥ 4 → 1 point

**B5.** Have you been attacked/beaten up since homeless? (Yes/No/Refused)

**B6.** Have you threatened to harm yourself or others in last year? (Yes/No/Refused)

**Scoring:** If B5=Yes OR B6=Yes → 1 point for "Risk of Harm"

**B7.** Legal issues that make renting difficult? (Yes/No/Refused)

**Scoring:** If Yes → 1 point

**B8.** Does anyone force/trick you to do things you don't want? (Yes/No/Refused)

**B9.** Do you do risky things (exchange sex for money, run drugs, unprotected sex, share needles)? (Yes/No/Refused)

**Scoring:** If B8=Yes OR B9=Yes → 1 point for "Risk of Exploitation"

**Total Section B Score:** 0-4 points

---

### SECTION C: SOCIALIZATION & DAILY FUNCTIONING (Need to Build)
Location: `frontend/app/assessment/SectionC_DailyFunctioning.tsx`

**Questions:**

**C10.** Does anyone think you owe them money (landlord, business, IRS, etc.)? (Yes/No/Refused)

**C11.** Do you get any money (government, pension, job, etc.)? (Yes/No/Refused)

**Scoring:** If C10=Yes OR C11=No → 1 point for "Money Management"

**C12.** Do you have planned activities that make you happy? (Yes/No/Refused)

**Scoring:** If No → 1 point for "Meaningful Daily Activity"

**C13.** Are you able to take care of basic needs (bathing, clothes, food, water)? (Yes/No/Refused)

**Scoring:** If No → 1 point for "Self-Care"

**C14.** Is your homelessness caused by relationship breakdown or abuse? (Yes/No/Refused)

**Scoring:** If Yes → 1 point for "Social Relationships"

**Total Section C Score:** 0-4 points

---

### SECTION D: WELLNESS (Need to Build)
Location: `frontend/app/assessment/SectionD_Wellness.tsx`

**Questions:**

**Physical Health (6 questions → 1 point max if ANY yes)**

**D15.** Had to leave housing due to physical health? (Yes/No/Refused)

**D16.** Chronic health issues (liver, kidneys, stomach, lungs, heart)? (Yes/No/Refused)

**D17.** Would HIV/AIDS program interest you? (Yes/No/Refused)

**D18.** Physical disabilities that limit housing or independence? (Yes/No/Refused)

**D19.** Do you avoid getting help when sick? (Yes/No/Refused)

**D20.** Are you currently pregnant? (Yes/No/N/A) *Female only*

**Scoring:** If ANY D15-D20 = Yes → 1 point for "Physical Health"

**Substance Use (2 questions → 1 point max if ANY yes)**

**D21.** Has drinking/drug use gotten you kicked out before? (Yes/No/Refused)

**D22.** Will drinking/drug use make staying housed difficult? (Yes/No/Refused)

**Scoring:** If D21=Yes OR D22=Yes → 1 point for "Substance Use"

**Mental Health (4 questions → 1 point max if ANY yes)**

**D23a.** Trouble maintaining housing due to mental health? (Yes/No/Refused)

**D23b.** Trouble maintaining housing due to head injury? (Yes/No/Refused)

**D23c.** Trouble maintaining housing due to learning disability? (Yes/No/Refused)

**D24.** Mental health/brain issues that require help to live independently? (Yes/No/Refused)

**Scoring:** If ANY D23a-D24 = Yes → 1 point for "Mental Health"

**Tri-Morbidity Bonus**

**Scoring:** If Physical Health=1 AND Substance Use=1 AND Mental Health=1 → +1 bonus point

**Medications (2 questions → 1 point max if ANY yes)**

**D25.** Doctor said take medications but you're not taking them? (Yes/No/Refused)

**D26.** Taking painkillers wrong or selling medications? (Yes/No/Refused)

**Scoring:** If D25=Yes OR D26=Yes → 1 point for "Medications"

**Abuse & Trauma (1 question)**

**D27.** Is your homelessness caused by emotional, physical, sexual abuse or trauma? (Yes/No/Refused)

**Scoring:** If Yes → 1 point

**Total Section D Score:** 0-6 points (includes tri-morbidity bonus)

---

### SECTION E: CONTACT INFO (Need to Build)
Location: `frontend/app/assessment/SectionE_Contact.tsx`

**Questions (Non-scored):**

1. Where is easiest to find you and what time? (Place + Time)
2. Phone number where we can reach you? (Optional)
3. Email where we can reach you? (Optional)
4. May we take your photo for ID verification? (Yes/No/Refused)

---

## SCORING LOGIC

Create: `frontend/lib/scoring.ts`

```typescript
interface AssessmentData {
  // Section A
  sleepingLocation: string;
  lengthHomeless: string;
  homelessEpisodes: number | string;
  
  // Section B
  erVisits: number;
  ambulance: number;
  hospitalized: number;
  crisisServices: number;
  policeInteractions: number;
  incarceration: number;
  attacked: boolean;
  selfHarm: boolean;
  legalIssues: boolean;
  forced: boolean;
  riskyBehaviors: boolean;
  
  // Section C
  oweMoney: boolean;
  hasIncome: boolean;
  meaningfulActivities: boolean;
  selfCare: boolean;
  relationshipCause: boolean;
  
  // Section D
  physicalHealthEviction: boolean;
  chronicHealth: boolean;
  hivAidsInterest: boolean;
  physicalDisability: boolean;
  avoidsHelp: boolean;
  pregnant: boolean | null;
  substanceEviction: boolean;
  substanceHousingDifficulty: boolean;
  mentalHealthEviction: boolean;
  headInjury: boolean;
  learningDisability: boolean;
  mentalHealthNeed: boolean;
  notTakingMeds: boolean;
  misusingMeds: boolean;
  abuseTrauma: boolean;
}

export function calculateScore(data: AssessmentData) {
  let totalScore = 0;
  let sectionScores = {
    presurvey: 0,
    sectionA: 0,
    sectionB: 0,
    sectionC: 0,
    sectionD: 0
  };
  
  // PRESURVEY: Age check (if 60+ → 1 point)
  // Note: Would need DOB from initial form
  
  // SECTION A
  const notShelter = !['shelters', 'transitional', 'safe-haven'].includes(data.sleepingLocation);
  if (notShelter) sectionScores.sectionA += 1;
  
  // Check chronicity: 1+ consecutive years OR 4+ episodes
  const episodes = typeof data.homelessEpisodes === 'number' ? data.homelessEpisodes : 0;
  const lengthYears = parseFloat(data.lengthHomeless) || 0;
  if (lengthYears >= 1 || episodes >= 4) sectionScores.sectionA += 1;
  
  // SECTION B
  const emergencyTotal = 
    (data.erVisits || 0) + 
    (data.ambulance || 0) + 
    (data.hospitalized || 0) + 
    (data.crisisServices || 0) + 
    (data.policeInteractions || 0) + 
    (data.incarceration || 0);
  if (emergencyTotal >= 4) sectionScores.sectionB += 1;
  
  if (data.attacked || data.selfHarm) sectionScores.sectionB += 1;
  if (data.legalIssues) sectionScores.sectionB += 1;
  if (data.forced || data.riskyBehaviors) sectionScores.sectionB += 1;
  
  // SECTION C
  if (data.oweMoney || !data.hasIncome) sectionScores.sectionC += 1;
  if (!data.meaningfulActivities) sectionScores.sectionC += 1;
  if (!data.selfCare) sectionScores.sectionC += 1;
  if (data.relationshipCause) sectionScores.sectionC += 1;
  
  // SECTION D
  let physicalHealth = 0, substanceUse = 0, mentalHealth = 0;
  
  if (data.physicalHealthEviction || data.chronicHealth || data.hivAidsInterest || 
      data.physicalDisability || data.avoidsHelp || data.pregnant) {
    physicalHealth = 1;
    sectionScores.sectionD += 1;
  }
  
  if (data.substanceEviction || data.substanceHousingDifficulty) {
    substanceUse = 1;
    sectionScores.sectionD += 1;
  }
  
  if (data.mentalHealthEviction || data.headInjury || 
      data.learningDisability || data.mentalHealthNeed) {
    mentalHealth = 1;
    sectionScores.sectionD += 1;
  }
  
  // Tri-morbidity bonus
  if (physicalHealth === 1 && substanceUse === 1 && mentalHealth === 1) {
    sectionScores.sectionD += 1;
  }
  
  if (data.notTakingMeds || data.misusingMeds) sectionScores.sectionD += 1;
  if (data.abuseTrauma) sectionScores.sectionD += 1;
  
  // Calculate total
  totalScore = Object.values(sectionScores).reduce((a, b) => a + b, 0);
  
  // Determine recommendation
  let recommendation = '';
  if (totalScore >= 0 && totalScore <= 3) {
    recommendation = 'No housing intervention';
  } else if (totalScore >= 4 && totalScore <= 7) {
    recommendation = 'Assessment for Rapid Re-Housing';
  } else {
    recommendation = 'Assessment for Permanent Supportive Housing/Housing First';
  }
  
  return {
    totalScore,
    sectionScores,
    recommendation,
    maxScore: 17
  };
}
```

---

## COMPONENT REQUIREMENTS

### Common Requirements for ALL Components:

1. **Mobile-First Design** - Test on 375px width minimum
2. **Tailwind CSS** - No custom CSS, only Tailwind utility classes
3. **TypeScript** - Full type safety with interfaces
4. **Accessibility** - WCAG 2.1 AA compliant
   - ARIA labels on all inputs
   - Keyboard navigation
   - Focus states
   - Screen reader friendly
5. **Auto-save** - Save to localStorage after each answer
6. **Progress Indicator** - Show current section/total sections
7. **Navigation** - Back/Next buttons, validate before proceeding
8. **"Refused" Option** - Every question must have "Prefer not to answer"
9. **Error Handling** - Clear validation messages
10. **Clean Code** - Comments explaining VI-SPDAT scoring rules

### Specific Component Patterns:

**For Yes/No Questions:**
```tsx
<div className="space-y-3">
  <div className="flex items-center">
    <input type="radio" id="q-yes" value="yes" className="h-4 w-4" />
    <label htmlFor="q-yes" className="ml-3">Yes</label>
  </div>
  <div className="flex items-center">
    <input type="radio" id="q-no" value="no" className="h-4 w-4" />
    <label htmlFor="q-no" className="ml-3">No</label>
  </div>
  <div className="flex items-center">
    <input type="radio" id="q-refused" value="refused" className="h-4 w-4" />
    <label htmlFor="q-refused" className="ml-3">Prefer not to answer</label>
  </div>
</div>
```

**For Number Inputs:**
```tsx
<input
  type="number"
  min="0"
  placeholder="Enter number..."
  className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
/>
```

---

## WHAT I NEED YOU TO GENERATE

### PRIORITY 1: Remaining Assessment Components

1. **SectionB_Risks.tsx** - Complete component with all B4-B9 questions
2. **SectionC_DailyFunctioning.tsx** - Complete component with C10-C14
3. **SectionD_Wellness.tsx** - Complete component with D15-D27
4. **SectionE_Contact.tsx** - Contact info collection (non-scored)

### PRIORITY 2: Results Page

5. **results/page.tsx** - Display score, recommendation, breakdown by section

### PRIORITY 3: Dashboard

6. **dashboard/page.tsx** - List all assessments with filters
7. **dashboard/[id]/page.tsx** - View single assessment details

### PRIORITY 4: Utilities

8. **lib/types.ts** - All TypeScript interfaces
9. **lib/storage.ts** - LocalStorage helpers
10. **components/assessment/ProgressBar.tsx** - Reusable progress indicator

---

## DESIGN SPECIFICATIONS

### Colors
- Primary: Blue-600 (#2563eb)
- Secondary: Green-600 (#16a34a)
- Background: Gray-50 (#f9fafb)
- Cards: White with shadow-sm
- Text: Gray-900 (headings), Gray-700 (body), Gray-500 (helper text)
- Error: Red-600 (#dc2626)

### Typography
- Headings: font-bold, text-2xl (Section titles)
- Questions: font-medium, text-lg
- Body: text-base (16px)
- Helper text: text-sm (14px)
- Use system fonts (no custom fonts)

### Spacing
- Page padding: py-8 px-4 sm:px-6 lg:px-8
- Card padding: p-6
- Section gaps: space-y-6
- Button gaps: gap-4

### Components
- Cards: rounded-lg shadow-sm
- Buttons: rounded-md with hover states
- Inputs: rounded-md with focus:ring-2 focus:ring-blue-500
- Progress bar: rounded-full h-2

---

## EXAMPLE: What Section A Looks Like (Reference)

```tsx
// This is what you're replicating for B, C, D, E
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
  onNext, onBack, initialData = {}, currentStep, totalSteps
}) => {
  // Component code... (see existing file)
};
```

---

## CRITICAL RULES

1. **EXACT VI-SPDAT QUESTIONS** - Use the exact wording I provided above
2. **EXACT SCORING RULES** - Follow the scoring logic exactly
3. **NO MODIFICATIONS** - This is a federally-mandated tool, don't change it
4. **MOBILE-FIRST** - Must work perfectly on phones
5. **ACCESSIBILITY** - This is for vulnerable populations, must be accessible
6. **AUTO-SAVE** - People may lose connection, save progress constantly
7. **CLEAR UI** - Confused users = bad data = people don't get housing
8. **ONE QUESTION VISIBLE AT A TIME ON MOBILE** - Don't overwhelm users

---

## OUTPUT FORMAT

For each component, provide:

1. **Complete .tsx file** ready to copy-paste
2. **Imports at top** (React, types, etc.)
3. **Interface definitions** for props and data
4. **Component function** with full implementation
5. **Export default** at bottom

Make each file self-contained and production-ready.

---

## GENERATE ALL FILES IN THIS ORDER:

1. SectionB_Risks.tsx
2. SectionC_DailyFunctioning.tsx  
3. SectionD_Wellness.tsx
4. SectionE_Contact.tsx
5. results/page.tsx
6. lib/scoring.ts (complete version)
7. lib/types.ts
8. dashboard/page.tsx (simplified for demo)

---

## ADDITIONAL CONTEXT

This is for people experiencing homelessness in Long Beach. Many will:
- Access via smartphone (not desktop)
- Have limited education
- Be in crisis/stressed
- Distrust systems
- Need clear, respectful language

Use:
- Simple language
- Encouraging tone
- Clear instructions
- Visible progress
- Easy navigation
- Non-judgmental wording

Avoid:
- Jargon
- Long paragraphs
- Tiny text
- Hidden options
- Confusing navigation
- Shame/blame language

---

## SUCCESS CRITERIA

When you're done, I should be able to:

1. Copy all files into my Next.js project
2. Run `npm run dev`
3. Navigate to `/assessment`
4. Complete all 5 sections on my phone
5. See my score and recommendation
6. View the assessment in the dashboard

No bugs, no missing pieces, ready to demo on November 15.

---

## BUDGET AWARENESS

This prompt will use approximately 5,000-8,000 tokens for your response. The complete code generation should cost ~$0.50-$1.00 on Vertex AI.

Long Beach contract value: $75,000
Cost to build this MVP: ~$1
ROI: 75,000x

Worth it.

---

## LET'S GO

Generate all the components. Make them beautiful, accessible, and production-ready. 

This is going to change lives in Long Beach.

Build it.
