class TermDictionary:
    def __init__(self, items):
        self.words = items
        self._len = len(items)
        self._max_word_len = len(max(items, key=len))+1

    def _levenstein(self, aux_matrix, word1, word2):
        word1_len = len(word1)
        word2_len = len(word2)

        for i in range(word1_len+1):
            aux_matrix[i][0] = i

        for j in range(word2_len+1):
            aux_matrix[0][j] = j

        for i, ch1 in enumerate(word1, start=1):
            for j, ch2 in enumerate(word2, start=1):
                cost = 0 if ch1 == ch2 else 1
                aux_matrix[i][j] = min([
                    aux_matrix[i-1][j] + 1,
                    aux_matrix[i][j-1] + 1,
                    aux_matrix[i-1][j-1] + cost
                ])

        return aux_matrix[word1_len][word2_len]

    def get_aux_list(self):
        return ['' for i in range(self._len)]

    def get_aux_matrix(self):
        return [[0 for j in range(self._max_word_len)]
                for i in range(self._max_word_len)]

    def suggestions(self, word, aux_list, aux_matrix):
        i = 0
        word_len = len(word)
        for elem in self.words:
            # Pre levenstein filters
            if elem == word:
                return (aux_list, 0)

            dist = self._levenstein(aux_matrix, word, elem)

            # Post levenstein filters
            if dist > 2:
                continue
            else:
                aux_list[i] = (dist, elem)
                i += 1
        return (aux_list, i)

