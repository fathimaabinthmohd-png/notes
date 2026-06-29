# Flask Tutorial for Students

This tutorial guides you through creating a simple web application using Flask, a lightweight Python web framework.

## Learning Objectives

By the end of this tutorial, you will be able to:
- Set up a Flask development environment
- Create routes and view functions
- Use templates to render HTML
- Handle HTTP GET and POST requests
- Pass data from Python to templates
- Apply basic CSS styling

## Prerequisites

- Python 3.6+ installed
- Basic knowledge of HTML and Python
- Familiarity with command line/terminal

## Step 1: Set Up the Project

1. **Create a project directory** (already done for you):
   ```bash
   mkdir flask_student_tutorial
   cd flask_student_tutorial
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   This installs Flask.

## Step 2: Explore the Code

### app.py

The main application file. Key concepts:

- `Flask(__name__)` creates the application instance.
- `@app.route('/')` decorates a function to handle requests to the root URL.
- `render_template()` loads HTML files from the `templates` folder.
- `request` object accesses form data.
- `redirect()` and `url_for()` help with navigation.

### Templates

HTML files in the `templates` folder use **Jinja2** templating:
- `{{ variable }}` inserts Python variables.
- `{% %}` tags control logic (loops, conditionals).
- Example: `{% for note in notes %}` loops through a list.

### Static Files

CSS, JavaScript, and images go in the `static` folder.
Reference them with `url_for('static', filename='style.css')`.

## Step 3: Run the Application

1. Ensure your virtual environment is activated.
2. Run the app:
   ```bash
   python app.py
   ```
3. Open a web browser and visit `http://127.0.0.1:5000/`
4. Try adding notes and clearing them.

## Step 4: Experiment (Suggested Exercises)

1. **Modify the home page**: Change the welcome message in `index.html`.
2. **Add a new route**: Create `/about` that shows information about Flask.
3. **Implement note deletion**: Add a delete button next to each note.
4. **Use a database**: Replace the in-memory list with SQLite using Flask-SQLAlchemy.
5. **Style it differently**: Edit `style.css` to change colors or layout.

## Troubleshooting

- **Port already in use**: Stop other Flask apps or change the port in `app.run(port=5001)`.
- **Template not found**: Ensure HTML files are inside the `templates` folder.
- **Missing module**: Verify you activated the virtual environment and installed Flask.

## Further Reading

- Official Flask Documentation: https://flask.palletsprojects.com/
- Jinja2 Templating: https://jinja.palletsprojects.com/
- HTML Forms: https://developer.mozilla.org/en-US/docs/Learn/Forms

Happy coding!