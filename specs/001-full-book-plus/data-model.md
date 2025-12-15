# Data Model: Interactive Physical AI & Humanoid Robotics Textbook

## Entities

### Learner Profile
**Description**: User's background information stored in localStorage
**Fields**:
- `id` (string): Unique identifier for the profile
- `softwareExperience` (string): "Beginner", "Intermediate", or "Advanced"
- `hardwareSetup` (string): Hardware configuration (e.g., "Jetson Orin", "RTX GPU", "Other")
- `learningStyle` (string): Learning preference (e.g., "Visual", "Text-based", "Hands-on")
- `createdAt` (timestamp): Profile creation date
- `updatedAt` (timestamp): Last profile update

**Validation Rules**:
- All fields are required
- `softwareExperience` must be one of the predefined values
- `hardwareSetup` must be non-empty string
- `learningStyle` must be one of the predefined values

### Personalization Settings
**Description**: Configuration that adjusts content depth based on user profile
**Fields**:
- `profileId` (string): Reference to Learner Profile
- `contentDepth` (string): "Basic", "Intermediate", or "Advanced"
- `examplePreference` (string): Type of examples to show based on profile
- `updatedAt` (timestamp): Last settings update

**Validation Rules**:
- `profileId` must reference an existing Learner Profile
- `contentDepth` must be one of the predefined values

### Translation State
**Description**: Current translation status for a chapter
**Fields**:
- `chapterId` (string): Identifier for the textbook chapter
- `isTranslated` (boolean): Whether Urdu translation is active
- `translationCache` (object): Cached Urdu content to avoid repeated API calls
- `lastTranslatedAt` (timestamp): When translation was last requested

**Validation Rules**:
- `chapterId` must be a valid chapter identifier
- `translationCache` must contain valid Urdu text if `isTranslated` is true

## Relationships

- **Learner Profile** → **Personalization Settings** (1:1)
  - Each profile has one set of personalization settings
- **Learner Profile** → **Translation State** (1:Many)
  - Each profile can have translation states for multiple chapters

## State Transitions

### Learner Profile
- **Unregistered** → **Profile Created** (when user completes signup modal)
- **Profile Created** → **Profile Updated** (when user modifies preferences)

### Translation State
- **English** → **Translating** (when user clicks Urdu button)
- **Translating** → **Translated** (when API call succeeds)
- **Translated** → **English** (when user switches back)
- **Translating** → **Error** (when API call fails)

## Data Flow

1. User completes signup modal → Learner Profile created in localStorage
2. User navigates to chapter → Translation State initialized for chapter
3. User clicks personalization button → Personalization Settings applied to content rendering
4. User clicks Urdu translation button → Translation State updated and API called
5. API returns Urdu content → Content rendered with RTL layout