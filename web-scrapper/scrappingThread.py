from PyQt5 import QtCore
from scrapping import *
from MovieDL import MovieDL


class ScrappingThread(QtCore.QThread):
    scrapingIterationFinished = QtCore.pyqtSignal(
        list)  # Signal for each iteration
    def __init__(self, index, link):
        super().__init__()
        self.scrappedData = []
        self.genreLinks = getGenres('genre.csv')
        self.link = link
        self.index = index

    def run(self):
        self.getData(self.genreLinks, self.index, self.link)

    def getData(self,genreLinks, index, link):

        url = 'https://www.imdb.com'
        Name, Year, Certificate, Duration, Genre, Rating, Description, Directors, Votes = [
        ], [], [], [], [], [], [], [], []

        while index < len(genreLinks):
            nextLink = link
            while nextLink:
                page = requests.get(nextLink)
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
                self.scrappedData = MovieDL.ReturnList(Name, Year, Certificate, Duration, Genre,
                          Rating, Description, Directors, Votes)
                self.scrapingIterationFinished.emit(self.scrappedData)
                
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
