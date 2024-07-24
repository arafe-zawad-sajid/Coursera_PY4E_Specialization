import sqlite3

conn = sqlite3.connect('spider1.sqlite')
cur = conn.cursor()

# we only are interested in pages in the SCC that have in and out links
# select the distinct ids that send out page rank
cur.execute('SELECT DISTINCT from_id FROM Links')
from_ids = list()
for row in cur:
    from_ids.append(row[0])
# select the dintinct ids that receive page rank
to_ids = list()
links = list()
cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
for row in cur:
    from_id = row[0]
    to_id = row[1]
    if from_id == to_id:
        continue
    if from_id not in from_ids:
        continue
    if to_id not in from_ids:
        continue
    links.append(row)
    if to_id not in to_ids:
        to_ids.append(to_id)

# get latest ranks for strongly connected components
prev_ranks = dict()
for node in from_ids:
    cur.execute('SELECT new_rank FROM Pages WHERE id=?', (node,))
    row = cur.fetchone()
    prev_ranks[node] = row[0]
#print('from_ids:', from_ids)  #
#print('to_ids', to_ids)  #
#print('links:', links)  #
#print(prev_ranks)  #

# sanity check prev_ranks
if len(prev_ranks) < 1:
    print('Nothing to page rank. Check data.')
    quit()

# iterations of page rank algorithm
sval = input('How many iterations: ')
many = 1
if len(sval) > 0:
    many = int(sval)
# performing page rank in memory
for i in range(many):
    next_ranks = dict()
    total = 0.0
    for (node, old_rank) in list(prev_ranks.items()):
        total = total+old_rank
        next_ranks[node] = 0.0
    # find the outbound links of each node and send page rank down each
    for (node, old_rank) in list(prev_ranks.items()):
        # find the outbound links for each node
        give_ids = list()
        for (from_id, to_id) in links:
            if from_id != node:
                continue
            if to_id not in to_ids:
                continue
            give_ids.append(to_id)
        #print(node, give_ids)  #
        if len(give_ids) < 1:
            continue
        # the amount of value each nodes give tot their outbound links
        amount = old_rank/len(give_ids)
        #print('amount:', amount)  #

        # send page rank down each outbound links for that node
        for id in give_ids:
            next_ranks[id] = next_ranks[id]+amount
            #print(id, ':', next_ranks[id])  #
    #print(next_ranks)  #

    # find evap factor
    newtot = 0.0
    for (node, next_rank) in list(next_ranks.items()):
        newtot = newtot+next_rank
    evap = (total-newtot)/len(next_ranks)
    #print(total, newtot, evap)  #

    # distributing the evap factor throughout the ranks
    for node in next_ranks:
        next_ranks[node] = next_ranks[node]+evap
    #print(next_ranks)  #
    newtot = 0.0
    for (node, next_rank) in list(next_ranks.items()):
        newtot = newtot + next_rank
    #print(newtot)  #

    # Compute the per-page average change from old rank to new ranks
    totdiff = 0.0
    for (node, old_rank) in list(prev_ranks.items()):
        new_rank = next_ranks[node]
        diff = abs(old_rank-new_rank)
        totdiff = totdiff+diff
    avgdiff = totdiff/len(prev_ranks)
    print(i+1, avgdiff)

    # rotate
    prev_ranks = next_ranks

# put the final ranks back into the db
print(list(next_ranks.items())[:5])
cur.execute('UPDATE Pages SET old_rank=new_rank')
for (id, new_rank) in list(next_ranks.items()):
    cur.execute('UPDATE Pages SET new_rank=? WHERE id=?', (new_rank, id))
conn.commit()
cur.close()
