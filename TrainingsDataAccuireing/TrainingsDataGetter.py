from pathlib import Path
from google_images_download import google_images_download
import os

scriptPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
print(scriptPath)


pathToQueries = scriptPath+"/SearchQuery.txt"
imgDownloadFolder = scriptPath+"/imgRaw/"
numberOfImagesToDownload = 1000

# creating downloader object
downloader = google_images_download.googleimagesdownload()

search_queries = []


def main():
    getSearchQueries()
    downloadImagesFromGoogle()

def downloadImagesFromGoogle():

    createDir(imgDownloadFolder)

    for query in search_queries:
        # keywords is the search query
        # format is the image file format
        # limit is the number of images to be downloaded
        # print urs is to print the image file url
        # size is the image size which can
        # be specified manually ("large, medium, icon")
        # aspect ratio denotes the height width ratio
        # of images to download. ("tall, square, wide, panoramic")
        arguments = {
            "keywords": query,
            "format": "jpg",
            "limit": numberOfImagesToDownload,
            "print_urls": True,
            "size": "medium",
            "output_directory": imgDownloadFolder,
            "no_directory": True,
            "chromedriver": "D:\\Git\\Schule\\GDKIPSTA\\TrainingsDataAccuireing\\chromedriver.exe"

        }
        try:
            downloader.download(arguments)

        # Handling File NotFound Error
        except FileNotFoundError:
            arguments = {
                "keywords": query,
                "format": "jpg",
                "limit": numberOfImagesToDownload,
                "print_urls": True,
                "size": "large",
                "output_directory": imgDownloadFolder,
                "no_directory": True,
                "chromedriver": "D:\\Git\\Schule\\GDKIPSTA\\TrainingsDataAccuireing\\chromedriver.exe"
            }

            # Providing arguments for the searched query
            try:
                # Downloading the photos based
                # on the given arguments
                downloader.download(arguments)
            except:
                pass


def createDir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def getSearchQueries():
    global search_queries

    with open(pathToQueries, 'r') as f:
        search_queries = f.readlines()

    for i, query in enumerate(search_queries):

        safeQuerySring = query

        safeQuerySring = safeQuerySring.replace("\n", "")
        safeQuerySring = safeQuerySring.replace("\r", "")

        search_queries[i] = safeQuerySring


main()
