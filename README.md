# IT Job Market Analyzer

Explore 8,184 LinkedIn job postings across nine IT fields. The Streamlit dashboard shows how postings are distributed across fields and lets you ask questions about a selected job title. Answers draw on up to three matching postings and include job IDs and quotes from the descriptions.

## Run the dashboard on Windows

From the project folder, run these commands in PowerShell using Python 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app\dashboard.py
```

The dashboard loads the processed data directly. To enable Gemini answers, create a `.env` file in the project root and add `GEMINI_API_KEY=your_key_here`. Keep your actual key private.

## Job classification

The notebook uses TF-IDF and logistic regression to classify postings into nine fields. The model achieved 92.69% accuracy and 88.51% macro F1 against rule-based labels. These scores measure agreement with the labeling rules. Evaluation against independently labeled examples is still pending.






## Dataset

This project uses [LinkedIn Job Postings (2023–2024)](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) by Arsh Koneru.

We filtered the original dataset to 8,184 IT job postings and assigned them to nine fields using classification rules. The processed dataset in `data/processed/it_jobs.pkl` is shared under the same [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/).