# 🌫️ Air Quality Prediction Using Machine Learning

Ovaj projekt predviđa ciljnu vrijednost kvalitete zraka koristeći **machine learning** model treniran nad AirQuality podacima. Rješenje uključuje **analizu podataka, treniranje i evaluaciju modela**, te **Flask web aplikaciju** koja nudi web formu i REST API za predikcije. 

Projekt je izrađen u sklopu kolegija (RUAP / Service Computing and Data Analysis) na FERIT-u, Osijek. 

---

## 📊 Problem Description

Predikcija kvalitete zraka je tipičan problem učenja iz podataka gdje na temelju senzorskih mjerenja želimo procijeniti (predvidjeti) izlaznu vrijednost koju model uči iz povijesnih zapisa. Aplikacija omogućava unos senzorskih vrijednosti i vraća predikciju iz treniranog modela. 

Model koristi sljedeće ulazne značajke (features): 

- `CO(GT)`
- `PT08.S1(CO)`
- `NMHC(GT)`
- `C6H6(GT)`
- `PT08.S2(NMHC)`
- `NOx(GT)`
- `PT08.S3(NOx)`
- `PT08.S4(NO2)`
- `PT08.S5(O3)`
- `T`
- `RH`
- `AH` 

---

## 📂 Dataset

U notebooku se koristi **AirQualityUCI** dataset (CSV) i radi se osnovno čišćenje poput uklanjanja “Unnamed” stupaca i trimanje naziva kolona. 

Primjer kolona u skupu podataka uključuje `Date`, `Time` i niz senzorskih mjera poput `CO(GT)`, `NOx(GT)`, `T`, `RH`, `AH`. 

---

## 🔎 Data Analysis

U sklopu notebooka rađena je priprema i analiza podataka kako bi se dobio smislen ulaz za modele, uključujući učitavanje CSV-a i osnovne transformacije kolona. 

Korištene su standardne metrike za evaluaciju klasifikacijskih modela (npr. accuracy, F1, classification report, confusion matrix) što upućuje da je barem jedan dio pipeline-a orijentiran na klasifikaciju. 

---

## 🤖 Machine Learning Models

U notebooku su implementirani i isprobani sljedeći modeli iz scikit-learn-a: 

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier
- K-Nearest Neighbors (KNN)
- Gradient Boosting Classifier 

Za spremanje/učitavanje modela koristi se `joblib`, a web aplikacija učitava finalni model iz `model.pkl` i poziva `model.predict(...)` nad pandas DataFrame-om. 

---

## ⚙️ Preprocessing

Prije predikcije, ulazni JSON/form podaci se validiraju i pretvaraju u `float`, zatim se slaže jedan red DataFrame-a s točno definiranim redoslijedom feature-a. 

U notebooku se koristi tipičan scikit-learn preprocessing stack (npr. imputacija i skaliranje kroz pipeline/transformere), ovisno o modelu. 

---

## 🌐 Web App + REST API

Trenirani model je izložen kroz **Flask** aplikaciju koja nudi i web UI i REST API. 

### Endpoints
- `GET /` – web forma (HTML) za unos feature-a. 
- `POST /predict` – predikcija preko forme, vraća renderani HTML s rezultatom ili greškom. 
- `POST /api/predict` – predikcija preko JSON-a, vraća `{ "prediction": "..." }` ili `{ "error": "..." }`. 

### Example Request (JSON)
API prima “flat” JSON ili objekt unutar `data`. 

```json
{
  "CO(GT)": 2.6,
  "PT08.S1(CO)": 1360,
  "NMHC(GT)": 150,
  "C6H6(GT)": 11.9,
  "PT08.S2(NMHC)": 1046,
  "NOx(GT)": 166,
  "PT08.S3(NOx)": 1056,
  "PT08.S4(NO2)": 1692,
  "PT08.S5(O3)": 1268,
  "T": 13.6,
  "RH": 48.9,
  "AH": 0.7578
}
