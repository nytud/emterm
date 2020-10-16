## a term-annotáció formája

### alap

Egyszavas term-ek.\
A term-jelölés simán egy plusz oszlopba kerül a `.tsv`-ben.\
Az egyes termek sorszámot kapnak, az annotáció formája: `<sorszám>:<term_id>`.\
A `term_id` a term-adatbázisban (IATE, EUROVOC, bármi) meghatározott azonosító.\
A `sorszám` _mondaton_ belüli term-sorszám az előfordulás sorrendjében.\
Ha egy termnek több `term_id`-je (=azonosítója) van (vagy ilyen!), akkor az elválasztó: `×`.

```txt
w_1  1:a
w_2
w_3  2:b×c
w_4
```

= `w_1` az egy `a` term, `w_3` az egy term, aminek 2 db azonosítója van: `b` és `c`.

### bonyolítás

Többszavas term-ek.\
A term minden szava kap jelölést, a term _első_ szava pont úgy, ahogy az egyszavas term-ek.\
A második, harmadik, stb. szónál csak a `sorszám`-ot ismételjük meg.\
Ha egy szó több term-ben is érintett, akkor `;` az elválasztó.

```txt
w_5  3:d
w_6  3;4:e×f
w_7  4
w_8  4 
w_9
```

= A `3` sorszámú term kétszavas (`w_5..w_6`), azonosítója: `d`.\
A `4` term háromszavas (`w_6..w_8`), két azonosítója van: `e` és `f`.\
`w_6` _két_ termben is érintett (ld. ';'), `3`-nak az utsó szava és egyben `4`-nek az első szava.

### piszkos trükk

A MARCELL projektben (ismeretlen okokból...) _csakis_ `:` és `;` lehet elválasztó karakter. _Emiatt kénytelen-kelletlen `×` helyett is `;`-t használunk._ A fenti példa ismét ebben a formában:

```txt
w_5  3:d
w_6  3;4:e;f
w_7  4
w_8  4 
w_9
```

_Állítás:_ így is egyértelműen értelmezhető marad az annotáció!\
_Így:_ amíg nem találunk `:`-ot, addig korábbi termek többedik szavának sorszámát látjuk `;`-vel elválasztva.\
Amikor `:`-t találunk, akkor ez egy term első szava, aminek az azonosítóit ';'-vel elválasztva látjuk az adott `:` és a következő `:` (vagy sor vége) között.\
Kemény, de működik. Ellenőrizhetjük `w_6`-ra.
