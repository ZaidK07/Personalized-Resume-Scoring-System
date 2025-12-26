from flask_restful import Resource
from flask import request
from config.utils import get_text_from_file
from gen_ai.agent_config.agent import invoke_agent


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

        main_list = []
        for resume in resume_text_list:
            user_prompt = f"""
            Job Description: {job_description_text}

            Resume: {resume.get('content')}

            User ID: {user_id}
            """

            response = invoke_agent(user_prompt = user_prompt)
            main_list.append({
                'name': resume['filename'],
                'response': response
            })

        return main_list, 200