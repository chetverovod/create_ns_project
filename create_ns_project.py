#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse

__version__ = "0.1.0"

def generate_tree_string(project_name, ns3_dir_name):
    """Generates an ASCII representation of the project tree."""
    tree = f"""
{project_name}/
├── {ns3_dir_name}/
│   ├── contrib/
│   ├── src/
│   │   └── my-module-1/
│   └── scratch/
├── simulations/
├── results/
│   ├── scenario-1/
│   └── scenario-2/
├── analysis/
├── plots/
├── doc/
├── README.md
└── .gitignore
"""
    return tree.strip()

def create_project_structure(project_name, ns3_version, output_path):
    """
    Creates a standardized directory structure for an NS-3 based project
    in a specified output directory.
    """
    ns3_dir_template = 'ns-3.xx'
    ns3_dir_name = f'ns-{ns3_version}'
    
    # Construct the full path for the project
    project_full_path = os.path.abspath(os.path.join(output_path, project_name))

    print(f"Creating project structure for '{project_name}' with NS-3 version {ns3_version}...")
    print(f"Project will be located at: {project_full_path}")

    # --- 1. Define directory structure using a template ---
    dirs_to_create_template = [
        '',
        f'{ns3_dir_template}/src/my-module-1',
        f'{ns3_dir_template}/contrib',
        f'{ns3_dir_template}/scratch',
        'simulations',
        'results/scenario-1',
        'results/scenario-2',
        'analysis',
        'plots',
        'doc'
    ]
    
    # Replace the template with the actual version
    dirs_to_create = [d.replace(ns3_dir_template, ns3_dir_name) for d in dirs_to_create_template]

    # --- 2. Define content for files that will be created ---
    
    # Descriptions for about_folder.md files in each directory
    about_descriptions_template = {
        '': 'Root of the simulation project.',
        f'{ns3_dir_template}': f'Placeholder for NS-{ns3_version} simulator source code. Clone or link the NS-3 repository here.',
        f'{ns3_dir_template}/src': 'Directory for your custom NS-3 modules.',
        f'{ns3_dir_template}/contrib': 'Directory for your custom NS-3 modules.',
        f'{ns3_dir_template}/src/my-module-1': 'Directory for your custom NS-3 module 1.',
        f'{ns3_dir_template}/scratch': 'Directory for quick, single-file simulation tests (if using NS-3\'s scratch directory).',
        'simulations': 'C++ scripts for running your main simulation scenarios.',
        'results': 'Directory for storing raw simulation results (e.g., .pcap, .dat files).',
        'results/scenario-1': 'Results for the first simulation scenario.',
        'results/scenario-2': 'Results for the second simulation scenario.',
        'analysis': 'Python scripts for data processing, analysis, and plotting.',
        'plots': 'Final plots and figures for reports and publications.',
        'doc': 'Project documentation, notes, and descriptions.'
    }
    
    # Replace the template in keys with the actual version
    about_descriptions = {
        k.replace(ns3_dir_template, ns3_dir_name): v 
        for k, v in about_descriptions_template.items()
    }

    # Generate the tree representation for the README
    tree_representation = generate_tree_string(project_name, ns3_dir_name)

    file_contents = {
        'README.md': f"""# {project_name}

An NS-3 based simulation project.

## Project Structure

```{tree_representation}```

## Directory Descriptions

Each directory contains an `about_folder.md` file with a more specific description.
- `{ns3_dir_name}/`: Placeholder for NS-{ns3_version} simulator source code or link.
- `simulations/`: C++ scripts for running simulation scenarios.
- `results/`: Directory for storing raw simulation results.
- `analysis/`: Python scripts for data processing and plotting.
- `plots/`: Final plots and figures for reports and publications.
- `doc/`: Project documentation.

## Quick Start

1.  Place NS-{ns3_version} source code or link to it into the `{ns3_dir_name}/` directory.
2.  Configure and build NS-3. Consult the official NS-3 documentation for your specific version, as the build system may have changed (e.g., using CMake).
3.  Write your simulation scripts in the `simulations/` directory.
4.  Run your simulations from the `{ns3_dir_name}/` directory, pointing to scripts in `../simulations/`.
5.  Process the results using scripts in the `analysis/` directory.
""",
        '.gitignore': f"""# Ignore NS-{ns3_version} build artifacts
{ns3_dir_name}/build/
{ns3_dir_name}/.lock-waf_*
{ns3_dir_name}/c4che/
{ns3_dir_name}/.confcheck_*

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
    # after the about_folder.md file is created.
    empty_dirs_template = {
        f'{ns3_dir_template}/src/my-module-1',
        f'{ns3_dir_template}/contrib',
        f'{ns3_dir_template}/scratch'
    }
    empty_dirs = {d.replace(ns3_dir_template, ns3_dir_name) for d in empty_dirs_template}

    # --- 3. Create directories and files ---
    try:
        # Create the project's root directory at the specified path
        os.makedirs(project_full_path, exist_ok=False)
        
        # Create all subdirectories and their special files
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
        print("📖 Read README.md and about_folder.md files for more details.")

    except FileExistsError:
        print(f"❌ Error: A directory named '{project_full_path}' already exists.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def main():
    """Main function to parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Utility to create a standard directory structure for an NS-3 based project.',
        epilog=f"""Example usage:
  # Create project 'my-proj' with NS-3.45 in the '~/projects' directory
  python create_ns3_project.py --project-name my-proj --output-path ~/projects --ns3-version 3.45
  
  # Create project 'another-proj' with the default NS-3 version in the './work' directory
  python create_ns3_project.py -p another-proj -o ./work

  # Show the utility version
  python create_ns3_project.py --version
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
    
    parser.add_argument(
        '--ns3-version', '-v',
        type=str,
        default='3.45', # Changed default to a more realistic X.XX format
        help='The NS-3 version to use for the project directory (e.g., 3.46). Default is "3.45".'
    )

    # Добавляем аргумент для отображения версии
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

    create_project_structure(args.project_name, args.ns3_version, args.output_path)

if __name__ == '__main__':
    main()

