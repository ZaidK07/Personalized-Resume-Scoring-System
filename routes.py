from views import Home

def register_routes(api):
    api.add_resource(Home,"/home")