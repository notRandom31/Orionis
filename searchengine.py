import os
import re

def create_index(dir):
    """
    Creates an index of the words in the files in the given directory and its subfolders,
    along with short descriptions.

    Args:
      dir: The directory containing the files to index.

    Returns:
      A dictionary where the keys are words and the values are lists of 
      tuples (filename, description) containing those words.
    """
    index = {}
    for root, _, files in os.walk(dir):  # Walk through all subdirectories
        for filename in files:
            if filename.endswith((".txt", ".png", ".jpg", ".jpeg")):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    if filename.endswith(".txt"):
                        text = f.read()
                        words = re.findall(r'\b\w+\b', text.lower())
                        for word in words:
                            if word not in index:
                                index[word] = []
                            # Extract first sentence as description (up to the first period)
                            description = text[:text.find('.') + 1]
                            index[word].append((filename, description))
                    else:  # For image files
                        # No text content to index, so use filename as key
                        if filename not in index:
                            index[filename] = []
                        index[filename].append((filename, "Image file"))  # Simple description
    return index

def search(index, query):
    print(f"Searching for: {query}")  # Print the query
    """
    Searches the index for the given query, handling text and image files differently.
    """
    query_words = re.findall(r'\b\w+\b', query.lower())
    results = []
    for word in query_words:
        if word in index:
            results.extend(index[word])
    print(f"Results: {results}")  # Print the raw results
    # Rank results (example: by frequency of search terms)
    ranked_results = {}
    for filename, description in results:
        filepath = find_file_in_subfolders(filename, r'C:\Users\nicholas.nesmith0001\Documents\Search Engine')
        if filepath:
            with open(filepath, 'r') as f:
                text = f.read().lower()
                count = sum(1 for w in query_words if w in text)
                ranked_results[filename] = count

    # Sort results by rank (descending)
    sorted_results = sorted(ranked_results.items(), key=lambda item: item[1], reverse=True)

    return [(filename, index[filename][0][1]) for filename, _ in sorted_results]