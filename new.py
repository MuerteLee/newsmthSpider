import urllib.parse  
import re, time,os 
import urllib.request  
import sqlite3

class sqliteOS3(object):
    def __init__(self, dataBasePath):
        super().__init__();
        if not os.path.isfile(dataBasePath):
           conn = sqlite3.connect(dataBasePath) 
           cu = conn.cursor()
           cu.execute("create table newsmth(id integer primary key autoincrement, urlID integer, nameTitle varchar(128) UNIQUE, postTime varchar(128) UNIQUE, sendKey interger)")
           conn.close()  

        self.dataBasePath = dataBasePath;
#        print(dataBasePath)

    def connectData(self,):
        return sqlite3.connect(self.dataBasePath); 

    def insertData(self, conn, urlID, nameTitle, postTime, sendKey):
        self.urlID = urlID;
        self.nameTitle = nameTitle;
        self.postTime = postTime;
        self.sendKey = sendKey;

#       print(self.dataBasePath)
        #conn = sqlite3.connect(self.dataBasePath);
        cu = conn.cursor(); 
        cmdLineInsert = "insert into newsmth values((select max(ID) from newsmth)+1," + self.urlID + "," + self.nameTitle + "," + self.postTime + "," + self.sendKey + ")"
#        print(cmdLineInsert)
        cu.execute(cmdLineInsert)
        conn.commit()

    def closeSqlite3(self, conn):
#        conn = self.connectData();
        conn.close()

    def searchAllSqlite3(self,conn):
        cur = conn.cursor()
        cur.execute('select * from newsmth')
        return (cur.fetchall())

    def searchURLSqlite3(self,conn, urlID):
        cur = conn.cursor()
        try:
            cur.execute("select * from newsmth where urlID=%s" %urlID)
            if len(cur.fetchall()) == 0:
                return True;
            else:
                return False;
        except sqlite3.Error as e:
            print("ERROR: searchURLSqlite3 error, please check your param! \n")
            return False;

    def searchNameTitleFromSqlite3(self,conn,urlID):
        cur = conn.cursor()
        try:
            cur.execute("select nameTitle from newsmth where urlID=%d" %urlID)
            return cur.fetchall();
        except sqlite3.Error as e:
            print("ERROR: searchNameTitleFromSqlite3 error, please check your param! \n")
            return False;

    def searchURLIdFromSqlite3(self,conn,sendKey):
        cur = conn.cursor()
        try:
            cur.execute("select urlID from newsmth where sendKey=%d" %sendKey)
            return cur.fetchall();
        except sqlite3.Error as e:
            print("ERROR: searchURLIdFromSqlite3 error, please check your param! \n")
            return False;

    def updateSendKeyValue(self, conn, urlID):
        cur = conn.cursor()
        try:
            cur.execute("UPDATE newsmth SET sendKey = 1 where urlID=%d" %urlID)
            conn.commit()
        except sqlite3.Error as e:
            print("ERROR: updateSendKeyValue error, please check your param! \n")
            conn.rollback()
            return False;
pUrlValue = 1
class parseUrl(sqliteOS3):
    def __init__(self, URL, dataBasePath):
        sqliteOS3.__init__(self, dataBasePath) 
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        data = opener.open(URL).read()
        self.mainData = data.decode("utf8").split('<div class="sec nav">')[-2].split('class="top"')[-1].split("</a></div></li>")
        self.dataBasePath = dataBasePath

    def getData(self):
        sql = sqliteOS3(self.dataBasePath)
        global pUrlValue 
        conn = sql.connectData()
        pValue = 0
        testKey = ["\u6d4b\u8bd5","QE","test","Test","qa","QA","qe"]
        for i in range(0, len(self.mainData)):
            if self.mainData[i].find("Career_Upgrade") != -1:
                urlLine = self.mainData[i].find('<a href="/article/Career_Upgrade/')
                if self.mainData[i][urlLine:].split('&nbsp;')[0].split('</div><div>')[-1].find(":") != -1:
                    pValue += 1;
                aLine = self.mainData[i][urlLine:].split('&nbsp;')[0].split('</div><div>')[0].find('</a>')
                #title
                for key in range(0,len(testKey)):
                    if ((re.sub('\d\d'+';', '',self.mainData[i][urlLine:].split('&nbsp;')[0].split('</div><div>')[0][:aLine].split('">')[-1]).replace('&#','')).strip()).find(testKey[key]) != -1:
                        titleName = (re.sub('\d\d'+';', '',self.mainData[i][urlLine:].split('&nbsp;')[0].split('</div><div>')[0][:aLine].split('">')[-1]).replace('&#','')).strip()
#                        print(titleName)
                        # urlId
                        urlID = self.mainData[i][urlLine:].split('&nbsp;')[0].split('</div><div>')[0][:aLine].split('">')[0].split('<a href="/article/Career_Upgrade/')[-1]
#                       print(urlID)
                        if self.mainData[i][urlLine:].split('&nbsp;')[0].split('</div><div>')[-1].find(":") != -1:
#                            pValue += 1;
                        #time
                            timePost = time.strftime('%Y-%m-%d',time.localtime(time.time())) + ' ' +self.mainData[i][urlLine:].split('&nbsp;')[0].split('</div><div>')[-1]
                            timePost = "'"+timePost+"'"
#                            print(timePost)
                            titleName ="'" + titleName + "'"
#                            print(titleName)

                            if sql.searchURLSqlite3(conn, urlID):
                                sql.insertData(conn, urlID, titleName, timePost, '0')

        print(sql.searchAllSqlite3(conn));
        sql.closeSqlite3(conn);
        if pValue >= 1:
            pUrlValue += 1
#            print(pUrlValue)

class parseURL:
    def __init__(self, URLID):
        super() .__init__();
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]

        URL = "http://www.newsmth.net/nForum/article/Career_Upgrade/"+URLID+"?ajax"
        self.URL = URL
        print(URL)
        try:
            data = opener.open(URL).read()
            self.mainUrlData = data.decode("GBK")
        except sqlite3.Error as e:
            print("Open url:%s is error, please check the URL!~\n" %URL)

    def parseURL(self,):
        try:
            if self.mainUrlData.find('<p>') == -1:
                print("\n\nThe URL maybe not exist, please check %s \n" %self.URL)
                return False 
            contextURL = self.mainUrlData.split('<p>')[1].split('FROM')[0].replace('&nbsp;','')
        except sqlite3.Error as e:
            print("Open url:%s is error, please check the URL!~\n" %self.URL)

        if contextURL.find('--<br ') != -1:
            return (contextURL.split('--<br ')[0])
        elif contextURL.find('-- <br ') != -1: 
            return (contextURL.split('-- <br ')[0])

class postMsg(sqliteOS3):
    def __init__(self, dataBasePath):
        sqliteOS3.__init__(self, dataBasePath) 
        sql = sqliteOS3(dataBasePath)
        conn = sql.connectData()
        return sql.searchURLIdFromSqlite3(conn, 0);

#        URLIDData = sql.searchURLIdFromSqlite3(conn, 0)
        
#    def urlContext
#        for i in range(0, len(URLIDData)):
#            URLID = URLIDData[i][0]
#            parseURLWeb = parseURL(str(URLID))
#            if parseURLWeb.parseURL():
#                print('\n')
#                print(str(sql.searchNameTitleFromSqlite3(conn,URLID)[0]).replace('(','').replace(')','').replace("'","")+":(Reprint)")
#                print(parseURLWeb.parseURL())
#                sql.updateSendKeyValue(conn,URLID);
#        print(sql.searchAllSqlite3(conn));

#if __name__ == '__main__':
class sendMsg:
    def __init__(self,):
        super().__init__();
        urlDefault = 1
        dataBasePath = "/home/licaijun/newsmth.db"
        while(1):
            url="http://m.newsmth.net/board/Career_Upgrade?p="+str(urlDefault)+"?ajax"  
            print(url)
            parseurl = parseUrl(url, dataBasePath)
            parseurl.getData()
            if pUrlValue > urlDefault:
                urlDefault = pUrlValue;
            else:
                break;

        URLIDDICT = postMsg(dataBasePath)
        return URLIDDICT
