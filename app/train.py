"""Kichik sentiment modelini o'rgatib, diskka saqlaydi."""
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# O'quv ma'lumotlari (real loyihada bu minglab qator bo'ladi)
texts = [
    "bu ajoyib mahsulot juda yoqdi", "zo'r sifat tavsiya qilaman",
    "mukammal xizmat rahmat", "yaxshi narx yaxshi sifat",
    "juda mamnunman yana olaman", "tez yetkazib berishdi zo'r",
    "yomon sifat pul isrof", "umuman yoqmadi afsus",
    "buzuq keldi qaytardim", "sekin xizmat yomon munosabat",
    "pulimga achindim yomon", "sifatsiz mahsulot olmang",
]
labels = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]  # 1=ijobiy, 0=salbiy

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf", LogisticRegression()),
])
model.fit(texts, labels)

joblib.dump(model, "model.joblib")
print("Model saqlandi: model.joblib")
