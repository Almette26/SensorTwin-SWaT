# Data Card — SWaT (Secure Water Treatment) Dataset

## 1. Sursă și Proveniență
* **Organizație emitentă:** iTrust, Center for Research in Cyber Security, Singapore University of Technology and Design (SUTD).
* **Testbed fizic:** Instalație industrială pilot de tratare a apei la scară redusă (capacitate: 5 galoane/minut), complet funcțională, alcătuită din 6 etape cascadate de proces (P1–P6) controlate prin 6 PLC-uri Allen-Bradley și magistrale industriale comune (EtherNet/IP, CIP).
* **Referință oficială:** Goh, J., Adepu, S., Junejo, K. N., & Mathur, A. (2016). *A Dataset to Support Research in the Design of Secure Water Treatment Systems*.

## 2. Perioadă de Colectare și Dimensiuni
* **Fișiere brute:**
  * `normal.csv`: 1.387.098 eșantioane (regim continuu exclusiv nominal, fără atacuri cibernetice).
  * `attack.csv`: 54.621 eșantioane (înregistrarea ferestrelor de atac activ, cuprinzând 36 de scenarii fizice distincte).
  * `merged.csv`: 1.441.719 eșantioane totale (concatenarea întregii perioade).
* **Partiționare implementată în pipeline (`src/data_loader.py`):**
  * **Train Set:** 1.040.323 eșantioane (primele 75% din seria normală, stare pur nominală a procesului).
  * **Test Set:** 401.396 eșantioane totale (restul de 346.775 eșantioane normale + cele 54.621 eșantioane de atac).
  * **Rata de atac în Test:** 13,61% (54.621 anomalii din 401.396 puncte), raport aliniat cu benchmark-urile canonice din literatură (ex. Ozbek et al., 12,14%).

## 3. Rezoluție Temporală și Format
* **Frecvență de eșantionare:** 1 Hz (1 măsurătoare pe secundă, pas de timp constant $\Delta t = 1\text{ s}$).
* **Format:** Fișiere tabelare CSV delimitate prin virgulă, conținând marca temporală (`Timestamp`), 51 de canale de proces și coloana binară de decizie (`Normal/Attack` mapată în `Label`: 0 = Normal, 1 = Attack).

## 4. Spațiul Senzorilor și Unități de Măsură
Setul acoperă 51 de tag-uri de proces distribuite pe subsistemele P1–P6:
* **Senzori de nivel (LIT):** `LIT101`, `LIT301`, `LIT401` — unitate: milimetri ($mm$).
* **Senzori de debit (FIT):** `FIT101`, `FIT201`, `FIT301`, `FIT401`, `FIT501`–`FIT504`, `FIT601` — unitate: metri cubi pe oră ($m^3/h$).
* **Senzori de presiune (PIT / DPIT):** `PIT501`–`PIT503`, `DPIT301` — unitate: kilopascali ($kPa$).
* **Analizoare chimice de calitate (AIT):** conductivitate, pH, redox, duritate (`AIT201`–`AIT203`, `AIT401`–`AIT402`, `AIT501`–`AIT504`) — unități: $\mu S/cm$, unități de $pH$, $mV$.
* **Actuatori - Pompe de proces (P):** `P101`–`P102`, `P201`–`P206`, `P301`–`P302`, `P401`–`P404`, `P501`–`P502`, `P601`–`P603` — valori discrete: $1$ (Oprit), $2$ (Pornit).
* **Actuatori - Vane motorizate (MV / UV):** `MV101`, `MV201`, `MV301`–`MV304`, `UV401` — valori discrete: $0$ (Închis), $1$ (Deschis), $2$ (Comutare).

## 5. Goluri, Valori Lipsă și Preprocesare
* **Lipsă date (Missing values):** Fără valori nule sau NaN în seriile temporale (achiziție industrială uniformă 1 Hz).
* **Curățare denumiri:** Eliminarea spațiilor parazite de tip whitespace din antetele coloanelor (ex. `' MV101'` $\rightarrow$ `'MV101'`).
* **Coloane constante (Zero-variance):** 7 atribute invariante (`P202`, `P301`, `P401`, `P404`, `P502`, `P601`, `P603`) sunt eliminate automat, rezultând un spațiu de intrare activ de 44 de variabile de proces.

## 6. Scalare și Prevenirea Scurgerilor Temporale
* **Split temporal:** Ordinea cronologică este menținută strict; nu se utilizează eșantionare aleatorie (*random shuffle*), prevenind scurgerile temporale de informație (*temporal leakage*).
* **Normalizare:** MinMax scaling în intervalul $[0, 1]$, calibrat (*fit*) exclusiv pe cele 1.040.323 eșantioane de antrenare și aplicat identic (*transform*) pe setul de test.

## 7. Licență și Condiții de Utilizare
* **Licență:** Acces de cercetare academică oferit de iTrust SUTD (Research Data Request Agreement).
* **Restricții:** Utilizare exclusiv în scopuri educaționale și științifice non-comerciale, cu obligativitatea citării testbed-ului original.