from pinecone import Pinecone, ServerlessSpec
import os


pc_api_key = os.getenv("PINECONE_API_KEY")

pc_client = Pinecone(api_key = pc_api_key)

index_name = "resume-scoring-system-index"

def ensure_pinecone_index():
    pc_index_list = pc_client.list_indexes().names()
    # print(pc_index_list)
    if index_name not in pc_index_list:
        print("Index not found in Pinecone. Creating Index!")

        pc_client.create_index(
            name = index_name,
            dimension = 1024,
            metric = 'cosine',
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    else:
        print("Index already exists, continuing execution.")



if __name__ == '__main__':
    ensure_pinecone_index()