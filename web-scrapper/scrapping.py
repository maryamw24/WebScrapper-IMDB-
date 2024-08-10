import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def writeData(Name, Year, Certificate, Duration, Genre, Rating, Description, Directors, Votes):
    df = pd.DataFrame(
        {'Name': Name, 'Year': Year, 'Certificate': Certificate, 'Duration': Duration,
         'Genre': Genre, 'Rating': Rating, 'Description': Description, 'Directors': Directors, 'Votes': Votes})
    df.to_csv('scrappingMovies.csv', encoding='utf-8',
              index=False, mode='a', header=False)


def getGenres(filename):
    genres = []
    with open(filename, mode='r') as file:
        genres = file.readlines()
    return genres


def saveProgress(filename, index, link):
    with open(filename, mode='w') as file:
        file.write(str(index)+','+link)


def loadProgress(filename):
    index = 0
    link = ''
    with open(filename, mode='r') as file:
        line = file.readlines()[0]
        line = line.split(',')
        index = int(line[0])
        link = line[1]
    return index, link


def getData(genreLinks,index,link):
   
    url = 'https://www.imdb.com'
    Name, Year, Certificate, Duration, Genre, Rating, Description, Directors, Votes = [
    ], [], [], [], [], [], [], [], []

    while index < len(genreLinks):
        nextLink = link
        while nextLink:
            page=requests.get(nextLink)
            content = page.text
            soup = BeautifulSoup(content, features="html.parser")
            movieCards = soup.find_all(
                'div', attrs={'class': 'lister-item mode-advanced'})
            for movie in movieCards:
                header = movie.find(
                    'h3', attrs={'class': 'lister-item-header'})

                # Get name
                name = header.find('a')
                Name.append(name.text if name else "No Name")

                # Get Year
                year = movie.find(
                    'span', attrs="lister-item-year text-muted unbold")
                yearText = year.text.strip()
                yearMatch = re.search(r'\d{4}', yearText)
                Year.append(int(yearMatch.group()) if yearMatch else 0)

                # Get certificate
                certificate = movie.find(
                    'span', attrs={'class': 'certificate'})
                Certificate.append(
                    certificate.text if certificate else "No Certificate")

                # Get Time
                time = movie.find('span', attrs={'class': 'runtime'})
                timeText = time.text.strip() if time else '000'
                timeMatch = re.search(r'\d{3}', timeText)
                Duration.append(int(timeMatch.group()) if timeMatch else 0)

                # Get Genere
                genre = movie.find('span', attrs={'class': 'genre'})
                Genre.append(genre.text.strip().replace(
                    '\n', '') if genre else "No Genre")

                # Get rating
                rating = movie.find('strong')
                Rating.append(float(rating.text) if rating else 0.0)

                # Get Description
                desc = movie.find_all('p', attrs={'class': 'text-muted'})
                Description.append(desc[1].text.strip().replace(
                    '\n', '') if desc else "No Description")

                # Get Director
                director = movie.find_all('p', attrs={'class': ''})
                director = director[0]
                anchor = director.find('a') if director else ''
                Directors.append(anchor.text if anchor else "")

                # Get Votes
                vote = movie.find_all('span', attrs={'name': 'nv'})
                Votes.append(vote[0].text if vote else '0')
            saveProgress('progress.csv', index, nextLink)
            writeData(Name, Year, Certificate, Duration, Genre,
                      Rating, Description, Directors, Votes)
            Name, Year, Certificate, Duration, Genre, Rating, Description, Directors, Votes = [
            ], [], [], [], [], [], [], [], []
            nextPage = soup.find(
                'a', attrs={'class': 'lister-page-next next-page'})
            if nextPage and nextPage.has_attr("href"):
                nextLink = url + nextPage['href']
            else:
                index += 1
                break
        if index < len(genreLinks):
            link = genreLinks[index]
            saveProgress('progress.csv', index, link)
        else:
            break


if __name__ == "__main__":
    genreLinks = getGenres('genre.csv')
    index, link = loadProgress("progress.csv")
    getData(genreLinks,index,link)