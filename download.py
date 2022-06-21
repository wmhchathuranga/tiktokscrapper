import requests
import os
import mysql.connector
from bs4 import BeautifulSoup
import time
import random
import sys

# Setup Database

mydb = mysql.connector.connect(
host="localhost", user="root", passwd="test",database="tiktokvideo"
	)
handler = mydb.cursor()
id_query = "SELECT id FROM videos ORDER BY 1"



def scrapper(href):

	try:

		handler.execute(id_query)
		db_id = handler.fetchall()[-1]
		db_id = db_id[0]
		db_id += 1
		print(db_id)

		# Fetch API

		video_url = href
		search_url = "https://api.tikmate.app/api/lookup?url="+video_url
		res = requests.post(search_url)
		res = res.json()


		# Fetch Description

		cookies = {"tt_csrf_token": "fluk9M8x-LI3bzIBaFY0qlP7f85-djfsCz98", "_abck": "E7740810C4D3DCFC8D5B436B6F1B5AEA~-1~YAAQxy3fF3AgdYuAAQAAdWPJqwc/fDdqFvqv0H/Ea3jA5X6ftmDMqLDclAMtDA+h1lUeR7bx/VE2HPOYLSiVjBwdXcWi69lEDpvS/rney70n59Vk5rN4urD2rEX5iQ9F1ygPhfKEsjW6s9HS+Df7cvYqlYG1EduEAJB3ryJMVtumlQVBQoxRdLYPnAQDb5t8IQpDY6xjA8F/AK5uD5vq8srobRaQ4JswRFI4YJwVLQeGK8kcVdhUnVj5wD+c+6BiELE0t/3l0K7JtkwyUXpXocX9y7N4mI8vjau9wZstcMkgi0mZi0V2UG+7mcgRZ4zvPDH0GQN3q8QFKeLIlF63zjT5YdiFac3oo+Dq1wpBm+19iQktUe1Ga52YWEw=~-1~-1~-1", "bm_sz": "828FDE95B9298A108E60B818D027F79F~YAAQxy3fF3MgdYuAAQAAdWPJqw9rFc+SBvIkgFM3lqQwFYp+rwEDYWH3TJlxBroMfGcilcXAgy3TZa1snzQu+5trFbcBxTh0dpo20ZaEeTRepBYY+919n+dM3QW5pjJ9/6+QbFA12lMJeskoCrq8dq3oh2e1zaV2gaDX9S1jU4gKEDBej16MNN+5/rwEoX/JmdVIh+a88CHX8vXbVzFpm3LpbeEtPJFsE4GG6N9PKVKHGSucPYVlUmE1EyWhNzfJ75qvqAhQdCcGvRGRISk1WA76JxecbNeRqgbY+Q7EmdAbhXA=~4605492~3424824", "__tea_cache_tokens_1988": "{%22_type_%22:%22default%22}", "csrf_session_id": "c6d42209e276e1d8b39279e713b724fa", "ttwid": "1%7C-12UgS8iHNCotNgLpJWt-LKA3xTyQD5vhW-ZM2dflFo%7C1652156609%7C67e64af15a0296d8873a9abf0a57a89bcb2b717e58a4e87c80ebf3e1d37d177c", "msToken": "WctlzKsA3TiTFsY-s8GLX_-H4Ff6vy5VbTBHWpG9ytE8rn49aRsSZCmiLj6446gSvKahklBPhT0BVN-mINOSLHFVkGQ8fv7Ud76ZdnAvaH9c0xCWgtDG928Hs-TCs9SSc0jKxMI=", "msToken": "KGBKqLFVuewLLAloOXRThIo2b3kv0rhQX5RCiadBvHnvHCsp397uldC6Zj1-_n6dZgyd0C37KpN23iq73hsCfwAWSIAlpbsTfI41x-kEZ3idi3xnQGWmt-L7KyuAlfJsh2zE6U0="}
		headers = {"Connection": "close", "Cache-Control": "max-age=0", "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
		res1 = requests.get(video_url, headers=headers, cookies=cookies)
		res1 = res1.text

		desc = res1.split('og:description" content="')[1]
		desc = desc.split('"')[0]
		video_description = desc

		# Extract Data


		author_name = res["author_name"]
		author_id = res["author_id"]
		video_id = res["id"]
		video_comment_count = res["comment_count"]
		video_like_count = res["like_count"]
		video_share_count = res["share_count"]
		video_file_name = video_id+".mp4"
		token = res["token"]
		

		# Print Data

		print(f'''

		Author Name : {author_name}
		Author Id : {author_id}
		Video Id : {video_id}
		Video URL : {video_url}
		Description : {video_description}
		Comments : {video_comment_count}
		Likes : {video_like_count}
		Shares : {video_share_count}
		File Name : {video_file_name}
			
		''')


		# SQL Add

		sql_query = f"INSERT INTO videos (id,author_name,author_id,video_id,video_url,description,comments,likes,shares,filename) VALUES ({db_id},'{author_name}','{author_id}','{video_id}','{video_url}','{video_description}',{video_comment_count}, {video_like_count}, {video_share_count}, '{video_file_name}')"


		handler.execute(sql_query)
		mydb.commit()

		# Downlaod Video

		download_url = "https://pride.nowmvideo.com/download/" + token + "/" + video_id +".mp4"
		cmd_wget = "wget "+download_url
		cmd_certutil = "certutil.exe -urlcache -f "+download_url+ " "+video_file_name 
		os.system(cmd_certutil)
		time.sleep(10)
	except Exception as err:
		print(err)
		time.sleep(5)
		pass



# Scrap Video urls

# word_site = "https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt"

# response = requests.get(word_site)
# list1 = response.text.splitlines()[30000:]

# f = open('proxy.txt','r')
# proxylist = f.read().split()


try:
	scrapper(sys.argv[1])
except Exception as err:
	print("Usage : python download.py 1.mp4")