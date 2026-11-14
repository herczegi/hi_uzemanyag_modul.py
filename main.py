import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from hi_uzemanyag_modul import HIUzemanyagNaplo, hi_atlagkoltseg_100km


app = tk.Tk()
app.title("HI Hibrid autós fogyasztás")
app.geometry("1240x760")
app.minsize(1000, 650)
app.configure(bg="#f3f5f7")

hi_naplo = HIUzemanyagNaplo()
hi_aram_ar_alap = tk.StringVar(value="70")

hi_stilus = ttk.Style()
hi_stilus.theme_use("clam")
hi_stilus.configure("TFrame", background="#f3f5f7")
hi_stilus.configure("TLabel", background="#f3f5f7", font=("Segoe UI", 10))
hi_stilus.configure("Title.TLabel", font=("Segoe UI", 19, "bold"), foreground="#183153")
hi_stilus.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#596579")
hi_stilus.configure("TButton", font=("Segoe UI", 10), padding=(10, 7))
hi_stilus.configure("Treeview", rowheight=27, font=("Segoe UI", 9))
hi_stilus.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

hi_fo = ttk.Frame(app, padding=16)
hi_fo.pack(fill="both", expand=True)
hi_fo.columnconfigure(0, weight=1)
hi_fo.rowconfigure(4, weight=1)

ttk.Label(hi_fo, text="Hibrid autós fogyasztás- és költségelemző", style="Title.TLabel").grid(
    row=0, column=0, sticky="w"
)

hi_beallitas = ttk.LabelFrame(hi_fo, text="Otthoni áram díja", padding=10)
hi_beallitas.grid(row=2, column=0, sticky="ew", pady=(0, 10))
ttk.Label(hi_beallitas, text="Áramár (Ft/kWh):").pack(side="left")
hi_aram_ar_mezo = ttk.Entry(hi_beallitas, textvariable=hi_aram_ar_alap, width=12)
hi_aram_ar_mezo.pack(side="left", padx=8)

hi_urlap = ttk.LabelFrame(hi_fo, text="Tankolás vagy otthoni töltés rögzítése", padding=10)
hi_urlap.grid(row=3, column=0, sticky="ew", pady=(0, 10))
hi_mezok = [
    ("Dátum (ÉÉÉÉ-HH-NN)", 0),
    ("Benzin (liter)", 1),
    ("Benzinár (Ft/l)", 2),
    ("Otthoni töltés (kWh)", 3),
    ("Kilométeróra (km)", 4),
]
hi_mezok_index = 0
while hi_mezok_index < len(hi_mezok):
    ttk.Label(hi_urlap, text=hi_mezok[hi_mezok_index][0]).grid(
        row=0, column=hi_mezok[hi_mezok_index][1], sticky="w", padx=5, pady=(0, 4)
    )
    hi_mezok_index += 1

hi_liter_valtozo = tk.StringVar()
hi_benzin_ar_valtozo = tk.StringVar()
hi_kwh_valtozo = tk.StringVar()
hi_kilometer_valtozo = tk.StringVar()
hi_teletank_valtozo = tk.BooleanVar(value=False)

hi_datum_mezo = DateEntry(
    hi_urlap,
    width=16,
    date_pattern="yyyy-mm-dd",
    locale="hu_HU",
    state="readonly"
)
hi_liter_mezo = ttk.Entry(hi_urlap, textvariable=hi_liter_valtozo)
hi_benzin_ar_mezo = ttk.Entry(hi_urlap, textvariable=hi_benzin_ar_valtozo)
hi_kwh_mezo = ttk.Entry(hi_urlap, textvariable=hi_kwh_valtozo)
hi_kilometer_mezo = ttk.Entry(hi_urlap, textvariable=hi_kilometer_valtozo)
hi_datum_mezo.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 8))
hi_liter_mezo.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 8))
hi_benzin_ar_mezo.grid(row=1, column=2, sticky="ew", padx=5, pady=(0, 8))
hi_kwh_mezo.grid(row=1, column=3, sticky="ew", padx=5, pady=(0, 8))
hi_kilometer_mezo.grid(row=1, column=4, sticky="ew", padx=5, pady=(0, 8))
hi_oszlop = 0
while hi_oszlop < 5:
    hi_urlap.columnconfigure(hi_oszlop, weight=1)
    hi_oszlop += 1

hi_gombok = ttk.Frame(hi_urlap)
hi_gombok.grid(row=2, column=0, columnspan=5, sticky="w", padx=5)
ttk.Checkbutton(hi_gombok, text="Teletankolás (fogyasztási méréshez)", variable=hi_teletank_valtozo).pack(
    side="left", padx=(0, 12)
)

hi_osszefoglalo = ttk.Frame(hi_fo)
hi_osszefoglalo.grid(row=4, column=0, sticky="nsew")
hi_osszefoglalo.columnconfigure(0, weight=1)
hi_osszefoglalo.rowconfigure(1, weight=1)

hi_kimutatas = ttk.Frame(hi_osszefoglalo)
hi_kimutatas.grid(row=0, column=0, sticky="ew", pady=(0, 10))
hi_oszlop = 0
while hi_oszlop < 5:
    hi_kimutatas.columnconfigure(hi_oszlop, weight=1)
    hi_oszlop += 1

hi_benzin_fogyasztas_szoveg = tk.StringVar(value="Nincs elég adat")
hi_elektromos_fogyasztas_szoveg = tk.StringVar(value="Nincs elég adat")
hi_osszes_koltseg_szoveg = tk.StringVar(value="0,00 Ft")
hi_havi_koltseg_szoveg = tk.StringVar(value="0,00 Ft")
hi_szaz_km_koltseg_szoveg = tk.StringVar(value="Nincs elég adat")


def hi_kartya_letrehozasa(cim, valtozo, oszlop):
    hi_kartya = ttk.LabelFrame(hi_kimutatas, text=cim, padding=9)
    hi_kartya.grid(row=0, column=oszlop, sticky="nsew", padx=(0 if oszlop == 0 else 5, 0))
    ttk.Label(hi_kartya, textvariable=valtozo, font=("Segoe UI", 12, "bold")).pack(anchor="w")


hi_kartya_letrehozasa("Benzinfogyasztás", hi_benzin_fogyasztas_szoveg, 0)
hi_kartya_letrehozasa("Elektromos fogyasztás", hi_elektromos_fogyasztas_szoveg, 1)
hi_kartya_letrehozasa("Összes energiaköltség", hi_osszes_koltseg_szoveg, 2)
hi_kartya_letrehozasa("Aktuális havi költség", hi_havi_koltseg_szoveg, 3)
hi_kartya_letrehozasa("Energiaköltség / 100 km", hi_szaz_km_koltseg_szoveg, 4)

hi_lista_keret = ttk.LabelFrame(hi_osszefoglalo, text="Rögzített tankolások és töltések", padding=7)
hi_lista_keret.grid(row=1, column=0, sticky="nsew")
hi_lista_keret.columnconfigure(0, weight=1)
hi_lista_keret.rowconfigure(0, weight=1)

hi_oszlopok = ("datum", "liter", "benzin_ar", "kwh", "aram_ar", "benzin_koltseg", "aram_koltseg", "kilometer", "teletank")
hi_tabla = ttk.Treeview(hi_lista_keret, columns=hi_oszlopok, show="headings", selectmode="browse")
hi_fejlecek = [
    ("datum", "Dátum", 95, "center"),
    ("liter", "Benzin (l)", 75, "e"),
    ("benzin_ar", "Benzinár (Ft/l)", 95, "e"),
    ("kwh", "Töltés (kWh)", 85, "e"),
    ("aram_ar", "Áramár (Ft/kWh)", 105, "e"),
    ("benzin_koltseg", "Benzinköltség (Ft)", 115, "e"),
    ("aram_koltseg", "Töltésköltség (Ft)", 115, "e"),
    ("kilometer", "Kilométeróra", 105, "e"),
    ("teletank", "Teletank", 75, "center"),
]
hi_fejlec_index = 0
while hi_fejlec_index < len(hi_fejlecek):
    hi_adat = hi_fejlecek[hi_fejlec_index]
    hi_tabla.heading(hi_adat[0], text=hi_adat[1])
    hi_tabla.column(hi_adat[0], width=hi_adat[2], anchor=hi_adat[3])
    hi_fejlec_index += 1
hi_tabla.grid(row=0, column=0, sticky="nsew")
hi_gorgeto = ttk.Scrollbar(hi_lista_keret, orient="vertical", command=hi_tabla.yview)
hi_gorgeto.grid(row=0, column=1, sticky="ns")
hi_tabla.configure(yscrollcommand=hi_gorgeto.set)


def hi_szam_formazasa(ertek, tizedes=2):
    return format(ertek, f",.{tizedes}f").replace(",", " ").replace(".", ",")


def hi_frissit():
    hi_meglevo_elemek = hi_tabla.get_children()
    hi_index = 0
    while hi_index < len(hi_meglevo_elemek):
        hi_tabla.delete(hi_meglevo_elemek[hi_index])
        hi_index += 1

    hi_tankolasok = hi_naplo.hi_lista()
    hi_index = 0
    while hi_index < len(hi_tankolasok):
        hi_tankolas = hi_tankolasok[hi_index]
        hi_tabla.insert(
            "",
            "end",
            iid=str(hi_tankolas["azonosito"]),
            values=(
                hi_tankolas["datum"],
                hi_szam_formazasa(hi_tankolas["liter"]),
                hi_szam_formazasa(hi_tankolas["benzin_ar"]),
                hi_szam_formazasa(hi_tankolas["kwh"]),
                hi_szam_formazasa(hi_tankolas["aram_ar"]),
                hi_szam_formazasa(hi_tankolas["benzin_koltseg"]),
                hi_szam_formazasa(hi_tankolas["aram_koltseg"]),
                hi_szam_formazasa(hi_tankolas["kilometer"], 0),
                "Igen" if hi_tankolas["teletank"] else "Nem",
            ),
        )
        hi_index += 1

    hi_osszes_koltseg_szoveg.set(f"{hi_szam_formazasa(hi_naplo.hi_osszes_koltseg())} Ft")
    hi_ma = date.today()
    hi_havi_koltseg_szoveg.set(
        f"{hi_szam_formazasa(hi_naplo.hi_havi_koltseg(hi_ma.year, hi_ma.month))} Ft"
    )

    hi_benzin_atlag, hi_elektromos_atlag = hi_naplo.hi_atlagfogyasztas()
    if hi_benzin_atlag is None:
        hi_benzin_fogyasztas_szoveg.set("Nincs elég adat")
        hi_elektromos_fogyasztas_szoveg.set("Nincs elég adat")
        hi_szaz_km_koltseg_szoveg.set("Nincs elég adat")
    else:
        hi_benzin_fogyasztas_szoveg.set(f"{hi_szam_formazasa(hi_benzin_atlag)} l/100 km")
        hi_elektromos_fogyasztas_szoveg.set(f"{hi_szam_formazasa(hi_elektromos_atlag)} kWh/100 km")
        hi_koltseg_100_km = hi_atlagkoltseg_100km(hi_tankolasok)
        if hi_koltseg_100_km is None:
            hi_szaz_km_koltseg_szoveg.set("Nincs elég adat")
        else:
            hi_szaz_km_koltseg_szoveg.set(f"{hi_szam_formazasa(hi_koltseg_100_km)} Ft/100 km")


def hi_hozzaadas_esemeny():
    try:
        hi_aram_ar = hi_aram_ar_alap.get().strip()
        hi_naplo.hi_hozzaad(
            hi_datum_mezo.get().strip(),
            hi_liter_valtozo.get().strip() or "0",
            hi_benzin_ar_valtozo.get().strip() or "0",
            hi_kwh_valtozo.get().strip() or "0",
            hi_aram_ar,
            hi_kilometer_valtozo.get().strip(),
            hi_teletank_valtozo.get(),
        )
    except ValueError as hi_hiba:
        messagebox.showerror("Hibás adat", str(hi_hiba), parent=app)
        return

    hi_liter_valtozo.set("")
    hi_benzin_ar_valtozo.set("")
    hi_kwh_valtozo.set("")
    hi_kilometer_valtozo.set("")
    hi_teletank_valtozo.set(False)
    hi_frissit()


def hi_torles_esemeny():
    hi_kivalasztott = hi_tabla.selection()
    if not hi_kivalasztott:
        messagebox.showinfo("Nincs kiválasztás", "Először válassz ki egy bejegyzést a listából.", parent=app)
        return
    hi_megerosites = messagebox.askyesno(
        "Bejegyzés törlése",
        "Biztosan törlöd a kiválasztott bejegyzést?",
        parent=app,
    )
    if hi_megerosites:
        hi_naplo.hi_torol(int(hi_kivalasztott[0]))
        hi_frissit()


ttk.Button(hi_gombok, text="Bejegyzés hozzáadása", command=hi_hozzaadas_esemeny).pack(side="left", padx=(0, 8))
ttk.Button(hi_gombok, text="Kiválasztott törlése", command=hi_torles_esemeny).pack(side="left")



hi_frissit()
app.mainloop()