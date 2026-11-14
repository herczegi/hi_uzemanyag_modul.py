HI Hibrid autós fogyasztás- és költségelemző

Herczeg István 
Y1X2XP

Felhasználói leírás
Python 3 szükséges, a tkinter és a datetime a Python része.
A naptárválasztóhoz telepíteni kell: pip install tkcalendar babel
python main.py-ban kell indítani

A program célja

A grafikus Python-program a hibrid autó benzinfogyasztását és otthoni elektromos töltését külön kezeli. Kiszámítja a benzinfogyasztást liter/100 km-ben, az elektromos fogyasztást kWh/100 km-ben, valamint az energiaköltségeket.

Fájlok

- main.py: Tkinter gui és eseménykezelő
- hi_uzemanyag_modul.py: adatellenőrzés, költség- és fogyasztásszámítás, naplózás

Modulok

- main.py indítófájl, a grafikus felület és az eseménykezelés
- hi_uzemanyag_modul.py: saját modul, az adatellenőrzés, a számítások és a naplózás
- Felhasznált modulok: tkinter, datetime, tkcalendar

main.py

Függvények:

- hi_kartya_letrehozasa: egy összesítő kártya létrehozása a felületen
- hi_szam_formazasa: számok magyaros formázása 
- hi_frissit: a táblázat és az összesítő kártyák újrarajzolása
- hi_hozzaadas_esemeny: a hozzáadás gomb eseménykezelője
- hi_torles_esemeny: a törlés gomb eseménykezelője

hi_uzemanyag_modul.py

Függvények:

- hi_szam_atalakitasa: szöveg számmá alakítása, a negatív érték elutasítása
- hi_adatok_ellenorzese: a dátum, a mennyiségek, az árak és a kilométeróra-állás ellenőrzése
- hi_tankolasi_koltseg: a benzintankolás költsége (liter × literár)
- hi_toltesi_koltseg: az otthoni töltés költsége (kWh × áramár)
- hi_havi_osszesites: egy adott hónap költségének összege
- hi_idoszaki_osszesites: a teletankolások közötti időszakok összesítése
- hi_atlagfogyasztas: benzin- és áramfogyasztás 100 km-re
- hi_atlagkoltseg_100km: energiaköltség 100 km-re

Osztály: HIUzemanyagNaplo, a tankolások és töltések tárolása

- __init__: üres napló létrehozása
- hi_hozzaad: új bejegyzés ellenőrzése, költségszámítása és tárolása
- hi_torol: bejegyzés törlése azonosító alapján
- hi_lista: a bejegyzések rendezett listája
- hi_osszes_koltseg: az összes energiaköltség
- hi_havi_koltseg: egy hónap költsége
- hi_atlagfogyasztas: az átlagfogyasztás kiszámítása


Használat:
 Add meg az otthoni áram díját Ft/kWh értékben,
 ,tankoláskor add meg a dátumot, a benzint literben, a benzin literárát és az autó kilométeróra állását
 ,otthoni töltéskor add meg a töltött kWh mennyiségét és a kilométeróra állását
 ,ha benzintankoláskor teljesen tele töltöd a tankot, jelöld be a teletankolást, de ha csak átlagot akarsz számolni, akkor is két teletankolásból tud a program átlagot számolni

Az áramár módosítása csak az új töltésekre vonatkozik. Minden bejegyzés a rögzítéskor érvényes áramárat és költséget tárolja

Számítás

A két egymást követő teletankolás közötti időszakban rögzített benzint és elektromos energiát a program összeadja. A megtett távolságot a két teletankolás kilométeróra-állásának különbsége adja

- Benzinfogyasztás = összes benzin / megtett km × 100
- Elektromos fogyasztás = összes kWh / megtett km × 100
- Költség = benzin költsége + otthoni töltés költsége
- Energiaköltség / 100 km = az időszak költsége / megtett km × 100

Fontos: a teletankolás jelölése a benzintank teljes feltöltését jelenti. A töltési és tankolási bejegyzéseknél is a valós kilométeróra-állást add meg. A fogyasztási eredmény csak legalább két teletankolás között jelenik meg.

ADattárolás:

Az adatok az alkalmazás futása alatt tárolódnak; a program bezárásakor elvesznek.
