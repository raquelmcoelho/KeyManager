from tkinter import messagebox
from TkinterMethods import *
from PIL import Image, ImageTk
from Classes import *
from socket import *
from random import *
import pickle

# socket
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect(("127.0.0.1", 9999))
print("cliente conectado")


# socket methods
def fecharjanela():
    clientsocket.send("sair".encode())
    clientsocket.close()
    tk.quit()


def requestsocketreplace(client):
    clientsocket.send("replace".encode())
    clientsocket.send(pickle.dumps(client))
    txt = clientsocket.recv(4096).decode()
    print(txt)
    return txt


# initial screen
def tela1():
    global img
    logo(miniframe, img)
    b(frame1, "Vamos começar", lambda: tela2(), [0.33, 0, 0.15, 0.33])
    b(frame1, "Mudar tema", lambda: mudartema(frame0, frame1, frame2, tk, lambda: tela1()), [0.33, 0.20, 0.15, 0.33])


# text screen
def tela2():
    limpaframe(frame1)
    limpaframe(frame2)
    lbl(frame1, txtintro, [0.25, 0, 0.85, 0.50])
    b(frame1, "ok", lambda: tela3(), [0.33, 0.85, 0.15, 0.33])


# login screen
def tela3():
    miniframe.destroy()
    limpaframe(frame0)
    limpaframe(frame1)
    limpaframe(frame2)
    tk.title("Inscrever||Entrar")
    lbl(frame0, "Para se inscrever ou entrar digite:", [0.15, 0.60, 0.30, 0.70])
    nome = labelentry(frame1, "Seu nome:", [0.10, 0.00, 0.25, 0.25], [0.35, 0.00, 0.25, 0.55])
    senha = labelentry(frame1, "Sua senha:", [0.10, 0.50, 0.25, 0.25], [0.35, 0.50, 0.25, 0.55])
    b(frame2, "Inscrever", lambda: tela4(nome.get().lower(), senha.get().lower()), [0.25, 0, 0.30, 0.25])
    b(frame2, "Entrar", lambda: tela5(nome.get().lower(), senha.get().lower()), [0.50, 0, 0.30, 0.25])
    b(frame2, "sair", lambda: fecharjanela(), [0.25, 0.30, 0.30, 0.50])


# subscribe screen
def tela4(nome, senha):
    if senha == "" or nome == "":
        messagebox.showinfo("erro", "Por favor preencha os dois espaços")
        tela3()
    else:
        nomecliente = nome
        senhacliente = senha

        def continuar():
            # dados numéricos ele armazena de uma vez e dados string ele armazenada com split e strip
            dados = [entrys[0].get(), entrys[1].get(), entrys[2].get()]
            for dado in range(len(dados)):
                dadoh = "".join(re.findall(r"\d+", dados[dado]))
                dados.append(dadoh)
            for _ in range(3):
                dados.remove(dados[0])
            dados += entrys[3].get().strip().split(" ") + entrys[4].get().strip().split(" ")
            print("dados: ", dados)
            if dados.count("") > 0:
                messagebox.showinfo("erro", "Você esqueceu de preencher um espaço corretamente")
                tela4(nomecliente, senhacliente)
            else:
                client = Cofre(nomecliente, senhacliente)
                for i1 in range(len(dados)):
                    if i1 <= 2:
                        # adicionando só numeros
                        client.adddados(dados[i1], 1)
                    else:
                        # adicionando strings
                        client.adddados(dados[i1], 0)
                resposta = requestsocketreplace(client)
                print(resposta)
                if resposta == "seu cliente foi substituido":
                    tela5(nomecliente, senhacliente)

        # GUI
        limpaframe(frame0)
        limpaframe(frame1)
        limpaframe(frame2)
        messagebox.showinfo("Dados Públicos", txtdados)
        lbl(frame0, "Dados Públicos - (dicas para o hacker)", [0.15, 0.30, 0.30, 0.70])
        entrys = [0, 0, 0, 0, 0]
        txts = ["Data de nascimento:", "N° de telefone:", "Número importante:", "Nome completo:", "Nome importante:"]
        # criar entrys para cada dado
        j = 0
        for i in range(5):
            entrys[i] = labelentry(frame1, txts[i], [0.05, j, 0.2, 0.40], [0.45, j, 0.2, 0.50])
            j += 0.2

        b(frame2, "Continuar", lambda: continuar(), [0.50, 0.30, 0.15, 0.25])
        b(frame2, "Voltar", lambda: tela3(), [0.25, 0.30, 0.15, 0.25])


# main screen
def tela5(nome, senha):
    # retornar para a inscrição
    if senha == "" or nome == "":
        messagebox.showinfo("erro", "Por favor preencha os dois espaços")
        tela3()
    # copiar cliente para manuseio
    else:
        idclient = str(nome) + str(senha)
        clientsocket.send("acessaruserinfo".encode())
        clientsocket.send(idclient.encode())
        infor = pickle.loads(clientsocket.recv(4096))

        print("Dados encontrados do cliente no file:", infor, "\nidclient:", idclient)
        if infor is None:
            messagebox.showinfo("erro", "Usuário não encontrado")
            tela3()
        else:
            # pegar o cliente no socket
            clientsocket.send("pegarclient".encode())
            clientsocket.send(pickle.dumps(infor))
            client = pickle.loads(clientsocket.recv(4096))
            nomecliente = nome
            senhacliente = senha

            # funções dos botões do frame2 (frame de baixo)
            def deletar2(num, elemento=""):
                # se o método for 1 ele quer deletar uma senha
                elem = elemento.lower()
                if num == 1:
                    if elem == "cofre" or elem == "" or elem not in client.cofre:
                        messagebox.showinfo("erro", "Não é possível deletar isto")
                        deletar(1)
                    else:
                        aviso = messagebox.askyesno("cuidado", "Tem certeza que deseja fazer isso?")
                        # se sim
                        if aviso == 1:
                            print("deletando cadeado")
                            del client.cofre[elemento]
                            message = requestsocketreplace(client)
                            if message == "seu cliente foi substituido":
                                tela5(nomecliente, senhacliente)
                        # se não
                        elif aviso == 0:
                            deletar(1)

                # se o número for 0 ele quer deletar um cliente
                elif num == 0:
                    a = messagebox.askyesno("cuidado", "Tem certeza que deseja fazer isso? Todos seus dados e "
                                                       "senhas serão apagados")
                    # se sim
                    if a == 1:
                        clientsocket.send("deleteuser".encode())
                        clientsocket.send(pickle.dumps(client))
                        txt = clientsocket.recv(4096).decode()
                        print(txt)
                        fecharjanela()
                    # se não
                    elif a == 0:
                        tela5(nomecliente, senhacliente)

            def deletar(metodo):
                limpaframe(frame0)
                limpaframe(frame1)
                limpaframe(frame2)
                lbl(frame1, "Qual cadeado você deseja deletar?", [0, 0, 0.20, 1])
                deletado = ent(frame1, [0.33, 0.30, 0.10, 0.33])
                b(frame2, 'deletar', lambda: deletar2(metodo, deletado.get()), [0.50, 0, 0.15, 0.25])
                b(frame2, "voltar", lambda: tela5(nomecliente, senhacliente), [0.25, 0, 0.15, 0.25])

            def logout():
                message = requestsocketreplace(client)
                if message == "seu cliente foi substituido":
                    fecharjanela()

            def printdados():
                limpaframe(frame0)
                limpaframe(frame1)
                limpaframe(frame2)
                txt = "Esses são os dados que usamos na hora de checar\n se suas senhas são seguras ou não:\n"
                for i in client.dados:
                    txt += "\n" + str(i)
                lbl(frame1, txt, [0, 0, 1, 1], just=LEFT)
                b(frame2, "voltar", lambda: tela5(nomecliente, senhacliente), [0.33, 0, 0.15, 0.33])

            def add():
                limpaframe(frame1)
                limpaframe(frame2)
                lbl(frame1, "O que você deseja adicionar ou substituir?", [0, 0, 0.10, 1])
                addcadeado = labelentry(frame1, "Seu cadeado: ", [0.10, 0.10, 0.10, 0.40], [0.50, 0.10, 0.10, 0.40])
                addsenha = labelentry(frame1, "Sua Senha: ", [0.10, 0.20, 0.10, 0.40], [0.50, 0.20, 0.10, 0.40])
                b(frame2, "adicionar", lambda: troca3(addcadeado.get(), addsenha.get()), [0.33, 0, 0.15, 0.33])
                b(frame2, "voltar", lambda: tela5(nomecliente, senhacliente), [0.33, 0.20, 0.15, 0.33])

            # funções do botão check
            def troca3(cadeado3, key2):
                if len(client.cofre) == 11 and cadeado3 not in client.cofre:
                    messagebox.showinfo("premium", "Pague nossa assinatura Premium\npor apenas 5,99 para ter acesso a"
                                                   " senhas ilimitadas ☺")
                    tela5(nomecliente, senhacliente)

                else:
                    limpaframe(frame1)
                    if cadeado3 == "cofre":
                        client.adicionarsenha("clientid", nomecliente + key2)
                        senhacliente2 = key2
                    else:
                        senhacliente2 = senhacliente
                    client.adicionarsenha(cadeado3, key2)
                    message = requestsocketreplace(client)
                    if message == "seu cliente foi substituido":
                        tela5(nomecliente, senhacliente2)

            def troca2(cadeado2, key):
                limpaframe(frame1)
                nivel, texto = client.checarsenha(key)
                lbl(frame1, cadeado2 + " : " + key, [0.25, 0, 0.10, 0.50])
                lbl(frame1, nivel + "\n" + texto, [0, 0.10, 0.60, 1])
                lbl(frame1, "Deseja por como a nova senha?", [0, 0.70, 0.10, 1])
                b(frame1, "sim", lambda: troca3(cadeado2, key), [0.50, 0.85, 0.10, 0.40])
                b(frame1, "tentar novamente", lambda: troca(cadeado2), [0.10, 0.85, 0.10, 0.40])

            def manual(cadeado1):
                limpaframe(frame1)
                lbl(frame1, "Inserir nova senha:", [0.33, 0, 0.10, 0.33])
                novasenha = ent(frame1, [0.33, 0.33, 0.10, 0.33])
                b(frame1, "avançar", lambda: troca2(cadeado1, novasenha.get()), [0.33, 0.66, 0.10, 0.33])

            def troca(cadeado):
                limpaframe(frame0)
                limpaframe(frame1)
                b(frame1, "Criar a nova senha", lambda: manual(cadeado), [0.16, 0, 0.10, 0.66])
                b(frame1, "Criar automaticamente senha forte",
                  lambda: troca2(cadeado, client.criarsenha(randint(7, 12))), [0.16, 0.10, 0.10, 0.66])

            def check(cadeadocheck, senhacheck):
                limpaframe(frame1)
                limpaframe(frame2)
                print(f"checando a senha {senhacheck} e o cadeado {cadeadocheck}")
                nivel, texto = client.checarsenha(senhacheck)
                lbl(frame1, cadeadocheck + " : " + senhacheck, [0.25, 0, 0.10, 0.50])
                lbl(frame1, nivel + "\n" + texto, [0, 0.10, 0.80, 1])
                b(frame1, "trocar", lambda: troca(cadeadocheck), [0.33, 0.90, 0.10, 0.33])
                b(frame2, "voltar", lambda: tela5(nomecliente, senhacliente), [0.33, 0.10, 0.15, 0.33])

            def definir_metodo(cadeado):
                return lambda: check(cadeado, client.cofre[cadeado])

            def labelbutton(cadeado, ytam):
                lbl(frame1, "%s :" % cadeado, [0, ytam, 0.10, 0.40], anc=E, just=RIGHT)
                lbl(frame1, "%10s" % client.cofre[cadeado], [0.40, ytam, 0.10, 0.40], anc=E, just=RIGHT)
                b(frame1, "check", definir_metodo(cadeado), [0.80, ytam, 0.10, 0.20])

            # GUI da tela5
            frame1.place(rely=0.10, relheight=0.56)
            frame1["borderwidth"] = 10
            frame1["relief"] = "sunken"
            tk.title("Cofre")
            limpaframe(frame0)
            limpaframe(frame1)
            limpaframe(frame2)
            lbl(frame0, "Seja bem vindo(a) %s" % client.user.name, [0.15, 0, 0.10, 0.70])

            if len(client.cofre) == 3:
                lbl(frame1,
                    """Adicione novas senhas com o botão Add/Replace
                        p.s : O cadeado cofre mostra a senha 
                        do próprio gerenciador de chaves""", [0, 0, 1, 1])

            elif 11 >= len(client.cofre) > 3:
                b(frame1, "______Cadeados______|________Senhas________|__Botão__",
                  lambda: messagebox.showinfo("info", "1- Cadeados: lugar que a chave abre" +
                                              "\n2- O cadeado cofre se refere ao próprio gerenciador"
                                              "\n3- Adicione novas senhas com o botão Add/Replace."), [0, 0, 0.1, 1])
                y = 0.1
                for i2 in client.cofre:
                    if i2 != "clientid" and i2 != "nome":
                        labelbutton(i2, y)
                        y += 1 / 10

            # botões de manuseio
            b(frame2, "Add/Replace senha", lambda: add(), [0.10, 0.18, 0.15, 0.40])
            b(frame2, "Apagar senha", lambda: deletar(1), [0.50, 0.18, 0.15, 0.40])
            b(frame2, "Ver meus dados", lambda: printdados(), [0.10, 0.33, 0.15, 0.40])
            b(frame2, "Instruções", lambda: messagebox.showinfo("instruções", txtinstrucoes), [0.50, 0.33, 0.15, 0.40])
            b(frame2, "Salvar e sair", lambda: logout(), [0.10, 0.48, 0.15, 0.40])
            b(frame2, "Excluir minha conta", lambda: deletar2(0), [0.50, 0.48, 0.15, 0.40])


# Tkinter GUI
tk = Tk()
tk.title("Key Manager")
tk.geometry("500x600+433+84")
tk.iconbitmap("images/lock.ico")
tk["bg"] = BG
tk.protocol("WM_DELETE_WINDOW", lambda: fecharjanela())
img = ImageTk.PhotoImage(Image.open("images/Key134.png"))

frame0 = Frame(tk, bg=BG)
frame0.place(relx=0, rely=0, relheight=0.33, relwidth=1)
frame1 = Frame(tk, bg=BG)
frame1.place(relx=0, rely=0.33, relheight=0.33, relwidth=1)
frame2 = Frame(tk, bg=BG)
frame2.place(relx=0, rely=0.66, relheight=0.33, relwidth=1)
miniframe = Frame(tk)

# chamar primeira tela
tela1()
mainloop()
