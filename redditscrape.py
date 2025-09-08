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


    def extract_comment_data(self, comment):
        """Extracts data for one comment, recursively processing replies."""
        comment_data = {
            "id": comment["data"]["id"],
            "author": comment["data"].get("author"),
            "body": comment["data"].get("body"),
            "score": comment["data"].get("score"),
            "created_utc": comment["data"].get("created_utc"),
            "replies": []
        }

        # check for replies (can be "" if no replies)
        replies = comment["data"].get("replies")
        if replies and isinstance(replies, dict):
            for reply in replies["data"]["children"]:
                if reply["kind"] == "t1":  # t1 = comment, t3 = post
                    comment_data["replies"].append(self.extract_comment_data(reply))

        return comment_data


    def get_all_comments(self):
        """Fetch all comments and nested replies for current post."""
        all_comments = []
        try:
            data = requests.get(url=self.comments_url, headers=self.headers).json()
            for child in data[1]["data"]["children"]:
                if child["kind"] == "t1":  # ensure it's a comment
                    all_comments.append(self.extract_comment_data(child))
        except Exception as e:
            print("Error fetching comments:", e)

        return all_comments



# print(d.comments())
# for x in range(len(d.comments())):

#     print(d.replies(x))
# print(d.comments_url)