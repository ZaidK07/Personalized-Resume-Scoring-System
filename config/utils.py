from config.pinecone_service.pc_config import generate_embedding, get_similar_cases


def get_top_cases(jd_summary, res_summary, user_id):
    embedding_text = jd_summary + res_summary

    embedding = generate_embedding(text = embedding_text)

    top_cases_list = get_similar_cases(user_id = user_id, embedding = embedding, top_k = 7)
    print("top cases list-->", top_cases_list)

    return top_cases_list