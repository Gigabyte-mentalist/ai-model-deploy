import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

texts = [
    "bu ajoyib mahsulot juda yoqdi", "zor sifat tavsiya qilaman",
    "mukammal xizmat rahmat", "yaxshi narx yaxshi sifat",
    "juda mamnunman yana olaman", "tez yetkazib berishdi zor",
    "yomon sifat pul isrof", "umuman yoqmadi afsus",
    "buzuq keldi qaytardim", "sekin xizmat yomon munosabat",
    "pulimga achindim yomon", "sifatsiz mahsulot olmang",
]
labels = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf", LogisticRegression()),
])
model.fit(texts, labels)
joblib.dump(model, "tests/test_model.joblib")
print("Test modeli yaratildi")
