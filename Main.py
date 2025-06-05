# Import librerie
import tkinter as tk
import ctypes

from fernetReq import *
from sqliteReq import *
from variabili import *
# from playsound import playsound

from tkinter import filedialog, PhotoImage, messagebox, ttk, font

# Creo la finestra principale (logIn)
logIn = tk.Tk()
logIn.title("Password Manager")
logIn.geometry("400x200")
logIn.resizable(False, False)
logIn.configure(bg=colore_sfondo)
logo = PhotoImage(file="Logo3.png")
logIn.iconphoto(True, logo)


def Uscita():
    home.destroy()


def InserisciServizio():
    global chiaveGenerataFernet, FernetKEY, logIn, nuovoServizio, home, servizioInput

    Servizio = servizioInput.get()
    Nickname = nicknameInput.get()
    Email = accountInput.get()
    Passkey = passwordInput.get()

    if (Servizio == "" and Nickname == "" and Email == "" and Passkey == ""):
        risposta = messagebox.showerror(
            "Nessun dato da inserire.", "Perfavore compila i campi e riprova")
    else:

        Servizio = Cripta(FernetKEY, Servizio)
        Nickname = Cripta(FernetKEY, Nickname)
        Email = Cripta(FernetKEY, Email)
        Passkey = Cripta(FernetKEY, Passkey)

        Inserisci(Servizio, Nickname, Email, Passkey)
        nuovoServizio.destroy()
        AggiornaQuery("", "")


def EliminaServizio(id, nome):
    global opzioni
    risposta = messagebox.askquestion(
        "Attenzione!", "Si desidera cancellare tutti i dati di "+nome+" ? L'azione è irreversibile!")
    print(risposta)
    if risposta == "yes":
        Elimina(id)
        opzioni.destroy()
        AggiornaQuery("", "")


def new():  # Funzione per inserire un nuovo servizio
    # Richiamo le variabili globali
    global chiaveGenerataFernet, FernetKEY, logIn, nuovoServizio, home, servizioInput, nicknameInput, accountInput, passwordInput
    nuovoServizio = tk.Toplevel(home)
    nuovoServizio.title("Aggiungi Servizio")
    nuovoServizio.geometry("350x150")
    nuovoServizio.configure(bg=colore_sfondo)
    nuovoServizio.resizable(False, False)

    # Creo i diversi campi

    # Etichetta + Campo 1
    ServizioTitolo = tk.Label(
        nuovoServizio, text="Servizio", bg=colore_sfondo, fg="#ffffff")
    ServizioTitolo.grid(row=1, column=0, sticky="e", padx=10, pady=5)
    servizioInput = tk.Entry(nuovoServizio)
    servizioInput.grid(row=1, column=1, padx=10, pady=5)

    # Etichetta + Campo 2
    NicknameTitiolo = tk.Label(
        nuovoServizio, text="Nickname", bg=colore_sfondo, fg="#ffffff")
    NicknameTitiolo.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    nicknameInput = tk.Entry(nuovoServizio)
    nicknameInput.grid(row=2, column=1, padx=10, pady=5)

    # Etichetta + Campo 3
    AccountTitiolo = tk.Label(
        nuovoServizio, text="Account", bg=colore_sfondo, fg="#ffffff")
    AccountTitiolo.grid(row=3, column=0, sticky="e", padx=10, pady=5)
    accountInput = tk.Entry(nuovoServizio)
    accountInput.grid(row=3, column=1, padx=10, pady=5)

    # Etichetta + Campo 4
    PasswordTitolo = tk.Label(
        nuovoServizio, text="Password", bg=colore_sfondo, fg="#ffffff")
    PasswordTitolo.grid(row=4, column=0, sticky="e", padx=10, pady=5)
    passwordInput = tk.Entry(nuovoServizio)
    passwordInput.grid(row=4, column=1, padx=10, pady=5)

    # Bottone per salvare i dati inseriti
    invia = tk.Button(nuovoServizio, text="Inserisci Servizio",
                      bd=0, command=InserisciServizio)
    invia.grid(row=1, column=3, padx=10, pady=5)
    nuovoServizio.mainloop()


def PulisciAppunti():
    home.clipboard_clear()
    print("Clipboard pulito")
    try:
        ctypes.windll.user32.OpenClipboard(0)
        ctypes.windll.user32.EmptyClipboard()
        ctypes.windll.user32.CloseClipboard()
    except tk.TclError:
        print("Clipboard è vuoto come previsto (TclError)")


def CopiaDato(event):
    global tree
    try:
        selezione = tree.selection()
        if selezione:
            prima_riga = selezione[0]
            valori_riga = tree.item(prima_riga, 'values')
            contenuto_da_copiare = valori_riga[1]
            print(f"Contenuto da copiare: '{contenuto_da_copiare}'")
            home.clipboard_clear()
            print("Clipboard pulito (dovrebbe essere vuoto ora)")
            home.clipboard_append(contenuto_da_copiare)
            home.update()
            print("Contenuto aggiunto al clipboard")
            print(f"Riga copiata: {contenuto_da_copiare}")
            # Programma la cancellazione degli appunti dopo 5 minuti (300000 millisecondi)
            home.after(5000, PulisciAppunti)
    except Exception as e:
        print(f"Errore durante la copia della riga: {e}")


def DettagliServizio(nomeCript, nome, id):
    global tree, service
    service = tk.Toplevel(home)
    service.title(nome)
    service.geometry("450x200")
    service.configure(bg=colore_sfondo)
    service.resizable(False, False)

    Dettagli = PrendiDati(id)
    conn.close()
    Nickname = Dettagli[0][1]
    Email = Dettagli[0][2]
    Passkey = Dettagli[0][3]

    Nickname = Decripta(FernetKEY, Nickname)
    Email = Decripta(FernetKEY, Email)
    Passkey = Decripta(FernetKEY, Passkey)

    datiServizio = [
        ("Servizio", nome),
        ("Nickname", Nickname),
        ("E-Mail", Email),
        ("Password", Passkey)
    ]
    intestazioni = ("Scritta", "Dato")

    tree = ttk.Treeview(service, columns=intestazioni, show='')

    for col in intestazioni:
        tree.column(col, width=100)

    for riga in datiServizio:
        tree.insert("", tk.END, values=riga)

    tree.pack(expand=True, fill='both')
    tree.bind("<ButtonRelease-1>", CopiaDato)
    service.mainloop()


def ConfermaModifica(id, comando):
    global opzioni, Cambia
    print(comando)
    risposta = messagebox.askquestion(
        "Attenzione!", "Si desidera confermare le modifiche apportate? L'azione è irreversibile!")
    print(risposta)
    if risposta == "yes":
        if comando == "1":
            colonna = "Servizio"
        elif comando == "2":
            colonna = "Nickname"
        elif comando == "3":
            colonna = "Email"
        elif comando == "4":
            colonna = "passkey"
        print("comando: " + comando)
        print("colonna: "+colonna)
        Cambia = Cambia.get()
        Cambia = Cripta(FernetKEY, Cambia)

        Modifica(colonna, Cambia, id)
        opzioni.destroy()
        ModServizio.destroy()
        AggiornaQuery("", "")


def ModificaServizio(id, comando):
    global ModServizio, Cambia
    ModServizio = tk.Toplevel(home)
    ModServizio.geometry('300x150')
    ModServizio.configure(bg=colore_sfondo)
    ModServizio.resizable(False, False)

    Dettagli = PrendiDati(id)
    Servizio = Dettagli[0][0]
    Nickname = Dettagli[0][1]
    Email = Dettagli[0][2]
    Passkey = Dettagli[0][3]
    print(Dettagli)

    Servizio = Decripta(FernetKEY, Servizio)
    Nickname = Decripta(FernetKEY, Nickname)
    Email = Decripta(FernetKEY, Email)
    Passkey = Decripta(FernetKEY, Passkey)

    if (comando == "1"):
        ModServizio.title("Cambia Servizio")
        VecchioDato = tk.Label(ModServizio, text=Servizio)
        VecchioDato.grid(row=0, column=0)
    elif (comando == "2"):
        ModServizio.title("Cambia Nickname")
        VecchioDato = tk.Label(ModServizio, text=Nickname)
        VecchioDato.grid(row=0, column=0)
    elif (comando == "3"):
        ModServizio.title("Cambia Email")
        VecchioDato = tk.Label(ModServizio, text=Email)
        VecchioDato.grid(row=0, column=0)
    elif (comando == "4"):
        ModServizio.title("Cambia Password")
        VecchioDato = tk.Label(ModServizio, text=Passkey)
        VecchioDato.grid(row=0, column=0)
    Cambia = tk.Entry(ModServizio, width=30)
    Cambia.grid(row=0, column=1, padx=10, pady=5)
    Conferma = tk.Button(ModServizio, text="Conferma",
                         command=lambda n1=id, n2=comando: ConfermaModifica(n1, n2))
    Conferma.grid(row=1, column=0, padx=10, pady=5)


def OpzioniServizio(id, nome):
    global opzioni
    opzioni = tk.Toplevel(home)
    opzioni.title(nome)
    opzioni.geometry('600x350')
    opzioni.configure(bg=colore_sfondo)
    opzioni.resizable(False, False)
    Label = tk.Label(opzioni, width=100, text=nome,
                     bg=colore_contrasto, fg="#ffffff", font=("Helvetica", 15))
    Label.grid(row=0, column=0, padx=5, pady=10, sticky='w')
    Elimina = tk.Button(opzioni, text="Elimina Servizio", bg='red', fg='#000000', bd=0,
                        width=15, height=1, font=("Helvetica", 12), command=lambda: EliminaServizio(id, nome))
    Elimina.grid(row=0, column=2, padx=5, pady=10)

    Dettagli = PrendiDati(id)
    Nickname = Dettagli[0][1]
    Email = Dettagli[0][2]
    Passkey = Dettagli[0][3]
    print(Dettagli)

    Nickname = Decripta(FernetKEY, Nickname)
    Email = Decripta(FernetKEY, Email)
    Passkey = Decripta(FernetKEY, Passkey)

    CambiaServizio = tk.Label(opzioni, text=nome, bg=colore_contrasto, fg="#ffffff", font=(
        "Helvetica", 15), bd=0, width=100, height=1, anchor='w', padx=5)
    CambiaServizio.grid(row=1, column=0, padx=5, pady=5, sticky='w')
    CambiaServizioBtn = tk.Button(opzioni, text="Cambia Servizio", bg=colore_contrasto, fg="#ffffff", font=(
        "Helvetica", 12), bd=0, width=15, height=1, command=lambda n1=id, n2="1":  ModificaServizio(n1, n2))
    CambiaServizioBtn.grid(row=1, column=2, padx=20, pady=5, sticky='e')

    CambiaNickname = tk.Label(opzioni, text=Nickname, bg=colore_contrasto, fg="#ffffff", font=(
        "Helvetica", 15), bd=0, width=100, height=1, anchor='w', padx=5)
    CambiaNickname.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    CambiaNicknameBtn = tk.Button(opzioni, text="Cambia Nickname", bg=colore_contrasto, fg="#ffffff", font=(
        "Helvetica", 12), bd=0, width=15, height=1, command=lambda n1=id, n2="2":  ModificaServizio(n1, n2))
    CambiaNicknameBtn.grid(row=2, column=2, padx=20, pady=5, sticky='e')

    CambiaEmail = tk.Label(opzioni, text=Email, bg=colore_contrasto, fg="#ffffff", font=(
        "Helvetica", 15), bd=0, width=100, height=1, anchor='w', padx=5)
    CambiaEmail.grid(row=3, column=0, padx=5, pady=5, sticky='w')
    CambiaEmailBtn = tk.Button(opzioni, text="Cambia Email", bg=colore_contrasto, fg="#ffffff", font=(
        "Helvetica", 12), bd=0, width=15, height=1, command=lambda n1=id, n2="3":  ModificaServizio(n1, n2))
    CambiaEmailBtn.grid(row=3, column=2, padx=20, pady=5, sticky='e')

    CambiaPassword = tk.Label(opzioni, text=Passkey, bg=colore_contrasto, fg="#ffffff", font=(
        "Helvetica", 15), bd=0, width=100, height=1, anchor='w', padx=5)
    CambiaPassword.grid(row=4, column=0, padx=5, pady=5, sticky='w')
    CambiaPasswordBtn = tk.Button(opzioni, text="Cambia Password", bg=colore_contrasto, fg="#ffffff", font=(
        "Helvetica", 12), bd=0, width=15, height=1, command=lambda n1=id, n2="4":  ModificaServizio(n1, n2))
    CambiaPasswordBtn.grid(row=4, column=2, padx=20, pady=5, sticky='e')
    opzioni.grid_columnconfigure(0, weight=1)
    opzioni.grid_columnconfigure(1, weight=1)
    opzioni.mainloop()


def AggiornaQuery(event, ricerca):
    global Servizi, ServiziDec, canvas, frame_bottoni

    PrendiServizi()
    ServiziQuery = []

    # Aggiunge alla nuova lista tutti i servizi che rispondono alla richerca
    for servizio in ServiziDec:
        if (ricerca in servizio[0]):
            ServiziQuery.append(servizio)

    # Elimina tutto il contenuto del canvas e ricrea "Frame_bottoni"
    canvas.delete("all")

    frame_bottoni = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_bottoni, anchor="ne")
    frame_bottoni = tk.Frame(canvas)
    canvas.configure(bg=colore_sfondo)
    frame_bottoni.configure(bg=colore_sfondo)
    canvas.create_window((0, 0), window=frame_bottoni, anchor="ne")

    # Riempie il frame con i servizi relativi alla ricerca dell'utente
    if ServiziQuery == []:
        label = tk.Label(
            frame_bottoni, text='Nessun risultato trovato', bg=colore_sfondo, fg="#ffffff")
        label.grid(row=0, column=0, pady=5)
    contatore = 0
    for servizio in ServiziQuery:
        contatore += 1
        scritta = servizio[0]
        label = tk.Button(frame_bottoni, text=scritta, bg=colore_contrasto, fg="#ffffff", bd=0, width=45,
                          height=1, command=lambda n3=servizio[1], n1=scritta, n2=scritta: DettagliServizio(n1, n2, n3))
        label.grid(row=contatore, column=0, sticky="e", padx=5, pady=2)
        Options = tk.Button(frame_bottoni, text="■", bg=colore_contrasto, fg="#ffffff", bd=0,
                            width=3, height=1, command=lambda n1=servizio[1], n2=scritta: OpzioniServizio(n1, n2))
        Options.grid(row=contatore, column=1, sticky="e", padx=5, pady=2)
    frame_bottoni.grid_columnconfigure(0, weight=1)
    frame_bottoni.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def PrendiServizi():
    global ServiziDec, Servizi
    try:
        Servizi = PrendiDatiServizi()
        contatore = 0
        ServiziDec = []
        for servizio in Servizi:
            scritta = servizio[0]
            scritta = Decripta(FernetKEY, scritta)
            dato = [scritta, servizio[1]]
            ServiziDec.append(dato)
            contatore += 1
    except:
        home.destroy()
        Errore = messagebox.showerror(
            "Attenzione!", "Qualcosa è andato storto o la chiave inserita non e valda, si prega di riprovare!")


def HomePage():
    global home, Servizi, canvas, frame_bottoni

    # Crea pagina home
    home = tk.Tk()
    home.title("home")
    home.geometry("600x350")
    home.configure(bg=colore_sfondo)
    home.resizable(False, False)
    home.grid_rowconfigure(0, weight=1)
    home.grid_columnconfigure(1, weight=1)

    # Connessione al database e decriptazione dei servizi
    PrendiServizi()

    # Creo il frame per la colonna di sinistra che conterrà il bottone Nuovo Servizio, Exit e il campo di ricerca
    left_frame = tk.Frame(home, width=200, bg=colore_sfondo)
    left_frame.grid(row=0, column=0, sticky='ns')
    left_frame.grid_propagate(False)

    UscitaBtn = tk.Button(left_frame, text="   Exit   ",
                          command=Uscita, bd=0, bg="red", width=12, height=1)
    UscitaBtn.grid(row=0, column=1, padx=2, pady=5)
    Nuovo = tk.Button(left_frame, text="Nuovo Servizio", bg=colore_contrasto,
                      fg="#ffffff", bd=0, command=new, width=12, height=1)
    Nuovo.grid(row=0, column=0, padx=2, pady=5)
    Cerca = tk.Entry(left_frame, width=30)
    Cerca.grid(row=1, column=0, columnspan=2, pady=10)
    Cerca.bind("<KeyRelease>", lambda event: AggiornaQuery(event, Cerca.get()))

    # Creo canvas e la barra di scorrimento per i vari servizi
    canvas = tk.Canvas(home)
    scrollbar = tk.Scrollbar(home, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=2, sticky="ns")
    scrollbar.grid(row=0, column=4, sticky="ns")

    # Creo il frame di destra che conterrà tutti i bottoni dei servizi
    frame_bottoni = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_bottoni, anchor="ne")
    frame_bottoni = tk.Frame(canvas)
    canvas.configure(bg=colore_sfondo)
    frame_bottoni.configure(bg=colore_sfondo)
    canvas.create_window((0, 0), window=frame_bottoni, anchor="ne")

    # Contenuto del Frame, se non è mai stato creato un servizio, verrà visualizzato un avviso, altrimenti verranno elencati uno ad uno i vari servizi
    if Servizi == []:
        label = tk.Label(
            frame_bottoni, text='Nessun servizio, seleziona "Nuovo Servizio" per crearne uno!', bg=colore_sfondo, fg="#ffffff")
        label.grid(row=0, column=0, pady=5)
    contatore = 0
    for servizio in Servizi:
        contatore += 1
        scritta = servizio[0]

        scritta = Decripta(FernetKEY, scritta)
        label = tk.Button(frame_bottoni, text=scritta, bg=colore_contrasto, fg="#ffffff", bd=0, width=45,
                          height=1, command=lambda n3=servizio[1], n1=scritta, n2=scritta: DettagliServizio(n1, n2, n3))
        label.grid(row=contatore, column=1, sticky="e", padx=5, pady=2)
        Options = tk.Button(frame_bottoni, text="■", bg=colore_contrasto, fg="#ffffff", bd=0,
                            width=3, height=1, command=lambda n1=servizio[1], n2=scritta: OpzioniServizio(n1, n2))
        Options.grid(row=contatore, column=2, sticky="e", padx=5, pady=2)

    frame_bottoni.grid_columnconfigure(0, weight=1)
    frame_bottoni.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    home.mainloop()


def CaricaKey():
    global chiaveGenerataFernet, FernetKEY, logIn, nuovoServizio, home, entry1, nicknameInput, accountInput
    file_path = filedialog.askopenfilename(
        title="Seleziona un file .key",
        filetypes=[("Key Files", "*.key"), ("Tutti i file", "*.*")]
    )

    # Se un file è stato scelto
    if file_path:
        global FernetKEY
        with open(file_path, "r") as file:
            FernetKEY = LeggiKey(file)
        print("Contenuto del file:")
        logIn.destroy()
        HomePage()
    else:
        print("Nessun file selezionato.")


def CreaKey():
    global chiaveGenerataFernet, FernetKEY, logIn, nuovoServizio, home
    chiaveGenerataFernet = GeneraKey()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".key",
        filetypes=[("Key Files", "*.key"), ("All Files", "*.*")],
        title="Salva il file .key")

    if file_path:
        with open(file_path, "w") as file:
            file.write(chiaveGenerataFernet.decode())
        print(f"File salvato in: {file_path}")
    else:
        print("Salvataggio annullato dall'utente.")

    print(chiaveGenerataFernet)


titolo = tk.Label(logIn, text="Inserire chiave", font=(
    "Helvetica", 20), bg=colore_sfondo, fg="#ffffff")
titolo.pack(pady=10)

Carica = tk.Button(logIn, text="Carica Key", bg=colore_contrasto, fg="#ffffff", font=(
    "Helvetica", 15), bd=0, command=CaricaKey, width=15, height=1)
Carica.pack(pady=5)

Crea = tk.Button(logIn, text="Genera key", font=("Helvetica", 15),
                 command=CreaKey, bg=colore_contrasto, bd=0, fg="#ffffff", width=15, height=1)
Crea.pack(pady=5)

logIn.mainloop()