// Complete VI-SPDAT Scoring Logic

export interface AssessmentData {
  // Basic Info
  dateOfBirth?: string;
  
  // Section A: Housing History
  sleepingLocation: string;
  sleepingLocationOther?: string;
  lengthHomeless: string;
  homelessEpisodes: number | string;
  
  // Section B: Risks
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
  
  // Section C: Daily Functioning
  oweMoney: string;
  hasIncome: string;
  meaningfulActivities: string;
  selfCare: string;
  relationshipCause: string;
  
  // Section D: Wellness
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
  
  // Section E: Contact (non-scored)
  bestLocation: string;
  bestTime: string;
  phone: string;
  email: string;
  photoConsent: string;
}

export interface ScoreResult {
  totalScore: number;
  maxScore: number;
  sectionScores: {
    presurvey: number;
    sectionA: number;
    sectionB: number;
    sectionC: number;
    sectionD: number;
  };
  recommendation: string;
  recommendationDescription: string;
  vulnerability: 'low' | 'moderate' | 'high';
}

export function calculateVISPDATScore(data: AssessmentData): ScoreResult {
  let totalScore = 0;
  const sectionScores = {
    presurvey: 0,
    sectionA: 0,
    sectionB: 0,
    sectionC: 0,
    sectionD: 0
  };

  // PRESURVEY: Age check (60+ → 1 point)
  if (data.dateOfBirth) {
    const age = calculateAge(data.dateOfBirth);
    if (age >= 60) {
      sectionScores.presurvey = 1;
    }
  }

  // SECTION A: HOUSING HISTORY (0-2 points)
  
  // A1: Sleeping location (1 point if NOT shelters/transitional/safe haven)
  const shelterOptions = ['shelters', 'transitional', 'safe-haven'];
  if (data.sleepingLocation && !shelterOptions.includes(data.sleepingLocation.toLowerCase())) {
    sectionScores.sectionA += 1;
  }

  // A2+A3: Chronicity check (1 point if 1+ years OR 4+ episodes)
  const episodes = typeof data.homelessEpisodes === 'number' ? data.homelessEpisodes : parseInt(String(data.homelessEpisodes)) || 0;
  const lengthYears = parseYearsFromString(data.lengthHomeless);
  
  if (lengthYears >= 1 || episodes >= 4) {
    sectionScores.sectionA += 1;
  }

  // SECTION B: RISKS (0-4 points)
  
  // B4: Emergency service use (1 point if total >= 4)
  const emergencyTotal = 
    (Number(data.erVisits) || 0) +
    (Number(data.ambulance) || 0) +
    (Number(data.hospitalized) || 0) +
    (Number(data.crisisServices) || 0) +
    (Number(data.policeInteractions) || 0) +
    (Number(data.incarceration) || 0);
  
  if (emergencyTotal >= 4) {
    sectionScores.sectionB += 1;
  }

  // B5+B6: Risk of harm (1 point if either yes)
  if (data.attacked === 'yes' || data.selfHarm === 'yes') {
    sectionScores.sectionB += 1;
  }

  // B7: Legal issues (1 point if yes)
  if (data.legalIssues === 'yes') {
    sectionScores.sectionB += 1;
  }

  // B8+B9: Risk of exploitation (1 point if either yes)
  if (data.forced === 'yes' || data.riskyBehaviors === 'yes') {
    sectionScores.sectionB += 1;
  }

  // SECTION C: DAILY FUNCTIONING (0-4 points)
  
  // C10+C11: Money management (1 point if owes money OR no income)
  if (data.oweMoney === 'yes' || data.hasIncome === 'no') {
    sectionScores.sectionC += 1;
  }

  // C12: Meaningful activities (1 point if no)
  if (data.meaningfulActivities === 'no') {
    sectionScores.sectionC += 1;
  }

  // C13: Self-care (1 point if no)
  if (data.selfCare === 'no') {
    sectionScores.sectionC += 1;
  }

  // C14: Relationship cause (1 point if yes)
  if (data.relationshipCause === 'yes') {
    sectionScores.sectionC += 1;
  }

  // SECTION D: WELLNESS (0-6 points)
  
  let physicalHealthPoint = 0;
  let substanceUsePoint = 0;
  let mentalHealthPoint = 0;

  // D15-D20: Physical health (1 point if ANY yes)
  if (
    data.physicalHealthEviction === 'yes' ||
    data.chronicHealth === 'yes' ||
    data.hivAidsInterest === 'yes' ||
    data.physicalDisability === 'yes' ||
    data.avoidsHelp === 'yes' ||
    data.pregnant === 'yes'
  ) {
    physicalHealthPoint = 1;
    sectionScores.sectionD += 1;
  }

  // D21+D22: Substance use (1 point if either yes)
  if (data.substanceEviction === 'yes' || data.substanceHousingDifficulty === 'yes') {
    substanceUsePoint = 1;
    sectionScores.sectionD += 1;
  }

  // D23+D24: Mental health (1 point if ANY yes)
  if (
    data.mentalHealthEviction === 'yes' ||
    data.headInjury === 'yes' ||
    data.learningDisability === 'yes' ||
    data.mentalHealthNeed === 'yes'
  ) {
    mentalHealthPoint = 1;
    sectionScores.sectionD += 1;
  }

  // Tri-morbidity bonus (1 point if all three: physical + substance + mental)
  if (physicalHealthPoint === 1 && substanceUsePoint === 1 && mentalHealthPoint === 1) {
    sectionScores.sectionD += 1;
  }

  // D25+D26: Medications (1 point if either yes)
  if (data.notTakingMeds === 'yes' || data.misusingMeds === 'yes') {
    sectionScores.sectionD += 1;
  }

  // D27: Abuse and trauma (1 point if yes)
  if (data.abuseTrauma === 'yes') {
    sectionScores.sectionD += 1;
  }

  // Calculate total score
  totalScore = Object.values(sectionScores).reduce((sum, score) => sum + score, 0);

  // Determine recommendation
  let recommendation = '';
  let recommendationDescription = '';
  let vulnerability: 'low' | 'moderate' | 'high' = 'low';

  if (totalScore >= 0 && totalScore <= 3) {
    recommendation = 'No Housing Intervention';
    recommendationDescription = 'You may benefit from prevention services and community resources.';
    vulnerability = 'low';
  } else if (totalScore >= 4 && totalScore <= 7) {
    recommendation = 'Rapid Re-Housing Assessment';
    recommendationDescription = 'You may be eligible for short to medium-term rental assistance with supportive services.';
    vulnerability = 'moderate';
  } else {
    recommendation = 'Permanent Supportive Housing Assessment';
    recommendationDescription = 'You may be eligible for long-term housing with ongoing supportive services (Housing First model).';
    vulnerability = 'high';
  }

  return {
    totalScore,
    maxScore: 17,
    sectionScores,
    recommendation,
    recommendationDescription,
    vulnerability
  };
}

// Helper function to calculate age from date of birth
function calculateAge(dateOfBirth: string): number {
  const today = new Date();
  const birthDate = new Date(dateOfBirth);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  
  return age;
}

// Helper function to parse years from text like "2 years", "18 months", "6 weeks"
function parseYearsFromString(text: string): number {
  if (!text) return 0;
  
  const lowerText = text.toLowerCase();
  
  // Look for year patterns
  const yearMatch = lowerText.match(/(\d+)\s*(year|yr)/);
  if (yearMatch) {
    return parseInt(yearMatch[1]);
  }
  
  // Look for month patterns
  const monthMatch = lowerText.match(/(\d+)\s*(month|mo)/);
  if (monthMatch) {
    return parseInt(monthMatch[1]) / 12;
  }
  
  // Look for week patterns
  const weekMatch = lowerText.match(/(\d+)\s*(week|wk)/);
  if (weekMatch) {
    return parseInt(weekMatch[1]) / 52;
  }
  
  return 0;
}

// Helper to get score color
export function getScoreColor(score: number): string {
  if (score <= 3) return 'text-green-600';
  if (score <= 7) return 'text-yellow-600';
  return 'text-red-600';
}

// Helper to get vulnerability badge color
export function getVulnerabilityColor(vulnerability: 'low' | 'moderate' | 'high'): string {
  switch (vulnerability) {
    case 'low':
      return 'bg-green-100 text-green-800';
    case 'moderate':
      return 'bg-yellow-100 text-yellow-800';
    case 'high':
      return 'bg-red-100 text-red-800';
  }
}
