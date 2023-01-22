import os

video_extensions = ['.264', '.3g2', '.3gp', '.arf', '.asf', '.asx', '.avi', '.bik', '.dash', 
'.dat', '.dvr', '.flv', '.h264', '.m2t', '.m2ts', '.m4v', '.mkv', '.mod', '.mov', '.mp4',
 '.mpeg', '.mpg', '.mts', '.ogv', '.proproj', '.rec', '.rmvb', '.swf', '.tod', '.tp', '.ts',
'.vob', '.webm', '.wlmp', '.wmv']

audio_extensions = ['.pcm', '.wav', '.aiff', '.mp3', '.aac', '.ogg', 
'.wma', '.flac', '.alac', '.cda', '.mid', '.midi', '.wpl', '.m4a']

picture_extensions = ['.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg',
 '.png', '.ps', '.psd', '.svg', '.tif', '.tiff']

word_extensions = ['.doc', '.docx', '.odt', '.pdf', '.rtf', '.tex', '.txt', 
'.wks', '.wps', '.wpd', '.ods', '.xlr', '.xls', '.xlsx', '.key', '.odp', 
'.pps', '.ppt', '.pptx', '.epub', '.log']

data_persistance = ['.csv', '.json']

pl_extensions = ['.c', '.class', '.cpp', '.cs', '.h', '.java', '.sh', '.swift',
 '.vb', '.css', '.html', '.htm', '.js', '.jsp', '.php', '.py', '.rss', '.rb',
  '.xhtml', '.db', '.sql', '.xml', '.jar', '.md', '.cfg']
zip_extensions = ['.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.gz', '.z', '.zip', '.xz']
executeables = [".exe", ".msi", ".out"]

class Classifier:
    ''''''
    def __init__(self, filename):
        self.filename = filename
        
    def isVideo(self):
        splitted = os.path.splitext(self.filename)
        if splitted[1]:
            if splitted[1].lower() in video_extensions:
                return True
            else:
                return False
        else:
            return False
    
    def isAudio(self):
        splitted = os.path.splitext(self.filename)
        if splitted[1]:
            if splitted[1].lower() in audio_extensions:
                return True
            else:
                return False
        else:
            return False
        
    def isPicture(self):
        splitted = os.path.splitext(self.filename)
        if splitted[1]:
            if splitted[1].lower() in picture_extensions:
                return True
            else:
                return False
        else:
            return False
        
    def isDoc(self):
        splitted = os.path.splitext(self.filename)
        if splitted[1]:
            if splitted[1].lower() in word_extensions:
                return True
            else:
                return False
        else:
            return False
        
    def isPersistance(self):
        splitted = os.path.splitext(self.filename)
        if splitted[1]:
            if splitted[1].lower() in data_persistance:
                return True
            else:
                return False
        else:
            return False
    
    def isProg(self):
        splitted = os.path.splitext(self.filename)
        if splitted[1]:
            if splitted[1].lower() in pl_extensions:
                return True
            else:
                return False
        else:
            return False
    
    def isCompressed(self):
        splitted = os.path.splitext(self.filename)
        if splitted[1]:
            if splitted[1].lower() in zip_extensions:
                return True
            else:
                return False
        else:
            return False
        
    def isExecutable(self):
        splitted = os.path.splitext(self.filename)
        if splitted[1]:
            if splitted[1].lower() in executeables:
                return True
            else:
                return False
        else:
            return False