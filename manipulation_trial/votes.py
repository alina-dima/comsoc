class Vote:
    """The class represents a vote."""
    def __init__(self, order, count):
        self.order = order
        self.count = count

    def __str__(self):
        return f"{self.count}: {self.order}"

    def set_manipulative_order(self, order):
        """The function sets the manipulative order of the vote."""
        self.order = order

    def contains_alternative(self, alternative):
        """The function returns true if the vote contains the alternative."""
        for pref in self.order:
            if alternative in pref:
                return True
        return False

    def remove_alternative(self, alternative):
        """The function removes an alternative from a vote."""
        for pref in self.order[:]:
            if alternative in pref[:]:
                pref.remove(alternative)
                if len(pref) == 0:
                    self.order.remove(pref)
                break

    def is_empty(self):
        """The function returns true if the vote is empty."""
        return len(self.order) == 0

    def prefers_alternative(self, alternative1, alternative2):
        """The function returns true if the voter prefers alternative1 to alternative2."""
        for pref in self.order:
            if alternative1 in pref and alternative2 in pref:
                return pref.index(alternative1) < pref.index(alternative2)
            elif alternative1 in pref:
                return True
            elif alternative2 in pref:
                return False
        return False

    def has_top_preference(self, alternative):
        """The function returns true if the vote has alternative as its top preference."""
        return alternative in self.order[0]