from preflibtools.instances import OrdinalInstance
import itertools
from collections import Counter
from tqdm import tqdm
import time

def get_lowest_pl_alt(orders, order_count, alternatives):
    '''The function returns the alternative with the lowest plurality score.'''
    pl_scores = {key: 0 for key in alternatives}

    for order_idx, order in enumerate(orders):
        for item in order[0]:
            pl_scores[item] += order_count[order_idx]

    # print("plurality scores:", pl_scores)
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
    c = Counter(orders)
    return list(c.keys()), list(c.values())


# for all possible combinations of voters (that did not vote for 8 previously) check all possible permutations of orders
def manipulate(orders, alternatives, winner,  not_winner_idxs):
    

    # generate all possible commbinations of voters with any length
    for v in tqdm(range(1, len(not_winner_idxs) + 1)):
        for voters in itertools.combinations(not_winner_idxs, v):
            # print(voters)
            
            # Generate all possible orders with any length
            for r in range(1, len(alternatives) + 1):
                for permutation in itertools.permutations(alternatives, r):
                    # print(permutation)
                    new_orders = orders.copy()
                    alternatives_copy = alternatives.copy()
                    for voter in voters:
                        # print(voter[0])
                        new_orders[voter] = permutation # change the order of voters to permutation
                        

                    new_orders_frq, order_counts = get_counts(new_orders)
                    # print(order_counts)

                    new_orders_list = []
                    for order in new_orders_frq:
                        aux = []
                        for item in order:
                            aux.append([item])
                        new_orders_list.append(aux)

                    # print("new order: ", new_orders_list)
                    # print("new order counts: ", order_counts)
                    new_winner = stv(new_orders_list, order_counts, alternatives_copy)
                    # print("winner", new_winner)
                    
                    if new_winner != winner:
                        print(new_winner)
                        return (new_winner, permutation, v)

    print("Cannot be manipulated")
    return



def main():
    profile = OrdinalInstance()
    # profile.parse_url("https://www.preflib.org/static/data/aspen/00016-00000001.toi")
    profile.parse_file("aspen_subset_3.toi")

    orders = [[list(items) for items in order] for order in profile.orders]
    order_count = [profile.multiplicity[order] for order in profile.orders]
    orders2 = [[items[0] for items in order] for order in profile.orders]

    all_orders = [[tuple(ballot)] * count for ballot, count in zip(orders2, order_count)] # repeat all ballots based on the order counts
    all_orders2 = []
    not_winner_idxs = []
    for o in all_orders:
        all_orders2.extend(o) 

    winner = 3
    not_winner_idxs = []
    for o in all_orders2:
        if winner not in o:
            not_winner_idxs.append(all_orders2.index(o)) # the indexes of the voters who did not place 8 among their preferences

    
    print(len(not_winner_idxs))
    # exit()
    
    alternatives = [6, 7, 8, 9]
    print(alternatives)
    alternatives_copy = alternatives.copy()


    winners = stv(orders, order_count, alternatives)
    print(winners)
    # exit()
    
    # for winner in winners:
    #     print(f"{winner}: {profile.alternatives_name[winner]}")

    start = time.time()
    (new_winner, permutation, v) = manipulate(all_orders2, alternatives_copy, winners,  not_winner_idxs)
    print("--- %s seconds ---" % (time.time() - start))

    print("new_winner:", new_winner)
    print("permutation", permutation)
    print("voters", v)

    # for winner in new_winner:
    #     print(f"{winner}: {profile.alternatives_name[winner]}")
    


if __name__ == "__main__":
    main()
