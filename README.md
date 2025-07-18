Use ̀ visualise_orbitals.py` for visualisation, when cube file already exists.
Use `generate_orbitals.py` for calculation of cube file and later visualization.
Copy visualize_orbitals.py or generate_orbitals.py to the directory with your calculation of the orbitals.
File Formats: <molecule_file>: all formats, accepted by VMD for molecule coordinates; <orbitals_file>: should always be cube (generated by `waveplot/cubegen`)
Execute the scripts with:
```bash
    python3 visualise_orbitals.py <molecule_file> <orbitals_file>
```
```bash
    python3 generate_orbitale.py <molecule_file>                      # Has to be xyz file in this case
```
You will be asked for your choices:
    Total Number of Orbitals to be calculated,
    Numbers of the Orbitals, which are to be calculated and
    Visualization (Background and Molecule Drawing Style) and potential generation of a Movie of the rotation.
