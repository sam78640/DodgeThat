import urllib.request
import urllib.response


class Get_Details():
    def __init__(self,username):
        self.username = username

    def get_points(self):
        self.req = urllib.request.Request("http://dodgethat.co.uk/user.php?username="+str(self.username)+"&get=points")
        self.res = urllib.request.urlopen(self.req)
        self.read = str(self.res.read())
        self.read = self.read.split("b'")
        self.read = self.read[1]
        self.read = self.read.split("'")
        self.read = self.read[0]
        return self.read

    def register_user(self):
        self.url = "http://dodgethat.co.uk/register.php?username="+str(self.username)+"&password=sameer123"
        self.req_u = urllib.request.Request(self.url)
        self.res_u = urllib.request.urlopen(self.url)
        self.read_u = str(self.res_u.read)
        return True

    def update_score(self,points):
        self.url = "http://dodgethat.co.uk/user.php?username="+str(self.username)+"&action=update&password=sameer123&points="+str(points)
        self.update = urllib.request.urlopen(self.url)
        return True


    def upload_score(self,points):
        url1 = "http://dodgethat.co.uk/upload_recent.php?username="+str(self.username)+"&points="+str(points)+"&password=sameer123"
        urllib.request.urlopen(url1)
        return True
    def save_user(self,username):
        file = open ("user.dat","wt")
        file.write(username)
        file.close()
    def load_user(self):
        username = []
        file = open ("user.dat",'rt')
        for users in file:
            username.append(users)
        return username[0]




