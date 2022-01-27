import psycopg2

def newRequest(dbname,ip,port,username,schemaName,schemaPass,newTokenTitle,assignTeam,priority,ctime,cdate):
    conn = psycopg2.connect(
    database=f'{dbname}', user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    cursor.execute(f"insert into tokendata values((select COALESCE(max(tokenno)+1,1) from tokendata),'{username}','{newTokenTitle}','{assignTeam}','{priority}','{ctime}','{cdate}')")
    conn.commit()
    cursor.execute(f"SELECT tokenno FROM tokendata where username = '{username}' and ctime='{ctime}' and cdate='{cdate}'")
    tokenid = cursor.fetchone()
    conn.close()
    return f"{tokenid[0]}"

def retriveData(dbname,ip,port,schemaName,schemaPass):
    conn = psycopg2.connect(
    database=f'{dbname}', user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    cursor.execute(f"select * from tokendata order by tokenno desc limit 350")
    tokenAllData = cursor.fetchall()
    tokenno=[]
    username=[]
    tokentitle=[]
    assignteam=[]                       #Retriving data from DB and storing it to arrays so that we can display on UI
    priority=[]
    ctime=[]
    cdate=[]
    tokenstatus=[]
    tClosedComments=[]
    for i in tokenAllData:
        tokenno.append(i[0])
        username.append(i[1])
        tokentitle.append(i[2])
        assignteam.append(i[3])
        priority.append(i[4])
        ctime.append(i[5])
        cdate.append(i[6])
        tokenstatus.append(i[7])
        tClosedComments.append(i[8])
    conn.close()
    tokenData=zip(tokenno,username,tokentitle,assignteam,priority,ctime,cdate,tokenstatus,tClosedComments)
    return tokenData

def userWorking(dbname,ip,port,cusername,schemaName,schemaPass,tokenId):
    conn = psycopg2.connect(
    database=f'{dbname}', user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    cursor.execute(f"update tokendata set tokenstatus='WIP' where tokenno={tokenId}")
    cursor.execute(f"update tokendata set assignteam='{cusername}' where tokenno={tokenId}")
    conn.commit()
    conn.close()
    return f"wip"  

def tokenClosed(dbname,ip,port,cusername,schemaName,schemaPass,tokenId,Ccomment):
    conn = psycopg2.connect(
    database=f'{dbname}', user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    cursor.execute(f"update tokendata set tokenstatus='CLOSED' where tokenno={tokenId}")
    cursor.execute(f"update tokendata set assignteam='{cusername}' where tokenno={tokenId}")
    cursor.execute(f"update tokendata set closedcomment='{Ccomment}' where tokenno={tokenId}")

    conn.commit()
    conn.close()
    return f"closed"  


