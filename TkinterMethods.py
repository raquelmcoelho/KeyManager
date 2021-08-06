from tkinter import *

# padrões
BG = "#00ffff"
FG = "#222222"
FONT = ("Century Gothic", "12")
escolhadetema = 0

# textos
txtintro = """\nAqui é possivel armazenar \nsuas senhas em um lugar seguro\ntrocar se estiverem fracas
\nchecar sua segurança\ncriar senhas aleatórias \na acessa-las se necessario
"""
txtdados = """\n
No momento de checar se suas senhas são seguras ou não precisamos ter dados básicos seus que todos tem acesso (públicos) 
\nIsto para evitar que um hacker que lhe conheça na internet tenha pistas do que procurar primeiro na sua senha
\nPor isso vamos evitar essas pistas na hora de criar senhas novas
"""
txtinstrucoes = """
\n\nCADEADO: o lugar de onde ele abre
P.S o cadeado "cofre" é o cadeado do seu gerenciador de senhas
\n\nSENHA: a chave do cadeado
\n\nBOTÃO CHECK: checa o nível de força e segurança da sua senha
\n\nBOTÃO ADD/REPLACE SENHA: Adicionar ou substituir. 
Você ou entra com um cadeado novo ou com um já existente, 
se ele já existir então a senha dele será substituída pela chave que você inserir.
\n\nBOTÃO APAGAR SENHA: apaga algum cadeado que você inserir
\n\nBOTÃO VER DADOS: lhe é informado os dados que usamos como base
(fornecidos por você) para checar e criar suas senhas
\n\nBOTÃO SALVAR E SAIR: sua conta e dados são atualizados
\n\nBOTÃO EXCLUIR MINHA CONTA: sua conta é excluída não podendo ser recuperada"""


# funções para o tkinter
def mudarcor(framename):
    for widget in framename.winfo_children():
        widget["bg"] = BG
        widget["fg"] = FG
    framename["bg"] = BG
    limpaframe(framename)


def mudartema(f, f1, f2, tk_, func):
    global BG, FG, escolhadetema
    fontes = [("#4d004d", "#ff9900"), ("#ff0066", "#ffffff"), ("#0b4b88", "#ffff00"), ("#d10000", "#ffffff"),
              ("#222222", "#00ffff")]
    escolha = escolhadetema % len(fontes)
    print("escolha de fonte", escolhadetema, "%", len(fontes), "=",  escolha, fontes[escolha])
    FG = fontes[escolha][0]
    BG = fontes[escolha][1]
    escolhadetema += 1
    mudarcor(f)
    mudarcor(f1)
    mudarcor(f2)
    tk_["bg"] = BG
    func()


def limpaframe(framename):
    for widget in framename.winfo_children():
        widget.destroy()


def labelentry(frame, txt, p, p2):
    lbl(frame, txt, p)
    return ent(frame, p2)


def lbl(frame, txt, p, anc=CENTER, just=CENTER):
    Label(frame, text=txt, font=FONT, bg=BG, fg=FG, anchor=anc,
          justify=just).place(relx=p[0], rely=p[1], relheight=p[2], relwidth=p[3])


def b(frame, txt, command, p):
    Button(frame, text=txt, command=command,
           font=FONT, bg=FG, fg=BG).place(relx=p[0], rely=p[1], relheight=p[2], relwidth=p[3])


def ent(frame, p2):
    e = Entry(frame, font=FONT, bg="#eeeeee")
    e.place(relx=p2[0], rely=p2[1], relheight=p2[2], relwidth=p2[3])
    return e


def logo(miniframe, img):
    miniframe.place(relx=0, rely=0, relheight=0.25, relwidth=1)
    Label(miniframe, bg=FG, image=img).place(relx=0, rely=0, relheight=1, relwidth=1)
