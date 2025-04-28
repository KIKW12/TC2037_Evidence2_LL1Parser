import nltk
from nltk import CFG, ChartParser
from nltk.parse.generate import generate

class MusicalLanguageParser:
    def __init__(self, debug=False):
        # Define the musical language grammar after eliminating ambiguity and left recursion
        self.grammar_str = """
            S -> Composition
            Composition -> PhraseList
            PhraseList -> Phrase PhraseList_Prime
            PhraseList_Prime -> Phrase PhraseList_Prime | 
            Phrase -> NoteSequence | ChordSequence
            NoteSequence -> Note NoteSequence_Prime
            NoteSequence_Prime -> Note NoteSequence_Prime | 
            Note -> Pitch Duration
            Pitch -> 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G'
            Duration -> 'whole' | 'half' | 'quarter' | 'eighth' | 'sixteenth'
            ChordSequence -> Chord ChordSequence_Prime
            ChordSequence_Prime -> Chord ChordSequence_Prime | 
            Chord -> '(' PitchList ')' Duration
            PitchList -> Pitch PitchList_Prime
            PitchList_Prime -> Pitch PitchList_Prime | 
        """
        
        # Create the CFG from the grammar string
        self.grammar = CFG.fromstring(self.grammar_str)
        
        # Create a Chart Parser for better handling of the grammar
        self.parser = ChartParser(self.grammar)
        
        # Debug flag
        self.debug = debug
        
    def tokenize(self, text):
        """
        Properly tokenize the input text, handling parentheses separately.
        
        Args:
            text (str): The input text to tokenize
            
        Returns:
            list: List of tokens
        """
        # Replace parentheses with spaces around them for proper tokenization
        text = text.replace('(', ' ( ').replace(')', ' ) ')
        # Split by whitespace and filter out empty tokens
        tokens = [token for token in text.split() if token.strip()]
        
        if self.debug:
            print(f"Tokenized input: {tokens}")
            
        return tokens
        
    def parse(self, text):
        """
        Parse the given text according to the musical language grammar.
        
        Args:
            text (str): A string of tokens to parse
        
        Returns:
            list: List of parse trees or empty list if parsing fails
        """
        tokens = self.tokenize(text)
        try:
            # Get all parse trees
            trees = list(self.parser.parse(tokens))
            if self.debug and not trees:
                print("Parsing failed for input tokens:", tokens)
            return trees
        except Exception as e:
            if self.debug:
                print(f"Parsing error: {e}")
            return []
    
    def is_valid(self, text):
        """
        Check if the given text is valid according to the grammar.
        
        Args:
            text (str): A string of tokens to validate
        
        Returns:
            bool: True if the text is valid, False otherwise
        """
        trees = self.parse(text)
        return len(trees) > 0
    
    def print_parse_tree(self, text):
        """
        Print the parse tree for the given text.
        
        Args:
            text (str): A string of tokens to parse
        """
        trees = self.parse(text)
        if trees:
            for i, tree in enumerate(trees):
                print(f"Parse Tree {i+1}:")
                tree.pretty_print()
        else:
            print("No valid parse trees found.")
            
    def generate_examples(self, n=10, depth=5):
        """
        Generate example sentences from the grammar with a depth limit.
        
        Args:
            n (int): Maximum number of examples to generate
            depth (int): Maximum depth for generation to prevent overly long examples
            
        Returns:
            list: List of generated sentences
        """
        examples = []
        try:
            # Using a depth limit to prevent very long outputs
            for sentence in generate(self.grammar, depth=depth, n=n):
                examples.append(' '.join(sentence))
                if len(examples) >= n:
                    break
        except Exception as e:
            print(f"Example generation warning: {e}")
            # If generation fails, provide some manual examples
            examples = [
                "C quarter",
                "A whole B half",
                "C quarter D half E whole",
                "( C E G ) whole",
                "C quarter ( D F A ) half"
            ]
        return examples
        
    def interactive_mode(self):
        """
        Enter an interactive mode where the user can write their own musical sentences
        and get immediate feedback on their validity.
        """
        print("\n=== Interactive Musical Language Mode ===")
        print("Enter musical sentences to check if they're valid or 'q' to quit.")
        print("Example format: 'C quarter D half' or '( C E G ) whole'")
        print("Valid pitches: A, B, C, D, E, F, G")
        print("Valid durations: whole, half, quarter, eighth, sixteenth")
        
        while True:
            user_input = input("\nEnter a musical sentence (or 'q' to quit): ").strip()
            if user_input.lower() == 'q':
                print("Exiting interactive mode.")
                break
            
            if not user_input:
                continue
                
            is_valid = self.is_valid(user_input)
            print(f"'{user_input}': {'VALID' if is_valid else 'INVALID'}")
            
            if is_valid:
                show_tree = input("Show parse tree? (y/n): ").strip().lower()
                if show_tree == 'y':
                    self.print_parse_tree(user_input)
            else:
                print("The sentence doesn't conform to the musical language grammar.")
                print("Try again or enter 'q' to quit.")


def test_parser():
    """Function to test the parser with various examples."""
    parser = MusicalLanguageParser(debug=True)
    
    # Test valid examples
    valid_examples = [
        "C quarter",
        "C quarter D half",
        "( C E G ) whole",
        "C quarter ( E G B ) whole D half",
        "( C E G ) whole ( D F A ) half",
        "C quarter D half ( E G B ) whole F sixteenth"
    ]
    
    print("Testing Valid Examples:")
    for example in valid_examples:
        is_valid = parser.is_valid(example)
        print(f"'{example}': {'VALID' if is_valid else 'INVALID'}")
    
    # Test invalid examples
    invalid_examples = [
        "quarter C",
        "C D quarter",
        "( C E G",
        "H quarter",
        "C long"
    ]
    
    print("\nTesting Invalid Examples:")
    for example in invalid_examples:
        is_valid = parser.is_valid(example)
        print(f"'{example}': {'VALID' if is_valid else 'INVALID'}")


def demo():
    parser = MusicalLanguageParser()
    
    print("Musical Language Parser Demo")
    print("=" * 30)
    
    # Valid examples
    valid_examples = [
        "C quarter",
        "C quarter D half",
        "( C E G ) whole",
        "C quarter ( E G B ) whole D half",
        "( C E G ) whole ( D F A ) half"
    ]
    
    print("Testing Valid Examples:")
    for example in valid_examples:
        is_valid = parser.is_valid(example)
        print(f"'{example}': {'VALID' if is_valid else 'INVALID'}")
        if is_valid:
            # Display the first parse tree for demonstration
            trees = parser.parse(example)
            if trees:
                print("Parse Tree:")
                trees[0].pretty_print()
        print("-" * 30)
    
    # Invalid examples
    invalid_examples = [
        "quarter C",
        "C D quarter",
        "( C E G",
        "H quarter",
        "C long"
    ]
    
    print("\nTesting Invalid Examples:")
    for example in invalid_examples:
        is_valid = parser.is_valid(example)
        print(f"'{example}': {'VALID' if is_valid else 'INVALID'}")
        print("-" * 30)
    
    # Generate predefined examples instead of using the generator
    print("\nExample Musical Language Strings:")
    examples = [
        "C quarter",
        "A whole B half C quarter",
        "( C E G ) whole",
        "D half ( F A C ) quarter E eighth",
        "C quarter D half ( E G B ) whole F sixteenth"
    ]
    for i, example in enumerate(examples):
        print(f"Example {i+1}: {example}")
        if parser.is_valid(example):
            print("  (Valid)")
        else:
            print("  (Invalid)")


if __name__ == "__main__":
    # Run basic tests
    test_parser()
    
    # Run the demo
    print("\n")
    demo()
    
    # Ask user if they want to enter interactive mode
    user_choice = input("\nWould you like to write your own musical sentences? (y/n): ").strip().lower()
    if user_choice == 'y':
        parser = MusicalLanguageParser()
        parser.interactive_mode()
    else:
        print("Goodbye!")