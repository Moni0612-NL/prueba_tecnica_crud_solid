from app import create_app

def create_app_wrapper():
    return create_app()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

