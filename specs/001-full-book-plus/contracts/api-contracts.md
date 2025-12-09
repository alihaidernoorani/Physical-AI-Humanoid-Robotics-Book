# API Contracts: Interactive Physical AI & Humanoid Robotics Textbook

## Authentication API Contract

### better-auth Client Interface
```
Interface: AuthClient
Methods:
  - signIn(): Promise<AuthResult>
  - signOut(): Promise<void>
  - getSession(): Promise<UserSession | null>
  - createUser(profile: UserProfileInput): Promise<CreateResult>
```

### User Profile API
```
Endpoint: /api/profile (client-side only via localStorage)
Methods:
  - GET /profile -> UserProfile
  - POST /profile -> CreateResult
  - PUT /profile -> UpdateResult
  - DELETE /profile -> DeleteResult

Input: UserProfileInput
{
  "softwareExperience": "Beginner" | "Intermediate" | "Advanced",
  "hardwareSetup": string,
  "learningStyle": string
}

Output: UserProfile
{
  "id": string,
  "softwareExperience": "Beginner" | "Intermediate" | "Advanced",
  "hardwareSetup": string,
  "learningStyle": string,
  "createdAt": string,
  "updatedAt": string
}
```

## Translation API Contract

### LibreTranslate Integration
```
Interface: TranslationService
Methods:
  - translate(content: string, sourceLang: string, targetLang: string): Promise<TranslationResult>
  - isAvailable(): Promise<boolean>

Input: TranslationRequest
{
  "q": string,           // Text to translate
  "source": string,      // Source language code (e.g., "en")
  "target": string,      // Target language code (e.g., "ur")
  "format": "text"       // Content format
}

Output: TranslationResult
{
  "translatedText": string,
  "detectedSourceLanguage": string,
  "success": boolean,
  "error": string | null
}
```

### Urdu Translation Skill Interface
```
Interface: UrduTranslationSkill
Methods:
  - translate(text: string): Promise<UrduTranslationResult>
  - getSupportedLanguages(): string[]
  - isReady(): boolean

Input: UrduTranslationInput
{
  "text": string,
  "chapterId": string
}

Output: UrduTranslationResult
{
  "urduText": string,
  "rtlLayout": boolean,
  "success": boolean,
  "error": string | null,
  "cached": boolean
}
```

## Personalization API Contract

### Content Personalization Interface
```
Interface: PersonalizationService
Methods:
  - getPersonalizedContent(chapterId: string, profile: UserProfile): Promise<PersonalizedContent>
  - updateSettings(settings: PersonalizationSettings): Promise<UpdateResult>

Input: PersonalizationSettings
{
  "userId": string,
  "contentDepth": "Basic" | "Intermediate" | "Advanced",
  "examplePreference": "Simple" | "Complex" | "Mixed"
}

Output: PersonalizedContent
{
  "content": string,
  "adjustedDepth": "Basic" | "Intermediate" | "Advanced",
  "modifiedSections": string[],
  "success": boolean,
  "error": string | null
}
```

## UI Component API Contracts

### Personalization Button Component
```
Component: PersonalizationButton
Props:
  - profile: UserProfile | null
  - onProfileUpdate: (profile: UserProfile) => void
  - disabled: boolean
  - className: string

Events:
  - onPersonalizationToggle: (enabled: boolean) => void
  - onSettingsChange: (settings: PersonalizationSettings) => void
```

### Urdu Translation Button Component
```
Component: UrduTranslationButton
Props:
  - chapterId: string
  - isTranslated: boolean
  - isLoading: boolean
  - disabled: boolean
  - className: string

Events:
  - onTranslationStart: () => void
  - onTranslationComplete: (result: UrduTranslationResult) => void
  - onTranslationError: (error: string) => void
```

### User Profile Modal Component
```
Component: UserProfileModal
Props:
  - isOpen: boolean
  - onClose: () => void
  - onSubmit: (profile: UserProfileInput) => Promise<void>
  - profile: UserProfile | null

Events:
  - onProfileSubmit: (profile: UserProfileInput) => Promise<void>
  - onProfileCancel: () => void
```

## Data Storage Contracts

### localStorage Schema
```
Storage Key: better-auth.user-session
Value: {
  "user": {
    "id": string,
    "email": string,
    "createdAt": string
  },
  "expiresAt": string
}

Storage Key: textbook.user-profile
Value: {
  "id": string,
  "softwareExperience": "Beginner" | "Intermediate" | "Advanced",
  "hardwareSetup": string,
  "learningStyle": string,
  "createdAt": string,
  "updatedAt": string
}

Storage Key: textbook.personalization-settings
Value: {
  "userId": string,
  "contentDepth": "Basic" | "Intermediate" | "Advanced",
  "examplePreference": "Simple" | "Complex" | "Mixed",
  "updatedAt": string
}

Storage Key: textbook.translation-cache
Value: {
  "chapterId": {
    "originalHash": string,
    "translatedContent": string,
    "lastTranslatedAt": string
  }
}
```

## Error Handling Contracts

### Standard Error Format
```
Error Object:
{
  "code": string,        // Error code (e.g., "AUTH_ERROR", "TRANSLATION_FAILED")
  "message": string,     // Human-readable error message
  "details": any,        // Additional error details
  "timestamp": string    // When error occurred
}
```

### Expected Error Codes
- AUTH_ERROR: Authentication-related failures
- PROFILE_NOT_FOUND: User profile not available
- TRANSLATION_FAILED: Translation service unavailable
- NETWORK_ERROR: Network connectivity issues
- STORAGE_ERROR: localStorage access issues
- VALIDATION_ERROR: Input validation failures