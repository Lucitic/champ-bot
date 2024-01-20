class Categorizer: #class that takes in a string and returns categories with weights

    def __init__(dic): #dictionary should be {catgory: corresponding_keywords}
        self.categories = dic
        self.weights = {}
        for key in dic:
            self.weights[key] = 0

    def sort(string_of_prefs): #returns a copy of v@self.weights with weights for this particular v@string_of_prefs
        pref_weights = self.weights.copy()
        cleaned_string = re.sub('[^a-zA-Z\d\s:]', " ", string_of_prefs)
        split_string = cleaned_string.split()
        for key_word in self.categories:
            for word in self.categories[key_word]:
                if word in split_string:
                    pref_weights[key_word] += 1
        return pref_weights
