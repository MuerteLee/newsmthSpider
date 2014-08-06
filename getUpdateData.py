import urllib.parse  
import urllib.request  
import datetime
import sqlite3
import os

defaultPage = 1
class dataBase(object):
    def __init__(self, dataBasePath):
        super().__init__();
        if not os.path.isfile(dataBasePath):
           conn = sqlite3.connect(dataBasePath) 
           cu = conn.cursor()
           cu.execute("create table newsmthUpdate(id integer primary key autoincrement, urlID integer, nameTitle varchar(128), postTime varchar(128), updateKey interger, pageNum interger)")
           conn.close()  

        self.dataBasePath = dataBasePath;

    def connectData(self,):
        return sqlite3.connect(self.dataBasePath); 

    def insertData(self, conn, urlID, nameTitle, postTime, updateKey,pageNum):
        self.urlID = urlID;
        self.nameTitle = nameTitle;
        self.postTime = postTime;
        self.updateKey = updateKey;
        self.pageNum = pageNum;

        cu = conn.cursor(); 
        cmdLineInsert = "insert into newsmthUpdate values((select max(ID) from newsmthUpdate)+1," + self.urlID + "," + self.nameTitle + "," + self.postTime + "," + self.updateKey + "," + self.pageNum + ")"
        cu.execute(cmdLineInsert)
        conn.commit()

    def closeSqlite3(self, conn):
        conn.close()

    def searchURLSqlite3(self,conn, urlID):
        cur = conn.cursor()
        try:
            cur.execute("select * from newsmthUpdate where urlID=%s" %urlID)
            if len(cur.fetchall()) == 0:
                return True;
            else:
                return False;
        except sqlite3.Error as e:
            print("ERROR: searchURLSqlite3 error, please check your param! \n")
            return False;

    def getPostTimeByUrlID(self,conn, urlID, pageNum):
        cur = conn.cursor()
        try:
            cur.execute("select postTime from newsmthUpdate where urlID=%d and pageNum=%d" %(urlID,pageNum))
            if len(cur.fetchall()) == 0:
                return False;
            else:
                cur.execute("select postTime from newsmthUpdate where urlID=%d and pageNum=%d" %(urlID,pageNum))
                return cur.fetchall()[0][0];
        except sqlite3.Error as e:
            print("ERROR: searchURLSqlite3 error, please check your param! \n")
            return False;

    def getPostTime(self,conn, pageNum):
        cur = conn.cursor()
        try:
            cur.execute("select postTime, urlID from newsmthUpdate where pageNum=%d" %(pageNum))
            if len(cur.fetchall()) == 0:
                return False;
            else:
                cur.execute("select postTime, urlID from newsmthUpdate where pageNum=%d" %(pageNum))
                return cur.fetchall();
        except sqlite3.Error as e:
            print("ERROR: searchURLSqlite3 error, please check your param! \n")
            return False;
    
    def updatePageNum(self, conn, urlID):
        cur = conn.cursor()
        try:
            cur.execute("UPDATE newsmthUpdate SET pageNum = 0 where urlID=%d" %urlID)
            conn.commit()
        except sqlite3.Error as e:
            print("ERROR: updatePageNum error, please check your param! \n")
            conn.rollback()
            return False;

    def updateMaxIdPageNum(self,conn,id):
        cur = conn.cursor()
        try:
            cur.execute("UPDATE newsmthUpdate SET pageNum = 0 where  id=%d" %id)
            conn.commit()
        except sqlite3.Error as e:
            print("ERROR: updatePageNum error, please check your param! \n")
            conn.rollback()
            return False;

def currentTime():
    now = datetime.datetime.now()
    return str(now).split(' ')[0].split('-')

class parseTestUrl(dataBase):
    def __init__(self, URL, dataBasePath):
        dataBase.__init__(self,dataBasePath)
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        try:
            data = opener.open(URL).read()
        except Exception as e:
            print("Error: open url=%s error\n" %URL)
            return False
        self.dataSite = data.decode('GBK').split('</th></tr></thead><tbody><tr ')[1].split("</a></td></tr></tbody></table></div>")[0].split('</a></td></tr><tr ><td class="title_8">')[1:]
        self.dataBasePath = dataBasePath
        self.sql = dataBase(self.dataBasePath)
        self.conn = self.sql.connectData()

    def returnDateSite(self,):
        return self.dataSite

    def getDay(self, sql, conn, topicID):
        return (sql.getPostTimeByUrlID(conn, int(topicID.strip()), 1))

    def getTopicID(self,):
        topicIDD=[]
        nowDay = currentTime()
        testKey = ["\u6d4b\u8bd5","QE","test","Test","qa","QA","qe"]
        startDay = datetime.datetime(int(nowDay[0]),int(nowDay[1]),int(nowDay[2]))

        for i in range(0, len(self.dataSite)):
           dataSiteTmp = (self.dataSite[i].split('</samp></a></td><td class="title_9">')[1].split('</td><td class="title_10">'))
           topicID = dataSiteTmp[0].split('">')[0].split('/')[-1].strip()
           topicTitle = dataSiteTmp[0].split('">')[1].strip()
           topicTime = dataSiteTmp[1].split('</td><td class="title_12">')[0].replace('&emsp;','').strip()
           if topicTime.find(':') != -1:
                topicTime = str(datetime.datetime.now()).split(' ')[0]

           topicUser = dataSiteTmp[1].split('</td><td class="title_12">')[1].split('class="c63f">')[1].split('</a></td><td class="title_11 middle">')[0].strip()
           topicTimeDetail = topicTime.split('-')
           
           endDay = datetime.datetime(int(topicTimeDetail[0]),int(topicTimeDetail[1]),int(topicTimeDetail[2]))
           if ((startDay - endDay).days) < 7:
                for key in range(0, len(testKey)):
                    if topicTitle.find(testKey[key]) == -1 and topicUser != 'muerte':
                        topicIDD.append(topicID)
#                        print("postTopic ID is = %s" %topicID)
                        break
        return topicIDD

    def getData(self,):
        global defaultPage
        countEffective = 1
        nowDay = currentTime()
        testKey = ["\u6d4b\u8bd5","QE","test","Test","qa","QA","qe"]
        startDay = datetime.datetime(int(nowDay[0]),int(nowDay[1]),int(nowDay[2]))

        for i in range(0, len(self.dataSite)):
           dataSiteTmp = (self.dataSite[i].split('</samp></a></td><td class="title_9">')[1].split('</td><td class="title_10">'))
           topicID = dataSiteTmp[0].split('">')[0].split('/')[-1].strip()
           topicTitle = dataSiteTmp[0].split('">')[1].strip()
           topicTime = dataSiteTmp[1].split('</td><td class="title_12">')[0].replace('&emsp;','').strip()
           if topicTime.find(':') != -1:
                topicTime = str(datetime.datetime.now()).split(' ')[0]

           topicUser = dataSiteTmp[1].split('</td><td class="title_12">')[1].split('class="c63f">')[1].split('</a></td><td class="title_11 middle">')[0].strip()
           topicTimeDetail = topicTime.split('-')
           
           endDay = datetime.datetime(int(topicTimeDetail[0]),int(topicTimeDetail[1]),int(topicTimeDetail[2]))
#           print(self.getDay(sql, conn, topicID))
           if ((startDay - endDay).days) < 7:
                for key in range(0, len(testKey)):
                    if topicTitle.find(testKey[key]) == -1 and topicUser != 'muerte':
                        topicTitle = "'" + topicTitle+"'"
                        topicTime = "'"+topicTime+"'"
                        if self.sql.searchURLSqlite3(self.conn, topicID):
                           self.sql.insertData(self.conn, topicID, topicTitle, topicTime, '0', '1')
#                        print("postTopic ID is = %s" %topicID)
#                        print("postTopic title is = %s" %topicTitle)
#                        print("postTopic time is = %s" %topicTime)
#                        print("postTopic User is = %s\n" %topicUser)
                        break
           else:
                countEffective += 1 
        if countEffective  < 30:
                defaultPage += 1 

class updateTopic():
    def __init__(self,):
        super().__init__()
        urlDefault = 1
        dataBasePath = "/home/licaijun/newsmthUpdate.db"
        while(1):
            url="http://www.newsmth.net/nForum/board/SoftwareTesting?p="+str(urlDefault)+"?ajax"
            parseurl = parseTestUrl(url, dataBasePath)
#            print(parseurl.getTopicID())
            parseurl.getData()
            if defaultPage > urlDefault:
                   urlDefault = defaultPage
            else:
                   break;


if __name__ == "__main__":
    updateTopic()
