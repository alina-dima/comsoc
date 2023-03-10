from votes import Vote as Vote


class Profile:
    """The class represents a profile."""
    def __init__(self, profile_data):
        self.votes = []
        self.alternatives = list(range(1, profile_data.num_alternatives+1))
        self.all_alternatives = {key: value for key, value in profile_data.alternatives_name.items()}

        for order in profile_data.orders:
            vote = Vote([list(items) for items in order], profile_data.multiplicity[order])
            self.votes.append(vote)

        self.winner_found = False

    def set_winner_found(self):
        """The function sets the winner found flag."""
        self.winner_found = True

    def has_alternatives(self):
        """The function returns true if the profile has alternatives."""
        return len(self.alternatives) > 0

    def get_lowest_pl_alternatives(self):
        """The function returns a list of alternatives with the lowest plurality score."""
        pl_scores = {key: 0 for key in self.alternatives}

        for vote in self.votes:
            for preference in vote.order[0]:
                pl_scores[preference] += vote.count / len(vote.order[0])

        min_votes = min(pl_scores.values())
        return [key for key in pl_scores if pl_scores[key] == min_votes]

    def remove_alternative(self, alternative):
        """The function removes an alternative from the profile."""
        for vote in self.votes[:]:
            vote.remove_alternative(alternative)
            if vote.is_empty():
                self.votes.remove(vote)

        temp_alternatives = self.alternatives.copy()
        self.alternatives.remove(alternative)

        if not self.has_alternatives():
            self.alternatives = temp_alternatives
            self.set_winner_found()

    def get_winner(self, show_progress=False, show_names=True):
        """The function returns the winner of the profile."""
        while not self.winner_found:
            lowest_pl_alternatives = self.get_lowest_pl_alternatives()
            for alternative in lowest_pl_alternatives:
                if show_progress:
                    if show_names:
                        print(f"Removing {alternative}: {self.all_alternatives[alternative]}")
                    else:
                        print(f"Removing {alternative}")
                self.remove_alternative(alternative)
        return self.alternatives


