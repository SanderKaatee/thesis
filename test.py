    def recur_subset(self, s):
        self.subsets = []
        l = self.num_features_to_consider:
            for x in itertools.combinations(s, l):
                numbers = self.arg_to_combination_numbers(x)
                if self.init_phase or (str(numbers) in self.combination_feature_weights):
                        self.subsets.append(list(x))
