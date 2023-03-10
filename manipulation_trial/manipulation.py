import random
from preflibtools.instances import OrdinalInstance
from profiles import Profile

if __name__ == '__main__':
    # load the profile data
    profile_data = OrdinalInstance()
    profile_data.parse_url("https://www.preflib.org/static/data/aspen/00016-00000001.toi")

    # create the profile
    profile = Profile(profile_data)

    manipulation_order1 = [[2], [3], [4], [5], [4], [1], [7], [9], [6], [11], [10]]
    manipulation_order2 = [[3], [2], [4], [5], [4], [1], [7], [9], [6], [11], [10]]

    number_of_manipulations = 0
    for vote in profile.votes:
        if vote.prefers_alternative(2, 8):
            if random.random() < 0.7:
                vote.set_manipulative_order(manipulation_order1)
            else:
                vote.set_manipulative_order(manipulation_order2)
            # vote.set_manipulative_order(manipulation_order2)
            number_of_manipulations += vote.count

    # print the STV winner/s
    for winner in profile.get_winner(show_progress=True, show_names=False):
        print(f"STV winner: {winner} - {profile.all_alternatives[winner]}")

    print(f"Number of manipulations: {number_of_manipulations}")