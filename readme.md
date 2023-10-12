## note* ##
# 1.first install python 
# 2. type in cmd: "pip install -r requirements.txt"
# 3. type in cmd: "python dijkstra.py" to start program

To run a Python project on macOS, you can follow these steps:

1. **Install Python**: macOS typically comes with Python pre-installed. You can check the installed version by opening the Terminal and running `python --version` or `python3 --version`. If it's not installed or you want to use a different version, consider installing it from the official Python website or using a package manager like Homebrew.

   - Official Python website: https://www.python.org/downloads/
   - Homebrew (if not installed): https://brew.sh/

2. **Create a Project Directory**: Organize your Python project in a directory. You can create one using the Terminal:

   ```bash
   mkdir MyPythonProject
   cd MyPythonProject
   ```

3. **Set up Virtual Environment (Optional but Recommended)**: It's a good practice to create a virtual environment for your project to isolate dependencies. To create and activate a virtual environment, run:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. **Write Your Python Code**: Create a Python script or a Python file (e.g., `main.py`) and write your Python code in it.

5. **Install Dependencies (if any)**: If your project relies on external libraries or packages, you can install them using `pip`. For example:

   ```bash
   pip install networkx matplotlib
   ```

6. **Run Your Python Script**: Navigate to the project directory where your Python file is located and run it using Python. For example:

   ```bash
   python main.py
   ```

7. **View the Output**: Your Python script should run, and any output or graphical window (if applicable) will be displayed on the screen.

8. **Exit the Virtual Environment (if used)**: When you're done with your project, you can exit the virtual environment by running:

   ```bash
   deactivate
   ```

Remember to replace `main.py` with the actual name of your Python script or file, and adjust the instructions as needed based on your project's requirements.