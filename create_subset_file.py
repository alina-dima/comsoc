from preflibtools.instances import OrdinalInstance
from collections import Counter

def get_subset_alternatives(all_orders2, alternatives_to_keep):
    all_orders_small = []
    for o in all_orders2:
        new_o = tuple([x for x in alternatives_to_keep if x in o])
        if len(new_o) > 0:
            all_orders_small.append(new_o)

    return all_orders_small


def  write_subset_to_file(values_and_counts, alternatives_to_keep, file_name):
    file = open(file_name, "w+")

    orders, counts = values_and_counts

    file.write(
    f'''# FILE NAME: 00016-00000001.toi
# TITLE: Aspen SMALL
# DESCRIPTION
# DATA TYPE: toi
# MODIFICATION TYPE: original
# RELATES TO
# RELATED FILES: 00016-00000001.dat,00016-00000001.toc
# PUBLICATION DATE: 2014-07-0
# MODIFICATION DATE: 2022-09-1
# NUMBER ALTERNATIVES: {len(alternatives_to_keep)}
# NUMBER VOTERS: {sum(counts)}
# NUMBER UNIQUE ORDERS: {len(orders)}
# ALTERNATIVE NAME 1: Jackie Kasabach
# ALTERNATIVE NAME 2: Jack Johnson
# ALTERNATIVE NAME 3: Adam Frisch
# ALTERNATIVE NAME 4: Torre\n''')

    for c, o in zip(counts, orders):
        
        file.write(f"{c}: ")
        file.write(','.join([str(x) for x in o]))
        file.write("\n")

    print(f"{file_name} created")
    file.close()


def get_counts(orders):
    c = Counter(orders)
    return list(c.keys()), list(c.values())

def main():
    profile = OrdinalInstance()
    # profile.parse_url("https://www.preflib.org/static/data/aspen/00016-00000001.toi")
    
    profile.parse_file("aspen_2009_data.toi")

    ##################################
    alternatives_to_keep = [8, 2, 1]
    file_name="aspen_subset_3.toi"
    #################################

    order_count = [profile.multiplicity[order] for order in profile.orders]
    orders2 = [[items[0] for items in order] for order in profile.orders]
    all_orders = [[tuple(ballot)] * count for ballot, count in zip(orders2, order_count)] # repeat all ballots based on the order counts
    
    all_orders2 = []
    for o in all_orders:
        all_orders2.extend(o) 


    all_orders_small = get_subset_alternatives(all_orders2, alternatives_to_keep)
    values_and_counts = get_counts(all_orders_small)
    write_subset_to_file(values_and_counts, alternatives_to_keep, file_name)


if __name__ == "__main__":
    main()
