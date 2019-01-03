# -*- coding: utf-8 -*-

import sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests
    all_dict = {}
    for item in contests.find():
        if all_dict.__contains__(item['user_id']):
            all_dict[item['user_id']]['score'] += item['score']
            all_dict[item['user_id']]['submit_time'] += item['submit_time']
        else:
            all_dict[item['user_id']] = item

    newList = sorted(all_dict.values(), key=lambda x : (x['score'], -x['submit_time']))
 
    count = 1
    new_dict = {}
    for item in reversed(newList):
        item['rank'] = count
        count += 1
        new_dict[item['user_id']] = item


    if not new_dict.__contains__(user_id):
        print('NOTFOUND')
        sys.exit(0)

    print(newList)
    rank = new_dict[user_id]['rank']
    score = new_dict[user_id]['score']
    submit_time = new_dict[user_id]['submit_time']
    return rank, score, submit_time

if __name__ == '__main__':
    paramFlag = False
    paramLength = len(sys.argv[1:])
    paramFlag = paramLength > 1 or paramLength == 0 
    if paramFlag:
        print('Parameter Error')
        sys.exit(0)
    try:
        user_id = int(sys.argv[1:][0])
    except:
        print('Parameter Error')
        sys.exit(0)

    userdata = get_rank(user_id)
    print(userdata)
