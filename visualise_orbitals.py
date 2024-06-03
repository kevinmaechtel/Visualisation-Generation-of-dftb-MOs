import subprocess
import sys
import os
import tempfile

def create_vmd_script(molecule_file,orbital_file, background_color, molecule_style, movie_maker):
    # Create a temporary VMD script file
    vmd_script = f"""\
    # Load molecule from XYZ format
    set molecule [mol new "{molecule_file}"]

    # Load MO data
    set MO [mol addfile "{orbital_file}"]

    # Display the molecule
    display resetview $molecule

    # Displaying positive MO
    mol color ColorID "0"
    mol representation isosurface "0.02, Isosurface, Solid Surface"
    mol addrep $MO

    # Displaying negative MO
    mol color ColorID "1"
    mol representation isosurface "-0.02, Isosurface, Solid Surface"
    mol addrep $MO

    # Display update
    display update
    """

    #Setting Background color
    if background_color == '1':
        vmd_script += f"""\
        color Display Background 8
        """
    elif background_color == '2' or background_color == '':
        vmd_script += f"""\
        color Display Background 16
        """

    #Setting Molecule Style
    if molecule_style == '1' or molecule_style == '':
        vmd_script += f"""\
        mol modstyle rep0 $molecule Lines
        """
    elif molecule_style == '2':
        vmd_script += f"""\
        mol modstyle rep0 $molecule CPK
        """
    elif molecule_style == '3':
        vmd_script += f"""\
        mol modstyle rep0 $molecule Licorice "0.2"
        """

    #Defining movie style
    if movie_maker in ('yes', 'y'):
        vmd_script += f"""\
        source /data/user4/Kevin/scripts/script_orbitals/rotation_animatied_gif.tcl
        make_rotation_animated_gif
        """

    #writing into temporary file
    script_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    script_file.write(vmd_script)
    
    script_file.close()

    return script_file.name

def user_choices():
    #setting Background color
    while True:
        print("------------------------------------------------------------------------")
        print("What color do you want the background to be?")
        print("For white enter 1.")
        print("For black enter 2 (Standard).")
        print("------------------------------------------------------------------------")
        background_color = input("Background color: ")
        if background_color == '1':
            print("You chose 1: white.")
            break
        elif background_color == '2' or background_color == '':
            print("You chose 2: black.")
            break
        else:
            print("Invalid choice.")
    
    #setting Style for Molecule Display
    while True:
        print("------------------------------------------------------------------------")
        print("What style do you want the molecule to be presented in?")
        print("For Lines enter 1 (Standard).")
        print("For CPK enter 2.")
        print('For Licorice enter 3.')
        print("------------------------------------------------------------------------")
        molecule_style = input("Molecule Style: ")
        if molecule_style == '1' or molecule_style == '':
            print("You chose 1: Lines.")
            break
        elif molecule_style == '2':
            print("You chose 2: CPK.")
            break
        elif molecule_style == '3':
            print("You chose 3: Licorice")
            break
        else:
            print("Invalid choice.")

    #setting movie generation to yes or no
    while True:
        print("------------------------------------------------------------------------")
        print("Do you want a movie of a 360° rotation around all three axes to be made?")
        print("The generation of a movie takes about two minutes.")
        print("Options yes/y, no/n; Standard: no")
        print("------------------------------------------------------------------------")
        movie_maker = input("Do you want to make a movie? ")
        if movie_maker in ('yes','y'):
            print("You chose yes: You want to make a movie.")
            print("The movies will be saved as rotation_x.gif, rotation_y.gif and rotaion_z.gif.")
            break
        elif movie_maker in ('no','n',''):
            print("You chose no: you don't want to make a movie.")
            break
        else:
            print("Invalid choice.")
            print("Exiting")

    return background_color, molecule_style, movie_maker

def launch_vmd_with_script(script_file):
    # Launch VMD with the specified script file
    vmd_process = subprocess.Popen(['vmd', '-e', script_file])
    return vmd_process

if __name__ == '__main__':

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