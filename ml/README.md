## PromptGuard binary baseline

From the repository root:

```bash
python -m pip install -r ml/requirements.txt
python ml/train.py
```

This downloads the public deepset/prompt-injections dataset, evaluates on its provided held-out test split, and saves a TF-IDF + Logistic Regression pipeline under `ml/models/`.

This is a research baseline, **not** a production security guarantee. It does not yet distinguish jailbreaks from other injection types. Do not load untrusted joblib files.
