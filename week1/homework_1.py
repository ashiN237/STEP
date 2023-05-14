from typing import List
import sys


def find_all_anagram(random_word: str, dictionary: List[str]) -> List[str]:
  """find all anagrams of random_word

    Args:
        random_word (str): any input alphabetic string 
        dictionary (List[str]): the list of dictionaries given

    Returns:
        List[str]: the list of all anagrams
  """
  sorted_random_word = sorted(random_word)
  new_dict = [[sorted(word), word] for word in dictionary]
  new_dict.sort()
  anagram = binary_search(sorted_random_word, new_dict)
  return anagram


def binary_search(sorted_random_word: str, dictionary: List[tuple]) -> List[str]:
  """binary search

    Args:
        sorted_random_word (str): sorted random word
        dictionary (List[tuple]): sorted list of tuples containing sorted word and original word

    Returns:
        List[str]: list of all anagrams
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
  """change text file to list

    Args:
        text (str): the name of the input text file

    Returns:
        List[str]: the list of words in the input text file
  """
  with open(text, 'r') as f:
    new_list = f.readlines()
  new_list = [word.strip() for word in new_list]
  return new_list


def list_to_text(name: str, words: List[str]) -> None:
  """change list to text file

    Args:
        name (str): the name of the output text file
        words (List[str]): the list of words to write in the output text file
  """
  new_words = "\n".join(words)
  with open(name, 'w') as f:
    f.write(new_words)


def main(input_file: str, output_file: str, random_word: str) -> None:
  dictionary = text_to_list(input_file)
  anagram = find_all_anagram(random_word, dictionary)

  if not anagram:
    print(None)
  else:
    print(anagram)

  list_to_text(output_file, anagram)


if __name__ == "__main__":
  if len(sys.argv) != 4:
    print("Usage: python3 homework_1.py input_file output_file rondom_word")
  else:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    random_word = sys.argv[3]
    main(input_file, output_file, random_word)
