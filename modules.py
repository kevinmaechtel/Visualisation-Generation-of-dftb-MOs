import os
import shutil
import subprocess
import fileinput
import tempfile
from typing import List, Tuple

def read_elements(molecule_xyz: str) -> List[str]:
    """Reads all different elements from a molecule coordinates file.

    Args:
        molecule_xyz (str): xyz file containing the molecule coordinates

    Returns:
        List[str]: List of all different elements in the molecule (every element is only listed once)
    """
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

def run_dftb(molecule_xyz: str, elements: List[str]) -> None:
    """Runs a DFTB+ calculation to generate the eigenvectors.

    Args:
        molecule_xyz (str): File containing the molecule coordinates in xyz format
        elements (List[str]): List of all different elements in the molecule
    
    Returns:
        None: Runs DFTB+ calculation and writes the output to dftb.out
    """

    current_directory = os.getcwd()
    # Generating the Input filr for DFTB+
    dftb_in = "Geometry = xyzFormat{\n"
    dftb_in += f'  <<< "{molecule_xyz}"\n'
    dftb_in += "}\n"
    dftb_in += """
Hamiltonian = DFTB {
    SCC = Yes
    SCCTolerance = 1.0e-5
    Charge = 0.0
    
    MaxSCCIterations = 500
    
    MaxAngularMomentum = {
"""
    if 'C' in elements:
        dftb_in += "          C = 'p'\n"
    if 'H' in elements:
        dftb_in += "          H = 's'\n"
    if 'N' in elements:
        dftb_in += "          N = 'p'\n"
    if 'O' in elements:
        dftb_in += "          O = 'p'\n"
    if 'S' in elements:
        dftb_in += "          S = 'p'\n"
    if 'Si' in elements:
        dftb_in += "          Si = 'd'\n"

    dftb_in += '''    }
    
    SlaterKosterFiles = Type2FileNames {
            Prefix = "/home/wxie/test-parameters/MIO/Compressed/"
            Separator = ""
            Suffix = "-c.spl"
            LowerCaseTypeName = Yes
            }
            
}

Options = {
    WriteDetailedXML = Yes
}

Analysis = {
    WriteEigenvectors = Yes
}'''

    #replacing lines
    with open(f"{current_directory}/dftb_in.hsd", 'w') as file:
        file.write(dftb_in)
        file.close()
    subprocess.run('/usr/local/bin/dftb+ dftb_in.hsd > dftb.out', shell=True)
    return

def input_waveplot(num_orbital: int) -> None:
    """Runs a Waveplot calculation to generate the orbital cube files.

    Args:
        num_orbital (int): Number of the orbital to be calculated

    Returns:
        None: Runs Waveplot calculation and writes the output to waveplot.out
    """
    current_directory = os.getcwd()

    # Generate the input file for Waveplot
    waveplot_in = '''#Genral Options

Options = {
    RealComponent = Yes                  # Plot real component of the wavefunction
  PlottedSpins = { -1 1 }
  PlottedLevels = {'''
    waveplot_in += f' {num_orbital} '
    waveplot_in += '''}                # Levels to plot
    PlottedRegion =  OptimalCuboid { }    # Region to plot
  NrOfPoints = { 80 80 80 }            # Number of grid points in each direction
  NrOfCachedGrids = -1                 # Nr of cached grids (speeds up things)
  Verbose = Yes                        # Wanna see a lot of messages?
}

DetailedXML = "detailed.xml"           # File containing the detailed xml output
                                       # of DFTB+
EigenvecBin = "eigenvec.bin"           # File cointaining the binary eigenvecs


# Definition of the basis
Basis =   {
 Resolution = 0.005
H = {
  AtomicNumber = 1
  Orbital = {
    AngularMomentum = 0
    Occupation = 1.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.000000000000000e+00   2.000000000000000e+00
    }
    Coefficients = {
       -2.276520915935000e+00   2.664106182380000e-01  -7.942749361803000e-03
        1.745369301500000e+01  -5.422967929262000e+00   9.637082466960000e-01
       -1.270143472317000e+01  -6.556866359468000e+00  -8.530648663672999e-01
    }
  }
}

C = {
  AtomicNumber = 6
  Orbital = {
    AngularMomentum = 0
    Occupation = 2.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.140000000000000e+00   2.620000000000000e+00
        6.000000000000000e+00
    }
    Coefficients = {
       -5.171232639696000e-01   6.773263954720000e-02  -2.225281827092000e-03
        1.308444510734000e+01  -5.212739736338000e+00   7.538242674175000e-01
       -1.215154761544000e+01  -9.329029568076001e+00  -2.006616061528000e-02
       -7.500610238649000e+00  -4.778512145112000e+00  -6.236333225369000e+00
    }
  }
  Orbital = {
    AngularMomentum = 1
    Occupation = 2.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.140000000000000e+00   2.620000000000000e+00
        6.000000000000000e+00
    }
    Coefficients = {
       -2.302004373076000e-02   2.865521221155000e-03  -8.868108742828000e-05
        3.228406687797000e-01  -1.994592260910000e-01   3.517324557778000e-02
        1.328563289838000e+01  -7.908233500176000e+00   6.945422441225000e+00
       -5.876689745586000e+00  -1.246833563825000e+01  -2.019487289358000e+01
    }
  }
}

N = {
  AtomicNumber = 7
  Orbital = {
    AngularMomentum = 0
    Occupation = 2.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.200000000000000e+00   2.900000000000000e+00
        7.000000000000000e+00
    }
    Coefficients = {
       -3.302567988643000e-01   4.628890986505000e-02  -1.617882644426000e-03
        8.365077199002000e+00  -3.760456728155000e+00   6.021328827950000e-01
       -5.179972901351000e+00  -6.849832710531000e+00   4.936659905968000e+00
       -1.176693800218000e+01  -1.378100804625000e+01  -1.905464854497000e+01
    }
  }
  Orbital = {
    AngularMomentum = 1
    Occupation = 3.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.200000000000000e+00   2.900000000000000e+00
        7.000000000000000e+00
    }
    Coefficients = {
       -7.512067638765000e-03   1.013394624100000e-03  -3.366860900721000e-05
       -2.488766679052000e-01   2.812182695080000e-02   6.919789784753000e-03
        1.805074634985000e+01  -1.053023147878000e+01   1.094617732220000e+01
       -5.960665506270000e+00  -1.692968016184000e+01  -3.489162811458000e+01
    }
  }
}

O = {
  AtomicNumber = 8
  Orbital = {
    AngularMomentum = 0
    Occupation = 2.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.260000000000000e+00   3.170000000000000e+00
        8.000000000000000e+00
    }
    Coefficients = {
       -2.300263542394000e-01   3.373238483322000e-02  -1.228102515314000e-03
        8.727954241408000e+00  -4.018881386000000e+00   6.211728416152000e-01
       -8.850444226866999e+00   1.213257127410000e+00  -1.933914291320000e+00
       -1.024719261284000e+01  -1.061297839371000e+01  -2.059822265426000e+01
    }
  }
  Orbital = {
    AngularMomentum = 1
    Occupation = 4.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.260000000000000e+00   3.170000000000000e+00
        8.000000000000000e+00
    }
    Coefficients = {
       -1.824842607631000e-02   2.454656104605000e-03  -8.140759910265999e-05
        1.310853832670000e+00  -5.877880459230000e-01   7.896698815037000e-02
        1.813778671956000e+01  -1.163569961247000e+01   1.000530135949000e+01
       -2.929548774143000e+00  -1.398199236449000e+01  -4.178366969313000e+01
    }
  }
}

S = {
  AtomicNumber = 16
  Orbital = {
    AngularMomentum = 0
    Occupation = 2.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.190000000000000e+00   2.830000000000000e+00
        6.730000000000000e+00   1.600000000000000e+01
    }
    Coefficients = {
       -1.250714643528000e-01   1.569960958977000e-02  -4.922860544878000e-04
        1.514082520313000e+01  -5.187075928731000e+00   5.339980252229000e-01
       -3.752313136927000e+01   7.651296914361000e+00  -1.377409848847000e+01
        3.595323418915000e+01  -3.087980561984000e+01   1.138078668898000e+02
       -2.138793772996000e+00  -3.344748112398000e+01  -7.385789882169000e+01
    }
  }
  Orbital = {
    AngularMomentum = 1
    Occupation = 4.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.190000000000000e+00   2.830000000000000e+00
        6.730000000000000e+00   1.600000000000000e+01
    }
    Coefficients = {
       -4.322268443574000e-02   5.274668380760000e-03  -1.600345098760000e-04
        6.072629691998000e+00  -2.068514313570000e+00   2.083757645683000e-01
       -1.361349308773000e+01   7.457121019079000e+00  -5.016769432106000e+00
       -2.689742375494000e+01   1.581488122902000e+01   5.510050851407000e+00
       -5.962945794916000e+00  -7.718853770100000e+00   5.283308701910000e+01
    }
  }
  Orbital = {
    AngularMomentum = 2
    Occupation = 0.000000
    Cutoff = 5.0
    Exponents = {
        5.000000000000000e-01   1.190000000000000e+00   2.830000000000000e+00
        6.730000000000000e+00   1.600000000000000e+01
    }
    Coefficients = {
       -6.612660556195000e-03   7.323736267852001e-04  -2.008751787738000e-05
        2.903129220115000e+00  -8.479140042084000e-01   6.879445333019001e-02
       -1.052897769092000e+01   1.197299778271000e+01  -6.954424955674000e+00
        2.894491644082000e+01  -1.492260098233000e+01   1.033305812242000e+02
       -1.266694735825000e+01  -5.060185551926000e+01  -2.670483778124000e+02
    }
  }
}

P = {
  AtomicNumber = 15
  Orbital = {
    AngularMomentum = 0
    Occupation = 2.000000
    Cutoff = 6.0
    Exponents = {
      0.50 1.19 2.83 6.73 15.0
    }
    Coefficients = {
      -2.406283825929e-03  -1.678807121513e-03   1.200469179096e-04
       1.634883493972e+01  -5.088235592779e+00   4.158227830243e-01
      -3.007051694760e+01  -6.543659186768e+00  -1.501085195192e+01
       2.572522507581e+01  -3.326508829000e+01   5.605394257763e+01
      -1.998853853101e+00  -2.801503757753e+01  -5.602736660470e+01
    }
  }
  Orbital = {
    AngularMomentum = 1
    Occupation = 3.000000
    Cutoff = 6.0
    Exponents = {
      0.50 1.19 2.83 6.73 15.0
    }
    Coefficients = {
      -4.444209399217e-02   5.351996859789e-03  -1.602711067828e-04
       7.543608527860e+00  -2.500355838853e+00   2.418682305964e-01
      -1.984166384030e+01   8.180587473256e+00  -8.106065195406e+00
      -2.145014490645e+00  -2.905062507994e+01   7.819611813468e+01
      -1.916826066072e+01  -6.969959061208e+01  -1.436825465361e+02
    }
  }
  Orbital = {
    AngularMomentum = 2
    Occupation = 0.000000
    Cutoff = 6.0
    Exponents = {
      0.50 1.19 2.83 6.73 15.0
    }
    Coefficients = {
      -6.703577128028e-03   7.385474787442e-04  -2.015243797942e-05
       3.167621590163e+00  -9.163337185478e-01   7.339158418475e-02
      -1.621796888450e+01   1.626287607966e+01  -8.671695721803e+00
       5.555017428375e+01  -7.531838877483e+01   1.944924637046e+02
      -3.694092368331e+01  -1.511628833320e+02  -5.495374759459e+02
    }
  }
}

F {
  AtomicNumber = 9
  Orbital {
    AngularMomentum = 0
    Occupation = 2.000000000000000E+000
    Cutoff = 6.00
    Exponents {
    5.000000000000000E-001 1.030000000000000E+000 2.120000000000000E+000 4.370000000000000E+000 9.000000000000000E+000
    }
    Coefficients {
    -3.091247713505259E-001 3.469836991741562E-002 -9.880147036005432E-004
    9.363780142977594E+000 -2.786863698217137E+000 3.064675708706853E-001
    -4.368672492890823E+001 1.380543913727014E+001 -8.788555804207959E+000
    6.072454560154594E+001 -1.610059091018885E+001 6.689176291155650E+001
    -1.367745898259258E+001 -4.821248389953696E+001 -3.728787453266563E+001
    }
  }
  Orbital {
    AngularMomentum = 1
    Occupation = 5.000000000000000E+000
    Cutoff = 6.00
    Exponents {
    5.000000000000000E-001 1.030000000000000E+000 2.120000000000000E+000 4.370000000000000E+000 9.000000000000000E+000
    }
    Coefficients {
    2.572862213506755E-003 -3.031942117078430E-004 8.866761168203333E-006
    2.432622615262761E-001 -4.682978556659022E-002 1.428610706954104E-003
    -7.965599858951141E+000 9.385034645920030E+000 -2.077842855927055E+000
    4.848143576189935E+001 -2.142241980711530E+001 4.365481749554218E+001
    -1.864601574844123E+001 -5.562698695114018E+001 -9.322568503537332E+001
    }
  }
}

Cl {
  AtomicNumber = 17
  Orbital {
    AngularMomentum = 0
    Occupation = 2.000000000000000E+000
    Cutoff = 6.00
    Exponents {
    5.000000000000000E-001 1.210000000000000E+000 2.920000000000000E+000 7.040000000000000E+000 1.700000000000000E+001
    }
    Coefficients {
    -2.625047151651286E-002 2.724096153188547E-003 -6.938641148770734E-005
    1.660305941097010E+001 -5.240864833135435E+000 4.361753640589678E-001
    -9.090639711276134E+001 8.211352934332446E+001 -5.112009700471025E+001
    1.093633138306482E+002 -1.589369348562520E+000 4.618006787930927E+002
    -2.286046272625614E+001 -1.454369557581990E+002 -3.459258194764265E+002
    }
  }
  Orbital {
    AngularMomentum = 1
    Occupation = 5.000000000000000E+000
    Cutoff = 6.00
    Exponents {
    5.000000000000000E-001 1.210000000000000E+000 2.920000000000000E+000 7.040000000000000E+000 1.700000000000000E+001
    }
    Coefficients {
    6.989034503461015E-003 -6.879699614259214E-004 1.656956721224828E-005
    -6.713037529623749E+000 2.054043990088945E+000 -1.626502867769332E-001
    1.948399623241347E+001 -2.057817206076270E+001 1.545785692634875E+001
    4.467129188223081E+001 -9.944516808068479E+001 6.781483093541429E+001
    -1.310919616997139E+001 -9.480643297171522E+001 -5.597031285395628E+002
    }
  }
}

Br {
  AtomicNumber = 35
  Orbital {
    AngularMomentum = 0
    Occupation = 2.000000000000000E+000
    Cutoff = 6.00
    Exponents {
    3.500000000000000E+001 1.210022746246794E+001 4.183300132670378E+000 1.446253804259539E+000 5.000000000000000E-001
    }
    Coefficients {
    3.105303444785479E+001 2.570111380583361E+002 2.844309778968854E+003
    -2.858074491606314E+001 -1.861287611223188E+002 -4.034757698914281E+002
    2.145511346159876E+001 1.311740175347266E+001 1.758903450136605E+001
    -5.384732247652027E+000 -8.085460760594457E-001 1.005997212073494E-002
    6.191710174978510E-002 -9.394877560439783E-003 3.399981386124437E-004
    }
  }
  Orbital {
    AngularMomentum = 1
    Occupation = 5.000000000000000E+000
    Cutoff = 6.00
    Exponents {
    3.500000000000000E+001 1.210022746246794E+001 4.183300132670378E+000 1.446253804259539E+000 5.000000000000000E-001
    }
    Coefficients {
    7.881553423131739E+001 4.023533814144205E+002 9.641621419010851E+003
    8.340281352084027E+001 1.154450987978768E+001 -6.915400815893352E+002
    -1.403100458894255E+001 -1.175951149515016E+001 1.814971470113711E+001
    1.393892911723274E+000 1.071102578102040E+000 -9.102407088162173E-002
    -1.304403344542948E-002 1.790267087140626E-003 -5.845139908158330E-005
    }
  }
}

I {
  AtomicNumber = 53
  Orbital {
    AngularMomentum = 0
    Occupation = 2.000000000000000E+000
    Cutoff = 6.00
    Exponents {
    5.300000000000000E+001 1.651769350533408E+001 5.147815070493500E+000 1.604340218048139E+000 5.000000000000000E-001
    }
    Coefficients {
    5.110698086257967E+001 6.024748061241903E+002 1.394508300607809E+004
    -7.983272562377573E+001 -4.281882853278961E+002 -1.430127957829505E+003
    6.032930283227850E+001 -1.166373651684578E+002 2.102249702081233E+001
    -7.868497818635478E+000 1.126743791948310E+001 -1.242178953935215E+000
    2.002732783268818E-002 -4.267671051305455E-003 2.173932444155924E-004
    }
  }
  Orbital {
    AngularMomentum = 1
    Occupation = 5.000000000000000E+000
    Cutoff = 6.00
    Exponents {
    5.300000000000000E+001 1.651769350533408E+001 5.147815070493500E+000 1.604340218048139E+000 5.000000000000000E-001
    }
    Coefficients {
    1.817286089921099E+002 4.534167420198830E+002 5.740074407047359E+004
    1.828391301294797E+002 -5.563616652478928E+002 -1.987531573021972E+003
    -4.610383609497270E+001 1.568667505225703E+002 -5.863733356417897E+001
    1.858359479217722E+000 -4.041624630291535E+000 3.671762955082002E-001
    -1.190867577953982E-003 3.770326094239628E-004 -2.184763161964902E-005
    }
  }
}

  <<+ "dftb_in.hsd"  
}
'''
    with open(f"{current_directory}/waveplot_in.hsd", 'w') as file:
        file.write(waveplot_in)
        file.close()
    subprocess.run('/usr/local/bin/waveplot waveplot_in.hsd > waveplot.out', shell=True)
    return

def create_vmd_script(molecule_file: str,orbital_file: str, background_color: int, molecule_style: int, movie_maker: int) -> str:
    """Creates a VMD script file to visualize the molecule and the orbitals.

    Args:
        molecule_file (str): File containing the molecule coordinates in xyz format
        orbital_file (str): File containing the orbital data
        background_color (int): Background color for the VMD visualization (1: white, 2: black)
        molecule_style (int): Style for the molecule visualization (1: Lines, 2: CPK, 3: Licorice)
        movie_maker (int): Whether a movie should be generated (1: yes, 2: no)
    
    Returns:
        str: Name of the temporary VMD script file
    """
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
        source /data/user9/kevin/scripts/script_orbitals/rotation_animatied_gif.tcl
        make_rotation_animated_gif
        """
            
    #writing into temporary file
    script_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    script_file.write(vmd_script)
    
    script_file.close()

    return script_file.name

def user_choices() -> Tuple[int,int,str]:
    """Prompts the user for choices regarding the visualization.

    Returns:
        Tuple[int,int,str]: Background color (1:white, 2: black), molecule style (1: Lines, 2: Licorice, 3: CPK), and movie maker (yes, no) choices
    """
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

def launch_vmd_with_script(script_file: str) -> subprocess.Popen:
    """Launches VMD with the specified script file.

    Args:
        script_file (str): Name of the VMD script file

    Returns:
        subprocess.Popen: Process object for the VMD process
    """
    # Launch VMD with the specified script file
    vmd_process = subprocess.Popen(['vmd', '-e', script_file])
    return vmd_process
