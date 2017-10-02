# -*- coding:utf-8 -*-
# followers.py

import tweepy
from tweepy.error import TweepError
import sys
import time
import logging
from random import randint
from time import sleep

def getApiInstance(consumer_keys, consumer_secrets, access_token_keys, access_token_secrets):
    apis = []
    for consumer_key, consumer_secret, access_token_key, access_token_secret in zip(consumer_keys, consumer_secrets, access_token_keys, access_token_secrets):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        #利用制限にひっかかた時に必要時間待機する
        apis.append(tweepy.API(auth, wait_on_rate_limit = True))
    print(apis)
    return apis

def unFollow(apis):

    unfollow_list = []
    for api in apis:
        try:
            print("Loading followers..")
            follower_list = api.followers_ids()
            print("followers are loaded!")
            print("Loading follow accounts..")
            follow_list = api.friends_ids()
            print("follow accounts are loaded!")

            if len(follow_list) - len(follower_list) <= 0:
                return

            length = len(follow_list)

            # フォローしているアカウントがフォロワーにいなかったらアンフォロー
            for index, follow_account in enumerate(follow_list):
                print(str(index) + "/" + str(length))
                if not follow_account in follower_list:
                    api.destroy_friendship(follow_account)
                    print("unfollow is success!")
                    # unfollow_list[api].extend(follow_account)
                time.sleep(1)
            # print("Unfollow {} users!".format(str(len(unfollow_list[api]))))
            print("unfollow is done!")

        except TweepError as e:
            # print(e)
            if e.api_code and e.api_code == 160:
                print(e.message)
                continue
            elif e.api_code == 161: # フォロー上限が来ている時は次のアカウントへ
                print("follow limit! go a next account!")
                continue
            elif e.api_code == 401:
                print("Unauthorized Error!")
                continue
            elif e.api_code == 89:
                print('Invalid or expired token!')
                continue
            else:
                print("Unknown Error!")
                continue

    return unfollow_list

def search_word_and_follow(apis, keywords**):
    user_ids = []
    # keywords =[u'プログラミング']
    query = ' OR '.join(keywords)
    count = 0
    follow_num = 1000

    for api in apis:
        try:
            for tweet in tweepy.Cursor(api.search, q=query, count=follow_num).items():
                print(tweet.user.id)
                api.create_friendship(tweet.user.id)
                count+=1
                sleep(randint(1, 3))
                if count == 100:
                    count=0
                    sleep(30)
        except TweepError as e:
            if e.api_code == 162 or e.api_code == 160: # フォローをブロック or すでにフォロー
                print("already follow!")
                continue
            elif e.api_code == 161: # フォロー上限が来ている時は次のアカウントへ
                print("follow limit! go a next account!")
                continue
            elif e.api_code == 401:
                print("Unauthorized Error!")
                continue
            elif e.api_code == 89:
                print('Invalid or expired token!')
                continue
            else:
                print("Unknown Error!")
                continue

def benchmark_follow(apis):
    user_ids = []
    benchmark_account_ids =[]
    query = ' OR '.join(keywords)
    count = 0
    follow_num = 1000

    for api in apis:
        print(api)
        print(len(tweepy.Cursor(api.search, q=query, count=follow_num).items()))
        exit(1)
        for tweet in tweepy.Cursor(api.search, q=query, count=follow_num).items():
            try:
                print(tweet.user.id)
                api.create_friendship(tweet.user.id)
                count+=1
                sleep(randint(1, 3))
                if count == 100:
                    count=0
                    sleep(30)
            except TweepError as e:
                if e.api_code == 162 or e.api_code == 160: # フォローをブロック or すでにフォロー
                    print("already follow!")
                    continue
                elif e.api_code == 161: # フォロー上限が来ている時は次のアカウントへ
                    print("follow limit! go a next account!")
                    break
                elif e.api_code == 161: # フォロー上限が来ている時は次のアカウントへ
                    print("follow limit! go a next account!")
                    continue
                elif e.api_code == 401:
                    print("Unauthorized Error!")
                    continue
                elif e.api_code == 89:
                    print('Invalid or expired token!')
                    continue
                else:
                    print("Unknown Error!")
                    continue

def followBack(apis):

    follow_back_list = []
    strings = str

    for index, api in enumerate(apis):
        if index == 0:
            continue
        print("Loading followers..")
        follower_list = api.followers_ids()
        print("followers are loaded!")
        print("Loading follow accounts..")
        follow_list = api.friends_ids()
        print("follow accounts are loaded!")
        length = len(follower_list)
        # フォローしているアカウントがフォロワーにいなかったらアンフォロー
        for index, follower_account in enumerate(follower_list):
            print(strings(index) + "/" + strings(length))
            try:
                if not follower_account in follow_list:
                    api.create_friendship(follower_account)
                    print("follow is success!")
                    # follow_back_list[api].extend(follower_account)
                else:
                    print()
            except TweepError as e:
                if e.api_code  == 160 or e.api_code == 162:
                    print("already requests to follow!")
                    continue
                elif e.api_code == 161: # フォロー上限が来ている時は次のアカウントへ
                    print("follow limit! go a next account!")
                    break
                elif e.api_code == 401:
                    print("Unauthorized Error!")
                    continue
                elif e.api_code == 89:
                    print('Invalid or expired token!')
                    continue
                else:
                    print("Unknown Error!")
                    print(e.api_code)
                    continue
            time.sleep(1)
        print("follow back {} users!".format(str(len(follow_back_list[api]))))
        print("follow back is done!")

    return follow_back_list

if __name__ == "__main__":

    # screen_name = "lottiso1" #ロッチの中岡さんのアカウントをスクリーンネームで指定する
    # アクセスに必要なキーたち。それぞれのアカウントごとに順番を同じにして配置する。
    consumer_keys = ["hPLfgg7ehBZDGVYmfELzq28PO", "27ObxcVpe6ve7YpNbIkryoDm9", "x8QTZSmAbfoApap1wxfc1RCzT"]
    consumer_secrets = ["lvR3lXlSjeJaid5ejtd8zcnZiXCiF9C7FGrJCoLeG2IYyIeg0Z", "8zq2nlIGgYGZeZ1FvMGMBPUClHRGOKyCZvXzMX7OY7IJlrtuhb", "29HgPtduPAFnaBSpHCYA6Qae0sSj7Kjb4Y5AqG6dUCQrZqURLE"]
    access_token_keys = ["786480048765140992-RkfdXmwvQdC4titDWVWFDjim2xyCZn0", "786481781339938816-dA7YZZkQYyqj8kVGiuTjiOh6bggO4jK", "797721828684767232-nTJobrUmW3sCngKmGrrxNe12ykkViT3"]
    access_token_secrets = ["ELUc3OYQpmmTMor3Vg4Ni8ZtBGgmSP3w5chVQmzFyGwLa", "3ih91eN2OU6hGfpYm9sEJQYNWndOXepJEcqlOEyozXupD", "3YXdxsrEpUZZaebVtkyRUOiW2hdwpD66qmVtj5CCABDow"]

    api = getApiInstance(consumer_keys=consumer_keys, consumer_secrets=consumer_secrets, access_token_keys=access_token_keys, access_token_secrets=access_token_secrets)
    print("get Api is done!")
    # unfollow_list = unFollow(apis = api)
    follow_back_list = followBack(apis = api)
    search = search_word_and_follow(apis = api)

    print("done!") #数で確認してみる
