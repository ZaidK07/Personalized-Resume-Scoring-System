from views import Home, GetResumeScore

def register_routes(api):
    api.add_resource(Home,"/home")
    api.add_resource(GetResumeScore,"/get-resume-score")