# class ConnectServer:
#     def __init__(self,hostname,username,password):
#         self.hostname = hostname
#         self.username = username
#         self.password = password
#     def connection(self):
#         self.ftp = ftp(self.hostname)
#         self.ftp.login(self.username,self.password)
#         self.ftp.cwd('/public_html/')
#     def get_file(self):
#         self.connection()
#         self.file = open('scores.txt','wb')
#         self.ftp.retrbinary('RETR scores.txt',self.file.write,1024)
#         self.ftp.quit()
#         self.file.close()
#     def write_file(self):
#         self.connection()
#         self.ftp.storbinary('STOR scores.txt',open('scores.txt','rb'))
#         self.ftp.quit()
#
# class GetServerScores:
#     def __init__(self):
#         self.server = ConnectServer("server27.000webhost.com","a5332880","sameer123")
#         self.server.get_file()
#
#     def add_data(self,score):
#         self.server.get_file()
#         self.file_open = open('scores.txt','wt')
#         self.file_open.write(str(score))
#         self.file_open.close()
#         self.server.write_file()
#     def read_data(self):
#         self.file_read = open('scores.txt','rt')
#         for lines in self.file_read:
#             return lines
#         self.file_read.close()