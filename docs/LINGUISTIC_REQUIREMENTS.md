# Linguistic Requirements for FLExTrans Rule Assistant

**Version:** 1.0
**Date:** 2025-11-22
**Author:** Linguistic Analysis Team
**Status:** Comprehensive Requirements Document

## Executive Summary

This document provides a linguistic evaluation of the FLExTrans Rule Assistant from a typological perspective, identifying current capabilities, gaps, and requirements for supporting the world's linguistic diversity. The analysis covers 22 example rules, evaluates coverage across major language types (isolating, agglutinative, fusional, polysynthetic), and provides a roadmap for expanding linguistic coverage.

**Key Findings:**
- Current system excels at Indo-European fusional languages
- Strong support for agreement, affixation, and word order changes
- Critical gaps: infixes/circumfixes, tone, vowel harmony, polysynthesis
- Disjoint feature sets (Bantu) demonstrate sophisticated capabilities
- Need expanded support for typologically diverse languages

---

## Table of Contents

1. [Current Linguistic Coverage](#1-current-linguistic-coverage)
2. [Analysis by Language Type](#2-analysis-by-language-type)
3. [Critical Linguistic Gaps](#3-critical-linguistic-gaps)
4. [Priority Phenomena by Language Family](#4-priority-phenomena-by-language-family)
5. [Linguistic Test Suite](#5-linguistic-test-suite)
6. [Evaluation Criteria](#6-evaluation-criteria)
7. [Future Requirements](#7-future-requirements)
8. [Recommendations](#8-recommendations)

---

## 1. Current Linguistic Coverage

### 1.1 Analysis of 22 Example Rules

The Rule Assistant currently includes 22 example rule files demonstrating various linguistic phenomena. Analysis reveals strong coverage of specific morphosyntactic patterns:

#### 1.1.1 Agreement Patterns (Well Supported)

**Gender Agreement:**
- File: `Ex1a_Def-Noun.xml`, `Ex2_Adj-Noun.xml`, `SpanishFrenchRev2.xml`
- Linguistic Pattern: Noun-adjective gender concord (α matching)
- Languages: Romance (Spanish, French), Germanic (German), Indo-European
- Coverage: **Excellent** - handles multi-word agreement chains

**Number Agreement:**
- Files: Multiple examples with singular/plural (β matching)
- Linguistic Pattern: Controller-target agreement for number
- Languages: Most Indo-European, some Niger-Congo
- Coverage: **Excellent** - including unmarked defaults

**Case Agreement:**
- File: `EnglishGermanTripleRanking.xml`
- Linguistic Pattern: Nominative, accusative, dative, genitive
- Languages: German, Russian, Latin, Sanskrit
- Coverage: **Good** - handles case on determiners and adjectives

**Multiple Simultaneous Agreements:**
- File: `unmarked_default.xml`, `Ex3_Adj-Noun.xml`
- Linguistic Pattern: Gender + Number on single word
- Example: Spanish "las casas grandes" (fem.pl house.pl big.pl)
- Coverage: **Excellent**

#### 1.1.2 Morphological Processes (Partial Support)

**Suffixation:**
- Files: Most examples use suffix affixation
- Linguistic Pattern: Stem + suffix(es)
- Languages: Universal, but especially Turkic, Uralic, Bantu
- Coverage: **Excellent**

**Prefixation:**
- File: `SplitBantu.xml`
- Linguistic Pattern: Prefix + stem
- Languages: Bantu, some Austronesian, Athabaskan
- Coverage: **Excellent**

**Infixation:**
- Files: **NONE**
- Linguistic Pattern: affix inserted within stem
- Languages: **Tagalog, Arabic, Sanskrit, Khmer**
- Coverage: **Missing** (planned in implementation)

**Circumfixation:**
- Files: **NONE**
- Linguistic Pattern: prefix + stem + suffix as single morph
- Languages: **German (ge-...-t), Dutch, Afrikaans, Georgian**
- Coverage: **Missing** (planned in implementation)

**Reduplication:**
- Files: **NONE**
- Linguistic Pattern: Full or partial stem copying
- Languages: **Widespread: Austronesian, Niger-Congo, Salishan**
- Coverage: **Not supported** - major gap

#### 1.1.3 Syntactic Transformations (Well Supported)

**Word Order Changes:**
- File: `Ex2_Adj-Noun.xml` (Adj-N → N-Adj)
- Linguistic Pattern: Head-initial ↔ head-final
- Languages: English-Spanish, Germanic-Romance
- Coverage: **Excellent** - arbitrary reordering supported

**Word Insertion:**
- File: `insert_word.xml`
- Linguistic Pattern: Adding grammatical words (determiners, copulas)
- Languages: Translations between languages with/without articles
- Coverage: **Good** - can insert words with features

**Word Deletion:**
- File: `insert_word.xml` (shows removal in reverse direction)
- Linguistic Pattern: Removing source words not needed in target
- Languages: Pro-drop languages, article-less languages
- Coverage: **Good**

**Feature Reassignment:**
- File: `GermanSwedishDefToAffix.xml`
- Linguistic Pattern: Function word → affix or vice versa
- Languages: Scandinavian definiteness (suffixed article)
- Coverage: **Excellent** - key strength of system

#### 1.1.4 Advanced Features (Sophisticated)

**Disjoint Feature Sets:**
- File: `SplitBantu.xml`
- Linguistic Pattern: Multiple FLEx features → single Apertium co-feature
- Linguistic Rationale: Bantu noun classes conflate number+gender
  - Class 1/2: singular/plural human
  - Class 3/4: singular/plural plants
  - Cannot be decomposed into independent gender+number
- Languages: Bantu (Swahili, Zulu, Chichewa)
- Coverage: **Excellent** - demonstrates deep linguistic understanding
- **This is a sophisticated solution to a real typological challenge**

**Feature Ranking:**
- File: `EnglishGermanTripleRanking.xml`, `ranking.xml`
- Linguistic Pattern: Priority-based form selection for syncretism
- Linguistic Rationale: German "die" can be:
  - Feminine singular nominative (rank 3 for gender)
  - Plural all genders (rank 1 for number - preferred!)
  - Feminine singular accusative (rank 2 for case)
- Languages: Languages with paradigm syncretism
- Coverage: **Excellent** - handles real-world ambiguity

**Unmarked Defaults:**
- File: `unmarked_default.xml`, `GermanEnglishDoubleDefault.xml`
- Linguistic Pattern: Zero-marked or null morphology
- Linguistic Rationale: English doesn't mark singular overtly
- Languages: Most languages have some unmarked categories
- Coverage: **Good**

### 1.2 Strengths of Current System

1. **Sophisticated Agreement Handling:** The α, β, γ matching system elegantly handles multiple simultaneous agreement patterns, including complex scenarios like German determiner declension.

2. **Disjoint Feature Sets:** The Bantu example shows the system can handle non-compositional features - a challenge even for many MT systems. This indicates the architecture can be extended to other complex phenomena.

3. **Feature Ranking:** Addresses the real-world problem of syncretism (form ambiguity) in morphologically rich languages. This is linguistically sophisticated.

4. **Flexible Morphosyntactic Mapping:** Can handle function word ↔ affix alternations, critical for typologically diverse translations.

5. **Permutation Support:** The `create_permutations` attribute suggests capability for generating multiple rule variants.

### 1.3 Current Limitations

1. **Morphological Type Limitations:**
   - No infixes (planned but not implemented)
   - No circumfixes (planned but not implemented)
   - No reduplication support
   - No templatic morphology (Semitic root-pattern)
   - No tonal morphology

2. **Typological Biases:**
   - Examples heavily favor Indo-European languages
   - Limited polysynthetic language support
   - No serial verb construction examples
   - No classifier/counter system examples
   - No evidential system examples

3. **Phonological Processes:**
   - No vowel harmony (critical for Turkic, Uralic)
   - No tone changes (critical for African, Asian languages)
   - No consonant mutations (Celtic languages)
   - No stress-based patterns

4. **Dependency/Valency Patterns:**
   - No differential object marking
   - No switch-reference systems
   - No applicative/causative voice changes
   - No noun incorporation patterns

---

## 2. Analysis by Language Type

### 2.1 Isolating Languages

**Characteristics:** Little to no inflectional morphology, grammatical relations marked by word order and function words.

**Examples:** Mandarin Chinese, Vietnamese, Thai, Yoruba

**Current Support:**

✅ **Well Supported:**
- Word order changes (the primary mechanism)
- Function word insertion/deletion
- Particle handling (can be treated as words)

❌ **Gaps:**
- Tone changes (e.g., Mandarin tone sandhi, Thai tone morphology)
- Classifiers/counters (e.g., Mandarin 三本书 "three CLASSIFIER book")
- Sentence-final particles (pragmatic/evidential marking)
- Serial verb constructions (multi-verb predicates without conjunction)

**Priority Requirements:**
1. **Classifier systems** (HIGH) - Add category for numeral classifiers
2. **Tone marking** (MEDIUM) - Not critical for transfer rules but needed for phonology
3. **Serial verbs** (MEDIUM) - Multi-word verbal complexes

**Test Languages:**
- Mandarin Chinese (SVO, tonal, classifiers)
- Vietnamese (SVO, tonal, extensive classifiers)
- Yoruba (SVO, tonal, serial verbs)

### 2.2 Agglutinative Languages

**Characteristics:** Words formed by linear concatenation of morphemes, each expressing one grammatical category.

**Examples:** Turkish, Swahili, Finnish, Japanese, Korean, Quechua

**Current Support:**

✅ **Well Supported:**
- Multiple suffix chains (excellent)
- Prefix chains (Bantu example)
- Feature agreement across affixes
- Long morpheme sequences

❌ **Gaps:**
- Vowel harmony (Finnish, Turkish, Hungarian)
  - Finnish: talo-ssa (house-in) vs. käsi-ssä (hand-in)
  - Turkish: ev-ler-de (house-pl-loc) vs. köy-ler-de (village-pl-loc)
- Consonant gradation (Finnish, Sami)
- Honorific/social register affixes (Japanese, Korean)
- Evidential suffixes (Quechua, Turkish)

**Priority Requirements:**
1. **Vowel harmony** (HIGH) - Affects most Turkic, Uralic languages
2. **Evidential marking** (MEDIUM) - Grammatically obligatory in some languages
3. **Honorific systems** (LOW) - Can be handled with features, needs examples

**Test Languages:**
- Turkish (SOV, vowel harmony, rich agglutination)
- Finnish (SVO, vowel harmony, 15 cases)
- Swahili (SVO, Bantu noun classes, agglutinative verbs)
- Quechua (SOV, evidentials, switch-reference)

### 2.3 Fusional Languages

**Characteristics:** Multiple grammatical categories expressed in single morphemes; extensive allomorphy.

**Examples:** Russian, Spanish, German, Arabic, Sanskrit

**Current Support:**

✅ **Well Supported:**
- This is the system's strength
- Gender-number-case fusion (German, Russian)
- Multiple agreement patterns (Romance)
- Syncretism handling (feature ranking)
- Irregular forms (can use macros)

❌ **Gaps:**
- Ablaut/apophony (English sing-sang-sung, German trinken-trank-getrunken)
- Semitic root-and-pattern morphology (Arabic k-t-b → kitāb, maktab, kutub)
- Umlaut patterns (German Vater-Väter)
- Stress-based distinctions (Russian verbal aspect pairs)

**Priority Requirements:**
1. **Root-and-pattern morphology** (HIGH) - Critical for Semitic languages
2. **Ablaut patterns** (MEDIUM) - Common in Indo-European
3. **Suprasegmental features** (LOW) - Stress, tone in fusional systems

**Test Languages:**
- Russian (SVO, 6 cases, aspect, animacy)
- Arabic (VSO, root-pattern, broken plurals)
- Spanish (SVO, gender-number fusion, pronominal clitics)
- Sanskrit (SOV, 8 cases, extensive fusion)

### 2.4 Polysynthetic Languages

**Characteristics:** Entire sentences can be expressed in single words; noun incorporation; extensive agreement.

**Examples:** Inuktitut, Mohawk, Greenlandic, Chukchi, Nuu-chah-nulth

**Current Support:**

✅ **Moderately Supported:**
- Multiple affixes per word (somewhat supported)
- Agreement chains (partially)

❌ **Gaps:**
- **Noun incorporation** (CRITICAL GAP)
  - Mohawk: *wa'-ke-nákt-a-hninu-'* "I bought bread" (literally: "I-it-bread-bought")
  - Cannot be handled as word-to-affix; need N+V → V structure
- **Polypersonal agreement** (verb agrees with subject, object, indirect object)
  - Swahili: *ni-li-m-w-on-a* "I-PAST-him-see-FV" = "I saw him"
  - Current system could handle this but no examples
- **Applicatives** (adding arguments via morphology)
- **Switch-reference** (tracking subject continuity across clauses)
- **Directional/orientational affixes** (Athabaskan, Eskimo-Aleut)

**Priority Requirements:**
1. **Noun incorporation** (HIGH) - Core feature of polysynthetic languages
2. **Polypersonal agreement** (HIGH) - Multi-argument indexing on verb
3. **Applicative/causative morphology** (MEDIUM)
4. **Directional systems** (MEDIUM)

**Test Languages:**
- Inuktitut (polysynthetic, ergative, extensive incorporation)
- Mohawk (polysynthetic, complex agreement, incorporation)
- Greenlandic (polysynthetic, ergative, mood system)
- Nahuatl (agglutinating-polysynthetic, incorporation, complex verbs)

### 2.5 Summary Table: Support by Language Type

| Language Type | Overall Support | Strong Areas | Critical Gaps | Priority Level |
|---------------|----------------|--------------|---------------|----------------|
| **Isolating** | 60% | Word order, particles | Classifiers, tone, serial verbs | Medium |
| **Agglutinative** | 75% | Affix chains, agreement | Vowel harmony, evidentials | High |
| **Fusional** | 90% | Agreement, syncretism | Root-pattern, ablaut | Medium |
| **Polysynthetic** | 40% | Some affixation | Incorporation, polypersonal | High |

---

## 3. Critical Linguistic Gaps

### 3.1 Morphological Gaps

#### 3.1.1 Infixation (HIGH PRIORITY)

**Definition:** Affix inserted within the stem, not at edges.

**Linguistic Distribution:** Common in Austronesian, Semitic, some Indo-European.

**Examples:**

1. **Tagalog (Austronesian):**
   - *sulat* "write" → *s-um-ulat* "wrote" (um-infix)
   - *bili* "buy" → *b-in-ili* "bought" (in-infix)
   - *gradwet* "graduate" → *gr-um-adwet* "graduated"

2. **Arabic (Semitic):**
   - Root: k-t-b (writing)
   - *kataba* "he wrote" (CaCaCa pattern)
   - *kutiba* "it was written" (CuCiCa passive pattern)
   - Infixing vowels into consonantal root

3. **Ancient Greek:**
   - *lambanō* "I take" → *elabon* "I took" (aorist with infix)

**Current Status:** Planned in implementation but not yet available.

**Why Needed:** 20+ million Tagalog speakers, entire Austronesian family (1,200+ languages), all Semitic languages.

**Apertium Challenges:**
- Apertium transfer rules work on whole-word units
- Infixes require stem segmentation
- Phonological environment may condition infix placement

**Proposed Solution:**
- Mark affix as `type="infix"` with `position` attribute
- Generate warning in transfer file
- Handle in morphological analyzer rather than transfer rules
- See Implementation Plan §2 for details

#### 3.1.2 Circumfixation (HIGH PRIORITY)

**Definition:** Simultaneous prefix and suffix that function as single morpheme.

**Linguistic Distribution:** Germanic, Berber, some Afroasiatic, Georgian.

**Examples:**

1. **German Participles:**
   - *machen* "to make" → *ge-mach-t* "made"
   - *spielen* "to play" → *ge-spiel-t* "played"
   - Cannot separate ge- and -t; they form single "perfective" morpheme

2. **Dutch:**
   - *werken* "to work" → *ge-werk-t* "worked"

3. **Berber (Kabyle):**
   - Negative circumfix: *ur-...-ara*
   - *yečča* "he ate" → *ur-yečča-ara* "he didn't eat"

4. **Indonesian (Austronesian):**
   - *ke-...-an* (noun-forming circumfix)
   - *adil* "just" → *ke-adil-an* "justice"

**Current Status:** Planned in implementation but not yet available.

**Why Needed:** German participles are extremely common; affects all Germanic languages to some degree.

**Technical Challenge:**
- Need to split circumfix into prefix and suffix parts in output
- Single feature must trigger both parts
- Ordering constraints (circumfix wraps around stem)

**Proposed Solution:**
- Mark affix as `type="circumfix"`
- Generate both prefix and suffix parts in transfer rule
- Use tag splitting convention (e.g., "GE_T" → "GE" + "T")
- See Implementation Plan §2.4 for details

#### 3.1.3 Reduplication (MEDIUM-HIGH PRIORITY)

**Definition:** Full or partial repetition of base form to express grammatical meaning.

**Linguistic Distribution:** Extremely widespread - Austronesian, Niger-Congo, Salishan, Muskogean, many others.

**Types:**

1. **Full Reduplication:**
   - **Indonesian:** *orang* "person" → *orang-orang* "people" (plural)
   - **Malay:** *buku* "book" → *buku-buku* "books"

2. **Partial Reduplication:**
   - **Tagalog:** *sulat* "write" → *susulat* "will write" (CV-reduplication)
   - **Salish:** *qʷəl* "speak" → *qʷəqʷəl* "speaking" (C₁V-reduplication)

3. **Reduplication with Affix:**
   - **Turkish:** *beyaz* "white" → *bem-beyaz* "very white" (m-infix + reduplication)

**Current Status:** Not supported, no plans mentioned.

**Why Needed:**
- Austronesian family: 1,200+ languages, 400+ million speakers
- Critical in Niger-Congo, indigenous American languages
- Productive in many languages for plurals, intensification, aspect

**Technical Challenges:**
- Requires access to stem phonology
- May involve partial copying (first CV, first syllable, etc.)
- May involve phonological changes in copied material
- Not easily handled in transfer rules

**Proposed Solution:**
- Likely needs morphological analyzer handling
- Transfer rule could mark for reduplication
- Actual reduplication happens at generation time
- May need special attribute: `reduplication_type="full|CV|C1V|..."'

#### 3.1.4 Templatic Morphology (MEDIUM PRIORITY)

**Definition:** Root-and-pattern morphology where consonantal root interlocks with vocalic pattern.

**Linguistic Distribution:** Semitic languages (Arabic, Hebrew, Amharic), some Cushitic.

**Examples:**

**Arabic:**
- Root: √k-t-b (writing concept)
- Patterns:
  - *CaCaCa*: *kataba* "he wrote"
  - *CāCiC*: *kātib* "writer"
  - *maCCaC*: *maktab* "office, desk"
  - *CuCiCa*: *kutiba* "it was written" (passive)
  - *kitāb* "book"
  - *kutub* "books" (broken plural)

**Hebrew:**
- Root: √g-d-l (growing/greatness)
- *gadal* "he grew"
- *gadol* "big"
- *higdil* "he enlarged"
- *hitgadel* "he grew up" (reflexive)

**Current Status:** Not supported. Infixation support might partially help, but templatic morphology is fundamentally different.

**Why Needed:**
- Arabic: 300+ million speakers
- Hebrew: 9+ million speakers
- Amharic, Tigrinya, Maltese, many others
- Productive morphological system

**Technical Challenges:**
- Requires decomposing roots from patterns
- Cannot be handled as linear affixation
- May need root-level lexical entries in FLEx
- Apertium morphological analyzers need special handling

**Proposed Solution:**
- Long-term solution: Root-pattern feature in FLEx
- Short-term: Treat forms as suppletive (stored allomorphs)
- Use macros for pattern selection based on features
- Document limitations clearly

### 3.2 Phonological Gaps

#### 3.2.1 Vowel Harmony (HIGH PRIORITY)

**Definition:** Vowels within a word must agree in certain features (backness, rounding, height).

**Linguistic Distribution:** Turkic, Uralic, Mongolian, some Niger-Congo, Korean, Mongolian.

**Examples:**

1. **Turkish (Palatal Harmony):**
   - Back vowels: a, ı, o, u
   - Front vowels: e, i, ö, ü
   - *ev-ler-de* "house-PL-LOC" (all front vowels)
   - *kız-lar-da* "girl-PL-LOC" (all back vowels)
   - Suffix vowels determined by stem

2. **Finnish (Back-Front Harmony):**
   - *talo-ssa* "house-INESS" (back vowels: a, o)
   - *käsi-ssä* "hand-INESS" (front vowels: ä, i)
   - Suffixes have harmonic variants: -ssa/-ssä, -lla/-llä

3. **Hungarian:**
   - *ház-ban* "house-INESS" (back harmony)
   - *kéz-ben* "hand-INESS" (front harmony)

**Current Status:** Not supported.

**Why Needed:**
- Turkish: 80+ million speakers
- Finnish: 5+ million speakers
- Hungarian: 13+ million speakers
- All Turkic languages (150+ million total)
- All Uralic languages

**Technical Challenges:**
- Requires phonological features of stems
- Affixes need allomorphic variants
- May require multi-tier representation
- Cannot be handled as simple feature matching

**Proposed Solution:**
- Add phonological class attribute to stems (back/front, rounded/unrounded)
- Define harmonic affix variants in FLEx
- Transfer rule selects variant based on stem phonology
- May need special macro for harmonic suffix selection

**Implementation Feasibility:** Medium - requires extending FLEx data model to track phonological features.

#### 3.2.2 Tone (MEDIUM PRIORITY)

**Definition:** Pitch contours on syllables that distinguish meaning or mark grammar.

**Linguistic Distribution:** Most African languages, many Asian languages, some Mesoamerican, tone widespread worldwide.

**Types:**

1. **Lexical Tone:**
   - Distinguishes word meaning
   - **Mandarin:** *mā* (mother, high), *má* (hemp, rising), *mǎ* (horse, falling-rising), *mà* (scold, falling)

2. **Grammatical Tone:**
   - Marks grammatical categories
   - **Yoruba:** *ó wá* "he came" (high tone = past) vs. *ò wá* "he comes" (low tone = present)

3. **Tone Sandhi:**
   - Tone changes in context
   - **Mandarin:** Third tone + third tone → second tone + third tone
   - *nǐ hǎo* [ní hǎo] "hello"

**Current Status:** Not supported; no mechanism for suprasegmental features.

**Why Needed:**
- Majority of African languages are tonal
- Mandarin, Cantonese, Vietnamese, Thai, Burmese (billions of speakers)
- Grammatically significant in many languages

**Technical Challenges:**
- FLEx can represent tone orthographically
- Apertium doesn't model suprasegmentals well
- Tone changes hard to express in transfer rules
- May need phonological component

**Proposed Solution:**
- Short-term: Treat tonal variants as allomorphs
- Long-term: Add suprasegmental feature layer
- For grammatical tone: Use features to select tonal form
- For tone sandhi: Requires phonological post-processing

**Implementation Feasibility:** Low for full support; Medium for grammatical tone marking.

#### 3.2.3 Consonant Mutations (LOW-MEDIUM PRIORITY)

**Definition:** Initial consonant changes triggered by grammatical context.

**Linguistic Distribution:** Celtic languages, some African languages.

**Examples:**

1. **Welsh (Soft Mutation):**
   - *cath* "cat" → *ei gath* "his cat" (c → g)
   - *pen* "head" → *ei ben* "his head" (p → b)
   - *tad* "father" → *ei dad* "his father" (t → d)

2. **Irish:**
   - *cat* "cat" → *an cat* "the cat" → *mo chat* "my cat" (c → ch, lenition)

**Current Status:** Not supported.

**Why Needed:**
- Welsh: 700,000+ speakers
- Irish: 1.8 million speakers
- Scottish Gaelic, Breton, Cornish
- Grammatically obligatory

**Technical Challenges:**
- Requires phonological rules
- Conditioned by preceding word
- Multiple mutation types (soft, nasal, aspirate)

**Proposed Solution:**
- Use lexical variants for common mutated forms
- Add mutation trigger attribute to words
- Generate appropriate form in transfer rule
- May need macros for mutation selection

**Implementation Feasibility:** Medium - limited to Celtic, but important for those languages.

### 3.3 Syntactic Gaps

#### 3.3.1 Noun Incorporation (HIGH PRIORITY for Polysynthetic)

**Definition:** Noun stem combines with verb to form single word.

**Linguistic Distribution:** Polysynthetic languages, some agglutinative languages.

**Examples:**

1. **Mohawk (Iroquoian):**
   - *wa'-ke-nákt-a-hninu-'*
   - PAST-1sg-bread-Ø-buy-PUNC
   - "I bought bread" (literally: "I bread-bought")

2. **Chukchi (Chukotko-Kamchatkan):**
   - *t-ə-meyŋ-levt-pəγt-ə-rkən*
   - 1sg-large-head-hurt-PRES
   - "I have a big headache" (literally: "I big-head-ache")

3. **Greenlandic (Eskimo-Aleut):**
   - *qaya-r-puq* "kayak-have-3sg" = "he has a kayak"

**Current Status:** Not supported; fundamental limitation.

**Why Needed:**
- Defining feature of polysynthetic languages
- Common in indigenous American languages
- Productive in Eskimo-Aleut, Chukotko-Kamchatkan, Iroquoian

**Technical Challenges:**
- Rule Assistant models words, not morphemes
- N + V → V requires structural change
- Incorporated noun loses independence
- May need category change (n → v)

**Proposed Solution:**
- Extend XML schema to allow morpheme-level operations
- Add `<IncorporatedWord>` element that becomes affix/infix
- Transfer rule generates verb with incorporated noun stem
- May need separate module for incorporation

**Implementation Feasibility:** Low-Medium - requires architectural changes.

#### 3.3.2 Serial Verb Constructions (MEDIUM PRIORITY)

**Definition:** Multiple verbs in sequence functioning as single predicate, without conjunction.

**Linguistic Distribution:** West African, Southeast Asian, Creole languages.

**Examples:**

1. **Yoruba (Niger-Congo):**
   - *Ó mú ìwé wá*
   - 3sg take book come
   - "He brought a book" (literally: "take book come")

2. **Mandarin:**
   - *我 去 买 菜*
   - wǒ qù mǎi cài
   - I go buy vegetable
   - "I'm going to buy vegetables" (literally: "I go buy vegetable")

3. **Thai:**
   - *phǒm pai kin khâaw*
   - I go eat rice
   - "I'm going to eat" (literally: "I go eat rice")

**Current Status:** Partially supportable as multi-word sequences, but no special handling.

**Why Needed:**
- Widespread in West Africa (100+ million speakers)
- Common in Southeast Asia (1+ billion speakers)
- Productive in Creoles worldwide

**Technical Challenges:**
- Multiple verbs need to be recognized as single predicate
- Argument sharing between verbs
- Some languages have constraints on which verbs can serialize

**Proposed Solution:**
- Use multi-word rules with multiple verb categories
- Mark head verb for tense/aspect
- Other verbs as non-head
- May need special attribute for serial verb status

**Implementation Feasibility:** Medium - can be handled with existing multi-word rules, but needs examples.

#### 3.3.3 Classifiers/Counters (MEDIUM-HIGH PRIORITY)

**Definition:** Obligatory morphemes used with numbers or demonstratives to categorize nouns.

**Linguistic Distribution:** East Asian, Southeast Asian, some Mesoamerican.

**Examples:**

1. **Mandarin:**
   - *sān **běn** shū* "three **CL** book" = "three books" (flat objects)
   - *sān **zhī** gǒu* "three **CL** dog" = "three dogs" (animals)
   - *sān **gè** rén* "three **CL** person" = "three people" (general)
   - Cannot say *sān shū (ungrammatical)

2. **Japanese:**
   - *hon san-**satsu*** "book three-**CL**" = "three books" (bound volumes)
   - *inu san-**biki*** "dog three-**CL**" = "three dogs" (small animals)

3. **Thai:**
   - *mǎa sǎam **tua*** "dog three **CL**" = "three dogs"

**Current Status:** Could be handled as function words, but no examples.

**Why Needed:**
- Mandarin: 1+ billion speakers
- Japanese: 125+ million speakers
- Thai, Vietnamese, Korean, Burmese, and many others

**Technical Challenges:**
- Classifier selection depends on noun semantics
- Different classifiers for different contexts
- Word order varies by language

**Proposed Solution:**
- Add classifier as separate word category
- Link to noun via features (semantic class)
- Insert classifier in numeral contexts
- May need semantic features on nouns (animate, flat, cylindrical, etc.)

**Implementation Feasibility:** Medium - requires semantic features in FLEx.

#### 3.3.4 Evidentials (MEDIUM PRIORITY)

**Definition:** Grammatical marking of information source (direct observation, hearsay, inference).

**Linguistic Distribution:** Widespread in Americas, parts of Asia, scattered elsewhere.

**Examples:**

1. **Quechua (Andean):**
   - *Para-sha-n* "It's raining" (direct observation)
   - *Para-shi* "It's raining" (hearsay/reportative -shi)
   - *Para-cha* "It might be raining" (inference/conjecture -cha)

2. **Turkish:**
   - *Gel-di* "He came" (direct observation, witnessed past)
   - *Gel-miş* "He came" (indirect observation, inferential past -miş)

3. **Tibetan:**
   - *nga-s mthong-byung* "I saw it" (direct evidence)
   - *kho yong-'dug* "He is coming" (direct sensory evidence)
   - *kho yong-song* "He came" (non-sensory evidence)

**Current Status:** Could be handled as verbal affixes, but no examples.

**Why Needed:**
- Grammatically obligatory in many languages
- Quechua: 10+ million speakers
- Turkish: 80+ million speakers
- Many indigenous American languages

**Technical Challenges:**
- Source language may not mark evidentiality
- Target language may require it
- Choosing correct evidential requires discourse context

**Proposed Solution:**
- Treat as verbal affix feature
- Add default evidential for translations (e.g., direct)
- May need discourse-level module for accurate selection
- Can be handled with existing affix system

**Implementation Feasibility:** High - existing affix system can handle it; just needs examples.

---

## 4. Priority Phenomena by Language Family

### 4.1 Niger-Congo (1,500+ languages, 700+ million speakers)

**Critical Features:**
- ✅ Noun class agreement (Bantu) - **SUPPORTED** (SplitBantu.xml)
- ❌ Tone (lexical and grammatical) - **NOT SUPPORTED**
- ❌ Serial verb constructions - **NOT SUPPORTED**
- ✅ Prefixes and suffixes - **SUPPORTED**
- ❌ Reduplication - **NOT SUPPORTED**

**Priority:**
1. **HIGH:** Tone support (grammatical tone at minimum)
2. **MEDIUM:** Serial verbs
3. **MEDIUM:** Reduplication

**Representative Test Languages:**
- Swahili (Bantu, 100+ million speakers)
- Yoruba (tonal, serial verbs, 40+ million)
- Lingala (Bantu, tone, 15+ million)

### 4.2 Austronesian (1,200+ languages, 400+ million speakers)

**Critical Features:**
- ❌ Infixation - **NOT SUPPORTED** (planned)
- ❌ Reduplication (full and partial) - **NOT SUPPORTED**
- ✅ Prefixes and suffixes - **SUPPORTED**
- ❌ Circumfixes - **NOT SUPPORTED** (planned)
- ❌ Voice systems (actor, patient, locative focus) - **PARTIALLY SUPPORTED**

**Priority:**
1. **HIGH:** Infixation (extremely common)
2. **HIGH:** Reduplication (productive)
3. **MEDIUM:** Voice/focus systems
4. **MEDIUM:** Circumfixes

**Representative Test Languages:**
- Tagalog (100+ million speakers, rich infixation)
- Indonesian/Malay (290+ million speakers, affixation)
- Malagasy (VSO word order, voice system)

### 4.3 Sino-Tibetan (450+ languages, 1.4+ billion speakers)

**Critical Features:**
- ❌ Tone (lexical and grammatical) - **NOT SUPPORTED**
- ❌ Classifiers - **NOT SUPPORTED**
- ✅ Word order changes (isolating) - **SUPPORTED**
- ❌ Serial verbs (Mandarin) - **NOT SUPPORTED**
- ✅ Particles - **SUPPORTED** (as words)

**Priority:**
1. **HIGH:** Classifiers (obligatory in most languages)
2. **MEDIUM:** Tone (less critical for transfer, more for phonology)
3. **MEDIUM:** Serial verbs
4. **LOW:** Aspect particles (can be handled as words)

**Representative Test Languages:**
- Mandarin (1+ billion speakers)
- Cantonese (85+ million speakers)
- Tibetan (6+ million speakers, evidentials)
- Burmese (33+ million speakers, tonal)

### 4.4 Indo-European (445+ languages, 3+ billion speakers)

**Critical Features:**
- ✅ Gender-number-case agreement - **EXCELLENTLY SUPPORTED**
- ✅ Verbal conjugation - **SUPPORTED**
- ❌ Ablaut/apophony - **NOT SUPPORTED**
- ❌ Umlaut - **NOT SUPPORTED**
- ✅ Multiple affixation - **SUPPORTED**
- ❌ Consonant mutation (Celtic) - **NOT SUPPORTED**

**Priority:**
1. **MEDIUM:** Ablaut (common in Germanic strong verbs, but can use allomorphs)
2. **LOW:** Umlaut (German, can use allomorphs)
3. **MEDIUM:** Consonant mutation (Celtic languages)

**Representative Test Languages:**
- ✅ Spanish, German, Russian - **WELL COVERED**
- ❌ Welsh (consonant mutations) - **NEEDS WORK**
- ❌ Sanskrit (8 cases, complex fusion, ablaut) - **NEEDS TESTING**

### 4.5 Turkic (35+ languages, 170+ million speakers)

**Critical Features:**
- ✅ Agglutinative suffixation - **SUPPORTED**
- ❌ Vowel harmony - **NOT SUPPORTED**
- ❌ Evidentials - **NOT SUPPORTED** (can be handled as affix)
- ✅ SOV word order - **SUPPORTED**

**Priority:**
1. **HIGH:** Vowel harmony (affects all affixes)
2. **MEDIUM:** Evidentials (grammatically obligatory)

**Representative Test Languages:**
- Turkish (80+ million speakers)
- Uzbek (34+ million speakers)
- Kazakh (13+ million speakers)

### 4.6 Afro-Asiatic (375+ languages, 500+ million speakers)

**Critical Features:**
- ❌ Root-and-pattern morphology (Semitic) - **NOT SUPPORTED**
- ❌ Broken plurals (Arabic) - **NOT SUPPORTED**
- ❌ Templatic verb forms - **NOT SUPPORTED**
- ✅ Gender agreement - **SUPPORTED**
- ❌ Circumfixes (Berber) - **NOT SUPPORTED** (planned)

**Priority:**
1. **HIGH:** Root-and-pattern morphology (fundamental to Semitic)
2. **HIGH:** Broken plurals (Arabic, Hebrew)
3. **MEDIUM:** Berber circumfixes

**Representative Test Languages:**
- Arabic (300+ million speakers)
- Amharic (25+ million speakers)
- Hebrew (9+ million speakers)
- Kabyle Berber (5+ million speakers)

### 4.7 Uralic (38+ languages, 25+ million speakers)

**Critical Features:**
- ✅ Extensive case systems (15+ cases) - **SUPPORTED**
- ❌ Vowel harmony - **NOT SUPPORTED**
- ✅ Agglutinative suffixation - **SUPPORTED**
- ❌ Consonant gradation (Finnish) - **NOT SUPPORTED**

**Priority:**
1. **HIGH:** Vowel harmony (affects all affixes)
2. **MEDIUM:** Consonant gradation (Finnish, Estonian)

**Representative Test Languages:**
- Finnish (5+ million speakers)
- Hungarian (13+ million speakers)
- Estonian (1+ million speakers)

### 4.8 Austroasiatic (168+ languages, 120+ million speakers)

**Critical Features:**
- ❌ Infixation - **NOT SUPPORTED** (planned)
- ✅ Prefixes and suffixes - **SUPPORTED**
- ❌ Reduplication - **NOT SUPPORTED**
- ✅ Isolating tendencies (Vietnamese) - **SUPPORTED**
- ❌ Tone (Vietnamese) - **NOT SUPPORTED**

**Priority:**
1. **HIGH:** Infixation (Khmer)
2. **MEDIUM:** Tone (Vietnamese)
3. **MEDIUM:** Classifiers (Vietnamese)

**Representative Test Languages:**
- Vietnamese (85+ million speakers)
- Khmer (16+ million speakers)

### 4.9 Eskimo-Aleut / Chukotko-Kamchatkan (Polysynthetic)

**Critical Features:**
- ✅ Extensive affixation - **PARTIALLY SUPPORTED**
- ❌ Noun incorporation - **NOT SUPPORTED**
- ❌ Polypersonal agreement - **NOT SUPPORTED**
- ❌ Ergative alignment - **NOT SUPPORTED** (can be handled with features)

**Priority:**
1. **HIGH:** Noun incorporation (defining feature)
2. **HIGH:** Polypersonal agreement
3. **MEDIUM:** Ergativity handling

**Representative Test Languages:**
- Greenlandic (50,000 speakers - small but linguistically significant)
- Inuktitut (40,000 speakers)

---

## 5. Linguistic Test Suite

### 5.1 Minimal Test Pairs by Phenomenon

This section provides minimal linguistic test pairs for validating Rule Assistant capabilities.

#### 5.1.1 Agreement

**Test Case: Gender Agreement (Romance)**
```
Source (English): the big house
Target (Spanish): la casa grande (fem.sg)
Target (French): la grande maison (fem.sg)

Rule requirements:
- Gender α from noun 'house' (fem)
- Agreement on determiner: la (fem.sg)
- Agreement on adjective: grande (fem.sg or invariant)
```

**Test Case: Multi-Feature Agreement (German)**
```
Source (English): the book
Target (German): das Buch (neut.sg.nom)
                  den Büchern (neut.pl.dat)

Rule requirements:
- Gender (neut), number (sg/pl), case (nom/dat) agreement
- Determiner form selection with feature ranking
- Syncretism handling
```

#### 5.1.2 Affixation

**Test Case: Agglutinative Suffixes (Turkish-like)**
```
Source: in the houses
Target: ev-ler-de
        house-PL-LOC

Rule requirements:
- Plural suffix -ler
- Locative suffix -de
- Correct ordering (PL before case)
- Vowel harmony: -ler/-lar, -de/-da (NOT YET SUPPORTED)
```

**Test Case: Prefix Chain (Swahili-like Bantu)**
```
Source: we will see them
Target: tu-ta-wa-ona
        1PL-FUT-3PL.OBJ-see

Rule requirements:
- Subject prefix tu- (1pl)
- Tense prefix ta- (future)
- Object prefix wa- (3pl)
- Correct ordering
```

#### 5.1.3 Word Order

**Test Case: Adjective Position (English-Spanish)**
```
Source (English): the big house [Det-Adj-N]
Target (Spanish): la casa grande [Det-N-Adj]

Rule requirements:
- Reorder Adj-N to N-Adj
- Maintain determiner in initial position
- Gender agreement across all elements
```

**Test Case: SOV to SVO (Japanese-English)**
```
Source (Japanese): 田中さんが本を読みました
                   Tanaka-san ga hon o yomimashita
                   Tanaka-SUBJ book-OBJ read.PAST
Target (English): Tanaka read a book [SVO]

Rule requirements:
- Verb moves from final to middle position
- Subject remains initial
- Object moves before verb
- Particle removal (ga, o)
- Article insertion (a)
```

#### 5.1.4 Disjoint Features (Bantu Noun Classes)

**Test Case: Swahili Noun Class Agreement**
```
Source (English): big books
Target (Swahili): vi-tabu vi-kubwa
                  CL8-book CL8-big
                  (Class 7/8: ki-/vi-, singular/plural)

FLEx representation:
- Noun: class 8 (plural of class 7)
- Adjective: agrees with class 8

Apertium representation:
- Co-feature: BantuNounClass.CL8
- Maps to FLEx features: BantuPL.CL7_8

Rule requirements:
- DisjointFeatureSet mapping
- Number (plural) + noun class conflated
- Agreement on adjective prefix
```

#### 5.1.5 Feature Ranking (Syncretism)

**Test Case: German Definite Article**
```
Context: Looking up "die" for translation to English
Possibilities:
1. Feminine singular nominative (gender rank 3)
2. Plural all genders (number rank 1) ← CHOOSE THIS
3. Feminine singular accusative (case rank 2)

Rule requirements:
- Feature ranking attributes
- Prefer number over case over gender
- Select most common form when ambiguous
```

#### 5.1.6 Word Insertion

**Test Case: Article Insertion (Chinese-English)**
```
Source (Chinese): 猫
                  māo
                  cat
Target (English): the cat / a cat

Rule requirements:
- Insert determiner based on definiteness
- May need discourse context
- Default to indefinite article
```

#### 5.1.7 Category Change

**Test Case: Definiteness Encoding (Swedish-German)**
```
Source (Swedish): hus-et
                  house-DEF (definiteness as suffix)
Target (German): das Haus
                 the house (definiteness as separate word)

Rule requirements:
- Extract definiteness from suffix
- Generate separate determiner word
- Feature reassignment: affix → word
```

### 5.2 Extended Test Cases (20 Languages)

#### Test Language 1: Mandarin Chinese (Isolating, Tonal, Classifiers)

**Linguistic Features:**
- SVO word order
- Lexical tone (4 tones + neutral)
- Obligatory classifiers with numbers
- Serial verb constructions
- Aspect particles

**Test Sentence:**
```
我买了三本书
wǒ mǎi le sān běn shū
I buy ASP three CL book
"I bought three books"

Challenges for Rule Assistant:
❌ Tone not represented
❌ Classifier 本 (běn) for bound volumes
✅ Aspect particle 了 (le) - can be handled as word
✅ Word order (SVO) - supported
```

**Required Rule Components:**
- Classifier insertion based on noun semantics
- Aspect particle as separate word
- Number word handling

#### Test Language 2: Turkish (Agglutinative, Vowel Harmony)

**Linguistic Features:**
- SOV word order
- Extensive agglutinative suffixation
- Vowel harmony (palatal and labial)
- Evidential system

**Test Sentence:**
```
Kitap-lar-ı-m-ız-da
book-PL-ACC-1SG-PL-LOC
"in our books"

Vowel harmony:
- Back vowel stem: kız-lar-da "in the girls"
- Front vowel stem: kız → should be kız (mixed), but:
  Actually: göz-ler-de "in the eyes" (front vowels)

Challenges:
❌ Vowel harmony - suffix vowels must harmonize with stem
✅ Suffix chain - supported
✅ Possessive + plural - multiple suffixes supported
```

**Required Rule Components:**
- Vowel harmony feature on stems (back/front)
- Allomorphic suffix selection (-lar/-ler, -da/-de)
- Suffix ordering constraints

#### Test Language 3: Swahili (Bantu, Noun Classes, Agglutinative Verbs)

**Linguistic Features:**
- SVO word order
- 15+ noun classes with agreement
- Prefix-heavy morphology
- Polypersonal agreement on verbs

**Test Sentence:**
```
Wa-toto wa-wili wa-zuri wa-na-soma vi-tabu vi-kubwa
CL2-child CL2-two CL2-good CL2-PRES-read CL8-book CL8-big
"Two good children are reading big books"

Challenges:
✅ Noun class agreement - SUPPORTED via DisjointFeatureSets
✅ Prefix chains on verb: wa-na-soma (SUBJ-PRES-read)
✅ Agreement across NP (wa-toto wa-wili wa-zuri)
✅ Multiple noun classes in one sentence
```

**Required Rule Components:**
- DisjointFeatureSet for noun classes
- Verb prefix chain (subject + tense + object)
- Cross-NP agreement

#### Test Language 4: Arabic (Root-Pattern, Broken Plurals)

**Linguistic Features:**
- VSO word order
- Consonantal roots with vocalic patterns
- Broken plurals
- Templatic morphology

**Test Sentence:**
```
kataba     l-kātib-u      l-kitāb-a
write.PAST the-writer-NOM the-book-ACC
"The writer wrote the book"

Root: k-t-b (writing concept)
- kataba (CaCaCa) = "he wrote"
- kātib (CāCiC) = "writer"
- kitāb (CiCāC) = "book"
- kutub (CuCuC) = "books" (broken plural, not *kitāb-īn)

Challenges:
❌ Root-and-pattern morphology - NOT SUPPORTED
❌ Broken plurals - NOT SUPPORTED (would need stored forms)
✅ VSO word order - can be handled
✅ Case marking - can be handled
```

**Required Rule Components:**
- Root-pattern templatic system (long-term)
- Broken plural lexical storage (short-term workaround)
- VSO word order rules

#### Test Language 5: Tagalog (Austronesian, Infixation, Voice)

**Linguistic Features:**
- Verb-initial (VSO/VOS flexible)
- Extensive infixation
- Voice/focus system (actor, patient, locative, benefactive)
- Reduplication

**Test Sentence:**
```
B<um>ili ang babae ng isda sa tindahan
<AV>buy NOM woman ACC fish LOC store
"The woman bought fish at the store"

Infixation: bili "buy" → b-um-ili (actor voice)
Reduplication: bili → bi-bili "will buy"

Challenges:
❌ -um- infix - NOT SUPPORTED (planned)
❌ Reduplication - NOT SUPPORTED
✅ Voice system - can be handled with features
✅ Case particles (ang, ng, sa) - can be handled as words
```

**Required Rule Components:**
- Infix support (type="infix" with position)
- Reduplication mechanism
- Voice features on verbs

#### Test Language 6: Russian (Fusional, Rich Case System)

**Linguistic Features:**
- SVO word order (flexible)
- 6 cases with extensive fusion
- Gender-number-case agreement
- Aspect pairs (perfective/imperfective)

**Test Sentence:**
```
Krasiv-ye dom-a
beautiful-NOM.PL house-NOM.PL
"beautiful houses"

Genitive example:
krasiv-yx dom-ov (GEN.PL - different endings)

Challenges:
✅ Case-number-gender fusion - SUPPORTED
✅ Agreement patterns - SUPPORTED
✅ Syncretism - SUPPORTED via feature ranking
❌ Aspect pairs - can be handled as separate lexemes
```

**Required Rule Components:**
- Multi-feature fusion (gender + number + case)
- Feature ranking for ambiguous forms
- Flexible word order rules

#### Test Language 7: Finnish (Uralic, Vowel Harmony, 15 Cases)

**Linguistic Features:**
- SVO word order
- 15 cases (possibly more in analysis)
- Vowel harmony (back/front)
- Consonant gradation

**Test Sentence:**
```
talo-i-ssa
house-PL-INESS
"in houses" (back harmony: a, o)

käsi-ssä
hand-INESS
"in hand" (front harmony: ä, i)

Challenges:
✅ Extensive case system - SUPPORTED
❌ Vowel harmony - NOT SUPPORTED
❌ Consonant gradation - NOT SUPPORTED
✅ Suffix chains - SUPPORTED
```

**Required Rule Components:**
- Vowel harmony class on stems
- Harmonic suffix allomorphs
- Consonant gradation rules (complex)

#### Test Language 8: Japanese (Agglutinative, SOV, Honorifics)

**Linguistic Features:**
- SOV word order
- Subject/object particles
- Honorific system
- Numeral classifiers

**Test Sentence:**
```
Tanaka-san-ga hon-o san-satsu yon-da
Tanaka-HON-SUBJ book-OBJ three-CL read-PAST
"Mr. Tanaka read three books"

Challenges:
✅ SOV word order - SUPPORTED
✅ Particles as separate words - SUPPORTED
❌ Classifiers (satsu for books) - NOT SUPPORTED
✅ Honorifics as affixes - can be SUPPORTED
```

**Required Rule Components:**
- Classifier system (semantic features on nouns)
- Honorific features
- Particle insertion/deletion

#### Test Language 9: Welsh (Celtic, Consonant Mutations, VSO)

**Linguistic Features:**
- VSO word order
- Initial consonant mutations (soft, nasal, aspirate)
- Preposed particles
- Gender agreement

**Test Sentence:**
```
Mae'r  gath  fach yn cysgu
is-the cat   small PROG sleep
"The small cat is sleeping"

With possessive:
ei  gath (his cat) - soft mutation: c → g
ei  chath (her cat) - aspirate mutation: c → ch

Challenges:
✅ VSO word order - SUPPORTED
❌ Consonant mutations - NOT SUPPORTED
✅ Gender agreement - SUPPORTED
✅ Particle system - SUPPORTED
```

**Required Rule Components:**
- Mutation trigger features
- Allomorphic forms for mutated consonants
- VSO word order rules

#### Test Language 10: Quechua (Agglutinative, SOV, Evidentials)

**Linguistic Features:**
- SOV word order
- Agglutinative suffixation
- Evidential system (direct, reportative, inferential)
- Switch-reference

**Test Sentence:**
```
Para-sha-n
rain-DIRECT-3SG
"It's raining" (I see it)

Para-shi
rain-REPORTATIVE
"It's raining" (I heard)

Challenges:
✅ SOV word order - SUPPORTED
✅ Suffix chains - SUPPORTED
✅ Evidentials as affixes - CAN BE SUPPORTED
❌ Switch-reference - NOT SUPPORTED
```

**Required Rule Components:**
- Evidential features
- Default evidential for L1 without evidentials
- Switch-reference markers (complex)

#### Test Language 11: Hebrew (Semitic, Root-Pattern, VSO)

**Linguistic Features:**
- VSO word order
- Triconsonantal roots
- Vocalic patterns
- Construct state (noun-noun possession)

**Test Sentence:**
```
katav     ha-sofer    et   ha-sefer
write.PAST the-writer ACC  the-book
"The writer wrote the book"

Root: k-t-v
- katav (CaCaC) = "he wrote"
- sofer (CoCeC) = "writer"
- sefer (CeFeR) = "book"

Challenges:
❌ Root-pattern - NOT SUPPORTED
✅ VSO word order - SUPPORTED
✅ Definiteness marker ha- - can be handled as prefix
✅ Construct state - can be handled with rules
```

**Required Rule Components:**
- Root-pattern system (fundamental)
- Pattern selection based on features
- Construct state handling

#### Test Language 12: Vietnamese (Isolating, Tonal, Classifiers)

**Linguistic Features:**
- SVO word order
- No inflectional morphology
- 6 tones
- Obligatory classifiers

**Test Sentence:**
```
Tôi mua ba   cái sách
I   buy three CL  book
"I bought three books"

Challenges:
✅ SVO word order - SUPPORTED
✅ No morphology - SUPPORTED (simple)
❌ Tones - NOT SUPPORTED
❌ Classifiers - NOT SUPPORTED
✅ Aspect markers as particles - SUPPORTED
```

**Required Rule Components:**
- Classifier system
- Tone representation (orthographic)
- Serial verb handling

#### Test Language 13: Georgian (Kartvelian, Polypersonal, Complex Case)

**Linguistic Features:**
- SOV word order (flexible)
- Polypersonal agreement
- Complex case system
- Circumfixes

**Test Sentence:**
```
v-xatav
I-paint
"I paint"

m-xatav-s
me-paint-3SG
"he/she paints me"

Challenges:
✅ Polypersonal prefixes - CAN BE SUPPORTED
❌ Complex case alignment - NEEDS WORK
❌ Circumfixes - NOT SUPPORTED (planned)
```

**Required Rule Components:**
- Multiple agreement prefixes
- Case feature handling
- Circumfix support

#### Test Language 14: Greenlandic (Polysynthetic, Ergative, Incorporation)

**Linguistic Features:**
- SOV/flexible word order
- Extensive incorporation
- Polysynthetic structure
- Ergative alignment

**Test Sentence:**
```
Angut-ip     aallaat     qimmiq      taku-aa
man-ERG      makes       dog.ABS     see-3SG.3SG
"The man sees the dog"

Incorporation:
qimmi-qar-puq
dog-have-3SG
"He has a dog" (qimmiq "dog" incorporated)

Challenges:
✅ Ergative case - can be handled as feature
❌ Noun incorporation - NOT SUPPORTED
✅ Suffix chains - SUPPORTED
❌ Polysynthetic complexity - PARTIAL SUPPORT
```

**Required Rule Components:**
- Incorporation mechanism
- Ergative case features
- Long suffix chains

#### Test Language 15: Navajo (Athabaskan, Polysynthetic, Complex Verb)

**Linguistic Features:**
- SOV word order
- Highly complex verb template (10+ positions)
- Classificatory verbs
- Tonal

**Test Sentence:**
```
Ashkii    at'ééd    yiyiiłtsą
boy.NOM   girl.ACC  3.3.see.PERF
"The boy saw the girl"

Verb structure: yi-yii-ł-tsą
- yi: 3rd person object
- yii: perfective
- ł: classifier
- tsą: root "see"

Challenges:
✅ Prefix chains - CAN BE SUPPORTED
❌ Complex templatic positions - NEEDS WORK
❌ Classifiers (verbal) - NOT SUPPORTED
❌ Tone - NOT SUPPORTED
```

**Required Rule Components:**
- Complex prefix template system
- Verbal classifiers
- Tone (less critical for transfer)

#### Test Language 16: Mohawk (Iroquoian, Polysynthetic, Incorporation)

**Linguistic Features:**
- Polysynthetic
- Noun incorporation
- Polypersonal agreement
- Complex pronominal system

**Test Sentence:**
```
Wa'-ke-nákt-a-hninu-'
PAST-1sg-bread-Ø-buy-PUNC
"I bought bread"

Challenges:
✅ Polypersonal agreement - CAN BE SUPPORTED
❌ Noun incorporation (nákt "bread") - NOT SUPPORTED
✅ Pronominal prefixes - CAN BE SUPPORTED
```

**Required Rule Components:**
- Incorporation (N becomes part of V)
- Polypersonal agreement
- Complex verb template

#### Test Language 17: Hungarian (Uralic, Vowel Harmony, Agglutinative)

**Linguistic Features:**
- SVO word order
- 18+ cases
- Vowel harmony (back/front)
- Definite vs. indefinite conjugation

**Test Sentence:**
```
ház-ak-ban
house-PL-INESS
"in houses" (back harmony)

kéz-ben
hand-INESS
"in hand" (front harmony)

Challenges:
✅ Extensive case - SUPPORTED
❌ Vowel harmony - NOT SUPPORTED
✅ Definite/indefinite conjugation - can be handled
```

**Required Rule Components:**
- Vowel harmony
- Case suffix chains
- Conjugation paradigm selection

#### Test Language 18: Yoruba (Niger-Congo, Tonal, Serial Verbs)

**Linguistic Features:**
- SVO word order
- Grammatical tone
- Serial verb constructions
- No inflectional morphology

**Test Sentence:**
```
Ó    mú  ìwé   wá
3sg  take book come
"He brought a book"

Tonal: ó (high) = he, ò (low) = it
mú (high-low) "take" + wá (mid-low) "come" = serial verb

Challenges:
✅ SVO word order - SUPPORTED
❌ Tone (grammatical) - NOT SUPPORTED
❌ Serial verbs - NOT SUPPORTED
✅ No morphology (simple) - SUPPORTED
```

**Required Rule Components:**
- Tone features
- Serial verb multi-word patterns
- Tonal morphology rules

#### Test Language 19: Khmer (Austroasiatic, Infixation, Registers)

**Linguistic Features:**
- SVO word order
- Infixation
- Reduplication
- Register/politeness system

**Test Sentence:**
```
Kɲom baən tɨɲ siǝwphɨw
I    PAST buy book
"I bought a book"

Infixation example (not in sentence):
dae "walk" → d-ɔm-nae "take for a walk"

Challenges:
✅ SVO word order - SUPPORTED
❌ Infixation - NOT SUPPORTED (planned)
❌ Reduplication - NOT SUPPORTED
✅ Register particles - can be handled
```

**Required Rule Components:**
- Infixation
- Reduplication
- Register/politeness features

#### Test Language 20: Maori (Austronesian, VSO, Particles)

**Linguistic Features:**
- VSO word order
- Particle-heavy
- Reduplication
- Passive focus system

**Test Sentence:**
```
Kei  te   kai  te  tamaiti   i   te  āporo
PROG      eat      child     ACC     apple
"The child is eating the apple"

Reduplication:
kai "eat" → kai-kai "eating (continuous)"

Challenges:
✅ VSO word order - SUPPORTED
✅ Particle system - SUPPORTED
❌ Reduplication - NOT SUPPORTED
✅ Passives with particles - can be handled
```

**Required Rule Components:**
- VSO rules
- Particle insertion
- Reduplication
- Passive voice system

### 5.3 Minimal Functionality Requirements per Test Language

| Language | Critical Features | Current Support | Gap Priority |
|----------|------------------|-----------------|--------------|
| Mandarin | Classifiers, tone | 40% | HIGH (classifiers) |
| Turkish | Vowel harmony, suffixes | 60% | HIGH (harmony) |
| Swahili | Noun classes, prefixes | 90% | LOW (well supported) |
| Arabic | Root-pattern, broken plurals | 30% | HIGH (root-pattern) |
| Tagalog | Infixation, voice | 50% | HIGH (infixes) |
| Russian | Case fusion, agreement | 95% | LOW (excellent) |
| Finnish | Vowel harmony, cases | 70% | HIGH (harmony) |
| Japanese | Classifiers, SOV | 70% | MEDIUM (classifiers) |
| Welsh | Mutations, VSO | 60% | MEDIUM (mutations) |
| Quechua | Evidentials, agglutination | 75% | MEDIUM (evidentials) |
| Hebrew | Root-pattern, VSO | 35% | HIGH (root-pattern) |
| Vietnamese | Classifiers, tone | 50% | MEDIUM (classifiers) |
| Georgian | Polypersonal, circumfixes | 60% | MEDIUM (circumfixes) |
| Greenlandic | Incorporation, polysynthetic | 40% | HIGH (incorporation) |
| Navajo | Complex verb template | 45% | MEDIUM (specialized) |
| Mohawk | Incorporation | 40% | HIGH (incorporation) |
| Hungarian | Vowel harmony, cases | 70% | HIGH (harmony) |
| Yoruba | Tone, serial verbs | 50% | MEDIUM (tone/serials) |
| Khmer | Infixation | 50% | HIGH (infixation) |
| Maori | Reduplication | 70% | MEDIUM (reduplication) |

---

## 6. Evaluation Criteria for Linguistic Adequacy

### 6.1 Typological Coverage Metrics

**Metric 1: Language Type Coverage**
- Target: ≥80% support for each major type (isolating, agglutinative, fusional, polysynthetic)
- Current: Fusional 90%, Agglutinative 75%, Isolating 60%, Polysynthetic 40%
- **Gap: Need to improve polysynthetic and isolating support**

**Metric 2: Geographic Distribution**
- Target: At least basic support for languages from all continents
- Current: Strong in Europe, partial in Africa/Asia, weak in Americas/Oceania
- **Gap: Need indigenous American and Oceanian language support**

**Metric 3: Speaker Population Coverage**
- Target: ≥90% of world's speakers can use system for their language family
- Current: ~85% (strong Indo-European, Sino-Tibetan, Niger-Congo; weak Austronesian, Turkic, Semitic)
- **Gap: Need Austronesian infixation, Turkic vowel harmony, Semitic root-pattern**

### 6.2 Feature Coverage Checklist

**Morphological Features:**
- ✅ Prefixes
- ✅ Suffixes
- ⏳ Infixes (planned)
- ⏳ Circumfixes (planned)
- ❌ Reduplication (full)
- ❌ Reduplication (partial)
- ❌ Root-and-pattern
- ❌ Ablaut
- ✅ Zero morphology / unmarked

**Syntactic Features:**
- ✅ Word order changes (all 6 basic types possible)
- ✅ Word insertion
- ✅ Word deletion
- ✅ Head switching
- ❌ Noun incorporation
- ❌ Serial verb constructions
- ❌ Classifier systems

**Agreement Features:**
- ✅ Gender
- ✅ Number
- ✅ Case
- ✅ Person (via features)
- ✅ Multiple simultaneous agreements
- ✅ Controller-target relationships
- ✅ Long-distance agreement
- ❌ Polypersonal agreement (multiple objects)

**Phonological Features:**
- ❌ Tone
- ❌ Vowel harmony
- ❌ Consonant harmony
- ❌ Consonant mutations
- ❌ Stress patterns
- ❌ Consonant gradation

**Special Systems:**
- ✅ Disjoint feature sets (Bantu)
- ✅ Feature ranking (syncretism)
- ✅ Unmarked defaults
- ❌ Evidentials
- ❌ Classifiers/counters
- ❌ Honorific/social register

### 6.3 Quality Criteria

**Criterion 1: Naturalness**
- Generated forms should be natural and idiomatic
- Not just grammatical, but preferred by native speakers
- Measure: Native speaker acceptability judgments

**Criterion 2: Coverage of Paradigm**
- System should handle full range of forms in a paradigm
- Not just common forms, but also rare/marked forms
- Measure: Paradigm completion rate

**Criterion 3: Edge Case Handling**
- Irregular forms
- Defective paradigms
- Suppletion
- Measure: Success rate on non-canonical examples

**Criterion 4: Typological Appropriateness**
- Rules should reflect actual linguistic patterns
- Not impose unnatural analyses
- Measure: Linguistic expert review

**Criterion 5: Scalability**
- System should work for small and large lexicons
- Performance should not degrade with complexity
- Measure: Processing time for large projects

### 6.4 Evaluation Methodology

**Phase 1: Expert Linguistic Review**
1. Linguist analyzes rule capabilities
2. Maps to typological database (WALS, Grambank)
3. Identifies gaps
4. Prioritizes based on speaker populations and typological importance

**Phase 2: Test Suite Validation**
1. Create minimal test pairs for each phenomenon
2. Attempt to model with Rule Assistant
3. Document successes and failures
4. Assign capability scores (0-100%)

**Phase 3: Real-World Language Projects**
1. Select 20 typologically diverse languages
2. Attempt to build small translation system for each
3. Document obstacles and workarounds
4. Measure completeness of linguistic coverage

**Phase 4: User Feedback**
1. Survey field linguists using system
2. Collect reports of unsupported phenomena
3. Prioritize based on frequency of requests
4. Iterate on improvements

---

## 7. Future Requirements

### 7.1 Immediate Priorities (Next 6 Months)

1. **Implement Infixation Support**
   - Timeline: 3-4 weeks
   - Impact: HIGH - enables Austronesian languages (400M speakers)
   - See Implementation Plan §2

2. **Implement Circumfixation Support**
   - Timeline: 3-4 weeks
   - Impact: MEDIUM - enables Germanic participles, some Afroasiatic
   - See Implementation Plan §2

3. **Add Vowel Harmony Framework**
   - Timeline: 4-6 weeks
   - Impact: HIGH - enables Turkic (170M speakers), Uralic (25M speakers)
   - Requires: Phonological feature extension to FLEx data model

4. **Develop Classifier System**
   - Timeline: 4-6 weeks
   - Impact: HIGH - enables East/Southeast Asian languages (2B+ speakers)
   - Requires: Semantic features on nouns

### 7.2 Medium-Term Priorities (6-12 Months)

5. **Root-and-Pattern Morphology**
   - Timeline: 8-12 weeks
   - Impact: HIGH - enables Semitic languages (500M speakers)
   - Requires: Major architectural extension

6. **Reduplication Support**
   - Timeline: 6-8 weeks
   - Impact: MEDIUM-HIGH - widespread in Austronesian, Niger-Congo, Americas
   - Requires: Phonological rule component

7. **Noun Incorporation**
   - Timeline: 8-12 weeks
   - Impact: MEDIUM - critical for polysynthetic languages, smaller populations
   - Requires: Architectural changes to word-level model

8. **Serial Verb Construction Support**
   - Timeline: 4-6 weeks
   - Impact: MEDIUM - common in isolating languages
   - Requires: Multi-verb predicate handling

### 7.3 Long-Term Priorities (12-24 Months)

9. **Tone Support**
   - Timeline: 12-16 weeks
   - Impact: MEDIUM - critical for accuracy, less critical for basic MT
   - Requires: Suprasegmental feature layer

10. **Polypersonal Agreement**
    - Timeline: 6-8 weeks
    - Impact: MEDIUM - needed for some agglutinative and polysynthetic
    - Requires: Multiple agreement target handling

11. **Evidential System Support**
    - Timeline: 4-6 weeks
    - Impact: MEDIUM - common but can use defaults
    - Requires: Examples and documentation mostly

12. **Advanced Phonological Processes**
    - Consonant mutations
    - Consonant gradation
    - Stress assignment
    - Timeline: Variable, 4-12 weeks each
    - Impact: LOW-MEDIUM - language-specific, often can use allomorphs

### 7.4 Research and Exploration

**Areas for Future Investigation:**

1. **Machine Learning Augmentation**
   - Can ML predict feature rankings from corpus data?
   - Can ML suggest likely rules based on language typology?
   - Can ML identify paradigm patterns automatically?

2. **Corpus-Driven Rule Development**
   - Extract common patterns from parallel corpora
   - Suggest rules based on translation pairs
   - Validate rules against corpus examples

3. **Typological Database Integration**
   - Link to WALS (World Atlas of Language Structures)
   - Suggest likely features based on language family
   - Warn about unsupported phenomena for given language

4. **Universal Dependencies Integration**
   - Map to UD syntactic relations
   - Use UD treebanks for validation
   - Generate rules from UD structures

---

## 8. Recommendations

### 8.1 For Developers

1. **Prioritize High-Impact, High-Population Features**
   - Infixes and circumfixes (Austronesian, Germanic) - already planned ✅
   - Vowel harmony (Turkic, Uralic) - critical addition
   - Classifiers (East/Southeast Asian) - very high impact

2. **Create Language Family Templates**
   - Turkic template (vowel harmony, SOV, agglutination)
   - Bantu template (noun classes, prefixes) - exists ✅
   - Romance template (gender, case, agreement) - effectively exists
   - Austronesian template (infixes, voice, reduplication)

3. **Improve Documentation with Linguistic Examples**
   - Each feature should have examples from 3+ languages
   - Link to linguistic literature
   - Explain the *why* not just the *how*

4. **Add Typological Warnings**
   - When user selects language, warn about unsupported features
   - "Note: Tagalog uses infixation extensively. This is planned but not yet supported."

### 8.2 For Linguists

1. **Contribute Example Rules**
   - Create example rules for underrepresented language types
   - Document workarounds for unsupported features
   - Share templates for language families

2. **Test with Minority Languages**
   - Don't just test with major languages
   - Small language communities benefit most from these tools
   - Document success stories and challenges

3. **Provide Linguistic Validation**
   - Review generated rules for linguistic naturalness
   - Identify over-generation or under-generation
   - Suggest improvements to linguistic coverage

4. **Create Pedagogical Materials**
   - Tutorials for specific language families
   - Workshops for SIL field linguists
   - Case studies of successful projects

### 8.3 For Project Management

1. **Balance European and Non-European Languages**
   - Current examples are heavily European
   - Need more Asian, African, American, Oceanian examples
   - Ensure typological diversity in test suite

2. **Engage with Language Communities**
   - Partner with language communities using FLExTrans
   - Gather requirements from actual users
   - Prioritize features based on real-world needs

3. **Track Typological Coverage Metrics**
   - Regularly assess coverage across language types
   - Set targets for improvement (e.g., "80% support for all major types by 2026")
   - Report on progress

4. **Invest in Phonological Component**
   - Many gaps are phonological (tone, vowel harmony, mutations)
   - Consider adding phonological rule module
   - This would unlock many language families

### 8.4 Success Stories to Amplify

1. **Bantu Noun Classes (SplitBantu.xml)**
   - This is sophisticated and linguistically sound
   - Demonstrates the system can handle complex typological features
   - Should be highlighted in publications/presentations

2. **Feature Ranking for Syncretism**
   - Elegant solution to real-world problem
   - Shows linguistic sophistication
   - Could be extended to other ambiguous cases

3. **Flexible Agreement System**
   - α, β, γ matching is powerful and intuitive
   - Handles long-distance agreement well
   - Foundation for many other phenomena

---

## 9. Conclusion

The FLExTrans Rule Assistant demonstrates strong linguistic capabilities for Indo-European fusional languages and Bantu noun class systems. The disjoint feature set mechanism (SplitBantu.xml) and feature ranking system showcase sophisticated linguistic understanding.

**Current Strengths:**
- Excellent support for agreement, case, and gender systems
- Sophisticated handling of syncretism and feature conflicts
- Flexible word order transformation
- Strong affix support (prefixes, suffixes)

**Critical Gaps Identified:**
- Infixes (HIGH PRIORITY) - 400M+ Austronesian speakers
- Circumfixes (HIGH PRIORITY) - Germanic, Afroasiatic
- Vowel harmony (HIGH PRIORITY) - 200M+ Turkic/Uralic speakers
- Root-and-pattern (HIGH PRIORITY) - 500M+ Semitic speakers
- Classifiers (HIGH PRIORITY) - 2B+ East/Southeast Asian speakers
- Reduplication (MEDIUM PRIORITY) - widespread globally
- Noun incorporation (MEDIUM PRIORITY) - polysynthetic languages

**Recommended Focus Areas:**
1. Complete planned infix/circumfix implementation (already in progress)
2. Add vowel harmony support (architectural extension needed)
3. Develop classifier system (new feature type)
4. Create language family templates (Turkic, Austronesian, Semitic)
5. Expand test suite to cover 20+ typologically diverse languages

By addressing these gaps, the Rule Assistant can expand from strong Indo-European/Bantu coverage to truly global linguistic coverage, serving the world's language diversity.

---

## Appendix A: Typological Feature Inventory

### Agreement Features
- Gender (masculine, feminine, neuter, common, etc.)
- Number (singular, dual, trial, paucal, plural)
- Case (nominative, accusative, ergative, absolutive, dative, genitive, locative, etc.)
- Person (1st, 2nd, 3rd; inclusive/exclusive)
- Animacy (animate, inanimate, human, non-human)
- Definiteness (definite, indefinite, specific)
- Noun class/classifier (Bantu classes, numeral classifiers, etc.)

### Tense/Aspect/Mood (TAM)
- Tense (past, present, future, remote past, recent past, etc.)
- Aspect (perfective, imperfective, progressive, habitual, etc.)
- Mood (indicative, subjunctive, conditional, imperative, etc.)
- Evidentiality (direct, indirect, reportative, inferential, etc.)

### Voice and Valency
- Voice (active, passive, middle, antipassive, causative, applicative)
- Transitivity (transitive, intransitive, ditransitive)
- Valency-changing operations (causative, applicative, benefactive)

### Word Order Patterns (All 6 basic types)
- SVO (Subject-Verb-Object): English, Spanish, Mandarin
- SOV (Subject-Object-Verb): Japanese, Turkish, Hindi
- VSO (Verb-Subject-Object): Welsh, Arabic, Tagalog
- VOS (Verb-Object-Subject): Malagasy, Fijian
- OVS (Object-Verb-Subject): Hixkaryana (rare)
- OSV (Object-Subject-Verb): Warao (rare)

### Morphological Types
- Isolating (minimal morphology): Mandarin, Vietnamese
- Agglutinative (one meaning per morpheme): Turkish, Swahili, Finnish
- Fusional (multiple meanings per morpheme): Spanish, Russian, Arabic
- Polysynthetic (sentence-like words): Inuktitut, Mohawk, Greenlandic

---

## Appendix B: References and Resources

### Linguistic Typology References

**Standard Typology Resources:**
- Comrie, Bernard. 1989. *Language Universals and Linguistic Typology*. University of Chicago Press.
- Croft, William. 2002. *Typology and Universals*. Cambridge University Press.
- Dryer, Matthew S. and Martin Haspelmath (eds.). 2013. *The World Atlas of Language Structures Online*. Leipzig: Max Planck Institute for Evolutionary Anthropology. (Available at http://wals.info)

**Morphology:**
- Haspelmath, Martin and Andrea Sims. 2010. *Understanding Morphology*. Hodder Education.
- Spencer, Andrew and Arnold Zwicky (eds.). 2001. *The Handbook of Morphology*. Blackwell.

**Agreement Systems:**
- Corbett, Greville. 2006. *Agreement*. Cambridge University Press.
- Corbett, Greville. 2012. *Features*. Cambridge University Press.

**Specific Language Families:**
- **Bantu:** Nurse, Derek and Gérard Philippson (eds.). 2003. *The Bantu Languages*. Routledge.
- **Austronesian:** Adelaar, Alexander and Nikolaus Himmelmann (eds.). 2005. *The Austronesian Languages of Asia and Madagascar*. Routledge.
- **Turkic:** Johanson, Lars and Éva Csató (eds.). 1998. *The Turkic Languages*. Routledge.

### Online Databases

- **WALS Online:** http://wals.info - World Atlas of Language Structures
- **Grambank:** https://grambank.clld.org - Typological database
- **Glottolog:** https://glottolog.org - Comprehensive language catalog
- **Universal Dependencies:** https://universaldependencies.org - Syntactic annotation standard

### FLEx and Apertium Resources

- **FLEx Help:** FieldWorks Language Explorer documentation
- **Apertium Wiki:** https://wiki.apertium.org - MT system documentation
- **FLExTrans GitHub:** https://github.com/rmlockwood/FLExTrans - Project repository

---

**Document Metadata:**
- **Version:** 1.0
- **Last Updated:** 2025-11-22
- **Contributors:** Linguistic Analysis Team
- **Review Status:** Initial draft pending review by field linguists
- **Next Review:** After implementation of infixes/circumfixes

---

*This document is part of the FLExTrans project documentation suite. For technical implementation details, see the RuleAssistant_Implementation_Plan.md. For developer guidance, see LINGUISTIC_GUIDE_FOR_DEVELOPERS.md.*
