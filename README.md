# 🕵️‍♂️ Fraud Detection System

A complete fraud detection pipeline using data simulation, rule-based scoring, and machine learning (Random Forest) to identify suspicious reimbursement transactions.

---

## 📌 Project Structure

📁 Sistema_fraude/
├── 📄 gerar_dados.py
├── 📄 estatisticas.py
├── 📄 regras_fraude.py
├── 📄 modelo_fraude_ml.py
├── 📄 pontuacao_risco.py
├── 📊 dataset_reembolsos_simulado.xlsx
├── 📊 tabela_final_reembolsos_com_score.xlsx
├── 📊 tabela_com_resultado_ml.xlsx
└── 📁 venv/


---

## 🚀 Steps Performed

### 1. **Synthetic Dataset Generation**
- Faker + NumPy to simulate realistic reimbursement data.
- 5,000 transactions from random employees, departments, and approvers.

### 2. **Descriptive Analytics**
- Histograms, bar plots, and time series to understand patterns and trends.
- Exported with Seaborn/Matplotlib.

### 3. **Rule-Based Fraud Scoring**
- Duplicated claims.
- Values 2x std above the mean.
- Approvers with 90%+ approval rates.
- Employees with more than 10% of total expenses.

### 4. **Machine Learning Model**
- `RandomForestClassifier` + SMOTE for class imbalance.
- Achieved **F1 score = 1.00** (on synthetic data).
- Saved final ML predictions.

---

## 🧠 Technologies Used

- Python, Pandas, NumPy
- Faker (data generation)
- Matplotlib, Seaborn
- scikit-learn, imbalanced-learn
- Excel I/O

---

## 📈 Results

- Model trained with synthetic fraud labels.
- Exported results to Excel for Power BI dashboards.

---

## 🧰 Future Work

- Connect to real-world datasets.
- Implement auto-alerts and dashboards in Power BI.
- Integrate with API for live detection.

---

## 📷 Badge

![Fraud Detection Badge](https://raw.githubusercontent.com/ricardohenrique1609/Fraude-detection/main/imagens/badge_fraude.png)


---

## 👨‍💻 Author

**Ricardo Henrique Ramos Silva**  
[LinkedIn](https://linkedin.com/in/ricardo-henrique-28939b275) | [Portfolio](https://curriculoricardo.netlify.app/)

---

⭐️ Don't forget to leave a star if you liked it!
