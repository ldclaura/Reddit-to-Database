from redditscrape import Reddit_Scrape
# from gemini import AIGen
scrape = Reddit_Scrape()
print(scrape)
post = scrape.top_post(2)
print(post)
print("-----post-----")
for num in list(post.keys()):
    for title in post[num]:
        print(title) #title
        thetitle = title
        print(post[num][title][0]) #desc
        thedesc = post[num][title][0]
commentsreplies = ""
for comment in scrape.comments():
    print(comment)
    print("-----comments------")
    print(scrape.comments()[comment])
    print(f"-----{len(scrape.replies(comment))}replies-----")
    print(scrape.replies(comment))
    commentsreplies + scrape.comments()[comment] #+ scrape.replies(comment)
    for reply in range(len(scrape.replies(comment))):
        commentsreplies + reply
print(commentsreplies)
