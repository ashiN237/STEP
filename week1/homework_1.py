from typing import List
import argparse

## How to use
#
# $ python3 homework_1.py dictionary.txt output.txt input_word


def find_all_anagram(random_word: str, dictionary: List[str]) -> List[str]:
  """Find all anagrams of the given random word.

    Args:
        random_word (str): The random word for which to find anagrams.
        dictionary (List[str]): The list of words in the dictionary.

    Returns:
        List[str]: The list of all anagrams found.
  """
  sorted_random_word = sorted(random_word)
  new_dict = [[sorted(word), word] for word in dictionary]
  new_dict.sort()
  anagram = binary_search(sorted_random_word, new_dict)
  return anagram


def binary_search(sorted_random_word: str, dictionary: List[tuple]) -> List[str]:
  """Perform binary search to find all anagrams.

    Args:
        sorted_random_word (str): The sorted random word.
        dictionary (List[tuple]): The sorted list of tuples containing sorted word and original word.

    Returns:
        List[str]: The list of all anagrams found.
  """
  left = 0
  right = len(dictionary) - 1
  word = []

  while left <= right:
    mid = (left + right) // 2
    if dictionary[mid][0] > sorted_random_word:
      right = mid - 1
    elif dictionary[mid][0] < sorted_random_word:
      left = mid + 1
    else:
      for i in range(mid, -1, -1):
        if dictionary[i][0] == sorted_random_word:
          word.append(dictionary[i][1])
        else:
          break
      for i in range(mid+1, len(dictionary)):
        if dictionary[i][0] == sorted_random_word:
          word.append(dictionary[i][1])
        else:
          break
      break

  return word


def text_to_list(text: str) -> List[str]:
  """Convert a text file to a list of words.

    Args:
        text (str): The name of the input text file.

    Returns:
        List[str]: The list of words in the input text file.
  """
  with open(text, 'r') as f:
    new_list = f.readlines()
  new_list = [word.strip() for word in new_list]
  return new_list



def list_to_text(name: str, words: List[str]) -> None:
  """Convert a list of words to a text file.

    Args:
        name (str): The name of the output text file.
        words (List[str]): The list of words to write in the output text file.
  """
  new_words = "\n".join(words)
  with open(name, 'w') as f:
    f.write(new_words)


def main():
  """Main function to find anagrams."""
  parser = argparse.ArgumentParser(description="Find anagrams in a text file using a dictionary file")
  parser.add_argument('dictionary_file', type=str, help='Path to the dictionary file')
  parser.add_argument('output_file', type=str, help='Path to the output file')
  parser.add_argument('random_word', type=str, help='Path to the random word')
  args = parser.parse_args()

  dictionary = text_to_list(args.dictionary_file)
  anagram = find_all_anagram(args.random_word, dictionary)

  if not anagram:
    print("There is no anagram")
  else:
    print(anagram)

  list_to_text(args.output_file, anagram)


if __name__ == "__main__":
  main()