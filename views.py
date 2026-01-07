from flask_restful import Resource
from flask import request
from config.utils import get_text_from_file
from gen_ai.agent_config.agent import invoke_agent
from config.pinecone_service.pc_config import generate_embedding, add_feedback_record


class Home(Resource):
    def get(self):
        return {'msg': 'This is home page!'}


class GetResumeScore(Resource):
    def post(self):
        job_description_file = request.files.get('job_description')
        resume_files = request.files.getlist('resume_files')
        user_id = request.form.get('user_id')
        print(user_id)

        if not job_description_file or not resume_files:
            return {'msg': 'Upload Job Description & Resume please!'}

        job_description_text = get_text_from_file(file = job_description_file)
        # print("job description text-->", job_description_text)

        resume_text_list = []
        for resume in resume_files:
            resume_name = resume.filename.lower()
            resume_text = get_text_from_file(file = resume)

            if resume_text == None:
                print(f"Skipped resume with name: {resume_name}, because of unsupported file format!")
                continue

            resume_text_list.append({
                'filename': resume_name,
                'content': resume_text
            })

        scored_list = []
        for resume in resume_text_list:
            user_prompt = f"""
            Job Description: {job_description_text}

            Resume: {resume.get('content')}

            User ID: {user_id}
            """

            response = invoke_agent(user_prompt = user_prompt)
            scored_list.append({
                'resume_name': resume['filename'],
                'model_response': response,
                'resume_content': resume['content'],
                'job_description': job_description_text
            })

        return {'scored_list': scored_list}, 200


class SubmitFeedback(Resource):
    def post(self):
        json_data = request.get_json()

        user_id = json_data.get('user_id')
        job_description = json_data.get('job_description')
        resume_content = json_data.get('resume_content')
        reason = json_data.get('reason')

        if not all([user_id, job_description, resume_content, reason]):
            return {'msg': 'Missing required fields'}, 400

        combined_text = job_description[:1000] + resume_content[:1000]

        embedding = generate_embedding(text=combined_text)

        vector_id = add_feedback_record(
            user_id = user_id,
            job_description = job_description[:1000],
            resume = resume_content[:1000],
            reason = reason,
            embedding = embedding
        )

        return {'msg': 'Feedback saved successfully', 'id': vector_id}, 200