# create_ns_project

Tool *create_ns_project* creates folder tree for new simulation project for NS-3 network simulator.
**Example:**
```
ipython ./create_ns_project.py -p my_project -o ~/workspace_ns3.45/ns-allinone-3.45/ns-3-external-contrib  -v 3.45 
```

**Options:**

usage: create_ns_project.py [-h] --project-name PROJECT_NAME [--output-path OUTPUT_PATH]
                            [--ns3-version NS3_VERSION] [--version]

Utility to create a standard directory structure for an NS-3 based project.

options:
  -h, --help            show this help message and exit
  --project-name PROJECT_NAME, -p PROJECT_NAME
                        The name for the new project (a directory with this name will be created).
  --output-path OUTPUT_PATH, -o OUTPUT_PATH
                        The directory where the project folder will be created. Defaults to the current
                        directory.
  --ns3-version NS3_VERSION, -v NS3_VERSION
                        The NS-3 version to use for the project directory (e.g., 3.46). Default is
                        "3.45".
  --version, -V         Show program's version number and exit.

Example usage: # Create project 'my-proj' with NS-3.45 in the '~/projects' directory python
create_ns3_project.py --project-name my-proj --output-path ~/projects --ns3-version 3.45 # Create project
'another-proj' with the default NS-3 version in the './work' directory python create_ns3_project.py -p
another-proj -o ./work # Show the utility version python create_ns3_project.py --version













