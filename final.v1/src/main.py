import os
from utils.constants import STUDENT_FILE
from views.cli_view import run_cli

if not os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, 'w') as f:
        f.write('[]')

if __name__ == "__main__":
    run_cli()

