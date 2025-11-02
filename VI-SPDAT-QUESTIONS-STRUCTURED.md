# VI-SPDAT v2.0 Single Adults - Structured Questions for Development

## SCORING SUMMARY
- **Total Points:** 17
- **Recommendations:**
  - 0-3: No housing intervention
  - 4-7: Assessment for Rapid Re-Housing
  - 8+: Assessment for Permanent Supportive Housing/Housing First

---

## PRE-SURVEY SCORE (1 point max)

### Age Check
**Question:** Date of Birth
**Scoring:** If 60 years or older → Score 1 point
**Field Type:** Date input
**Score Variable:** `presurvey_score`

---

## SECTION A: HISTORY OF HOUSING & HOMELESSNESS (2 points max)

### A1. Current Sleeping Location (1 point max)
**Question:** "Where do you sleep most frequently?"
**Options:**
- Shelters
- Transitional Housing
- Safe Haven
- Outdoors
- Other (specify)
- Refused

**Scoring:** If answer is anything OTHER than "Shelter", "Transitional Housing", or "Safe Haven" → Score 1 point
**Field Type:** Radio buttons
**Score Variable:** `a1_score`

### A2. Length of Current Homelessness
**Question:** "How long has it been since you lived in permanent stable housing?"
**Options:**
- Free text / number input
- Refused

**Field Type:** Text input (duration)
**Score Variable:** N/A (used in A3 calculation)

### A3. Homeless Episodes (1 point max)
**Question:** "In the last three years, how many times have you been homeless?"
**Options:**
- Number input
- Refused

**Scoring:** If experienced 1+ consecutive years of homelessness AND/OR 4+ episodes → Score 1 point
**Field Type:** Number input
**Score Variable:** `a3_score`

**Section A Total:** `presurvey_score + a1_score + a3_score` (max 2 points for section A)

---

## SECTION B: RISKS (4 points max)

### B4. Emergency Service Use (1 point max)
**Question:** "In the past six months, how many times have you..."

**B4a.** "Received health care at an emergency department/room?"
- Number input or Refused

**B4b.** "Taken an ambulance to the hospital?"
- Number input or Refused

**B4c.** "Been hospitalized as an inpatient?"
- Number input or Refused

**B4d.** "Used a crisis service, including sexual assault crisis, mental health crisis, family/intimate violence, distress centers and suicide prevention hotlines?"
- Number input or Refused

**B4e.** "Talked to police because you witnessed a crime, were the victim of a crime, or the alleged perpetrator of a crime or because the police told you that you must move along?"
- Number input or Refused

**B4f.** "Stayed one or more nights in a holding cell, jail or prison, whether that was a short-term stay like the drunk tank, a longer stay for a more serious offence, or anything in between?"
- Number input or Refused

**Scoring:** If total interactions (sum of a-f) ≥ 4 → Score 1 point for Emergency Service Use
**Field Type:** Number inputs (6 fields)
**Score Variable:** `b4_score`

### B5-B6. Risk of Harm (1 point max)

**B5.** "Have you been attacked or beaten up since you've become homeless?"
- Yes / No / Refused

**B6.** "Have you threatened to or tried to harm yourself or anyone else in the last year?"
- Yes / No / Refused

**Scoring:** If YES to B5 OR B6 → Score 1 point for Risk of Harm
**Field Type:** Radio buttons (Yes/No/Refused)
**Score Variable:** `b5_b6_score`

### B7. Legal Issues (1 point max)
**Question:** "Do you have any legal stuff going on right now that may result in you being locked up, having to pay fines, or that make it more difficult to rent a place to live?"
- Yes / No / Refused

**Scoring:** If YES → Score 1 point
**Field Type:** Radio buttons
**Score Variable:** `b7_score`

### B8-B9. Risk of Exploitation (1 point max)

**B8.** "Does anybody force or trick you to do things that you do not want to do?"
- Yes / No / Refused

**B9.** "Do you ever do things that may be considered to be risky like exchange sex for money, run drugs for someone, have unprotected sex with someone you don't know, share a needle, or anything like that?"
- Yes / No / Refused

**Scoring:** If YES to B8 OR B9 → Score 1 point for Risk of Exploitation
**Field Type:** Radio buttons (Yes/No/Refused)
**Score Variable:** `b8_b9_score`

**Section B Total:** `b4_score + b5_b6_score + b7_score + b8_b9_score` (max 4 points)

---

## SECTION C: SOCIALIZATION & DAILY FUNCTIONING (4 points max)

### C10-C11. Money Management (1 point max)

**C10.** "Is there any person, past landlord, business, bookie, dealer, or government group like the IRS that thinks you owe them money?"
- Yes / No / Refused

**C11.** "Do you get any money from the government, a pension, an inheritance, working under the table, a regular job, or anything like that?"
- Yes / No / Refused

**Scoring:** If YES to C10 OR NO to C11 → Score 1 point for Money Management
**Field Type:** Radio buttons (Yes/No/Refused)
**Score Variable:** `c10_c11_score`

### C12. Meaningful Daily Activity (1 point max)
**Question:** "Do you have planned activities, other than just surviving, that make you feel happy and fulfilled?"
- Yes / No / Refused

**Scoring:** If NO → Score 1 point
**Field Type:** Radio buttons
**Score Variable:** `c12_score`

### C13. Self-Care (1 point max)
**Question:** "Are you currently able to take care of basic needs like bathing, changing clothes, using a restroom, getting food and clean water and other things like that?"
- Yes / No / Refused

**Scoring:** If NO → Score 1 point
**Field Type:** Radio buttons
**Score Variable:** `c13_score`

### C14. Social Relationships (1 point max)
**Question:** "Is your current homelessness in any way caused by a relationship that broke down, an unhealthy or abusive relationship, or because family or friends caused you to become evicted?"
- Yes / No / Refused

**Scoring:** If YES → Score 1 point
**Field Type:** Radio buttons
**Score Variable:** `c14_score`

**Section C Total:** `c10_c11_score + c12_score + c13_score + c14_score` (max 4 points)

---

## SECTION D: WELLNESS (6 points max)

### D15-D20. Physical Health (1 point max)

**D15.** "Have you ever had to leave an apartment, shelter program, or other place you were staying because of your physical health?"
- Yes / No / Refused

**D16.** "Do you have any chronic health issues with your liver, kidneys, stomach, lungs or heart?"
- Yes / No / Refused

**D17.** "If there was space available in a program that specifically assists people that live with HIV or AIDS, would that be of interest to you?"
- Yes / No / Refused

**D18.** "Do you have any physical disabilities that would limit the type of housing you could access, or would make it hard to live independently because you'd need help?"
- Yes / No / Refused

**D19.** "When you are sick or not feeling well, do you avoid getting help?"
- Yes / No / Refused

**D20.** "Are you currently pregnant?" (For female respondents only)
- Yes / No / N/A or Refused

**Scoring:** If YES to ANY of D15-D20 → Score 1 point for Physical Health
**Field Type:** Radio buttons (Yes/No/Refused)
**Score Variable:** `physical_health_score`

### D21-D22. Substance Use (1 point max)

**D21.** "Has your drinking or drug use led you to being kicked out of an apartment or program where you were staying in the past?"
- Yes / No / Refused

**D22.** "Will drinking or drug use make it difficult for you to stay housed or afford your housing?"
- Yes / No / Refused

**Scoring:** If YES to D21 OR D22 → Score 1 point for Substance Use
**Field Type:** Radio buttons (Yes/No/Refused)
**Score Variable:** `substance_use_score`

### D23-D24. Mental Health (1 point max)

**D23.** "Have you ever had trouble maintaining your housing, or been kicked out of an apartment, shelter program or other place you were staying, because of:"

**D23a.** "A mental health issue or concern?"
- Yes / No / Refused

**D23b.** "A past head injury?"
- Yes / No / Refused

**D23c.** "A learning disability, developmental disability, or other impairment?"
- Yes / No / Refused

**D24.** "Do you have any mental health or brain issues that would make it hard for you to live independently because you'd need help?"
- Yes / No / Refused

**Scoring:** If YES to ANY of D23a-D24 → Score 1 point for Mental Health
**Field Type:** Radio buttons (Yes/No/Refused)
**Score Variable:** `mental_health_score`

### Tri-Morbidity Bonus (1 point max)
**Scoring:** If scored 1 for Physical Health AND 1 for Substance Use AND 1 for Mental Health → Score 1 additional point for Tri-Morbidity
**Score Variable:** `tri_morbidity_score`

### D25-D26. Medications (1 point max)

**D25.** "Are there any medications that a doctor said you should be taking that, for whatever reason, you are not taking?"
- Yes / No / Refused

**D26.** "Are there any medications like painkillers that you don't take the way the doctor prescribed or where you sell the medication?"
- Yes / No / Refused

**Scoring:** If YES to D25 OR D26 → Score 1 point for Medications
**Field Type:** Radio buttons (Yes/No/Refused)
**Score Variable:** `medications_score`

### D27. Abuse and Trauma (1 point max)
**Question:** "Has your current period of homelessness been caused by an experience of emotional, physical, psychological, sexual, or other type of abuse, or by any other trauma you have experienced?"
- Yes / No / Refused

**Scoring:** If YES → Score 1 point
**Field Type:** Radio buttons
**Score Variable:** `abuse_trauma_score`

**Section D Total:** `physical_health_score + substance_use_score + mental_health_score + tri_morbidity_score + medications_score + abuse_trauma_score` (max 6 points)

---

## FOLLOW-UP QUESTIONS (Non-Scored)

These questions help with case management but don't affect the VI-SPDAT score:

### Contact Information
1. "On a regular day, where is it easiest to find you and what time of day is easiest to do so?"
   - Place: Text input
   - Time: Time input

2. "Is there a phone number and/or email where someone can safely get in touch with you or leave you a message?"
   - Phone: Phone input
   - Email: Email input

3. "May I take your picture so that it is easier to find you and confirm your identity in the future?"
   - Yes / No / Refused
   - (Optional photo upload)

---

## TOTAL SCORE CALCULATION

```javascript
const totalScore = 
  presurvey_score +           // 0-1
  a1_score +                  // 0-1
  a3_score +                  // 0-1
  b4_score +                  // 0-1
  b5_b6_score +              // 0-1
  b7_score +                  // 0-1
  b8_b9_score +              // 0-1
  c10_c11_score +            // 0-1
  c12_score +                 // 0-1
  c13_score +                 // 0-1
  c14_score +                 // 0-1
  physical_health_score +     // 0-1
  substance_use_score +       // 0-1
  mental_health_score +       // 0-1
  tri_morbidity_score +       // 0-1
  medications_score +         // 0-1
  abuse_trauma_score;         // 0-1

// Total range: 0-17 points

// Recommendation
let recommendation;
if (totalScore >= 0 && totalScore <= 3) {
  recommendation = "No housing intervention";
} else if (totalScore >= 4 && totalScore <= 7) {
  recommendation = "Assessment for Rapid Re-Housing";
} else if (totalScore >= 8) {
  recommendation = "Assessment for Permanent Supportive Housing/Housing First";
}
```

---

## DATA STRUCTURE FOR HMIS COMPATIBILITY

```json
{
  "assessment_id": "uuid",
  "assessment_date": "ISO 8601 datetime",
  "assessment_location": "string",
  "assessor_name": "string",
  "assessor_organization": "string",
  "assessor_type": "Team|Staff|Volunteer",
  
  "client": {
    "first_name": "string",
    "last_name": "string",
    "nickname": "string",
    "date_of_birth": "date",
    "age": "integer",
    "ssn_last_4": "string (optional)",
    "preferred_language": "string",
    "consent_given": "boolean"
  },
  
  "responses": {
    "a1_sleeping_location": "string",
    "a2_length_homeless": "string",
    "a3_homeless_episodes": "integer",
    "b4a_er_visits": "integer",
    "b4b_ambulance": "integer",
    "b4c_hospitalized": "integer",
    "b4d_crisis_services": "integer",
    "b4e_police_interactions": "integer",
    "b4f_incarceration": "integer",
    "b5_attacked": "boolean",
    "b6_self_harm": "boolean",
    "b7_legal_issues": "boolean",
    "b8_forced_actions": "boolean",
    "b9_risky_behaviors": "boolean",
    "c10_owes_money": "boolean",
    "c11_has_income": "boolean",
    "c12_meaningful_activities": "boolean",
    "c13_self_care": "boolean",
    "c14_relationship_cause": "boolean",
    "d15_health_eviction": "boolean",
    "d16_chronic_health": "boolean",
    "d17_hiv_aids_interest": "boolean",
    "d18_physical_disability": "boolean",
    "d19_avoids_health_help": "boolean",
    "d20_pregnant": "boolean|null",
    "d21_substance_eviction": "boolean",
    "d22_substance_housing": "boolean",
    "d23a_mental_health_eviction": "boolean",
    "d23b_head_injury": "boolean",
    "d23c_learning_disability": "boolean",
    "d24_mental_health_need": "boolean",
    "d25_not_taking_meds": "boolean",
    "d26_misusing_meds": "boolean",
    "d27_abuse_trauma": "boolean"
  },
  
  "scores": {
    "presurvey": 0,
    "section_a": 0,
    "section_b": 0,
    "section_c": 0,
    "section_d": 0,
    "total": 0,
    "recommendation": "string"
  },
  
  "contact_info": {
    "best_location": "string",
    "best_time": "string",
    "phone": "string (optional)",
    "email": "string (optional)",
    "photo_consent": "boolean",
    "photo_url": "string (optional)"
  }
}
```

---

## UI/UX NOTES

### Progress Indicator
Show 5 sections:
1. Basic Info
2. Housing History
3. Risks
4. Daily Life
5. Health & Wellness

### Question Flow
- One question per screen on mobile
- Group related questions on desktop
- Show progress bar
- Allow "Back" navigation
- Auto-save after each answer
- "Save & Resume Later" button

### Accessibility
- Clear, plain language
- Screen reader compatible
- High contrast mode
- Large touch targets (mobile)
- Option to skip/refuse any question

### Sensitive Questions
- Domestic violence detection: If D27 = Yes, trigger special handling
- Pregnancy question: Only show if gender = female
- Trauma questions: Include trauma-informed language/support resources

---

## DEVELOPMENT PRIORITY

### Phase 1 (MVP for Demo):
1. ✅ All questions rendered correctly
2. ✅ Scoring algorithm working
3. ✅ Recommendation display
4. ✅ Save/resume functionality
5. ✅ Mobile-responsive

### Phase 2 (Post-Demo):
6. HMIS export format
7. Assessor dashboard
8. Analytics/reporting
9. Print PDF capability
10. Multi-language support

---

**File Created:** November 1, 2025  
**Ready for Development:** YES  
**Use this as your source of truth for building the VI-SPDAT form**
