# Rule Assistant Development Roadmap

**Document Version:** 1.0
**Date:** November 22, 2025
**Project:** FLExTrans
**Author:** Development Team

---

## 1. Executive Summary

### 1.1 Current State of Rule Assistant

The Rule Assistant is a core feature of FLExTrans that enables linguists to create Apertium transfer rules through a graphical interface, bridging the gap between linguistic expertise and machine translation implementation. As of version 3.14.4 (October 2025), the system provides:

**Core Capabilities:**
- **Automated Rule Generation:** Converts linguist-friendly rule specifications into Apertium transfer XML
- **Morphological Handling:** Supports prefix and suffix operations with feature-based agreement
- **Split Feature Support:** Specialized handling for Bantu-style noun class systems (split by number)
- **Rule Permutation:** Automatic generation of rule variants for different word orderings
- **Live Testing:** Interactive rule tester for immediate feedback
- **Multilingual Interface:** Localization support (English, German, Spanish)
- **Database Integration:** Direct access to FLEx morphological and lexical data

**Technical Architecture:**
- Python-based rule generation engine (`CreateApertiumRules.py`)
- GUI front-end for rule specification
- Integration with Apertium transfer rule system
- Test data generation from source texts

**Known Limitations:**
- **Morphological Coverage:** No support for infixes, circumfixes, or templatic morphology
- **Phonological Processing:** No phonological rule application
- **Suppletion:** No handling of suppletive forms
- **Macro Reuse:** Multi-source macro reuse disabled (Issue #661)
- **Code Debt:** Several TODOs and incomplete error handling

### 1.2 Vision for Feature Completeness

The Rule Assistant should become a **comprehensive linguistic rule authoring system** that:

1. **Handles the Full Range of Morphological Phenomena**
   - All affix types (prefix, suffix, infix, circumfix)
   - Templatic morphology (e.g., Semitic root-and-pattern systems)
   - Reduplication (full, partial, CV patterns)
   - Suppletion and stem alternations

2. **Integrates Phonological Processing**
   - Phonological rule application at morpheme boundaries
   - Tone and vowel harmony systems
   - Sandhi and liaison phenomena

3. **Provides Superior User Experience**
   - Interactive debugging with step-by-step rule execution
   - Rich visual feedback and error diagnostics
   - Comprehensive rule library with language-specific templates
   - "Wizard" interfaces for common rule patterns

4. **Ensures Production Readiness**
   - Robust error handling and validation
   - Performance optimization for large rule sets
   - Comprehensive documentation and tutorials
   - Automated testing infrastructure

### 1.3 Key Milestones

| Phase | Timeline | Primary Deliverable | Impact |
|-------|----------|---------------------|--------|
| **Phase 1:** Critical Technical Debt | 1-2 months | Stable, maintainable codebase | Foundation for future development |
| **Phase 2:** Core Linguistic Features | 3-6 months | Infix/circumfix support, phonology hooks | Expands language coverage significantly |
| **Phase 3:** Usability Enhancements | 2-4 months | Interactive debugger, rule library | Improves linguist productivity |
| **Phase 4:** Advanced Linguistics | 6-12 months | Reduplication, templatic morphology | Enables complex language pairs |

**Total Estimated Timeline:** 12-24 months for full feature completeness

---

## 2. Phased Development Plan

### Phase 1: Critical Technical Debt (1-2 months)

**Objective:** Establish a solid, maintainable foundation by addressing technical debt and known issues.

#### 2.1.1 Fix Outstanding TODO Items

**Task 1.1: Complete Affix Tag Generation (CreateApertiumRules.py:233)**
- **Current State:** TODO comment indicates incomplete implementation for generating category definitions with affix constraints
- **Required Work:**
  - Implement `GetCategoryName()` logic to handle affix features in tag generation
  - Ensure proper permutation of affix tags alongside stem features
  - Add unit tests for various affix+feature combinations
- **Estimated Effort:** 3-5 days
- **Dependencies:** None
- **Success Metric:** All category definitions with affixes generate complete tag lists

**Task 1.2: Refactor Variable Naming in GetMultiFeatureMacro (CreateApertiumRules.py:808)**
- **Current State:** Variable names reference "lemma" even when handling affixes
- **Required Work:**
  - Rename variables to be morphologically neutral (e.g., `destValue`, `sourceValue`)
  - Update comments to clarify dual usage for lemmas and affixes
  - Improve code documentation
- **Estimated Effort:** 2 days
- **Dependencies:** None
- **Success Metric:** Code review confirms clarity; no functional changes

**Task 1.3: Implement Proper Noun Handling (CreateApertiumRules.py:1252)**
- **Current State:** Capitalization logic doesn't check if a word is a proper noun
- **Required Work:**
  - Query FLEx database for proper noun categories
  - Preserve capitalization for proper nouns regardless of position
  - Add configuration option for proper noun handling strategy
- **Estimated Effort:** 4-6 days
- **Dependencies:** FLEx API access for grammatical categories
- **Success Metric:** Proper nouns maintain capitalization; common nouns follow sentence position rules

**Task 1.4: Validate File Mode for Rule Assistant File (CreateApertiumRules.py:1552)**
- **Current State:** TODO indicates uncertainty about file opening mode
- **Required Work:**
  - Verify correct mode ("r" for reading XML)
  - Add explicit encoding specification (UTF-8)
  - Implement proper exception handling with user-friendly error messages
- **Estimated Effort:** 1 day
- **Dependencies:** None
- **Success Metric:** No file encoding errors; clear error messages on file access failures

#### 2.1.2 Re-enable Multi-Source Macro Reuse (Issue #661)

**Background:** Multi-source macro reuse was disabled due to unspecified problems, leading to code duplication and larger transfer files.

**Investigation Phase (Week 1-2):**
- Review Issue #661 in detail to understand root cause
- Analyze current macro generation to identify reuse opportunities
- Test edge cases that may have caused original problems

**Implementation Phase (Week 3-4):**
- Develop improved macro lookup that handles:
  - Different category orderings
  - Partial feature overlap
  - Default value variations
- Add comprehensive unit tests for macro reuse scenarios
- Implement rollback mechanism if issues detected

**Validation Phase (Week 5-6):**
- Test on existing language pairs (especially complex ones)
- Measure transfer file size reduction
- Performance benchmarking

**Estimated Effort:** 4-6 weeks
**Risk:** Medium (may uncover architectural issues)
**Success Metric:** 30-50% reduction in redundant macros; no regression in rule generation

#### 2.1.3 Enhanced Error Messages and Validation

**Task 1.6: Feature Validation Framework**
- **Required Work:**
  - Validate feature names exist in FLEx databases before rule generation
  - Check category compatibility (e.g., don't allow verb features on nouns)
  - Verify match groups have consistent feature usage
  - Implement early validation in GUI before rule saving
- **Estimated Effort:** 2 weeks
- **Success Metric:** 90% of rule errors caught before generation; clear error messages with remediation suggestions

**Task 1.7: Improved Error Reporting**
- **Current State:** Generic error messages; difficult to diagnose issues
- **Required Work:**
  - Add error codes and structured error information
  - Create error message catalog with examples
  - Implement context-aware error messages (show rule name, word ID, feature label)
  - Add "Show More Details" option for technical information
- **Estimated Effort:** 1.5 weeks
- **Success Metric:** User testing shows 80% reduction in time to fix rule errors

**Task 1.8: Rule File Integrity Checks**
- **Required Work:**
  - Validate Rule Assistant XML against schema
  - Check for orphaned match groups
  - Detect circular dependencies
  - Warn about potentially problematic rule patterns
- **Estimated Effort:** 1 week
- **Success Metric:** Zero crashes due to malformed input; helpful warnings for common mistakes

#### 2.1.4 Phase 1 Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Code Quality | Zero TODO comments in critical paths | Code review |
| Test Coverage | >80% for CreateApertiumRules.py | pytest-cov |
| Error Clarity | User testing shows 80% improvement | User survey |
| Macro Efficiency | 30-50% reduction in redundant macros | File size comparison |
| Regression Testing | Zero new bugs introduced | Integration test suite |

---

### Phase 2: Core Linguistic Features (3-6 months)

**Objective:** Expand morphological coverage to handle infix, circumfix, and phonological phenomena.

#### 2.2.1 Infix Support

**Linguistic Background:**
Infixes are affixes inserted within a root morpheme (e.g., Tagalog: *sulat* "write" → *s-um-ulat* "wrote"; English slang: *abso-bloody-lutely*).

**Design Specification:**

**GUI Changes:**
- Add "Infix" option to affix type dropdown
- Infix position specification:
  - After position N (character index)
  - Before position N (from end)
  - After first vowel/consonant
  - Before last vowel/consonant
  - Custom regex pattern for insertion point
- Environment specification for phonologically-conditioned infixes

**Backend Implementation:**
- Extend `FeatureSpec` dataclass with `infixPosition` field
- Modify `GetAttributeMacro` to generate infix insertion logic
- Apertium integration:
  - Use `<clip>` to extract lemma
  - String manipulation in macro to insert infix
  - Handle multiple infixes in single word

**Technical Challenges:**
- Apertium's stream format doesn't natively support infix operations
- Requires custom macro generation with string operations
- May need target-side phonological rules for accurate placement

**Implementation Tasks:**
1. Design FLEx-to-infix-specification mapping (1 week)
2. Extend Rule Assistant XML schema for infixes (1 week)
3. Implement GUI for infix specification (2 weeks)
4. Backend macro generation for infixes (3 weeks)
5. Testing with real language data (Tagalog, Khmer) (2 weeks)

**Estimated Effort:** 9 weeks
**Dependencies:** Phase 1 complete
**Success Metric:** Successfully handle 3+ infix types from different language families

#### 2.2.2 Circumfix Support

**Linguistic Background:**
Circumfixes are simultaneous prefix and suffix (e.g., German: *ge-lauf-t* "run-PAST.PART"; Indonesian: *ke-besar-an* "greatness").

**Design Specification:**

**Key Distinction:** True circumfixes (single morpheme expressed discontinuously) vs. independent prefix+suffix combinations

**GUI Changes:**
- Add "Circumfix" affix type
- Interface to specify:
  - Prefix portion
  - Suffix portion
  - Feature(s) marked by circumfix
  - Conditions for use (phonological, morphological)

**Backend Implementation:**
- Extend affix handling to track paired prefix-suffix
- Ensure atomic treatment (both parts required)
- Handle paradigms with partial circumfix patterns

**Implementation Tasks:**
1. Linguistic research on circumfix typology (1 week)
2. Schema extension for circumfix representation (1 week)
3. GUI implementation (2 weeks)
4. Backend logic for paired affix generation (3 weeks)
5. Testing with German, Indonesian, Berber data (2 weeks)

**Estimated Effort:** 9 weeks
**Dependencies:** Infix support completed
**Success Metric:** Correctly generate circumfix patterns for 3+ languages; handle mixed paradigms

#### 2.2.3 Phonological Rule Hooks

**Linguistic Background:**
Morpheme combinations often trigger phonological changes (assimilation, deletion, insertion, vowel harmony, tone changes).

**Design Specification:**

**Architecture:**
- **Pre-transfer Phonology:** Applied to source before bilingual lookup (STAMP synthesis)
- **Post-transfer Phonology:** Applied to target after transfer rules
- **Morphophonology:** Applied at affix boundaries during generation

**Required Infrastructure:**
- Integration point with FLExTrans phonological rule system
- Rule triggering based on:
  - Morpheme boundaries
  - Feature combinations
  - Phonological environment
- Ordering control (rule application sequence)

**GUI Changes:**
- Checkbox: "Apply phonological rules to this affix"
- Rule selection interface
- Preview of phonological application

**Backend Implementation:**
- Add hooks in `ProcessRule` to call phonological processors
- Pass morphological context to phonological rules
- Handle phonological opacity (counter-feeding, counter-bleeding)

**Implementation Tasks:**
1. Design phonology integration architecture (2 weeks)
2. Create phonological rule specification format (2 weeks)
3. Implement rule application engine (4 weeks)
4. GUI for rule assignment (2 weeks)
5. Testing with vowel harmony (Turkish), assimilation (Korean), tone (Yoruba) (3 weeks)

**Estimated Effort:** 13 weeks
**Dependencies:** Phase 1 complete; consultation with STAMP team
**Risk:** High (complex interaction with existing phonology)
**Success Metric:** Handle 5+ phonological phenomena types correctly

#### 2.2.4 Suppletion Handling

**Linguistic Background:**
Suppletion: morphologically-related forms with completely different stems (*go/went*, *good/better/best*).

**Design Specification:**

**Detection:**
- Query FLEx for allomorph relationships
- Identify suppletive alternations via:
  - Explicit marking in FLEx
  - Heuristic: allomorphs with <50% phonological overlap
  - Manual specification

**GUI Changes:**
- Display suppletive alternations for selection
- Interface to map source suppletion to target suppletion
- Default selection: most frequent form

**Backend Implementation:**
- Extend `GetMultiFeatureMacro` to handle stem selection
- Generate conditionals based on features triggering suppletion
- Fallback to default form when conditions unclear

**Apertium Integration:**
- Add to bilingual dictionary as separate entries
- Transfer rules select correct suppletive form
- Handle partial paradigms (suppletion in some cells only)

**Implementation Tasks:**
1. FLEx allomorph query implementation (2 weeks)
2. Suppletion detection heuristics (2 weeks)
3. GUI for suppletion mapping (2 weeks)
4. Macro generation for form selection (3 weeks)
5. Testing with English, Romance, Bantu languages (2 weeks)

**Estimated Effort:** 11 weeks
**Dependencies:** Multi-feature macro infrastructure (Phase 1.2)
**Success Metric:** Handle irregular paradigms for verbs (go/went) and adjectives (good/better/best)

#### 2.2.5 Advanced Feature Operations

**Objective:** Support complex feature manipulation beyond simple copying.

**Capabilities to Implement:**

**Feature Arithmetic:**
- Person agreement: 1st + 2nd → 1st (French: *nous*)
- Number combination: SG + SG → DUAL or PL
- Definiteness spreading

**Feature Defaults and Overrides:**
- Context-sensitive defaults
- Feature co-occurrence restrictions
- Automatic feature inference

**Feature Hierarchies:**
- Subsumption relationships (MASCULINE ⊂ ANIMATE)
- Feature unification for agreement
- Underspecification handling

**Implementation Tasks:**
1. Design feature operation specification language (2 weeks)
2. Implement feature algebra (3 weeks)
3. GUI for feature operations (3 weeks)
4. Testing with agreement-heavy languages (2 weeks)

**Estimated Effort:** 10 weeks
**Success Metric:** Handle complex agreement patterns (e.g., Swahili noun class concord)

#### 2.2.6 Phase 2 Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Morphological Coverage | Support 90% of affix types in WALS | Linguistic analysis |
| Language Compatibility | Successfully handle 10+ typologically diverse languages | Test suite |
| Phonological Integration | Zero conflicts with existing phonology system | Integration tests |
| Suppletion Accuracy | 95% correct form selection in test paradigms | Automated testing |
| Feature Operations | Handle 20+ complex agreement patterns | Linguist review |

---

### Phase 3: Usability Enhancements (2-4 months)

**Objective:** Improve user experience and productivity through better tools, documentation, and interface improvements.

#### 2.3.1 Interactive Rule Tester/Debugger

**Current State:** Live Rule Tester shows final output but limited insight into rule application process.

**Enhanced Capabilities:**

**Step-Through Debugging:**
- Rule-by-rule execution with pause
- Variable inspection at each step
- Feature value tracking through transfer
- Macro expansion visualization

**Visual Feedback:**
- Highlight which rule matched
- Show pattern matching process
- Display macro internal state
- Animate feature flow between words

**Debugging Tools:**
- Breakpoints on specific rules
- Watch expressions for variables
- Rule execution history/backtrace
- Compare expected vs. actual output

**GUI Design:**
- Multi-pane interface:
  - Source sentence pane
  - Rule list with execution status
  - Variable/feature inspector
  - Output pane with annotations
- Execution controls (step, continue, run to breakpoint)

**Implementation Tasks:**
1. Design debugger architecture (2 weeks)
2. Instrument Apertium for step-through execution (4 weeks)
3. Build debugging GUI (4 weeks)
4. Integrate with existing Live Rule Tester (2 weeks)
5. User testing and refinement (2 weeks)

**Estimated Effort:** 14 weeks
**Dependencies:** Phase 2 completion for full feature coverage
**Success Metric:** User testing shows 60% reduction in time to diagnose rule problems

#### 2.3.2 Rule Library Expansion

**Current State:** Users create rules from scratch; no templates or examples.

**Proposed Library:**

**Rule Templates by Phenomenon:**
- Basic SVO → SOV reordering
- Verb agreement (subject, object, multiple)
- Noun class concord
- Definiteness marking
- Tense/aspect/mood transfer
- Case marking patterns
- Classifier systems

**Language-Specific Collections:**
- Bantu noun class system (expanded beyond current)
- Romance verb conjugation
- Agglutinative verb complexes (Turkish, Finnish)
- Polysynthetic incorporation patterns
- Classifier languages (Chinese, Vietnamese)

**Import and Customization:**
- Browse library by language family or phenomenon
- Preview template before import
- Customize feature mappings
- Merge with existing rules

**Community Contributions:**
- Submit rules to shared repository
- Rating and review system
- Documentation requirements

**Implementation Tasks:**
1. Create initial rule library (30-40 templates) (4 weeks)
2. Build library browser GUI (3 weeks)
3. Implement import/customization workflow (2 weeks)
4. Create contribution platform (3 weeks)
5. Documentation for all templates (3 weeks)

**Estimated Effort:** 15 weeks
**Dependencies:** None (can proceed in parallel)
**Success Metric:** 50% of new projects start from template; 20 community contributions in 6 months

#### 2.3.3 Comprehensive Documentation

**Current State:** Minimal documentation; steep learning curve.

**Documentation Suite:**

**User Guide:**
- Getting started tutorial (step-by-step first rule)
- Concept explanations (match groups, macros, features)
- How-to guides for common tasks
- Troubleshooting guide
- Video tutorials

**Linguistic Guide:**
- Morphological phenomena and how to handle them
- Best practices for specific language types
- Worked examples from published language pairs
- Limitations and workarounds

**Technical Reference:**
- Complete API documentation
- Rule Assistant XML schema documentation
- Generated Apertium code explanation
- Extension points for developers

**Case Studies:**
- 5-10 detailed language pair implementations
- Explanation of linguistic decisions
- Performance considerations
- Lessons learned

**Format and Delivery:**
- Interactive web documentation (e.g., MkDocs)
- PDF user manual
- In-application help (context-sensitive)
- Searchable knowledge base

**Implementation Tasks:**
1. Content planning and structure (1 week)
2. User Guide writing (4 weeks)
3. Linguistic Guide writing (4 weeks)
4. Technical Reference (3 weeks)
5. Case Studies (4 weeks)
6. Video production (3 weeks)
7. Documentation platform setup (2 weeks)

**Estimated Effort:** 21 weeks (overlapping with other tasks)
**Dependencies:** Phase 2 features documented as implemented
**Success Metric:** 80% of user questions answered in documentation; <5% support requests about documented features

#### 2.3.4 GUI Improvements

**Usability Issues to Address:**

**Navigation:**
- Breadcrumb navigation for complex rules
- Quick jump to related elements (e.g., source word → target word)
- Search/filter for features and categories
- Recent items history

**Visual Design:**
- Color coding for different element types
- Icon system for quick recognition
- Consistent spacing and alignment
- Accessibility compliance (WCAG 2.1 AA)

**Input Optimization:**
- Autocomplete for feature names
- Drag-and-drop for word reordering
- Keyboard shortcuts for common actions
- Batch operations (e.g., add same feature to multiple words)

**Validation Feedback:**
- Real-time validation indicators
- Inline error messages
- Suggestion system ("Did you mean...?")
- Warning for potentially problematic patterns

**Implementation Tasks:**
1. UX review and redesign (3 weeks)
2. Implement navigation improvements (2 weeks)
3. Visual refresh (2 weeks)
4. Input optimization (3 weeks)
5. Validation UI (2 weeks)
6. Accessibility audit and fixes (2 weeks)
7. User testing (2 weeks)

**Estimated Effort:** 16 weeks
**Dependencies:** None
**Success Metric:** User satisfaction score >4.0/5.0; task completion time reduced 40%

#### 2.3.5 Phase 3 Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Rule Debugging Speed | 60% faster problem diagnosis | User time studies |
| Template Usage | 50% of projects use templates | Usage analytics |
| Documentation Coverage | 80% of features documented | Documentation review |
| User Satisfaction | >4.0/5.0 rating | User surveys |
| Accessibility | WCAG 2.1 AA compliance | Automated and manual testing |

---

### Phase 4: Advanced Linguistics (6-12 months)

**Objective:** Handle the most complex morphological phenomena to enable MT for understudied and morphologically complex languages.

#### 2.4.1 Reduplication Patterns

**Linguistic Background:**
Reduplication: morphological process where all or part of a word is repeated to convey grammatical or semantic meaning.

**Types to Support:**

**Full Reduplication:**
- Complete stem copying (*Indonesian:* *rumah-rumah* "houses")
- May trigger phonological changes
- Often marks plurality, intensity, distribution

**Partial Reduplication:**
- Initial syllable (*Tagalog:* *bili* "buy" → *bibili* "will buy")
- Final syllable
- CV pattern (consonant-vowel of root)

**Fixed-Segment Reduplication:**
- Specific segments reduplicated regardless of base
- Often involves ablaut or vowel changes

**Semantic Types:**
- Grammatical: pluralization, aspect, mood
- Derivational: intensification, distribution
- Expressive: diminutive, pejorative

**Design Specification:**

**FLEx Integration:**
- Query reduplication patterns from FLEx morphology
- Identify reduplication templates
- Extract phonological constraints

**Rule Specification:**
- Select reduplication type (full, partial, CV)
- Specify copied segment (initial, final, entire)
- Define trigger conditions (features, categories)
- Map source reduplication to target reduplication

**Apertium Implementation:**
- Lexicon: list reduplicated forms or use generation rules
- Transfer: decide when to reduplicate
- Generation: produce correct reduplicated form

**Technical Challenges:**
- Apertium morphological analyzer/generator may not handle reduplication
- Requires integration with STAMP or custom generation
- Variable patterns difficult to encode compactly

**Implementation Tasks:**
1. Survey reduplication types in target languages (3 weeks)
2. Design reduplication specification system (3 weeks)
3. FLEx integration for reduplication queries (4 weeks)
4. GUI for reduplication rule creation (4 weeks)
5. Backend generation (consider STAMP integration) (6 weeks)
6. Testing with Indonesian, Tagalog, Chamorro (3 weeks)

**Estimated Effort:** 23 weeks
**Dependencies:** Phonological rule hooks (Phase 2.2.3)
**Risk:** High (may require STAMP integration or Apertium extension)
**Success Metric:** Handle 5+ reduplication types across 3+ language families

#### 2.4.2 Templatic Morphology

**Linguistic Background:**
Non-concatenative morphology where consonantal roots and vowel patterns combine (common in Semitic, some Cushitic).

**Example (Arabic):**
- Root: K-T-B (semantic core: "writing")
- Pattern CaCaCa + root → *kataba* "he wrote"
- Pattern maCCūC + root → *maktūb* "written"

**Design Specification:**

**Representation:**
- Separate root and pattern/template
- Root: sequence of consonants (or other root radicals)
- Pattern: slots with vowels and derivational affixes
- Mapping rules to combine them

**FLEx Integration:**
- Query root lexical entries
- Extract templates from inflectional paradigms
- Identify binyan/conjugation classes (for Arabic/Hebrew)

**Rule Creation:**
- Specify root in source word
- Map to target root (may differ)
- Select template based on features (binyan, voice, aspect)
- Generate output word

**Apertium Challenges:**
- Stream format assumes concatenative morphology
- May need special pre/post-processing
- Lexicon organization different from standard

**Potential Solutions:**
1. Pre-transfer decomposition: root + pattern → concatenative representation
2. Post-transfer synthesis: features → templatic generation
3. Hybrid: use STAMP for generation, Apertium for transfer logic

**Implementation Tasks:**
1. Research templatic morphology systems (4 weeks)
2. Design root-and-pattern representation (4 weeks)
3. FLEx integration for templatic data (5 weeks)
4. GUI for templatic rules (4 weeks)
5. Backend generation (likely requires STAMP) (8 weeks)
6. Testing with Arabic, Hebrew, Tigrinya (4 weeks)

**Estimated Effort:** 29 weeks
**Dependencies:** STAMP integration; may require STAMP enhancements
**Risk:** Very High (architectural change may be needed)
**Success Metric:** Successfully transfer 1 Semitic language pair with correct templatic morphology

#### 2.4.3 Tone and Vowel Harmony Systems

**Linguistic Background:**

**Tone:**
- Lexical tone (Mandarin: *mā* vs. *má* vs. *mǎ* vs. *mà*)
- Grammatical tone (tone changes for tense/aspect)
- Tone sandhi (tone changes in context)

**Vowel Harmony:**
- Front-back harmony (Turkish, Hungarian)
- ATR harmony (African languages)
- Rounding harmony
- May affect affixes across entire word

**Design Specification:**

**Tone Handling:**
- Represent tone in lexicon (likely already in FLEx)
- Rules to transfer tone patterns
- Tone sandhi rules (phonological)
- Different strategies for tone vs. non-tone target

**Vowel Harmony Handling:**
- Identify harmony feature (front/back, ATR, rounding)
- Determine harmony span (root triggers affix alternation)
- Select correct affix allomorph based on harmony
- Handle disharmonic/neutral elements

**FLEx Integration:**
- Query tone specifications
- Extract harmony rules from affix allomorphy
- Identify harmony domains

**Apertium Integration:**
- Tone: include in tags (may increase lexicon size)
- Harmony: select allomorphs in generation

**Implementation Tasks:**
1. Tone system design (3 weeks)
2. Vowel harmony system design (3 weeks)
3. FLEx integration (4 weeks)
4. GUI for tone/harmony specification (4 weeks)
5. Backend implementation (6 weeks)
6. Testing: Tone (Mandarin, Yoruba); Harmony (Turkish, Finnish) (4 weeks)

**Estimated Effort:** 24 weeks
**Dependencies:** Phonological rule system (Phase 2.2.3)
**Success Metric:** Correct tone transfer for 2 languages; correct harmony for 2 languages

#### 2.4.4 Clause-Level Transformations

**Linguistic Background:**
Transfer rules may need to restructure at clause level, not just word level.

**Phenomena:**

**Argument Structure Changes:**
- Voice alternations (active ↔ passive, applicative, causative)
- Incorporation (noun → verb complex)
- Serial verb constructions

**Word Order Transformations:**
- SVO ↔ SOV, VSO, etc.
- Question formation (movement, particles)
- Topicalization and focus constructions

**Clause Combining:**
- Different complementation strategies
- Relative clause formation
- Coordination vs. subordination

**Design Specification:**

**Extended Pattern Matching:**
- Match across chunks (not just adjacent words)
- Identify syntactic roles (subject, object, oblique)
- Handle discontinuous constituents

**Transformation Operations:**
- Reordering at clause level
- Insertion of functional words (complementizers, auxiliaries)
- Argument addition/deletion
- Clause type conversion

**FLEx Integration:**
- Query for argument structure information
- Access syntactic feature information
- Use interlinear text for pattern discovery

**Apertium Integration:**
- Use chunk-level transfer (interchunk, postchunk)
- Coordinate with word-level transfer
- Potential need for syntactic parsing

**Implementation Tasks:**
1. Survey clause-level phenomena in target languages (4 weeks)
2. Design extended pattern matching system (5 weeks)
3. Implement argument structure transfer (6 weeks)
4. Word order transformation engine (5 weeks)
5. GUI for clause-level rules (5 weeks)
6. Testing with diverse language pairs (4 weeks)

**Estimated Effort:** 29 weeks
**Dependencies:** Advanced Apertium features (interchunk, postchunk)
**Risk:** High (may require significant Apertium expertise)
**Success Metric:** Handle 10+ clause transformation patterns; successful complex language pair (e.g., English-Basque)

#### 2.4.5 Phase 4 Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Morphological Complexity | Handle World Atlas of Language Structures (WALS) max complexity | Linguistic review |
| Reduplication Coverage | 5+ reduplication types, 3+ language families | Test suite |
| Templatic Morphology | 1 successful Semitic language pair | Evaluation |
| Tone/Harmony | 2 tone languages, 2 harmony languages | Evaluation |
| Clause Transformation | 10+ transformation patterns | Linguist review |
| Language Diversity | Successfully handle 25+ typologically diverse languages | Language portfolio |

---

## 3. Resource Requirements

### 3.1 Development Skills Needed

**Core Team Composition:**

**Senior Software Engineer (1 FTE):**
- **Skills:** Python, XML processing, Qt/PyQt, software architecture
- **Responsibilities:**
  - Lead implementation of Phases 1-2
  - Code review and architecture decisions
  - Integration with Apertium and STAMP
- **Critical for:** All phases

**Computational Linguist/NLP Engineer (1 FTE):**
- **Skills:** Morphological analysis, finite-state technology, linguistic typology
- **Responsibilities:**
  - Design linguistic feature specifications
  - Apertium rule generation logic
  - Phonological and morphological algorithms
- **Critical for:** Phases 2, 4

**UI/UX Developer (0.5 FTE):**
- **Skills:** Qt/PyQt GUI development, UX design, accessibility
- **Responsibilities:**
  - GUI enhancements (Phase 3)
  - Debugger interface design
  - Usability testing
- **Critical for:** Phase 3 (can be contracted)

**Technical Writer (0.5 FTE):**
- **Skills:** Documentation, technical writing, video production
- **Responsibilities:**
  - User guide and reference documentation
  - Video tutorial production
  - Case study writing
- **Critical for:** Phase 3 (can be contracted)

**QA/Testing Specialist (0.25 FTE):**
- **Skills:** Software testing, test automation, linguistic data
- **Responsibilities:**
  - Test suite development
  - Regression testing
  - Language data validation
- **Critical for:** All phases

### 3.2 Linguistic Expertise Required

**Consultant Linguists (as needed):**

**Phase 2 Consultants:**
- Tagalog or Austronesian specialist (infix systems)
- Bantu language specialist (expanded noun class work)
- Phonologist (for phonological rule integration)

**Phase 4 Consultants:**
- Semitic language specialist (templatic morphology)
- Tone language specialist (Mandarin, Yoruba, or other)
- Turkic or Uralic specialist (vowel harmony)

**Community Partners:**
- SIL language teams for testing and feedback
- Academic linguists for validation
- Machine translation researchers for evaluation

**Estimated Consulting Budget:** $30,000-50,000 over 24 months

### 3.3 Testing Infrastructure

**Test Data Requirements:**

**Linguistic Test Suites:**
- 25+ language pairs covering diverse phenomena
- Morphological paradigm tables for each language
- Annotated test sentences (100-500 per language)
- Gold standard translations

**Regression Test Suite:**
- Automated tests for all current functionality
- Unit tests for new features
- Integration tests for end-to-end workflows
- Performance benchmarks

**Infrastructure:**
- Continuous Integration (CI) server
- Automated test execution on commit
- Test coverage reporting
- Performance monitoring

**FLEx Test Databases:**
- Representative databases for each language type
- Synthetic databases for edge case testing
- Version control for test databases

**Development Tools:**
- Version control (Git)
- Issue tracking (GitHub Issues or similar)
- Code review system (GitHub Pull Requests)
- Documentation platform (MkDocs, ReadTheDocs)

---

## 4. Risk Assessment

### 4.1 Technical Risks and Mitigation

**Risk 1: Apertium Architectural Limitations**

**Description:** Apertium was designed for concatenative morphology and may not easily support templatic morphology, complex reduplication, or certain phonological processes.

**Probability:** High for Phase 4 advanced features
**Impact:** High - may block implementation of some features

**Mitigation Strategies:**
- Early prototyping with Apertium for non-concatenative phenomena
- Engage Apertium community for advice and potential enhancements
- Consider hybrid approaches (STAMP for generation, Apertium for transfer)
- Design fallback solutions (e.g., expanded lexicons instead of generative rules)
- Budget for potential Apertium contributions/modifications

**Risk 2: FLEx API Stability and Coverage**

**Description:** FLEx API may not expose all needed morphological data, or API may change between versions.

**Probability:** Medium
**Impact:** Medium - may require workarounds or delayed features

**Mitigation Strategies:**
- Engage with FLEx development team early
- Document all API dependencies
- Build abstraction layer to isolate FLEx-specific code
- Participate in FLEx beta testing programs
- Maintain compatibility with multiple FLEx versions

**Risk 3: Performance Degradation with Complex Rules**

**Description:** Advanced features (especially Phase 4) may significantly slow rule generation and application.

**Probability:** Medium
**Impact:** Medium - affects user experience

**Mitigation Strategies:**
- Establish performance benchmarks early
- Profile code regularly to identify bottlenecks
- Implement caching for expensive operations
- Consider lazy evaluation for rule components
- Provide progress indicators for slow operations

**Risk 4: Multi-Source Macro Reuse (Issue #661) Re-emergence**

**Description:** Re-enabling multi-source macro reuse may reintroduce original bugs.

**Probability:** Medium
**Impact:** Medium - affects code quality and file size

**Mitigation Strategies:**
- Thorough investigation before implementation
- Comprehensive test suite for macro generation
- Gradual rollout with feature flag
- Easy rollback mechanism
- Extensive testing on real-world language pairs

### 4.2 Linguistic Risks

**Risk 5: Incomplete Linguistic Typology Coverage**

**Description:** Rare or poorly-documented morphological phenomena may not be anticipated.

**Probability:** High for less-studied languages
**Impact:** Medium - specific languages unsupported

**Mitigation Strategies:**
- Engage with linguistic typology experts
- Build extensible architecture for new phenomena
- Document unsupported phenomena clearly
- Provide workaround suggestions
- Maintain roadmap for future additions

**Risk 6: Over-Specification in Rule Assistant**

**Description:** Attempting to handle all linguistic phenomena may lead to an overly complex, unusable interface.

**Probability:** Medium
**Impact:** High - defeats purpose of "linguist-friendly" tool

**Mitigation Strategies:**
- Iterative UX testing at each phase
- Progressive disclosure (advanced features hidden by default)
- Template library for common patterns
- Wizard interfaces for complex features
- Regular user feedback sessions

### 4.3 Project Management Risks

**Risk 7: Scope Creep**

**Description:** Continuous discovery of new features may delay completion.

**Probability:** High
**Impact:** High - timeline and budget overruns

**Mitigation Strategies:**
- Strict phase boundaries with formal review
- Change request process for new features
- Maintain "future work" list separate from current phases
- Regular stakeholder communication on priorities
- MVP approach within each phase

**Risk 8: Resource Availability**

**Description:** Key personnel may become unavailable (illness, job change, other projects).

**Probability:** Medium
**Impact:** High - delays and knowledge loss

**Mitigation Strategies:**
- Comprehensive documentation of all work
- Pair programming for knowledge sharing
- Code review process ensures multiple people understand each area
- Cross-training team members
- Maintain relationships with potential contractors

**Risk 9: Dependency on External Projects**

**Description:** STAMP, Apertium, or FLEx development may not align with our needs.

**Probability:** Medium
**Impact:** Medium to High depending on dependency

**Mitigation Strategies:**
- Maintain good relationships with external project teams
- Contribute to external projects where possible
- Design with abstraction layers to reduce coupling
- Monitor external project roadmaps
- Budget for potential forking or alternative solutions

### 4.4 Risk Summary Matrix

| Risk | Probability | Impact | Mitigation Priority | Owner |
|------|------------|--------|-------------------|-------|
| Apertium Limitations | High | High | Critical | Computational Linguist |
| FLEx API Issues | Medium | Medium | High | Senior Engineer |
| Performance Issues | Medium | Medium | High | Senior Engineer |
| Macro Reuse Bugs | Medium | Medium | Medium | Senior Engineer |
| Typology Gaps | High | Medium | Medium | Computational Linguist |
| Over-Complexity | Medium | High | High | UI/UX Developer |
| Scope Creep | High | High | Critical | Project Manager |
| Resource Availability | Medium | High | High | Project Manager |
| External Dependencies | Medium | Med-High | High | Senior Engineer |

---

## 5. Success Criteria

### 5.1 How to Measure Feature Completeness

**Quantitative Metrics:**

**Morphological Coverage Index (MCI):**
- Metric: Percentage of WALS morphological feature types supported
- Current baseline: ~40% (concatenative affixation only)
- Phase 2 target: 70% (add infixes, circumfixes, basic phonology)
- Phase 4 target: 90% (add reduplication, templatic, harmony)
- Measurement: Annual linguistic audit against WALS database

**Feature Implementation Completeness (FIC):**
- Metric: Percentage of planned features fully implemented
- Phase targets:
  - Phase 1: 100% (all TODOs resolved, macro reuse working)
  - Phase 2: 100% (all core linguistic features)
  - Phase 3: 100% (all UX enhancements)
  - Phase 4: 80% (some advanced features may be deferred)
- Measurement: Feature checklist review

**Test Coverage:**
- Metric: Percentage of code covered by automated tests
- Target: >80% for CreateApertiumRules.py and core modules
- Measurement: pytest-cov or similar tool

**Qualitative Metrics:**

**Linguistic Validity:**
- Expert review by computational linguists
- Verification against linguistic literature
- Comparison with human-created transfer rules

**Code Quality:**
- Code review approval for all changes
- Adherence to style guide
- Documentation completeness

### 5.2 User Adoption Metrics

**Usage Statistics:**

**Active Projects:**
- Metric: Number of language pairs using Rule Assistant
- Current baseline: ~10-15 (estimate)
- Year 1 target: 25
- Year 2 target: 50
- Measurement: FLExTrans installation telemetry (opt-in)

**Rule Creation Rate:**
- Metric: Number of rules created per week
- Target: 100% increase over baseline after Phase 3 (better UX)
- Measurement: Telemetry (opt-in)

**Template Usage:**
- Metric: Percentage of new rules created from templates
- Target: 50% after Phase 3 rule library
- Measurement: Telemetry (opt-in)

**User Satisfaction:**

**Survey Metrics:**
- User satisfaction score: >4.0/5.0
- Net Promoter Score (NPS): >30
- Task completion success rate: >85%
- Measurement: Annual user survey

**Support Metrics:**
- Reduction in support requests: 50% (after Phase 3 documentation)
- Time to resolve issues: <7 days average
- Measurement: Issue tracker analytics

### 5.3 Language Coverage Goals

**Geographic and Genetic Diversity:**

**Language Families to Support (by end of Phase 4):**
1. Niger-Congo (Bantu, Kwa)
2. Afro-Asiatic (Semitic, Cushitic)
3. Indo-European (Romance, Germanic, Slavic, Indo-Aryan)
4. Sino-Tibetan (Chinese, Tibeto-Burman)
5. Austronesian (Malayo-Polynesian, Formosan)
6. Turkic
7. Uralic
8. Trans-New Guinea
9. Uto-Aztecan
10. Mayan

**Morphological Complexity Spectrum:**
- Isolating: Mandarin, Vietnamese (score 1-2 on agglutination index)
- Mildly synthetic: English, Spanish (score 3-5)
- Highly synthetic: Turkish, Swahili (score 6-8)
- Polysynthetic: Inuktitut, Mohawk (score 9-10)

**Target:** Successfully handle at least 2 languages from each complexity level.

**Specific High-Priority Languages (SIL partnerships):**
- 25 language pairs with active SIL projects
- Includes minority and endangered languages
- Diversity of morphological types
- Measurement: Case studies demonstrating success

### 5.4 Quality Benchmarks

**Translation Quality:**

**Automatic Metrics:**
- BLEU score: Improvement of 5-10 points over baseline (no Rule Assistant)
- METEOR score: Improvement of 3-5 points
- Character error rate: Reduction of 10-15%

**Human Evaluation:**
- Adequacy rating: >3.5/5.0
- Fluency rating: >3.5/5.0
- Post-editing time: 30% reduction vs. MT without Rule Assistant

**Rule Quality:**
- Manual review: 90% of generated rules judged "correct"
- No redundancy: <10% overlap in macro functionality
- Maintainability: 80% of linguists can modify rules after training

**Measurement:** Annual evaluation on standard test sets

### 5.5 Timeline Adherence

**Phase Completion Targets:**
- Phase 1: +/- 2 weeks of 1.5-month estimate
- Phase 2: +/- 1 month of 4.5-month estimate
- Phase 3: +/- 3 weeks of 3-month estimate
- Phase 4: +/- 2 months of 9-month estimate

**Overall Project:** Complete within 24 months (+/- 3 months)

**Measurement:** Monthly project status reports with burn-down charts

### 5.6 Success Criteria Summary

| Category | Metric | Target | Timeline |
|----------|--------|--------|----------|
| **Morphological Coverage** | WALS features supported | 90% | End of Phase 4 |
| **Feature Completeness** | Planned features implemented | 95% | End of Phase 4 |
| **Test Coverage** | Code coverage | >80% | Ongoing |
| **Active Projects** | Language pairs using RA | 50 | Year 2 |
| **User Satisfaction** | Survey score | >4.0/5.0 | After Phase 3 |
| **Language Diversity** | Language families | 10+ | End of Phase 4 |
| **Translation Quality** | BLEU improvement | +5-10 pts | End of Phase 4 |
| **Timeline** | Project completion | 24 months | +/- 3 months |

---

## 6. Conclusion and Next Steps

### 6.1 Summary

The Rule Assistant is a powerful tool that bridges linguistic expertise and machine translation technology. This roadmap outlines a path to transform it from a capable prototype to a comprehensive, production-ready system that can handle the full complexity of human language morphology.

**Key Achievements by Phase:**
- **Phase 1:** A stable, maintainable foundation with resolved technical debt
- **Phase 2:** Coverage of 90% of morphological phenomena
- **Phase 3:** A polished, user-friendly experience with comprehensive support
- **Phase 4:** Support for the world's most complex morphological systems

This represents an ambitious 12-24 month development effort that will position FLExTrans as the premier linguist-friendly machine translation toolkit.

### 6.2 Immediate Next Steps (Next 30 Days)

1. **Secure Funding and Resources (Week 1-2)**
   - Present roadmap to stakeholders
   - Identify funding sources (grants, partnerships)
   - Begin recruitment for core team

2. **Establish Infrastructure (Week 2-3)**
   - Set up development environment
   - Configure CI/CD pipeline
   - Create project tracking system
   - Establish communication channels

3. **Phase 1 Planning (Week 3-4)**
   - Break down Phase 1 tasks into sprint-sized chunks
   - Prioritize TODO items
   - Conduct Issue #661 investigation
   - Develop test plan

4. **Community Engagement (Week 4)**
   - Announce roadmap to FLExTrans community
   - Solicit feedback on priorities
   - Recruit beta testers for Phase 1
   - Engage with Apertium and STAMP communities

### 6.3 Decision Points

**3-Month Review (End of Phase 1):**
- Assess technical debt resolution success
- Re-evaluate Phase 2 timeline based on Phase 1 learnings
- Decision: Proceed to Phase 2 or extend Phase 1

**9-Month Review (Mid-Phase 2):**
- Evaluate linguistic feature coverage
- Assess Apertium integration challenges
- Decision: Adjust Phase 4 scope based on Phase 2 feasibility

**15-Month Review (End of Phase 3):**
- User adoption and satisfaction assessment
- Documentation completeness check
- Decision: Prioritize Phase 4 features based on user needs

**24-Month Review (End of Phase 4):**
- Overall project success evaluation
- Plan for ongoing maintenance and enhancement
- Decision: Future development priorities

### 6.4 Long-Term Vision (Beyond 24 Months)

**Potential Future Directions:**
- **AI-Assisted Rule Generation:** Use machine learning to suggest rules based on parallel corpora
- **Syntax-Semantics Interface:** Deeper integration of syntactic and semantic transfer
- **Real-Time Collaboration:** Multi-user rule editing for team projects
- **Rule Optimization:** Automatic rule ordering and conflict resolution
- **Cross-Platform Support:** Web-based Rule Assistant for broader accessibility

**Sustainability:**
- Community-driven development model
- Regular release cycle (quarterly updates)
- Long-term support for core language pairs
- Integration with evolving FLEx, Apertium, STAMP ecosystems

---

## Appendix A: Glossary

**Apertium:** Open-source machine translation platform using shallow transfer approach

**Circumfix:** Affix consisting of simultaneous prefix and suffix (e.g., German *ge-...-t*)

**FLEx:** FieldWorks Language Explorer, SIL's linguistic database and analysis tool

**Infix:** Affix inserted within a root morpheme (e.g., Tagalog *-um-*)

**Macro:** Reusable code block in Apertium transfer rules for complex operations

**Reduplication:** Morphological process involving repetition of all or part of a word

**STAMP:** Synthesis via Affix Morphological Processing, used in FLExTrans for generation

**Suppletion:** Morphologically related forms with completely different stems (*go/went*)

**Templatic Morphology:** Non-concatenative morphology (root and pattern, e.g., Semitic)

**Transfer Rule:** Rule specifying how to map source language structure to target language

---

## Appendix B: References and Resources

**Linguistic Typology:**
- Haspelmath, Martin et al. *World Atlas of Language Structures (WALS)*. https://wals.info/
- Payne, Thomas. *Describing Morphosyntax*. Cambridge University Press, 1997.

**Machine Translation:**
- Forcada, Mikel et al. "Apertium: a free/open-source platform for rule-based machine translation." *Machine Translation* 25.2 (2011): 127-144.
- Lockwood, Ronald M. *FLExTrans Documentation*. SIL International.

**Morphological Theory:**
- Spencer, Andrew & Zwicky, Arnold. *The Handbook of Morphology*. Blackwell, 2001.
- Haspelmath, Martin & Sims, Andrea. *Understanding Morphology*. 2nd ed. Routledge, 2010.

**Software Engineering:**
- Martin, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall, 2008.
- Fowler, Martin. *Refactoring: Improving the Design of Existing Code*. Addison-Wesley, 2018.

---

**Document Control:**
- **Version:** 1.0
- **Date:** November 22, 2025
- **Next Review:** January 22, 2026
- **Approval:** Pending stakeholder review
- **Change Log:** Initial version

---

*This roadmap is a living document and should be updated quarterly to reflect progress, new insights, and changing priorities.*
