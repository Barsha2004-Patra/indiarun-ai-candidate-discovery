import re


SKILL_DATABASE = [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "LLM",
    "PyTorch",
    "TensorFlow",
    "Keras",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "SQL",
    "Spark",
    "Airflow",
    "Kafka",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Git",
    "Linux",
    "FastAPI",
    "Flask",
    "Django",
    "LangChain",
    "Hugging Face",
    "Transformers",
    "RAG",
    "Milvus",
    "Pinecone",
    "FAISS",
    "Vector Database",
    "LoRA",
    "GAN",
    "MLOps",
    "Weights & Biases",
    "BentoML",
]


def parse_job_description(job_text):

    text = job_text.lower()

    parsed = {
        "title": "",
        "experience": 0,
        "required_skills": [],
    }

    # -------- Experience --------
    exp = re.search(r"(\d+)\+?\s*years?", text)

    if exp:
        parsed["experience"] = int(exp.group(1))

    # -------- Title --------
    title_patterns = [
        r"machine learning engineer",
        r"data scientist",
        r"data engineer",
        r"ai engineer",
        r"backend engineer",
        r"software engineer",
        r"ml engineer",
        r"genai engineer",
    ]

    for pattern in title_patterns:
        if pattern in text:
            parsed["title"] = pattern.title()
            break

    # -------- Skills --------
    found = []

    for skill in SKILL_DATABASE:
        if skill.lower() in text:
            found.append(skill)

    parsed["required_skills"] = sorted(set(found))

    return parsed