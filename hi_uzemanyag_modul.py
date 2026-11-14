from datetime import datetime


def hi_szam_atalakitasa(ertek, megnevezes):
    try:
        hi_eredmeny = float(str(ertek).replace(",", ".").strip())
    except ValueError as hi_hiba:
        raise ValueError(f"A(z) {megnevezes} értékét számmal add meg.") from hi_hiba
    if hi_eredmeny < 0:
        raise ValueError(f"A(z) {megnevezes} nem lehet negatív.")
    return hi_eredmeny


def hi_adatok_ellenorzese(datum, liter, benzin_ar, kwh, aram_ar, kilometer):
    try:
        datetime.strptime(datum, "%Y-%m-%d")
    except ValueError as hi_hiba:
        raise ValueError("A dátum formátuma ÉÉÉÉ-HH-NN legyen, például 2026-11-13.") from hi_hiba

    hi_liter = hi_szam_atalakitasa(liter, "benzinkút mennyiség")
    hi_benzin_ar = hi_szam_atalakitasa(benzin_ar, "benzin literára")
    hi_kwh = hi_szam_atalakitasa(kwh, "otthoni töltés mennyisége")
    hi_aram_ar = hi_szam_atalakitasa(aram_ar, "otthoni áramár")

    try:
        hi_kilometer = int(str(kilometer).strip())
    except ValueError as hi_hiba:
        raise ValueError("A kilométeróra-állás egész szám legyen.") from hi_hiba

    if hi_liter == 0 and hi_kwh == 0:
        raise ValueError("Legalább benzintankolást vagy elektromos töltést adj meg.")
    if hi_liter > 0 and hi_benzin_ar <= 0:
        raise ValueError("Benzintankolásnál a literárnak nullánál nagyobbnak kell lennie.")
    if hi_kwh > 0 and hi_aram_ar <= 0:
        raise ValueError("Elektromos töltésnél az áramárnak nullánál nagyobbnak kell lennie.")
    if hi_kilometer < 0:
        raise ValueError("A kilométeróra-állás nem lehet negatív.")

    return hi_liter, hi_benzin_ar, hi_kwh, hi_aram_ar, hi_kilometer


def hi_tankolasi_koltseg(liter, literar):
    return round(float(liter) * float(literar), 2)


def hi_toltesi_koltseg(kwh, aram_ar):
    return round(float(kwh) * float(aram_ar), 2)


def hi_havi_osszesites(tankolasok, ev, honap):
    hi_osszeg = 0.0
    hi_index = 0
    while hi_index < len(tankolasok):
        hi_tankolas = tankolasok[hi_index]
        hi_datum = datetime.strptime(hi_tankolas["datum"], "%Y-%m-%d")
        if hi_datum.year == ev and hi_datum.month == honap:
            hi_osszeg += hi_tankolas["teljes_koltseg"]
        hi_index += 1
    return round(hi_osszeg, 2)


def hi_idoszaki_osszesites(tankolasok):
    hi_rendezett = sorted(
        tankolasok,
        key=lambda hi_tankolas: (
            hi_tankolas["kilometer"],
            hi_tankolas["datum"],
            hi_tankolas["azonosito"]
        )
    )
    hi_teletank_poziciok = []
    hi_index = 0
    while hi_index < len(hi_rendezett):
        if hi_rendezett[hi_index]["teletank"]:
            hi_teletank_poziciok.append(hi_index)
        hi_index += 1

    hi_osszes_liter = 0.0
    hi_osszes_kwh = 0.0
    hi_osszes_benzin_koltseg = 0.0
    hi_osszes_aram_koltseg = 0.0
    hi_osszes_kilometer = 0

    hi_index = 1
    while hi_index < len(hi_teletank_poziciok):
        hi_kezdo = hi_teletank_poziciok[hi_index - 1]
        hi_veg = hi_teletank_poziciok[hi_index]
        hi_megtett_km = hi_rendezett[hi_veg]["kilometer"] - hi_rendezett[hi_kezdo]["kilometer"]

        if hi_megtett_km > 0:
            hi_pozicio = hi_kezdo + 1
            while hi_pozicio <= hi_veg:
                hi_osszes_liter += hi_rendezett[hi_pozicio]["liter"]
                hi_osszes_benzin_koltseg += hi_rendezett[hi_pozicio]["benzin_koltseg"]
                hi_pozicio += 1

            hi_pozicio = hi_kezdo
            while hi_pozicio < hi_veg:
                hi_osszes_kwh += hi_rendezett[hi_pozicio]["kwh"]
                hi_osszes_aram_koltseg += hi_rendezett[hi_pozicio]["aram_koltseg"]
                hi_pozicio += 1

            hi_osszes_kilometer += hi_megtett_km
        hi_index += 1

    return (
        hi_osszes_liter,
        hi_osszes_kwh,
        hi_osszes_benzin_koltseg,
        hi_osszes_aram_koltseg,
        hi_osszes_kilometer,
    )


def hi_atlagfogyasztas(tankolasok):
    (
        hi_osszes_liter,
        hi_osszes_kwh,
        hi_osszes_benzin_koltseg,
        hi_osszes_aram_koltseg,
        hi_osszes_kilometer,
    ) = hi_idoszaki_osszesites(tankolasok)

    if hi_osszes_kilometer == 0:
        return None, None

    hi_benzin_atlag = hi_osszes_liter / hi_osszes_kilometer * 100
    hi_elektromos_atlag = hi_osszes_kwh / hi_osszes_kilometer * 100
    return round(hi_benzin_atlag, 2), round(hi_elektromos_atlag, 2)


def hi_atlagkoltseg_100km(tankolasok):
    (
        hi_osszes_liter,
        hi_osszes_kwh,
        hi_osszes_benzin_koltseg,
        hi_osszes_aram_koltseg,
        hi_osszes_kilometer,
    ) = hi_idoszaki_osszesites(tankolasok)

    if hi_osszes_kilometer == 0:
        return None
    return round(
        (hi_osszes_benzin_koltseg + hi_osszes_aram_koltseg)
        / hi_osszes_kilometer * 100,
        2,
    )


class HIUzemanyagNaplo:
    def __init__(self):
        self.hi_tankolasok = []
        self.hi_kovetkezo_azonosito = 1

    def hi_hozzaad(self, datum, liter, benzin_ar, kwh, aram_ar, kilometer, teletank):
        hi_liter, hi_benzin_ar, hi_kwh, hi_aram_ar, hi_kilometer = hi_adatok_ellenorzese(
            datum, liter, benzin_ar, kwh, aram_ar, kilometer
        )
        if teletank and hi_liter <= 0:
            raise ValueError("A teletankolás jelöléséhez benzintankolást is adj meg.")

        hi_index = 0
        while hi_index < len(self.hi_tankolasok):
            if self.hi_tankolasok[hi_index]["kilometer"] > hi_kilometer:
                raise ValueError("Az új kilométeróra-állás nem lehet kisebb egy korábbi bejegyzésénél.")
            hi_index += 1

        hi_benzin_koltseg = hi_tankolasi_koltseg(hi_liter, hi_benzin_ar) if hi_liter > 0 else 0.0
        hi_aram_koltseg = hi_toltesi_koltseg(hi_kwh, hi_aram_ar) if hi_kwh > 0 else 0.0
        hi_bejegyzes = {
            "azonosito": self.hi_kovetkezo_azonosito,
            "datum": datum,
            "liter": hi_liter,
            "benzin_ar": hi_benzin_ar,
            "kwh": hi_kwh,
            "aram_ar": hi_aram_ar,
            "kilometer": hi_kilometer,
            "teletank": bool(teletank),
            "benzin_koltseg": hi_benzin_koltseg,
            "aram_koltseg": hi_aram_koltseg,
            "teljes_koltseg": hi_benzin_koltseg + hi_aram_koltseg,
        }
        self.hi_tankolasok.append(hi_bejegyzes)
        self.hi_kovetkezo_azonosito += 1

    def hi_torol(self, azonosito):
        hi_index = 0
        while hi_index < len(self.hi_tankolasok):
            if self.hi_tankolasok[hi_index]["azonosito"] == azonosito:
                del self.hi_tankolasok[hi_index]
                return
            hi_index += 1

    def hi_lista(self):
        return sorted(
            self.hi_tankolasok,
            key=lambda hi_tankolas: (
                hi_tankolas["kilometer"],
                hi_tankolas["datum"],
                hi_tankolas["azonosito"]
            )
        )

    def hi_osszes_koltseg(self):
        hi_osszeg = 0.0
        hi_index = 0
        while hi_index < len(self.hi_tankolasok):
            hi_osszeg += self.hi_tankolasok[hi_index]["teljes_koltseg"]
            hi_index += 1
        return round(hi_osszeg, 2)

    def hi_havi_koltseg(self, ev, honap):
        return hi_havi_osszesites(self.hi_tankolasok, ev, honap)

    def hi_atlagfogyasztas(self):
        return hi_atlagfogyasztas(self.hi_tankolasok)
