def story_routes(app):
    @app.get("/story")
    def read_story():
        return {"message": "hello Shakestory, from story route"}
