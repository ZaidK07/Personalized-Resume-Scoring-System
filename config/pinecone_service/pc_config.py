from pinecone import Pinecone, ServerlessSpec
import os
import uuid


pc_client = Pinecone(api_key = os.getenv("PINECONE_API_KEY"))

index_name = "resume-scoring-system-index"

embedding_model_name = 'multilingual-e5-large'


def ensure_pinecone_index():
    pc_index_list = pc_client.list_indexes().names()
    # print(pc_index_list)
    if index_name not in pc_index_list:
        print("Index not found in Pinecone. Creating Index!")

        pc_client.create_index(
            name = index_name,
            dimension = 1024,
            metric = 'cosine',
            spec = ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    else:
        print("Index already exists, continuing execution.")


def add_feedback_record(user_id, job_description, resume, reason, embedding):
    vector_id = str(uuid.uuid4().hex)

    metadata = {
        "user_id": user_id,
        "jd_summary": job_description[:1000],
        "resume_summary": resume[:1000],
        "feedback": reason
    }
    pc_client.Index(index_name).upsert(vectors=[(vector_id, embedding, metadata)])
    print("Added feedback to pinecone, ID--->", vector_id)

    return vector_id


def get_similar_cases(user_id, embedding, top_k=7):
    result = pc_client.Index(index_name).query(
        vector=embedding,
        top_k=top_k,
        filter={
            "user_id": {"$eq": user_id}
        },
        include_metadata=True # metadata means the text data we inserted or it just returns ID
    ).get('matches')
    return result


def generate_embedding(text):
    embedding = pc_client.inference.embed(
        model = embedding_model_name,
        inputs = [text],
        parameters = {"input_type": "passage", "truncate": "END"}
    )[0].values
    return embedding



if __name__ == '__main__':
    ensure_pinecone_index()

    # vector_id = add_feedback_record(
    #     user_id="test_user",
    #     job_description="Backend Python developer role",
    #     resume="Python developer with ML experience",
    #     reason="Good skill match",
    #     embedding=[0.01] * 1024
    # )
    # print(vector_id)

    response = get_similar_cases(user_id = 'test_user',embedding=[0.01]*1024)
    print(response)

    # embed = generate_embedding(text = 'Hello there!')
    # print(embed)