from app import create_app,db


# Create the app with default config or custom config
app = create_app()

@app.cli.command("check-db")
def check_db():
    try:
        # Execute a simple query to test the connection
        db.session.execute('SELECT 1')  # SQLite test query
        print("Database connection is successful!")
    except Exception as e:
        print(f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
