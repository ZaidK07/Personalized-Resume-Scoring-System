from views import Home, GetResumeScore, SubmitFeedback

def register_routes(api):
    api.add_resource(Home,"/home")
    api.add_resource(GetResumeScore,"/get-resume-score")
    api.add_resource(SubmitFeedback,"/submit-feedback")