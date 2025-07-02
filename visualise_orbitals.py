import sys
import os

from modules import create_vmd_script, user_choices, launch_vmd_with_script

if __name__ == '__main__':

    # Check, if enough elements are present
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} CoordinatesFile CubeFile")
        exit()

    #reading input files input
    molecule_file_path=sys.argv[1]
    orbital_file_path=sys.argv[2]

    #Checking for files specified in orbitals.inp
    condition_1 = os.path.isfile(molecule_file_path)
    if condition_1 is not False:
        print(f"Found Coordinates file: {molecule_file_path}")
    else:
        print(f"Specified Coordinates file {molecule_file_path} not found --> exiting.")
        exit()
    condition_2 = os.path.isfile(orbital_file_path)
    if condition_2 is not False:
        print(f"Found Orbital file: {orbital_file_path}")
    else:
        print(f"Specified Orbital file {orbital_file_path} not found --> exiting.")
        exit()

    #user choices
    background_color, molecule_style, movie_maker = user_choices()
    
    # Create VMD script
    vmd_script_file = create_vmd_script(molecule_file_path,orbital_file_path, background_color, molecule_style, movie_maker)

    print("------------------------------------------------------------------------")
    print("Launching VMD and loading Data into VMD.")
    print("------------------------------------------------------------------------")

    # Launch VMD with the script
    vmd_process = launch_vmd_with_script(vmd_script_file)

    # Wait for VMD to finish
    vmd_process.wait()

    # Clean up: Remove temporary script file
    os.remove(vmd_script_file)

    #removing Snapshots from movie
    if movie_maker in ('yes', 'y'):
        del_vec = ['0000','0001','0002','0003','0004','0005','0006','0007','0008','0009','0010','0011','0012','0013','0014','0015','0016','0017','0018','0019','0020','0021','0022','0023','0024','0025','0026','0027','0028','0029','0030','0031','0032','0033','0034','0035']
        for i in del_vec:
            os.remove(f'snap.{i}.rgb')