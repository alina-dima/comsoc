from preflibtools.instances import OrdinalInstance
import itertools
from tqdm import tqdm
import time
from copy import deepcopy


def get_lowest_pl_alt(orders, order_count, alternatives):
    '''The function returns the alternative with the lowest plurality score.'''
    pl_scores = {key: 0 for key in alternatives}

    for order_idx, order in enumerate(orders):
        for item in order[0]:
            pl_scores[item] += (1 / len(order[0])) * order_count[order_idx]

    min_votes = min(pl_scores.values())
    return [key for key in pl_scores if pl_scores[key] == min_votes]


def remove_from_p(orders, order_count, alternative):
    '''The function removes an alternative from a profile.'''
    new_orders = []
    new_order_count = []
    for order_idx, order in enumerate(orders):
        new_order = []
        for pref in order:
            if alternative in pref:
                pref.remove(alternative)
            if len(pref) > 0:
                new_order.append(pref)
        if len(new_order) > 0:
            new_orders.append(new_order)
            new_order_count.append(order_count[order_idx])
    return new_orders, new_order_count


def stv(orders, order_count, alternatives):
    '''The function returns the STV winner given a profile.'''
    prev = alternatives.copy()
    while len(alternatives):
        lowest_pl_alt = get_lowest_pl_alt(orders, order_count, alternatives)
        prev = alternatives.copy()
        for alt in lowest_pl_alt:
            alternatives.remove(alt)
            orders, order_count = remove_from_p(orders, order_count, alt)
    return prev


def get_counts(orders):
    '''Returns the counts.'''
    counts = {}
    for order in orders:
        key = tuple([tuple(item) for item in order])
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    keys_list = [[list(items) for items in order] for order in list(counts.keys())]
    return keys_list, list(counts.values())


def all_v_pref_nw(new_winner, winner, orders, voters):
    '''The function returns whether all manipulated voters
       prefer the new winner to the original winner.'''
    prefer_nw = True
    for voter in voters:
        seen_new_winner = False
        for option in orders[voter]:
            if option == new_winner:
                seen_new_winner = True
            elif option == winner and not seen_new_winner:
                prefer_nw = False
                break

        if not prefer_nw:
            break
        if not seen_new_winner:
            prefer_nw = False
            break
    return prefer_nw


def manipulate(orders, alternatives, winner, not_winner_idxs):
    '''Checks all possible permutations of orders for all possible
       combinations of voters (that did not vote for 8 previously).'''

    # Generate all possible commbinations of voters with any length
    print("Manipulating...")
    for voters_len in tqdm(range(1, len(not_winner_idxs) + 1)):
        for voters in itertools.combinations(not_winner_idxs, voters_len):
            # Generate all possible orders with any length
            for perm_len in range(1, len(alternatives) + 1):
                for permutation in itertools.permutations(alternatives, perm_len):
                    old_ballots = []
                    new_orders = deepcopy(orders)
                    alternatives_copy = deepcopy(alternatives)
                    for voter in voters:
                        # change the order of voters to permutation
                        new_orders[voter] = [[item] for item in list(permutation)]
                        old_ballots.append(orders[voter])

                    new_orders, order_counts = get_counts(new_orders)

                    new_winner = stv(new_orders, order_counts, alternatives_copy)

                    if all_v_pref_nw(new_winner, winner, orders, voters) and new_winner != winner:
                        perm_as_list = [[item] for item in list(permutation)]
                        return (new_winner, perm_as_list, voters_len, old_ballots)
    return None


def flatten_orders(orders, order_count):
    '''Repeats all ballots based on the order counts.'''
    all_orders = [[ballot] * count for ballot, count in zip(orders, order_count)]
    all_orders2 = []
    for orders in all_orders:
        all_orders2.extend(orders)
    return all_orders2


def get_manipulable_idxs(all_orders, winners):
    '''Returns the indexes of the voters that did not place the original winner(s)
       as their top preference.'''
    not_winner_idxs = []
    for order in all_orders:
        win_in_order = False
        for winner in winners:
            if winner in order[0]:
                win_in_order = True
                break
        if not win_in_order:
            not_winner_idxs.append(all_orders.index(order))
    return not_winner_idxs


def main():
    '''Computes original STV winner(s) and tries to manipulate the elections.'''
    profile = OrdinalInstance()
    profile.parse_file("aspen_subset_3.toi")

    orders = [[list(items) for items in order] for order in profile.orders]
    order_count = [profile.multiplicity[order] for order in profile.orders]
    alternatives = list(profile.alternatives_name.keys())

    # Compute original winners
    winners = stv(deepcopy(orders), deepcopy(order_count), deepcopy(alternatives))
    print("Original winner(s):", [str(winner) + ": " + profile.alternatives_name[winner]\
                                 for winner in winners], "\n")

    # Start manipulation
    start = time.time()
    try:
        all_orders = flatten_orders(orders, order_count)
        not_winner_idxs = get_manipulable_idxs(all_orders, winners)
        (new_winner, perm, voters, old_ballots) = manipulate(all_orders, deepcopy(alternatives),\
                                                             winners, not_winner_idxs)
        print("The profile is manipulable with:")
        print("\t- new_winner(s):", [str(winner) + ": " + profile.alternatives_name[winner]\
                                     for winner in new_winner])
        print("\t- permutation:", perm)
        print("\t- number of voters:", voters)
        print("\t- old ballots: ", old_ballots)
    except TypeError:
        print("The profile cannot be manipulated.")
    print(f"Manipulation runtime: --- {time.time() - start} seconds ---")


if __name__ == "__main__":
    main()
