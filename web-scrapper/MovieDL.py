import pandas as pd
from Movie import Movie


class MovieDL:
    __movies = []

    @classmethod
    def addMovie(cls, movie):
        cls.__movies.append(movie)

    @classmethod
    @property
    def movies(cls):
        return cls.__movies
    
    @staticmethod
    def ReturnList(title, year, certificate, duration, genre, rating, description, director, votes):
        list = []
        for i in range(len(title)):
            movie = Movie(title[i], year[i], certificate[i], duration[i], genre[i], rating[i], description[i], director[i], votes[i])
            list.append(movie)
        return list
    
    @staticmethod
    def loadMovies(filename):
        dataFrame = pd.read_csv(filename)
        for index, row in dataFrame.iterrows():
            # Year, Certificate, Duration, Genre, Rating, Description, Director, Votes
            movie = Movie(row['Title'], int(row['Year']), row['Certificate'], int(row['Duration']), row['Genre'],
                          float(row['Rating']), row['Description'], row['Director'], int(row['Votes']))
            MovieDL.addMovie(movie)

    