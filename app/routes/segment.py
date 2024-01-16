def segment_routes(app):
    @app.get("/segment")
    def read_segment():
        return {"message": "hello Shakestory, from segment route"}
