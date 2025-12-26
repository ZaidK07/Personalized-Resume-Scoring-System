from config.pinecone_service.pc_config import generate_embedding, get_similar_cases
from docx import Document
from pypdf import PdfReader
import io


def get_top_cases(jd_summary, res_summary, user_id):
    embedding_text = jd_summary + res_summary

    embedding = generate_embedding(text = embedding_text)

    top_cases_list = get_similar_cases(user_id = user_id, embedding = embedding, top_k = 7)
    print("top cases list-->", top_cases_list)

    return top_cases_list


def get_text_from_file(file):
    file_name = file.filename.lower()

    if file_name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file.read()))
        return "".join(p.extract_text() for p in reader.pages)

    if file_name.endswith(".docx"):
        doc = Document(io.BytesIO(file.read()))
        return "\n".join(p.text for p in doc.paragraphs)

    if file_name.endswith(".txt"):
        return file.read().decode("utf-8")

    return None