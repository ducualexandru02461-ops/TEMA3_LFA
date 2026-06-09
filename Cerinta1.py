from collections import deque

w = open("Cerinta1.out", "w")

def citeste_pda ():
    pda = {}
    with open("Cerinta1.in") as f:
        stari = [x for x in f.readline().split()]
        alfabet = [x for x in f.readline().split()]
        nr_tranzitii = int(f.readline())
        tranzitii = {}
        for linie in range(nr_tranzitii):
            linie = [x for x in f.readline().split()]
            cheie = (linie[0], linie[1], linie[2])
            valoare = (linie[3], linie[4])
            if cheie not in tranzitii:
                tranzitii[cheie] = []
            tranzitii[cheie].append(valoare)

        stare_initiala = f.readline().strip()
        simbol_initial_stiva = f.readline().strip()
        multime_stari_finale = [x for x in f.readline().strip().split()]
        mod_acceptare = f.readline().strip()
        cuvant_verificat = f.readline().strip()

        return stari, alfabet, nr_tranzitii, tranzitii, stare_initiala, simbol_initial_stiva, multime_stari_finale, mod_acceptare, cuvant_verificat

print(citeste_pda())
stari, alfabet, nr_tranzitii, tranzitii, stare_initiala, simbol_initial_stiva, multime_stari_finale, mod_acceptare, cuvant_verificat = citeste_pda()

def simulator_pda(stare_initiala, simbol_initial_stiva, multime_stari_finale, cuvant_verificat, mod_acceptare, tranzitii, simbol_lambda = "lambda"):
    configuratie_initiala = (stare_initiala, 0, simbol_initial_stiva)
    coada = deque([configuratie_initiala])
    vizitate = set([configuratie_initiala])

    while coada:
        stare_curenta, index_curent, stiva_curenta = coada.popleft()
        if index_curent == len(cuvant_verificat):
            acceptat = False
            if mod_acceptare == "stare_finala" and stare_curenta in multime_stari_finale:
                acceptat = True
            elif mod_acceptare == "stiva_goala" and len(stiva_curenta) == 0:
                acceptat = True
            elif mod_acceptare == "ambele" and stare_curenta in multime_stari_finale and len(stiva_curenta) == 0:
                acceptat = True

            if acceptat:
                return True

        if len(stiva_curenta) == 0: #daca nu am indeplinit conditiile de acceptare de mai sus, automatul s-a blocat
            continue

        varf_stiva = stiva_curenta[0]
        mutari_posibile = []

        if index_curent < len(cuvant_verificat):
            litera_curenta = cuvant_verificat[index_curent]
            cheie_normala = (stare_curenta, litera_curenta, varf_stiva)
            mutari_posibile.append((cheie_normala, False))

        cheie_lambda = (stare_curenta, simbol_lambda, varf_stiva)
        mutari_posibile.append((cheie_lambda, True))

        for cheie, este_lambda in mutari_posibile:
            if cheie in tranzitii: #cautam o regula pentru aceasta configuratie
                for stare_urmatoare, sir_pus_stiva in tranzitii[cheie]:
                    if este_lambda:
                        index_nou = index_curent #ramanem pe loc
                    else:
                        index_nou = index_curent + 1 #mergem mai departe
                    if sir_pus_stiva == simbol_lambda:
                        sir_de_adaugat = ""
                    else:
                        sir_de_adaugat = sir_pus_stiva
                    stiva_noua = sir_de_adaugat + stiva_curenta[1:]
                    configuratie_noua = (stare_urmatoare, index_nou, stiva_noua)
                    if configuratie_noua not in vizitate:
                        vizitate.add(configuratie_noua)
                        coada.append(configuratie_noua)
    return False

if simulator_pda(stare_initiala, simbol_initial_stiva, multime_stari_finale, cuvant_verificat, mod_acceptare, tranzitii, simbol_lambda = "lambda"):
    w.write("ACCEPTAT")
else:
    w.write("RESPINS")
