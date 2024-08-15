import sqlite3
import glicko2

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
    conn.commit()
    cursor.close()


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


    player1.update_player([loserelo],[0],[1])
    player2.update_player([winnerelo],[1],[0])
    
    update1 = player1.getRating()
    update2 = player2.getRating()
    ClosesqliteOBJ(cursor)

    conn = sqlite3.connect("C:\\Users\\diyaj\\myenv\\EsportsManager\\db.sqlite3")
    cursor = conn.cursor()
    sql = (f"UPDATE Users SET Wins='{winnerwins}', ELO='{update1}' WHERE Name='{winner}'")
    cursor.execute(sql)
    conn.commit()

    cursor.execute(f"UPDATE Users SET Losses='{loserlosses}', ELO='{update2}' WHERE Name='{loser}'")
    conn.commit()

    sql = f"INSERT INTO History (Winner,Loser,WinnerElo,LoserElo,WinnerEloChange,LoserEloChange) VALUES ('{winner}','{loser}','{winnerelo}','{loserelo}','{update1-winnerelo}','{update2-loserelo}')"
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    return

def GETallinfofromdb() -> dict:
    cursor = CreatesqliteOBJ()
    sql = f"SELECT Name,Wins,Losses,ELO FROM Users"
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
            }
        })
        z+=1
    return returndict
    
    

if __name__ == "__main__":
    pass