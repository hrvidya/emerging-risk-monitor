from services.chroma_store import (
    init_collection,
    upsert_texts
)

collection = init_collection()

documents = [
    "Cyber attacks can target banking systems and steal financial data.",
    "Phishing emails are commonly used to obtain employee credentials.",
    "Ransomware attacks can lock critical infrastructure systems.",
    "Insider threats may expose confidential customer information.",
    "Distributed denial-of-service attacks can disrupt online services.",
    "Fraudulent transactions should be monitored in real time.",
    "AI systems can help detect suspicious financial activities.",
    "Weak passwords increase the risk of unauthorized access.",
    "Security audits help identify system vulnerabilities early.",
    "Regular monitoring improves incident response capabilities."
]

ids = [f"doc_{i}" for i in range(len(documents))]

metadatas = [
    {"topic": "risk_monitoring"} for _ in documents
]

upsert_texts(
    collection=collection,
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

print("Successfully seeded 10 documents into ChromaDB.")