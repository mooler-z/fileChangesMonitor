import os, re
import string
from classify_files import Classifier

class PicVidDiff:
    '''instantiate the class with the first argument as the movie poster
    name and second argument the path to the movies location:
    
        inst = PicVidDiff("movie poster name.jpeg", "/path/to/movies/folder")
        result = inst.predictMovie()
        
    '''
    def __init__(self, picName, searchPath):
        self.possible_separators = ['.', '-', '_']
        self.picName = picName
        self.searchPath = searchPath
        self.posPatterns = [r'199\d{1}|201\d{1}|202\d{1}', r'\d+p']
        
    def getPatterned(self, fileName):
        if Classifier(fileName).isPicture() or Classifier(fileName).isVideo():
            nameOnly = os.path.splitext(fileName)[0]
            for pattern in self.posPatterns:
                rs = re.search(pattern, nameOnly)
                if rs:
                    nameOnly = nameOnly[:rs.start()]
                    return nameOnly.strip()
            else:
                return nameOnly
        else:
            return
            
    def partSplit(self, result):
        _split = result
        for p in self.possible_separators:
            res = _split.split(p)
            _split = " ".join(res)
        else:
            _split = _split.split(" ")
        return _split
    
    def splitPattern(self, customName=""):
        if not customName:
            result = self.getPatterned(self.picName)
        else:
            result = self.getPatterned(customName)
        if result:
            result = self.partSplit(result)
            return result
        else:
            return
    
    def getMovies(self):
        walks = os.walk(self.searchPath)
        videos = []
        for tups in walks:
            for tup in tups[2]:
                if Classifier(tup).isVideo():
                    videos.append(os.path.join(tups[0],tup))
        return videos
    
    def compareArrays(self, picArr, vidArr):
        picArr = [i.lower() for i in picArr]
        vidArr = [i.lower() for i in vidArr]
        
        count = 0
        for arr in picArr:
            if arr in vidArr:
                count += 1
                
        predNum = count/len(picArr) * 100
        if predNum >= 51:
            return predNum
        else:
            return 0
    
    def predictMovie(self):
        possible_movies = self.getMovies()
        picNameAnalysis = self.splitPattern()
        if len(picNameAnalysis) >= 3:
            picNameAnalysis = picNameAnalysis[:3]
    
        possibilities = []
        for movie in possible_movies:
            movie_arr = self.splitPattern(os.path.basename(movie))
            if len(movie_arr) >= 3:
                movie_arr = movie_arr[:3]
                
            res = self.compareArrays(picNameAnalysis, movie_arr)
            if res:
                possibilities.append([movie, res])
        
        maxPrediction = 0
        maxPred = []
        if len(possibilities) > 1:
            for poss in possibilities:
                if poss[1] > maxPrediction:
                    maxPrediction = poss[1]
                    maxPred = poss
            return maxPred[0][0]
        
        elif len(possibilities)==1:
            return possibilities[0][0]

        else:
            return "Movie not found"

##################### Example #####################
# d = PicVidDiff("detective-pikachu-photo-u2.jpeg", "../test/Browser")
# print(d.predictMovie())
##################### Example #####################