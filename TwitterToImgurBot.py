# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imgurpython import ImgurClient
import praw
from praw.models import Comment
import urllib
import re
import requests
import os
import time

### API ###

client_id= #**
client_secret= #**
access_token = #**
refresh_token = #**
imgur = ImgurClient(client_id, client_secret, refresh_token)
imgur.set_user_auth(access_token, refresh_token)

reddit = praw.Reddit('TwitterToImgurBot')
subreddit = reddit.subreddit("formula1")

## SCRAPE /r/formula1 ###

for submission in subreddit.new(limit=200):
	if submission.domain == "twitter.com":
			url = submission.url
			page = requests.get(url)
			soup = BeautifulSoup(page.text, "html.parser")
			soup_string = str(soup)
			tweet = soup.find('p', {'class': 'tweet-text'}).text
			soup_filter = str(soup.find('div', {'class': 'AdaptiveMedia-photoContainer'}))
			image_url = re.findall('data-image-url="(.*)"', soup_filter)
			if image_url == []:
				continue
			tweet = tweet.split('pic', 1)[0]
			tweet = tweet.replace('#','/#')		
			
			### UPLOAD IMAGE TO IMGUR, RETRIEVE URL ###
			if not os.path.isfile("tti_posts_replied_to.txt"):
				posts_replied_to = []
			else:
				with open("tti_posts_replied_to.txt", "r") as f:
					posts_replied_to = f.read()
					posts_replied_to = posts_replied_to.split("\n")
					posts_replied_to = list(filter(None, posts_replied_to))
			if submission.id in posts_replied_to:
				continue
			time.sleep(10)
			
			if len(image_url) == 1:
				image_url = image_url[0]
				
				### UPLOAD IMAGE TO IMGUR, RETRIEVE URL ###
				
				ImgurImage = imgur.upload_from_url(image_url, config=None, anon=True)
				final_url = ImgurImage['link']
			elif len(image_url) > 1:
				### UPLOAD IMAGES TO IMGUR, RETRIEVE ALBUM URL ###
	
				list_of_images = []
				for image in image_url:
					list_of_images.append(imgur.upload_from_url(image, config=None, anon=False)['id'])
				fields = {}
				fields['title'] = "TwitterToImgurBot_Album"
				fields['description'] = "Enjoy!"
				fields['privacy'] = 'public'
				ImgurAlbum = imgur.create_album(fields)
				ImgurAlbumImages = imgur.album_add_images(ImgurAlbum['id'], list_of_images)
				final_url = "imgur.com/a/" + ImgurAlbum['id']

			### POST TO REDDIT ###
			submission.reply('%s \n\n[Image Contained in Tweet](%s)\n***\n ^(You can leave feedback by replying to me)' % (tweet, final_url))
			posts_replied_to.append(submission.id)
			
			with open("tti_posts_replied_to.txt", "w") as f:
				for post_id in posts_replied_to:
					f.write(post_id + "\n")