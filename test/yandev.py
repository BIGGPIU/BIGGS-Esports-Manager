import sqlite3
import glicko2
import re
import math

def optimalcleanlist(listobj) -> str:
    '''
    Removes brackets from a list and converts it into a string. use this for putting lists in your db
    '''
    string = str(listobj)
    cleaned_text = re.sub(r'[\[\]]', '', string)
    cleaned_text = re.sub(r"'", '', string)
    return cleaned_text
    
def strip(string) -> str:
    string = str(string).replace("(","")
    string = string.replace("'","")
    string = string.replace("[","")
    string = string.replace("]","")
    string = string.replace('"',"")
    string = string.replace("/","")
    string = string.replace(")","")
    string = string.replace(",","")
    string = string.replace("\\n"," ")
    string = string.replace("\\n\\n"," ")
    return string

def striplist(string) -> list:
    string = str(string).replace("(","")
    string = string.replace("'","")
    string = string.replace("[","")
    string = string.replace("]","")
    string = string.replace('"',"")
    string = string.replace("/","")
    string = string.replace(")","")
    string = string.replace(", ",",")
    string = string.split(",")
    return string

def CreatesqliteOBJ():
    conn = sqlite3.connect("C:\\Users\\diyaj\\myenv\\EsportsManager\\db.sqlite3")
    cursor = conn.cursor()
    return cursor

def ClosesqliteOBJ(var):
    var.close()


def GETnamesFROMdb():
    sql = ("SELECT Name FROM Users")
    cursor = CreatesqliteOBJ()
    cursor.execute(sql)
    hold = cursor.fetchall()
    hold = striplist(hold)
    for i in hold:
        if i == "":
            hold.remove(i)
    ClosesqliteOBJ(cursor)
    return hold

def CREATEuserindb(rawrequest):
    temp = dict(rawrequest)
    create = temp.get("create")
    create = create[0]
    conn = sqlite3.connect("C:\\Users\\diyaj\\myenv\\EsportsManager\\db.sqlite3")
    cursor = conn.cursor()
    sql = (f"INSERT INTO Users (Name,Wins,Losses,ELO) VALUES ('{create}','0','0','1500');")
    cursor.execute(sql)
    sql = f"INSERT INTO Series (Name,SP,TOPONE,TOPTWO,TOPTHREE,PARTICIPATED,RankMultiplier) VALUES ('{create}','0','0','0','0','0','1')"
    cursor.execute(sql)
    conn.commit()
    cursor.close()

def ADDSPtodb(rawrequest,dilute=False):
    temp = dict(rawrequest)
    name = temp.get("tournament")[0]
    placement = temp.get("placement")[0]
    conn = sqlite3.connect("C:\\Users\\diyaj\\myenv\\EsportsManager\\db.sqlite3")
    cursor = conn.cursor()
    sql = f"SELECT SP,TOPONE,TOPTWO,TOPTHREE,PARTICIPATED,RankMultiplier FROM Series WHERE Name='{name}'"
    cursor.execute(sql)
    hold = cursor.fetchall()[0]
    SP = hold[0]
    first = int(hold[1])
    second = int(hold[2])
    third = int(hold[3])
    participated = int(hold[4])
    rmp = GETrmp(cursor,name)
    if dilute == False:
        if placement == "Did Not Place":
            points = 1
            participated += 1
        elif placement == "1":
            points = 5
            first += 1
        elif placement == "2":
            points = 4
            second += 1
        elif placement == "3":
            points = 3
            third += 1
        elif placement == "4":
            points = 2
            participated += 1
    else:
        if placement == "Did Not Place":
            points = 1
        elif placement == "1":
            points = 2
            first += 1
        elif placement == "2":
            points = 2
            second += 1
        elif placement == "3":
            points = 2
            third += 1
        elif placement == "4":
            points = 1
            participated += 1
    SP += int(points*rmp)
    sql = f"UPDATE Series SET SP='{SP}', TOPONE='{first}', TOPTWO='{second}', TOPTHREE='{third}',PARTICIPATED='{participated}',RankMultiplier='{rmp}' WHERE Name='{name}'"
    cursor.execute(sql)
    conn.commit()


def GETrmp(cursor,name):
    sql = f"SELECT Rank FROM Users WHERE Name='{name}'"
    cursor.execute(sql)
    hold = cursor.fetchone()[0]
    if 3 >= hold:
        rmp = 1.00
    elif hold == 4:
        rmp = 1.10
    elif hold == 5:
        rmp = 1.20
    elif hold == 6:
        rmp = 1.30
    return rmp


def ADDgametodb(rawrequest):
    temp = dict(rawrequest)

    winner = temp["player1"]
    loser = temp["player2"]
    winner = winner[0]
    loser = loser[0]

    player1 = glicko2.Player()
    player1.setRd(1)
    player2 = glicko2.Player()
    player2.setRd(1)

    cursor = CreatesqliteOBJ()
    
    try:
        winnerrecent = GETrecentfromdb(cursor,winner)
    except:
        winnerrecent = ["Nobody",1]
    if winnerrecent[0] == loser:
        winnerrecent[1] = int(winnerrecent[1])
        winnerrecent[1] += 1
        winnerdfactor = winnerrecent[1]
    else:
        winnerrecent[0] = loser
        winnerrecent[1] = 1
        winnerdfactor = 1
    try:
        loserrecent = GETrecentfromdb(cursor,loser)
    except:
        loserrecent = ["Nobody",1]
    if loserrecent[0] == winner:
        loserrecent[1] = int(loserrecent[1])
        loserrecent[1] += 1
        loserdfactor = loserrecent[1]
    else:
        loserrecent[0] = winner
        winnerrecent[1] = 1
        loserdfactor = 1

    cursor.execute(f"SELECT ELO FROM Users WHERE Name='{winner}'")
    winnerelo = cursor.fetchone()[0]
    player1.setRating(winnerelo)

    cursor.execute(f"SELECT ELO FROM Users WHERE Name='{loser}'")
    loserelo = cursor.fetchone()[0]
    player2.setRating(loserelo)

    cursor.execute(f"SELECT Wins FROM Users WHERE Name='{winner}'")
    winnerwins = int(cursor.fetchone()[0])
    winnerwins += 1 

    cursor.execute(f"SELECT Losses FROM Users WHERE Name='{loser}'")
    loserlosses = int(cursor.fetchone()[0])
    loserlosses += 1 

    bchange1 = player1.getRating()
    bchange2 = player2.getRating() 

    player1.update_player([loserelo],[80],[1])
    player2.update_player([winnerelo],[80],[0])
    
    update1 = player1.getRating()
    update2 = player2.getRating() 

    finalupdate1 = update1-bchange1
    finalupdate1 = finalupdate1/winnerdfactor
    finalupdate1 = finalupdate1
    update1 = bchange1 + finalupdate1

    finalupdate2 = update2-bchange2
    finalupdate2 = finalupdate2/loserdfactor
    finalupdate2 = finalupdate2
    update2 = bchange2 + finalupdate2
    
    ClosesqliteOBJ(cursor)

    conn = sqlite3.connect("C:\\Users\\diyaj\\myenv\\EsportsManager\\db.sqlite3")
    cursor = conn.cursor()
    sql = (f"UPDATE Users SET Wins='{winnerwins}', ELO='{math.floor(winnerelo+(finalupdate1*100))}', Recent='{optimalcleanlist(winnerrecent)}' WHERE Name='{winner}'")
    cursor.execute(sql)
    conn.commit()

    cursor.execute(f"UPDATE Users SET Losses='{loserlosses}', ELO='{math.floor(loserelo+(finalupdate2*100))}', Recent='{optimalcleanlist(loserrecent)}' WHERE Name='{loser}'")
    conn.commit()

    sql = f"INSERT INTO History (Winner,Loser,WinnerElo,LoserElo,WinnerEloChange,LoserEloChange) VALUES ('{winner}','{loser}','{winnerelo}','{loserelo}','{finalupdate1*100}','{finalupdate2*100}')"
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    UPDATERANKfromdb(winner)
    UPDATERANKfromdb(loser)
    return

def GETrecentfromdb(cursorobj,usr):
    """
    Gets the users most recent opponent in the format 
    [USERNAME,AMOUNT]
    """
    sql = f"SELECT Recent FROM Users WHERE Name='{usr}'"
    cursorobj.execute(sql)
    hold = cursorobj.fetchone()[0]
    hold = hold.split(",")
    for i in range(len(hold)):
        hold[i] = strip(hold[i])
    return hold


def UPDATERANKfromdb(user1):
    conn = sqlite3.connect("C:\\Users\\diyaj\\myenv\\EsportsManager\\db.sqlite3")
    cursor = conn.cursor()
    sql = f"SELECT ELO FROM USERS WHERE NAME='{user1}'"
    cursor.execute(sql)
    returned = cursor.fetchall()[0]
    returned = returned[0]
    if 800 >= returned:
        x = 1 # Wood
    elif 801 <= returned <= 1200:
        x = 2 # Bronze
    elif 1201 <= returned <= 1700:
        x = 3 # Silver
    elif 1701 <= returned <= 1900:
        x = 4 # Diamond
    elif 1901 <= returned <= 2300:
        x = 5 # Platinum
    elif 2301 < returned:
        x = 6 # HOM
    sql = f"UPDATE Users SET Rank='{x}' WHERE Name='{user1}'"
    cursor.execute(sql)
    conn.commit()
    conn.close()

    
def GETallinfofromdb() -> dict:
    cursor = CreatesqliteOBJ()
    sql = f"SELECT Name,Wins,Losses,ELO,Rank FROM Users ORDER BY ELO DESC"
    cursor.execute(sql)
    hold = cursor.fetchall()
    returndict = {}
    z = 1 
    for i in hold:
        returndict.update({
            z: {
                "Name":i[0],
                "Wins":i[1],
                "Losses":i[2],
                "ELO":i[3],
                "Rank":i[4],
            }
        })
        z+=1
    return returndict

def GETallSPinfofromdb():
    cursor = CreatesqliteOBJ()
    sql = f"SELECT Name,SP,TOPONE,TOPTWO,TOPTHREE,PARTICIPATED,RankMultiplier FROM Series ORDER BY SP DESC"
    cursor.execute(sql)
    hold = cursor.fetchall()
    returndict = {}
    z = 1
    for i in hold:
        returndict.update({
            z: {
                "Name":i[0],
                "SP":i[1],
                "1st":i[2],
                "2nd":i[3],
                "3rd":i[4],
                "DNP":i[5],
                "Multiplier":i[6]
            }
        })
        z+=1
    return returndict
    
def UPDATErankperiod() -> None:
    cursor = CreatesqliteOBJ()
    sql = "SELECT * FROM Users"
    cursor.execute(sql)
    allusers = cursor.fetchall()
    userdict = {}
    x = 0 
    for i in allusers:
        sql = f"SELECT * FROM Series WHERE Name='{i[0]}'"
        cursor.execute(sql)
        series = cursor.fetchall()
        userdict.update({
            f"{x}":{"User":i[0],
            "Wins":i[1],
            "Losses":i[2],
            "ELO":i[3],
            "Rank":i[5],
            "1st":series[0][2],
            "2nd":series[0][3],
            "3rd":series[0][4],
            "DNP":series[0][5]}
        })
        x+=1
    
    ClosesqliteOBJ(cursor)

    conn = sqlite3.connect("C:\\Users\\diyaj\\myenv\\EsportsManager\\db.sqlite3")
    cursor = conn.cursor()

    
    for i in userdict:
        donotedit = False
        try:
            sql = f"SELECT * FROM UserHistory WHERE Username='{userdict[i]['User']}'"
            cursor.execute(sql)
            hold = cursor.fetchall()
            hold = hold[0]
            elohistory = hold[1]
        except:
            sql = f"INSERT INTO UserHistory VALUES ('{userdict[i]['User']}','{userdict[i]['ELO']}','{userdict[i]['Wins']}','{userdict[i]['Losses']}','{userdict[i]['1st']}','{userdict[i]['2nd']}','{userdict[i]['3rd']}','{userdict[i]['DNP']}')"                                                                                
            cursor.execute(sql)
            conn.commit()
            sql = f"SELECT * FROM UserHistory WHERE Username='{userdict[i]['User']}'"
            cursor.execute(sql)
            hold = cursor.fetchall()
            hold = hold[0]
            elohistory = hold[1]
            donotedit = True
        if donotedit == False:
            elohistory += f",{userdict[i]['ELO']}"
            winhistory = hold[2]
            winhistory += f",{userdict[i]['Wins']}"
            losshistory = hold[3]
            losshistory += f",{userdict[i]['Losses']}"
            firsthistory = hold[4]
            firsthistory += f",{userdict[i]['1st']}"
            secondhistory = hold[5]
            secondhistory += f",{userdict[i]['2nd']}"
            thirdhistory = hold[6]
            thirdhistory += f",{userdict[i]['3rd']}"
            DNP = hold[7]
            DNP += f",{userdict[i]['DNP']}"

            sql = f"UPDATE UserHistory SET EloHistory='{elohistory}', WinHistory='{winhistory}', LossHistory='{losshistory}', FirstHistory='{firsthistory}', SecondHistory='{secondhistory}', ThirdHistory='{thirdhistory}', DnpHistory='{DNP}' WHERE Username='{userdict[i]['User']}'"
            cursor.execute(sql)
            conn.commit()

        

        



            

if __name__ == "__main__":
    UPDATErankperiod()