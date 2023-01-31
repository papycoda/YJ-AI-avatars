import time
import requests
from IPython.core.getipython import get_ipython

# Define a function to execute a cell in a Jupyter notebook by index
def run_cell(nb, cell_index):
    # Construct the URL to access the notebook
    url = f"http://localhost:8888/api/contents/{nb}"
    headers = {"Content-Type": "application/json"}
    # Get the notebook content from the URL
    response = requests.get(url, headers=headers)
    nb = response.json()
    cells = nb["content"]["cells"]
    # Get the code cell by index
    code_cell = cells[cell_index]
    # Create the payload to execute the code cell
    payload = {"cell_index": cell_index, "code": code_cell["source"]}
    # Execute the code cell
    response = requests.post(f"{url}/cells/{cell_index}/execute", headers=headers, json=payload)
    # Return the response in JSON format
    return response.json()

# Define a function to execute cells in a Jupyter notebook
def run_notebook(nb_name, cells):
    # Loop through each cell index
    for i, cell in enumerate(cells):
        # Execute the cell and get the result
        result = run_cell(nb_name, i)
        # Check if the cell has outputs
        if "outputs" in result:
            # Print the outputs
            for output in result["outputs"]:
                print(output["text"])
        else:
            # If the cell doesn't have outputs, print the traceback
            print(result["traceback"])
        # Wait for 5 seconds between each cell execution
        time.sleep(5)

# Get the IPython instance
ipython = get_ipython()
# Load the TensorBoard extension
ipython.magic("%load_ext tensorboard")

# Define the names of the two notebooks
nb1 = "Notebook_1.ipynb"
nb2 = "Notebook_2.ipynb"

# Define the cell indices to execute in each notebook
cells1 = [0, 1, 2]
cells2 = [0, 1, 2]

# Run the first notebook
run_notebook(nb1, cells1)
# Run the second notebook
run_notebook(nb2, cells2)
