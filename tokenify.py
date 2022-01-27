from flask import Flask,render_template,request,url_for,redirect,session,flash
import configparser
import BasicAuth
from datetime import timedelta
from datetime import datetime
import tokenDB

config = configparser.ConfigParser()
config.read('tokenify.ini')
ipaddress = config['appConfigs']['ipaddress']
secret_key = config['appConfigs']['secret_key']
port = config['appConfigs']['port']
dbname = config['dbConfigs']['dbname']
dbip = config['dbConfigs']['dbip']
dbport = config['dbConfigs']['dbport']

schemaName=config['dbConfigs']['schemaName']
schemaPass=config['dbConfigs']['schemaPass']

app = Flask(__name__,template_folder="webfolder")
app.secret_key=secret_key
                                                                      #Root Main Landing Page
@app.route("/",methods=['GET'])                 
def mroot():
    return render_template("root.html",ipaddress=ipaddress,port=port)
                                                                            #New user here
@app.route("/newuser",methods=['POST','GET'])                 
def newuser():
    return render_template("newuser.html",ipaddress=ipaddress,port=port)
                                                                            #New user here
@app.route("/about",methods=['POST','GET'])                 
def about():
    return render_template("about.html",ipaddress=ipaddress,port=port)


                                                                            #Authentication Here
@app.route("/uauth",methods=['POST'])                 
def uauth():
    username=request.form['username']
    password=request.form['password']
    var=BasicAuth.userpass(dbname,dbip,dbport,username,password,schemaName,schemaPass)
    uType=BasicAuth.userRoletype(dbname,dbip,dbport,username,password,schemaName,schemaPass)
    uTeam=BasicAuth.userTeam(dbname,dbip,dbport,username,password,schemaName,schemaPass)
    if var==False:
        return "You have entered wrong username or password"
    else:
        session.permanent = False
        app.permanent_session_lifetime = timedelta(minutes=30)
        session["username"]=username
        session["password"]=password
        session["uType"]=uType
        session["uTeam"]=uTeam

        if uType=="" or uType=="D":
            print(f"{username} is deactivated !")
            return f"{username} Wait For Admin To Approve Your Account or Kindly Ask Admin To Approve!!"

        elif uType=="A":
            if var==True:
                return redirect(url_for('aroot'),code=307)
            else:
                return "Admin Your Password Seems to Be wrong !!"
            

        else:
            if var==True:
                print(f"{username} has 'U' Flag")
                return redirect(url_for('uroot'),code=307)
            else:
                return render_template("WrongPasswordOrUsername.html")

                                                                        #Handling New User here
@app.route("/handleNewuser",methods=['POST'])                 
def handleNewuser():
    nusername=request.form['nusername']
    npassword=request.form['npassword']
    nuteam=request.form['uteam']
    nsuccess=BasicAuth.newuser(dbname,dbip,dbport,nusername,npassword,nuteam,schemaName,schemaPass)
    return nsuccess

                                                                        #Admin Allowing
@app.route("/aroot",methods=['POST'])                 
def aroot():
    if "username" in session:
        if session["uType"]!="A":
            return redirect(url_for('mroot'),code=307)
    
    admin_details=BasicAuth.adminDetails(dbname,dbip,schemaName,schemaPass,dbport)
    return render_template("adminPage.html",ipaddress=ipaddress,admin_details=admin_details,username=session["username"])

@app.route("/adminmodify",methods=['GET','POST'])       #Admin Modify page is here
def adminmodify():
    global untoModify
    untoModify=request.form['selectedUsername']
    uTeamtoModify=BasicAuth.adminModifyTeam(dbname,dbip,schemaName,schemaPass,dbport)
    uRoleToModify=BasicAuth.adminModifyRole(dbname,dbip,schemaName,schemaPass,dbport)

    return render_template("userModify.html",ipaddress=ipaddress,port=port,userTeamModify=uTeamtoModify,userRoleModify=uRoleToModify,username=untoModify)

@app.route("/modifyUser",methods=['GET','POST'])        #Actual modification get done here
def adminURModify():
    global untoModify
    uname=untoModify
    uteam=request.form['cUserTeam']
    urole=request.form['cUserRole']
    cModify=BasicAuth.modifyUser(dbname,dbip,dbport,schemaName,schemaPass,uname,uteam,urole)
    if cModify==True:
        return render_template("modifiedUser.html",ipaddress=ipaddress,port=port,username=uname,uteam=uteam,urole=urole)
    else:
        return f"<H1>OOPS !! Something Went Wrong Contact Admin !<h1>"


@app.route("/uroot",methods=['POST'])                 
def uroot():
    tokenData=tokenDB.retriveData(dbname,dbip,dbport,schemaName,schemaPass)
    return render_template("user.html",ipaddress=ipaddress,port=port,tokenData=tokenData)


@app.route("/nTokenRequest",methods=['POST'])                 
def nTokenRequest():
    if "username" in session:
        newTokenTitle=request.form['newTokenTitle']    
        assignTeam=request.form['assignTeam']    
        priority=request.form['priority']  
        now = datetime.now()
        ctime = now.strftime("%H:%M:%S")
        cdate=datetime.today().strftime('%Y-%m-%d')
        tusername=session["username"]
        tuteam=session["uTeam"]
        print(newTokenTitle,assignTeam,priority)
        print(ctime,cdate,tusername,tuteam)
        tokenid=tokenDB.newRequest(dbname,dbip,dbport,tusername,schemaName,schemaPass,newTokenTitle,assignTeam,priority,ctime,cdate)
        #return render_template("tokenCreated.html",tokenid=tokenid,username=tusername,newTokenTitle=newTokenTitle,assignTeam=assignTeam)
        return redirect(url_for('uroot'),code=307)

    return "You are not logged in <a href='/'>Click here to go to home</a>"

@app.route("/logout",methods=['POST','GET'])                 
def logout():
    session.pop('username',None)
    session.pop('password',None)
    session.pop('uType',None)
    session.pop('uTeam',None)
   
    return "You are logged out !!! <a href='/'>Click here to go to home</a>"

@app.route("/uworking",methods=['POST'])                ## user clicked on WIP        
def uworking():
    cToken=request.form['cToken']
    cUser=session["username"]
    wip=tokenDB.userWorking(dbname,dbip,dbport,cUser,schemaName,schemaPass,cToken)
    return redirect(url_for('uroot'),code=307)

@app.route("/tokenClosed",methods=['POST'])                ## user clicked on closed      
def tknClosed():
    closedToken=request.form['closedToken']
    Ccomment=request.form['ccomment']
    print(Ccomment)
    cUser=session["username"]
    wip=tokenDB.tokenClosed(dbname,dbip,dbport,cUser,schemaName,schemaPass,closedToken,Ccomment)
    return redirect(url_for('uroot'),code=307)


if __name__=='__main__':
    app.run(debug=True)
