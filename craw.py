import requests
from bs4 import BeautifulSoup
import os
import time

url = "http://www.ghibli.jp/info/013344/"
pathname = "/Users/ac_rl/Documents/crawl_ghibli_py/download_img"
r = requests.get(url)
web_content = r.text

def download_image(downloadPath,image_url):
    filename = image_url.split('/')[-1].split("?")[0]
    url_response = requests.get(image_url, stream=True, verify=False)
    with open(downloadPath+"/"+filename, 'wb') as f:
        for chunk in url_response.iter_content(chunk_size=8192):
          f.write(chunk)

# 以 Beautiful Soup 解析 HTML 程式碼 : 
soup = BeautifulSoup(web_content, 'html.parser')
movies = soup.find_all('a', class_="panelarea")
movieURL = [e.get('href') for e in movies]
print(movieURL)
time.sleep(5)

for movie in movieURL:
    startIndex = movie.find("works/")+6
    endIndex = movie.find("/#frame")
    downloadPath = pathname+"/"+movie[startIndex:endIndex]
    print("Movie:",movie[startIndex:endIndex])

    requestMovies = requests.get(movie)
    web_content = requestMovies.text
    # print(web_content)
    soup = BeautifulSoup(web_content, 'html.parser')
    images = soup.find_all('a',class_="panelarea")
    if not os.path.isdir(downloadPath):
            os.makedirs(downloadPath)
    for singlePic in images:
        imagesURL = singlePic.get('href')
        download_image(downloadPath,imagesURL)
        print("picture downloaded from: ",imagesURL)
        time.sleep(3)


