'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    dot_product = 0
    for key in vec1:
        if key in vec2:
            dot_product += vec1[key] * vec2[key]
    magnitude1 = norm(vec1)
    magnitude2 = norm(vec2)
    if magnitude1 == 0 or magnitude2 == 0:
        return -1

    return dot_product/(magnitude1 * magnitude2)



def build_semantic_descriptors(sentences):
    d = {}

    for sentence in sentences:
        words_in_sentence = set(sentence)

        for word in words_in_sentence:
            if word not in d:
                d[word] = {}

            for co_word in words_in_sentence:
                if co_word != word:
                    if co_word in d[word]:
                        d[word][co_word] += 1
                    else:
                        d[word][co_word] = 1
    return d




def build_semantic_descriptors_from_files(filenames):
    sentence_collection = []
    nono_punctuation = [",", "-", "--", ":", ";"]
    sentence_endings = [".", "!", "?"]

    for filename in filenames:
        with open(filename, "r", encoding="latin1") as file:
            raw_text = file.read().lower()

            for separator in sentence_endings:
                raw_text = raw_text.replace(separator, "|")

            for nono in nono_punctuation:
                raw_text = raw_text.replace(nono, "")

            sentences = raw_text.split("|")

            for sentence in sentences:
                words = sentence.split()
                if words:
                    sentence_collection.append(words)

    return build_semantic_descriptors(sentence_collection)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    top_match = choices[0]
    max_similarity = -1

    for choice in choices:
        if word in semantic_descriptors and choice in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
            if similarity > max_similarity:
                max_similarity = similarity
                top_match = choice

    return top_match



def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct_count = 0
    question_count = 0

    with open(filename, 'r') as file:
        for line in file:
            elements = line.strip().split()
            query_word = elements[0]
            expected_answer = elements[1]
            option_words = elements[2:]

            predicted = most_similar_word(query_word, option_words, semantic_descriptors, similarity_fn)

            if predicted == expected_answer:
                correct_count += 1
            question_count += 1

    accuracy = (correct_count / question_count) * 100
    return accuracy
