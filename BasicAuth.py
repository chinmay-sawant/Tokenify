import psycopg2

def userpass(dbname,ip,port,username,userpassword,schemaName,schemaPass):
    
    conn = psycopg2.connect(
    database=f"{dbname}", user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM userAuth where username = '{username}'")
    
    a = cursor.fetchone()
    if a==None:
        return False
    else:
        print(f"{a[0]} trying to login")
        if a[0]==username:

            cursor.execute(f"SELECT * FROM userAuth where username = '{username}'")
            b = cursor.fetchone()
            if b[1]==userpassword:
                print(f"{a[0]} is authenticated")
                return True
            else:
                print(f"{a[0]} has entered wrong password !!")
                
        else:
            print(f"{a[0]} does not have account !!")
            return False
        #Closing the connection
        conn.close()

def userRoletype(dbname,ip,port,username,userpassword,schemaName,schemaPass):
    conn = psycopg2.connect(
    database=f"{dbname}", user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM userAuth where username = '{username}'")
    a = cursor.fetchone()
  
    if a==None:
        print("Nun value")
        return "D"
    else:
        print(f"{username} Has {a[2]} flag!!!")

        conn.close()
        return a[2]

def userTeam(dbname,ip,port,username,userpassword,schemaName,schemaPass):
    conn = psycopg2.connect(
    database=f"{dbname}", user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM userAuth where username = '{username}'")
    a = cursor.fetchone()
    if a==None:
        return "NoTeam"

    print(f"{username} Has {a[3]} flag!!!")

    conn.close()
    return a[3]

def newuser(dbname,ip,port,username,userpassword,uteam,schemaName,schemaPass):
    conn = psycopg2.connect(
    database=f"{dbname}", user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    cursor.execute(f"insert into userAuth values('{username}','{userpassword}','D','{uteam}')")
    print(f"{username} Has Been Added !!!")
    conn.commit()
    conn.close()
    return f"{username} user has been created for {uteam} team"

def adminDetails(dbname,ip,schemaName,schemaPass,port):
    
    conn = psycopg2.connect(
    database=f"{dbname}", user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    #cursor.execute(f"SELECT * FROM userAuth where username = 'chinmay'")
    cursor.execute(f"SELECT * FROM userAuth")
    b = cursor.fetchall()
    ausername=[]
    autype=[]
    auteam=[]
    for i in b:
        ausername.append(i[0])
        autype.append(i[2])
        auteam.append(i[3])
    
    conn.close()
    admin_details = zip(ausername, autype,auteam)
    return admin_details

def adminModifyRole(dbname,ip,schemaName,schemaPass,port):
    conn = psycopg2.connect(
    database=f"{dbname}", user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    #cursor.execute(f"SELECT * FROM userAuth where username = 'chinmay'")
    #cursor.execute(f"SELECT * FROM userAuth")
    cursor.execute(f"SELECT distinct usertype FROM userAuth")
    a = cursor.fetchall()
    roleType=[]
    for i in a:
    
        roleType.append(i[0])
    return roleType


def adminModifyTeam(dbname,ip,schemaName,schemaPass,port):
    conn = psycopg2.connect(
    database=f"{dbname}", user=f'{schemaName}', password=f'{schemaPass}', host=f'{ip}', port= f'{port}'
    )
    cursor = conn.cursor()
    #cursor.execute(f"SELECT * FROM userAuth where username = 'chinmay'")
    #cursor.execute(f"SELECT * FROM userAuth")
    cursor.execute(f"SELECT distinct userteam FROM userAuth")
    b= cursor.fetchall()
    userTeam=[]
    for i in b:  
        userTeam.append(i[0])     
    return userTeam


def modifyUser(dbname,dbip,dbport,schemaName,schemaPass,username,uteam,urole):

    conn = psycopg2.connect(
    database=f"{dbname}", user=f'{schemaName}', password=f'{schemaPass}', host=f'{dbip}', port= f'{dbport}'
    )
    cursor = conn.cursor()
    #cursor.execute(f"SELECT * FROM userAuth where username = 'chinmay'")
    #cursor.execute(f"SELECT * FROM userAuth")
    cursor.execute(f"UPDATE userAuth SET usertype='{urole}',userteam='{uteam}' where username='{username}'")
    conn.commit()
    return True