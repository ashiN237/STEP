from typing import List
from collections import Counter
import argparse

## How to use
#
# $ python3 homework_2.py dictionary.txt input.txt output.txt

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]


class Word:
  """Represents a word with its score and character count."""

  def __init__(self, word: str) -> None:
    """Initialize a Word object.
        
      Args:
          word (str): The input word.
    """
    self.word = word
    self.score = sum(SCORES[ord(c) - ord('a')] for c in word)
    self.counter = Counter(word)


def find_highest_score_anagram(word: Word, dictionary: List[Word]) -> Word:
  """Find the anagram with the highest score from the given dictionary.
    
    Args:
        word (Word): The input word.
        dictionary (List[Word]): The list of Word objects representing the dictionary.
        
    Returns:
        Word: The anagram with the highest score.
    """
  for dict_word in dictionary:
    if all(dict_word.counter[key] <= word.counter[key] for key in dict_word.counter):
      return dict_word

  return None


def text_to_list(text: str) -> List[Word]:
  """Convert a text file to a list of Word objects.
    
    Args:
        text (str): The name of the input text file.
        
    Returns:
        List[Word]: The list of words in the input text file.
  """
  with open(text, 'r') as f:
    new_list = f.readlines()
  new_list = [Word(word.strip()) for word in new_list]
  return new_list


def list_to_text(name: str, words: List[str]) -> None:
  """Convert a list of words to a text file.
    
    Args:
        name (str): The name of the output text file.
        words (List[str]): The list of words to write in the output text file.
  """
  new_words = "\n".join(str(word) for word in words)
  with open(name, 'w') as f:
    f.write(new_words)


def main():
  """Main function to find anagrams in a text file using a dictionary file."""
  parser = argparse.ArgumentParser(description="Find anagrams in a text file using a dictionary file")
  parser.add_argument('dictionary_file', type=str, help='Path to the dictionary file')
  parser.add_argument('input_file', type=str, help='Path to the input file')
  parser.add_argument('output_file', type=str, help='Path to the output file')
  args = parser.parse_args()

  dictionary = text_to_list(args.dictionary_file)
  dictionary.sort(key=lambda x: x.score, reverse=True)
  input_words = text_to_list(args.input_file)
  anagrams = []

  for input_word in input_words:
    anagram = find_highest_score_anagram(input_word, dictionary)
    anagrams.append(anagram.word)

  list_to_text(args.output_file, anagrams)


if __name__ == '__main__':
    main()