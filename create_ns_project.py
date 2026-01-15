#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse

__version__ = "0.3.0" # Updated version

def generate_tree_string(project_name):
    """
    Generates an ASCII representation of the project tree.
    The tree is now independent of the NS-3 version and has empty contrib/src folders.
    """
    tree = f"""
{project_name}/
├── contrib/
├── src/
├── simulations/
├── results/
├── analysis/
├── plots/
├── doc/
├── README.md
└── .gitignore
"""
    return tree.strip()

def create_project_structure(project_name, output_path):
    """
    Creates a standardized directory structure for an NS-3 based project.
    The structure is designed to have its `src` and `contrib` folders copied
    into an existing NS-3 source tree.
    """
    # --- 1. Define directory structure ---
    # contrib and src are created empty, as requested.
    dirs_to_create = [
        '',
        'contrib',
        'src',
        'simulations',
        'results',
        'analysis',
        'plots',
        'doc'
    ]
    
    # --- 2. Define content for files ---
    
    # Descriptions for about_folder.md files in each directory
    about_descriptions = {
        '': 'Root of the simulation project.',
        'contrib': 'Directory for your modules intended for the `contrib` folder of your NS-3 distribution.',
        'src': 'Directory for your modules intended for the `src` folder of your NS-3 distribution.',
        'simulations': 'C++ scripts for running your main simulation scenarios.',
        'results': 'Directory for storing raw simulation results (e.g., .pcap, .dat files).',
        'analysis': 'Python scripts for data processing, analysis, and plotting.',
        'plots': 'Final plots and figures for reports and publications.',
        'doc': 'Project documentation, notes, and descriptions.'
    }

    # Generate the tree representation for the README
    tree_representation = generate_tree_string(project_name)

    file_contents = {
        'README.md': f"""# {project_name}

An NS-3 based simulation project.

## Project Structure

```{tree_representation}```

## Integration with NS-3

This project does not contain the NS-3 source code. It provides a structure for your custom modules.

1.  Develop your modules inside the `src/` and `contrib/` directories.
2.  Copy the contents of the `src/` and `contrib/` directories from this project into the corresponding directories of your NS-3 distribution.
3.  Reconfigure and build NS-3.
4.  Run simulations from the `ns-3/` directory using the scripts from the `simulations/` folder.

## Directory Descriptions

- `contrib/`: Modules best placed in the `contrib` folder of NS-3.
- `src/`: Modules best placed in the `src` folder of NS-3.
- `simulations/`: Scripts for running simulation scenarios.
- `results/`: Directory for storing raw simulation data.
- `analysis/`: Scripts for data analysis.
- `plots/`: Directory for final plots.
- `doc/`: Project documentation.
""",
        '.gitignore': f"""# Ignore simulation results
results/
*.pcap
*.dat
*.tr

# Ignore temporary files and OS files
*~
.DS_Store
Thumbs.db

# Ignore Python bytecode
__pycache__/
*.pyc

# Ignore gitkeep files (they are for git, not for tracking)
.gitkeep
**/.gitkeep
"""
    }
    
    # Define directories that should remain empty (and thus need a .gitkeep)
    # contrib and src are now intentionally empty.
    empty_dirs = {
        'contrib',
        'src',
    }

    # --- 3. Create directories and files ---
    try:
        project_full_path = os.path.abspath(os.path.join(output_path, project_name))
        os.makedirs(project_full_path, exist_ok=False)
        
        for dir_path in dirs_to_create:
            full_dir_path = os.path.join(project_full_path, dir_path)
            
            # Create the directory
            os.makedirs(full_dir_path, exist_ok=True)
            
            # Create about_folder.md file with the appropriate description
            description = about_descriptions.get(dir_path, "A project directory.")
            with open(os.path.join(full_dir_path, 'about_folder.md'), 'w', encoding='utf-8') as f:
                f.write(f"# {os.path.basename(full_dir_path) if dir_path else project_name}\n\n{description}\n")

            # Create .gitkeep file only if the directory is intended to be empty
            if dir_path in empty_dirs:
                with open(os.path.join(full_dir_path, '.gitkeep'), 'w') as f:
                    pass # Creates an empty file

        # Create top-level README.md and .gitignore files
        with open(os.path.join(project_full_path, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(file_contents['README.md'])
        
        with open(os.path.join(project_full_path, '.gitignore'), 'w', encoding='utf-8') as f:
            f.write(file_contents['.gitignore'])

        print(f"\n✅ Project '{project_name}' created successfully!")
        print(f"📁 Navigate to the directory: cd {project_full_path}")
        print("📖 Read README.md for instructions on integrating with NS-3.")

    except FileExistsError:
        print(f"❌ Error: A directory named '{project_full_path}' already exists.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def main():
    """Main function to parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Utility to create a standard directory structure for an NS-3 based project.',
        epilog=f"""Example usage:
  # Create project 'my-proj' in the '~/projects' directory
  python create_ns_project.py --project-name my-proj --output-path ~/projects
  
  # Create project 'another-proj' in the current directory
  python create_ns_project.py -p another-proj -o .
"""
    )
    
    parser.add_argument(
        '--project-name', '-p',
        type=str,
        required=True,
        help='The name for the new project (a directory with this name will be created).'
    )
    
    parser.add_argument(
        '--output-path', '-o',
        type=str,
        default='.',
        help='The directory where the project folder will be created. Defaults to the current directory.'
    )
    
    # Add argument to display version
    parser.add_argument(
        '--version', '-V',
        action='version',
        version=f'%(prog)s {__version__}',
        help='Show program\'s version number and exit.'
    )
    
    args = parser.parse_args()
    
    # Validate the output path
    if not os.path.isdir(args.output_path):
        print(f"❌ Error: The specified output path '{os.path.abspath(args.output_path)}' is not a valid directory.")
        return

    create_project_structure(args.project_name, args.output_path)

if __name__ == '__main__':
    main()
