from cgitb import handler
import requests
import os
import mysql.connector
from bs4 import BeautifulSoup
from moviepy.editor import *
import math


video_1 = VideoFileClip("endvideo.mp4")


class configs:
    download = False
    os = "windows"


class Database:
    HOST = "localhost"
    USER = "root"
    PASSWD = ""
    DATABASE = "tiktokvideos"
    TABLE = "videos"


class Video:
    author_name = ""
    author_id = ""
    video_id = ""
    video_description = ""
    video_comment_count = ""
    video_like_count = ""
    video_share_count = ""
    video_file_name = ""
    video_url = ""

    def __init__(self, author_name, author_id, video_id, video_comment_count, video_like_count, video_share_count, video_url, video_description) -> None:
        self.author_name = author_name
        self.author_id = author_id
        self.video_id = video_id
        self.video_comment_count = video_comment_count
        self.video_like_count = video_like_count
        self.video_share_count = video_share_count
        self.video_file_name = video_id + ".mp4"
        self.video_url = video_url
        self.video_description = video_description


class Request:

    base_url = "https://www.tiktok.com"
    foryou_url = base_url + "/foryou"

    cookies = {"tt_csrf_token": "5tVZ5Q5O-3KcJb174yyWIlJrO4NZuWaABMN0", "__tea_cache_tokens_1988": "{%22_type_%22:%22default%22}", "passport_csrf_token": "f264bd291dfb9a8d80215531438d3281", "passport_csrf_token_default": "f264bd291dfb9a8d80215531438d3281", "_ttp": "29YfTFgCbzsaql8LDLSWPxxpPRW", "_abck": "E7740810C4D3DCFC8D5B436B6F1B5AEA~-1~YAAQB6bWfScW+vyAAQAAcsoLBQcr96xOFRg6Sm+0AmUb8UJSCMl5ycMg0lNYmaaP2uwGeKiOzQS8q8LM7mfs354zdhx48tN1+49edLiPRuVCRmX3ciSDprVAoD59O7u4T+anuHtxnhDJXhS6Cf5nNbGz3WSZvcx0/KSBBRuXPgg9JiBl+1ipkPL9DYXXIBrPe05sX9STR/rq0JJCfhFzepzo529aFO4aCLWrDOC3i3pWytAe7Lk4QyOBQNMF8sHI7Ao9iFddWhybmvPI97xFtrD4tG97ix2pf5p5sa4WbdOwrjd9ZljqUEVsCoCbed0kpUIm15H3hBfddzGRm+b1fMx5oM5+QEydOD0yfe5/mJCY5sWxGuApPM45GxDKfBFEFOC4cDzL4hWmgQ==~-1~-1~-1",
               "bm_sz": "A0CBC2236768146872BECFBDC98DD2F9~YAAQB6bWfSoW+vyAAQAAcsoLBQ9fAmPyZfk1S1PFSUUDgonpXjAFpf1euMEd2DbUMur4mPBvbgIpYXq6zoJMyCqVbEiIERwsWbJUIyim3xPJyc2xpGx4FIQa+569v5g7hRiqDzg4XIAxQ6QMnp2wbxUjHNRaO7wTYED9cLSpmi6hSKTZguDOkvJHJde/Z5WShrJdcYxXW79Ulq4KPGWQNfB075d+pFh7Gn/Sl9GmGXU2B/rSSmMpaVnPg7wm6eUgi+A5cb4cUDAaNv05xwBKNVWxeAVlS8I4xvoFGB5Rwde0WQA=~3354932~3747894", "ttwid": "1%7C-12UgS8iHNCotNgLpJWt-LKA3xTyQD5vhW-ZM2dflFo%7C1653654075%7C6b3afb40a7ab15d439f3f693ca3402397c5f8b8c42958cac2de5efee6e4bedfc", "bm_sv": "E07856D38070C456F7404972A20EC888~YAAQxy3fF4DUXeuAAQAABbx2BQ/k5DXYVj96hscOtVsQ7VluABlLKCfGCs2zVYtPsVuT3yUpHFfYPgWw3JuiYPpxj4fFTuwV1pCNL2fYGiz9Yz2SUSlVPmIFzzAe5GnN7xmFkPtv8A5X4jFWw/5qHLNeSeXaqG5zNWCK89W+YDRZCgHAcBHkn94tEDG2bIn7kcqUyh4uvPaf06hUkjEaCZvYyP6OeD0YgCi6dSmfXIedrsxA5zjExEes6uuU2qUBfw==~1", "msToken": "lixlQlfP774_FeWliTmxAcxODc9kI52pzrGPv5-6tRk0Nu3-nGwTJ4aP4vX33oQ5hoGaOQ0UeTMSPwtFgEyHcpd9vQkC8fDHkGPFDvi1AKsU8mONPj0DbIT0XBcYOt3yp_WL6CI=", "msToken": "MpifpbFbDs4Y7CXx4VLDN98jDAvGXMliQCcHWkidtAafOkEdlJGt_e3t0G4FqMN241Mns4jUkwTyP1aNUXYRXuKVYB5Y2iPM0kdeEuq4QVDWAHdSszFawVIQaWoD1Ax26YxQ-Ws="}
    headers = {"Connection": "close", "Cache-Control": "max-age=0", "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}

    def getSoup(self, url):
        try:
            res = requests.get(url, headers=self.headers,
                               cookies=self.cookies, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
        except:
            # time.sleep(15)
            self.getSoup(url)
        return soup


def getProfile():

    page = request.getSoup(request.foryou_url)
    uname = page.find('a', attrs={"data-e2e": "video-author-avatar"})
    uname = uname['href']
    return request.base_url + uname


def getVideoLink(profile_link):
    videos = []
    page = request.getSoup(profile_link)
    div = page.findAll('div', attrs={"data-e2e": "user-post-item"})
    for i in div:
        video_link = i.find('a')
        videos.append(video_link['href'])
    return videos


def scrapper(href):

    # Fetch API

    video_url = href
    search_url = "https://api.tikmate.app/api/lookup?url=" + str(video_url)
    res = requests.post(search_url)
    res = res.json()

    # Fetch Description
    res1 = requests.get(video_url, headers=request.headers,
                        cookies=request.cookies)
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

    video = Video(author_name, author_id, video_id,
                  video_comment_count, video_like_count, video_share_count, video_url, video_description)

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
    # download(res["token"], video_file_name)
    dbCommit(video, res["token"])


def dbCommit(video, token):

    handler = connector.cursor()

    # sql_query = f"SELECT id FROM {db.TABLE} ORDER BY 1 DESC LIMIT 1"
    # handler.execute(sql_query)
    # try:
    #     id = handler.lastrowid + 1
    # except:
    #     id = 1
    sql_query = f"INSERT INTO {db.TABLE} (author_name,author_id,video_id,video_url,description,comments,likes,shares,filename) VALUES ('{video.author_name}','{video.author_id}','{video.video_id}','{video.video_url}','{video.video_description}',{video.video_comment_count}, {video.video_like_count}, {video.video_share_count}, '{video.video_file_name}')"

    try:
        download(token, video.video_file_name)
        handler.execute(sql_query)
        connector.commit()
        handler.close()
    except Exception as err:
        print(err)
        handler.close()
        pass


def download(token, video_filename):
    # Downlaod Video

    download_url = "https://pride.nowmvideo.com/download/" + \
        token + "/" + video_filename
    # cmd_wget = "wget "+download_url
    cmd_certutil = "certutil.exe -urlcache -f "+download_url + " "+video_filename
    os.system(cmd_certutil)
    video_2 = VideoFileClip(video_filename)
    video_3 = video_2.subclip(0, math.floor(video_1.duration)*0.8)
    final1 = video_3.resize((1080, 1920))
    final2 = video_1.resize((1080, 1920))
    finalVideo = concatenate_videoclips([final1, final2])
    finalVideo.write_videofile(
        'final2.mp4', threads=20, fps=60, bitrate="2500k")

    # time.sleep(10)


request = Request()
db = Database()
connector = mysql.connector.connect(
    host=db.HOST, user=db.USER, passwd=db.PASSWD, database=db.DATABASE)


def run():
    while True:
        try:
            profile_link = getProfile()
            print("Next profile : "+profile_link)
            video_links = getVideoLink(profile_link)
            print(video_links)
            for link in video_links:
                print(link)
                scrapper(link)
                # video = scrapper(link)
                # dbCommit(video)
        except Exception as err:
            print(err)
            # handler.close()
            # print("Duplicate Video Skipped..")
            pass
        # time.sleep(5)


run()
