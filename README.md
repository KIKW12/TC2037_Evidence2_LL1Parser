# Musical Language Parser

## Description
The language I chose was a Musical Language that captures basic music notation elements. The language allows for representing musical compositions with individual notes, chords, and sequences of musical elements.

This formal language is inspired by common music notation and could be helpful for simplified music representation, algorithmic composition, or educational purposes to demonstrate music theory concepts. The grammar provides a structured way to represent musical elements that could be used as an intermediate representation for music processing systems.

The **modeling technique** I decided to use was a Context-Free Grammar (CFG) to represent my solution, as CFGs are well-suited for representing hierarchical structures like musical phrases and nested elements like chords. As mentioned in Aho et al. (2006), context-free grammars are powerful tools for modeling languages that contain recursive structures, which is essential for representing complex musical compositions.

## Model of the Solution

I created a context-free grammar that handles various musical elements:

### Initial Grammar (with Ambiguity and Left Recursion)
```
S → Composition
Composition → Phrase | Composition Phrase
Phrase → NoteSequence | ChordSequence | Phrase Phrase
NoteSequence → Note | NoteSequence Note
Note → Pitch Duration
Pitch → 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G'
Duration → 'whole' | 'half' | 'quarter' | 'eighth' | 'sixteenth'
ChordSequence → Chord | ChordSequence Chord
Chord → '(' PitchList ')' Duration
PitchList → Pitch | Pitch PitchList
```

This initial grammar had issues with ambiguity (multiple parse trees for the same string) and left recursion (making it unsuitable for top-down parsing).

### Step-by-Step Ambiguity Elimination

#### Step 1: Identify Ambiguities
The main sources of ambiguity in the initial grammar are:
1. **Phrase Structure Ambiguity**: The rule `Phrase → Phrase Phrase` allows multiple ways to group phrases.
2. **Composition vs Phrase Ambiguity**: The rules `Composition → Phrase | Composition Phrase` and `Phrase → NoteSequence | ChordSequence | Phrase Phrase` create overlap in what these non-terminals can generate.

For example, the string "C quarter D half" could be parsed in multiple ways:
- As a Phrase containing two separate Note Phrases
- As a NoteSequence with two consecutive Notes

#### Step 2: Restructure Phrase Rule
Remove the recursive rule `Phrase → Phrase Phrase` which allows for multiple groupings:
```
Phrase → NoteSequence | ChordSequence
```

#### Step 3: Add Hierarchical Structure
Introduce clear distinctions between levels of musical elements:
```
Composition → PhraseList
PhraseList → Phrase | Phrase PhraseList
```

#### Step 4: Grammar after Ambiguity Elimination
```
S → Composition
Composition → PhraseList
PhraseList → Phrase | Phrase PhraseList
Phrase → NoteSequence | ChordSequence
NoteSequence → Note | Note NoteSequence
Note → Pitch Duration
Pitch → 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G'
Duration → 'whole' | 'half' | 'quarter' | 'eighth' | 'sixteenth'
ChordSequence → Chord | Chord ChordSequence
Chord → '(' PitchList ')' Duration
PitchList → Pitch | Pitch PitchList
```

The restructured grammar ensures that each valid string has exactly one parse tree, eliminating ambiguity.

### Syntactic Tree Example - Ambiguity Resolution

For the string "C quarter D half":

**Before Ambiguity Elimination (Multiple Parse Trees Possible):**
```
       Phrase
      /      \
 Phrase       Phrase
   |           |
NoteSeq       NoteSeq
   |           |
  Note         Note
 /   \        /   \
Pitch Dur    Pitch Dur
  |    |      |     |
 'C' 'quarter' 'D' 'half'
```

OR

```
       Phrase
         |
      NoteSeq
      /     \
   NoteSeq   Note
     |      /   \
    Note   Pitch Dur
   /   \    |     |
 Pitch Dur  'D'  'half'
   |    |
  'C' 'quarter'
```

**After Ambiguity Elimination (Only One Parse Tree):**
```
       Composition
           |
       PhraseList
           |
         Phrase
           |
       NoteSequence
       /         \
     Note       NoteSequence
    /   \           |
 Pitch  Dur        Note
   |     |        /   \
  'C' 'quarter' Pitch  Dur
                  |     |
                 'D'  'half'
```

### Step-by-Step Left Recursion Elimination

After eliminating ambiguity, we still have left recursion in the following rules:
```
PhraseList → Phrase | Phrase PhraseList
NoteSequence → Note | Note NoteSequence
ChordSequence → Chord | Chord ChordSequence
PitchList → Pitch | Pitch PitchList
```

#### Step 1: Left Recursion Elimination Algorithm
For a rule of the form `A → Aα | β`, we transform it to:
```
A → βA'
A' → αA' | ε
```
where ε represents an empty string.

#### Step 2: Transform PhraseList Rule
Original: `PhraseList → Phrase | Phrase PhraseList`
Transformed:
```
PhraseList → Phrase PhraseList_Prime
PhraseList_Prime → Phrase PhraseList_Prime | ε
```

#### Step 3: Transform NoteSequence Rule
Original: `NoteSequence → Note | Note NoteSequence`
Transformed:
```
NoteSequence → Note NoteSequence_Prime
NoteSequence_Prime → Note NoteSequence_Prime | ε
```

#### Step 4: Transform ChordSequence Rule
Original: `ChordSequence → Chord | Chord ChordSequence`
Transformed:
```
ChordSequence → Chord ChordSequence_Prime
ChordSequence_Prime → Chord ChordSequence_Prime | ε
```

#### Step 5: Transform PitchList Rule
Original: `PitchList → Pitch | Pitch PitchList`
Transformed:
```
PitchList → Pitch PitchList_Prime
PitchList_Prime → Pitch PitchList_Prime | ε
```

#### Step 6: Final Grammar (after Left Recursion Elimination)
```
S → Composition
Composition → PhraseList
PhraseList → Phrase PhraseList_Prime
PhraseList_Prime → Phrase PhraseList_Prime | ε
Phrase → NoteSequence | ChordSequence
NoteSequence → Note NoteSequence_Prime
NoteSequence_Prime → Note NoteSequence_Prime | ε
Note → Pitch Duration
Pitch → 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G'
Duration → 'whole' | 'half' | 'quarter' | 'eighth' | 'sixteenth'
ChordSequence → Chord ChordSequence_Prime
ChordSequence_Prime → Chord ChordSequence_Prime | ε
Chord → '(' PitchList ')' Duration
PitchList → Pitch PitchList_Prime
PitchList_Prime → Pitch PitchList_Prime | ε
```

This transformation preserves the language recognized by the grammar while making it suitable for LL(1) parsing.

### Syntactic Tree Example - Left Recursion Elimination

For the string "C quarter D half":

**Before Left Recursion Elimination:**
```
       NoteSequence
      /           \
    Note         NoteSequence
   /   \            |
Pitch  Dur         Note
  |     |         /   \
 'C' 'quarter'  Pitch  Dur
                  |     |
                 'D'  'half'
```

**After Left Recursion Elimination:**
```
       NoteSequence
       /         \
     Note      NoteSequence_Prime
    /   \        /       \
 Pitch  Dur    Note     NoteSequence_Prime
   |     |    /   \         |
  'C' 'quarter' Pitch Dur    ε
                 |    |
                'D'  'half'
```

## Implementation

For my implementation, I used Python with the NLTK library to create an LL(1) parser for the Musical Language. The implementation includes:

1. A `MusicalLanguageParser` class that handles parsing and validation
2. A tokenizer that properly handles musical notation including parentheses for chords
3. An interactive mode for testing musical sentences
4. Comprehensive unit tests for valid and invalid strings

The core parser implementation uses NLTK's ChartParser with the transformed grammar. To use the parser:

```python
from musical_language_parser import MusicalLanguageParser

# Create a parser
parser = MusicalLanguageParser()

# Check if a string is valid
result = parser.is_valid("C quarter D half")  # Returns True

# View the parse tree
parser.print_parse_tree("C quarter D half")

# Try your own musical sentences
parser.interactive_mode()
```

Some examples of inputs and outputs are:
- `C quarter D half` → Valid (a sequence of two notes)
- `( C E G ) whole` → Valid (a C major chord)
- `C quarter ( E G B ) whole D half` → Valid (mix of notes and chords)
- `quarter C` → Invalid (wrong order)
- `C D quarter` → Invalid (missing duration for first note)
- `H quarter` → Invalid ('H' is not a valid pitch)

## Tests

The file includes comprehensive tests for the parser covering:
- Valid single notes
- Valid note sequences
- Valid chords
- Valid chord sequences
- Valid mixed sequences of notes and chords
- Various invalid inputs

The tests ensure that the parser correctly accepts valid strings from the language and rejects invalid strings, conforming to the language specification.

## Analysis

### Chomsky Hierarchy Classification

The initial grammar belongs to Type 2 (Context-Free) in the Chomsky hierarchy because:
1. All production rules are of the form A → α, where A is a single non-terminal
2. There are no restrictions on the right side of productions
3. The grammar can generate nested structures

After eliminating ambiguity and left recursion, the grammar remains a Context-Free Grammar (Type 2), but with additional properties:
- It is non-ambiguous: each valid string has exactly one valid parse tree
- It is non-left-recursive: suitable for top-down parsing algorithms like LL(1)

### Time Complexity Analysis

1. **Original Grammar (Context-Free with Ambiguity and Left Recursion)**:
   - Time complexity: O(n³) using general CFG parsing algorithms like CYK
   - Space complexity: O(n²)

2. **Transformed Grammar (Context-Free without Ambiguity or Left Recursion)**:
   - Time complexity: O(n) for LL(1) parsing
   - Space complexity: O(n) for the parse stack

The final implementation has a linear time complexity with respect to the input string length, making it efficient for parsing musical language strings.

My first approach was to use a recursive descent parser implemented directly, but after reviewing the literature, I found that using NLTK's parsing tools with a properly transformed grammar provides better maintainability and extensibility as noted by Bird et al. (2009).

## References

* Aho, A.V., Lam, M.S., Sethi, R., & Ullman, J.D. (2006). Compilers: Principles, Techniques, and Tools (2nd Edition). Addison Wesley.

* Grune, D., & Jacobs, C.J. (2008). Parsing Techniques: A Practical Guide (2nd Edition). Springer.

* Hopcroft, J.E., Motwani, R., & Ullman, J.D. (2006). Introduction to Automata Theory, Languages, and Computation (3rd Edition). Pearson.

* Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. O'Reilly Media.