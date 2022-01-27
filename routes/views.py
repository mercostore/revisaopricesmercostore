from flask import render_template,redirect, url_for,request, flash
from routes.forms import LoginForm
from controllers.helpers import Consultas_BD
from flask_login import LoginManager, UserMixin, login_required, login_user,logout_user,login_manager
from models.model import Produtos, User,Seller
from controllers.executa_procedures import Procedimentos
from app import app,session,admin, ModelView,abort,db




@app.route("/")
@login_required
def index():
    return render_template("dashboard.html")

#Rota Login
@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    user = Consultas_BD()
    if request.method == "POST":
        nome = request.form.get("usuario")
        senha = request.form.get("senha")
        email = request.form.get("email")
        usuario = db.session.query(User).filter(User.nome==nome).first()
        session["user_id"] = usuario.idusuario
        
        try:
            user=Consultas_BD.consulta_usuario(nome,email,senha)
        except:
            print("Valores Invalidos")

        if not user:
            flash("Credênciais invalidas!")
            return redirect(url_for('login'))
            
        flash("Usuario Logado!")

        login_user(user)

        return redirect('/')
    return render_template("login.html",form=form)


#Rota logout
@login_required
@app.route("/sair")
def logout():
    logout_user()
    flash("Deslogado!")
    return redirect(url_for('index'))

#Rota Cadastro Usuario
@app.route('/registros', methods=["GET", "POST"])
@login_required
def registros():
    sellers = Seller.query.with_entities(Seller.sellername).all()
    if request.method == 'POST':
        seller = request.form["Sellers"]
        usuario = request.form["usuario"]
        email = request.form["email"]
        senha = request.form["senha"]
        
        try:
            user = Consultas_BD.cadastro_usuario(seller,usuario,email,senha)
        except Exception as e:
            print(e)
            print("Erro no cadastro do Usuario")

    return render_template('CadastroUser.html',sellers=sellers)
    

#Rotas referente as informações de produtos

@app.route("/precos",methods=['GET','POST'])
@login_required
def retorna_produtos():
    #Ainda falta adicionar paginação
    try:
        id_user = session["user_id"]
        user = db.session.query(User).filter(User.idusuario==id_user).first()
        usuario = user.idseller
        print(usuario)

  
        produtos = db.session.query(Produtos).filter(Produtos.idseller==id_user).all()
        for produto in produtos:
            print(produto)
     
    except:
        pass
  
    return render_template('tabela.html',produtos=produtos)
'''
#download relatorio
@app.route("/download",methods=['GET,POST'])
def download_relatorios():
    pass
'''
#Rota Relatorios
@app.route("/relatorios",methods=['GET','POST'])
@login_required
def retorna_relatorios():
    try:
        id_user = session["user_id"]
        produtos = db.session.query(Produtos).filter(Produtos.idseller==id_user).all()
    except:
        pass
    return render_template("relatorio.html",produtos=produtos)



#Class Admin Flask
class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


admin.add_view(SecureModelView(User, db.session))
admin.add_view(ModelView(Seller, db.session))
admin.add_view(ModelView(Produtos, db.session))


#Rotas painel Admin
@app.route('/logarpainel')
def paineladm():
    return render_template('loginadmin.html')

@app.route('/logarpainel',methods=['GET','POST'])
def is_loginadmin():

    username = request.form.get('username')
    password = request.form['password']
    email = request.form['email']
    user = User.query.filter(User.nome ==username,User.email == email, User.senha == password).first()
    if user:
        if 'Admin' in user.perfil:
            session['logged_in'] = True

            return redirect('/admin')