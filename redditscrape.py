from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
load_dotenv()


class Reddit_Scrape:
    def __init__(self):
        """ah"""
        self.headers = {"User-Agent": "python:subreddit.fetcher:v1.0 (by u/yourusername)"}
        self.mainpage = os.getenv("URL")

    def top_post(self, post):
        """{post number: {title: (desc, link)}}\n
        saves url as self.comments_url\n
        e.g. {2: {does someone know this?: where to buy icecream?, www.icecreamqueries.com}}"""
        response = requests.get(url=self.mainpage, headers=self.headers)
        print(response)
        data = response.json()
        if data["data"]["children"][post]["data"]["selftext"] == "":
            pass
        else:
            print(f'ID: {data["data"]["children"][post]["data"]["id"]}')
            print(f'TITLE: {data["data"]["children"][post]["data"]["title"]}')
            print(f'AUTHOR: {data["data"]["children"][post]["data"]["author"]}')
            print(f'SCORE: {data["data"]["children"][post]["data"]["score"]}')
            print(f'URL: {data["data"]["children"][post]["data"]["url"]}')
            print(f'CREATED_UTC: {data["data"]["children"][post]["data"]["created_utc"]}')
            # print(data["data"]["children"][x]["data"]["url"])
            diction = {post:
                       {"ID":data["data"]["children"][post]["data"]["id"],
                       "TITLE":data["data"]["children"][post]["data"]["title"],
                        "AUTHOR":data["data"]["children"][post]["data"]["author"],
                        "SCORE":data["data"]["children"][post]["data"]["score"],
                        "URL":data["data"]["children"][post]["data"]["url"],
                        "CREATED_UTC":data["data"]["children"][post]["data"]["created_utc"]}
                    }
            self.post_id = data["data"]["children"][post]["data"]["id"]
            self.comments_url = f'https://www.reddit.com{data["data"]["children"][post]["data"]["permalink"]}.json' # print(list(post[1].keys())[0]) #dict_keys(['key string']) to just 'key string'
            return diction
    def comments(self):
        """ah"""
        all_comments = []
        try:
            data = requests.get(url=self.comments_url, headers=self.headers).json()
            for _ in range(len(data[1]['data']['children'])):
                all_comments.append({
                    _ :
                    {"ID":data[1]["data"]["children"][_]["data"]["id"],
                     "author":data[1]["data"]["children"][_]["data"]["author"],
                     "body":data[1]["data"]["children"][_]["data"]["body"],
                     "score":data[1]["data"]["children"][_]["data"]["score"],
                     "created_utc":data[1]["data"]["children"][_]["data"]["created_utc"]
                     }
                })
                #return something
        except:
            pass
        return all_comments
    def replies(self, comment):
        """ah"""
        all_replies = []
        # {comment:
        # {reply: id, author, body, score, created_utc}}
        try:

            data = requests.get(url=self.comments_url, headers=self.headers).json()
            for _ in range(len(data[1]['data']['children'][comment]['data']['replies']['data']['children'])):
                print(comment)
                all_replies.append({
                    _ :
                    {"ID":data[1]['data']['children'][comment]['data']['replies']['data']['children'][_]['data']['id'],
                     "author":data[1]['data']['children'][comment]['data']['replies']['data']['children'][_]['data']['author'],
                     "body":data[1]['data']['children'][comment]['data']['replies']['data']['children'][_]['data']['body'],
                     "score":data[1]['data']['children'][comment]['data']['replies']['data']['children'][_]['data']['score'],
                     "created_utc":data[1]['data']['children'][comment]['data']['replies']['data']['children'][_]['data']['created_utc']
                     }
                })
            # for x in range(len(data[1]['data']['children'][comment]['data']['replies']['data']['children'])):#[0]['data']['body']
            #     all_replies.append(data[1]['data']['children'][comment]['data']['replies']['data']['children'][x]['data']['body'])
            #     try:
            #         for y in range(len(data[1]['data']['children'][comment]['data']['replies']['data']['children'][x]['data']['replies']['data']['children'])):
            #             all_replies.append(data[1]['data']['children'][comment]['data']['replies']['data']['children'][x]['data']['replies']['data']['children'][y]['data']['body'])
            #     except:
            #         pass
        except:
            pass
        return all_replies
d = Reddit_Scrape()
d.top_post(5)
print(d.comments())
for x in range(len(d.comments())):
    print(x)
    print(d.replies(x))
print(d.comments_url)