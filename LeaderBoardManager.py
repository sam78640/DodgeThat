import urllib.request
import urllib.response


class LeaderBoardManager:
    def __init__(self):
        print ("Leaderboard Connected")

    def get_data(self):
        self.url = "http://dodgethat.co.uk/leaderboard.php"
        self.req = urllib.request.Request(self.url)
        self.res = urllib.request.urlopen(self.req)
        self.read = str(self.res.read())
        return self.read

    def break_down(self):
        self.text = self.get_data()
        self.text = self.text.split("b'")
        self.text = self.text[1]
        self.text = self.text.split("'")
        self.text = self.text[0]
        return self.text

    def break_down_line(self):
        self.broken = self.break_down()
        self.broken = self.broken.split(";")
        return self.broken[:-1]

    def run(self):
        self.data = self.break_down_line()
        return self.data
