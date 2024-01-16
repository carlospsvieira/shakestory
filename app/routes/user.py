def user_routes(app):
    @app.get("/")
    def read_root():
        return {"message": "hello Shakestory, from user route"}
