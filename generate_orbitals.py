import sys
import subprocess
import shutil
import os
import fileinput

from modules import read_elements, run_dftb, create_vmd_script, user_choices, launch_vmd_with_script, input_waveplot

# Check, if enough elements are present
if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} CoordinatesFile")
    exit()

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

run_dftb(molecule_xyz, elements)

#Status Update
print("DFTB+ Calculation has finished.")
print("Starting Calculation of the Orbital Cube files using waveplot.")

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
    del_vec = ['0000','0001','0002','0003','0004','0005','0006','0007','0008',
               '0009','0010','0011','0012','0013','0014','0015','0016','0017',
               '0018','0019','0020','0021','0022','0023','0024','0025','0026',
               '0027','0028','0029','0030','0031','0032','0033','0034','0035']
    for i in del_vec:
        os.remove(f'snap.{i}.rgb')
