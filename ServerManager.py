import urllib.request
import urllib.response
import urllib.parse


class Scores:
    def __init__(self):
        print ("Server Connected")

    def load_website(self,url):
        self.req = urllib.request.Request(url)
        self.res = urllib.request.urlopen(self.req)
        self.resData = self.res.read()
        return self.resData

    def compare_scores(self,previous_score,new_score):
        if int(previous_score) < int(new_score):
            return True
        else:
            return False
    def upload_score(self,previous_score,new_score):
        self.compare = self.compare_scores(previous_score,new_score)
        if  self.compare == True:
            self.req_up = urllib.request.Request("http://dodgethat.co.uk/upload.php?score="+str(new_score)+"&password=sameer123")
            self.res_up = urllib.request.urlopen(self.req_up)
            self.res_up_read = self.res_up.read()
        else:
            print ("")

    def break_score(self,string_to_break):
        self.score = str(string_to_break)
        self.score = self.score.split("b'")
        self.score = self.score[1]
        self.score = self.score.split("'")
        self.score = self.score[0]
        return self.score

    def get_num_score(self):
        return self.break_score(self.load_website("http://dodgethat.co.uk/get.php"))

    def run(self,new_score):
        self.previous_score = self.get_num_score()
        self.upload_score(self.previous_score, new_score)
