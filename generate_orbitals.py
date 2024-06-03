import sys
import subprocess
import shutil
import os
import fileinput
import tempfile

#Setting current working directory
current_directory = os.getcwd()
os.chdir(current_directory)
#Read molecule name from command-line argument

molecule_xyz = sys.argv[1]
print(current_directory)

#Checking for xyz file specified
condition_1 = os.path.isfile(molecule_xyz)
if condition_1 is not False:
    print(f"Found Coordinates file: {molecule_xyz}")
else:
    print(f"Specified Coordinates file {molecule_xyz} not found --> exiting.")
    exit()

def read_elements(molecule_xyz):
    elements=[]
    with open(molecule_xyz, 'r') as file:
        # Skip the first two lines
        next(file)
        next(file)
        
        # Process the rest of the lines
        for line in file:
            # Split the line by whitespace
            columns = line.split()
            
            # Find the first non-empty column
            first_col = None
            for col in columns:
                if col.strip():  # Check if the column is not empty
                    first_col = col
                    break

            # Add the entry to elements if it's not already in the list
            if first_col and first_col not in elements:
                elements.append(first_col)
    
    return elements


#looking for all different elements (H,C,O,N)
elements = read_elements(molecule_xyz)

#Defining file names
gen_file="geom.gen"

#Reading Orbital to be calculated
while True:
    #Number of Orbitals to be plotted
    print("----------------------------------------------------------------------------------------------------")
    print("How many Orbitals do you want to calculate?")
    print("----------------------------------------------------------------------------------------------------")

    #Get user input
    number_orbitals = int(input("Your choice: "))

    # Prompt the user for input
    print("----------------------------------------------------------------------------------------------------")
    print("Which Orbital(s) do you want to calculate (number)?")
    print("----------------------------------------------------------------------------------------------------")

    orbitals = []
    for i in range(0,number_orbitals):
        # Get user input
        orbitals.append(input(f"Orbital {i+1}: "))
    break

#Giving Status update
print("Starting DFTB+ Calculation for generation of eigenvectors.")

def run_dftb(molecule_xyz, elements):
    current_directory = os.getcwd()
    shutil.copyfile('/home/user4/Kevin/scripts/script_orbitals/dftb_in.hsd', f"{current_directory}/dftb_in.hsd")
    res=[]
    old_lines=['<<< "in.xyz"',"#      C = 'p'","#      H = 's'","#      N = 'p'","#      O = 'p'"]
    new_lines=['<<< "'+molecule_xyz+'"']
    #Checking for elements
    if 'C' in elements:
        new_lines.append("      C = 'p'")
    if 'H' in elements:
        new_lines.append("      H = 's'")
    if 'N' in elements:
        new_lines.append("      N = 'p'")
    if 'O' in elements:
        new_lines.append("      O = 'p'")

    #replacing lines
    with fileinput.input(f'{current_directory}/dftb_in.hsd', inplace=True) as file:
        for line in file:
            for old, new in zip(old_lines, new_lines):
                line=line.replace(old,new)
            res.append(line)
            print(line, end='')
    subprocess.run('/usr/local/bin/dftb+ dftb_in.hsd > dftb.out', shell=True)

run_dftb(molecule_xyz, elements)

#Status Update
print("DFTB+ Calculation has finished.")
print("Starting Calculation of the Orbital Cube files using waveplot.")

def input_waveplot(num_orbital):
    current_directory = os.getcwd()
    shutil.copyfile('/home/user4/Kevin/scripts/script_orbitals/waveplot_in.hsd', f"{current_directory}/waveplot_in.hsd")
    with fileinput.input(f'{current_directory}/waveplot_in.hsd', inplace=True) as file:
        for line in file:
            new_line = line.replace('  PlottedLevels = { 79 80 }                # Levels to plot', '  PlottedLevels = { '+num_orbital+' }                # Levels to plot')
            print(new_line, end='')
    subprocess.run('/usr/local/bin/waveplot waveplot_in.hsd > waveplot.out', shell=True)

for i in range(0,number_orbitals):
    #Running Waveplot
    input_waveplot(orbitals[i])

#Status update
print("Waveplot Calculation has finished.")

#deleting temporary files
removal_files =['dftb_pin.hsd','detailed.out','detailed.xml','eigenvec.bin','charges.bin','waveplot_pin.hsd', 'waveplot.out', 'dftb.out']
removed_files = []
for file in removal_files:
    if os.path.exists(file) == True:
        os.remove(file)
        removed_files.append(file)
    else:
        print(f"File {file} does not exist.")
print(f"Files: ", end="") 
for i in range(0,len(removed_files)):
    print(f"{removed_files[i]} ", end="")
print(" have been removed.")

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

print("")
print("")
print("How do you want the molecule to look?")
#Defining Visualisation Choices
background_color, molecule_style, movie_maker = user_choices()


for i in range(0,number_orbitals):
    #reading input files input
    orbital_file_path=f"wp-1-1-{orbitals[i]}-real.cube"

    #Checking for xyz file specified
    condition_1 = os.path.isfile(orbital_file_path)
    if condition_1 is not False:
        print(f"Found Cube file: {orbital_file_path}")
    else:
        print(f"Specified Cube file {orbital_file_path} not found --> exiting.")
        exit()

    #Status update
    print("")
    print("")
    print(f"Starting Visualistaion of Orbital {orbitals[i]} using VMD.")
    print("")
    print("")
    
    # Create VMD script
    vmd_script_file = create_vmd_script(molecule_xyz,orbital_file_path, background_color, molecule_style, movie_maker)

    # Launch VMD with the script
    vmd_process = launch_vmd_with_script(vmd_script_file)

    # Wait for VMD to finish
    vmd_process.wait()

    # Clean up: Remove temporary script file
    os.remove(vmd_script_file)
    if movie_maker in ('yes','y'):
        os.rename('rotation_x.gif',f'MO_{orbitals[i]}_rotation_x.gif')
        os.rename('rotation_y.gif',f'MO_{orbitals[i]}_rotation_y.gif')
        os.rename('rotation_z.gif',f'MO_{orbitals[i]}_rotation_z.gif')


#removing Snapshots from movie
if movie_maker in ('yes', 'y'):
    del_vec = ['0000','0001','0002','0003','0004','0005','0006','0007','0008','0009','0010','0011','0012','0013','0014','0015','0016','0017','0018','0019','0020','0021','0022','0023','0024','0025','0026','0027','0028','0029','0030','0031','0032','0033','0034','0035']
    for i in del_vec:
        os.remove(f'snap.{i}.rgb')
