from preflibtools.instances import OrdinalInstance

def get_lowest_pl_alt(orders, order_count, alternatives):
    '''The function returns the alternative with the lowest plurality score.'''
    pl_scores = {key: 0 for key in alternatives}

    for order_idx, order in enumerate(orders):
        for item in order[0]:
            pl_scores[item] += order_count[order_idx]

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

def main():
    profile = OrdinalInstance()
    profile.parse_url("https://www.preflib.org/static/data/aspen/00016-00000001.toi")

    orders = [[list(items) for items in order] for order in profile.orders]
    order_count = [profile.multiplicity[order] for order in profile.orders]
    alternatives = [alt + 1 for alt in range(profile.num_alternatives)]
    for winner in stv(orders, order_count, alternatives):
        print(f"{winner}: {profile.alternatives_name[winner]}")

if __name__ == "__main__":
    main()
