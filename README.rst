PDB
===
| This is a bioinformatics implementation of the method outlined in the paper *Resolving the Ambiguity: Making Sense of Intrinsic Disorder when PDB Files Disagree* (submitted). The purpose of this method is to classify missing regions in PDB files by the pattern of disorder among multiple missing regions. If you find this method useful, please cite the corresponding paper.
`Methods and Objectives <https://github.com/shellydeforte/PDB/blob/master/methods.rst>`__



Python version support
==============
Python 2.7, 3.4 and higher


Dependencies
==============

**Required**

-  `Biopython <http://biopython.org/wiki/Main_Page>`__
-  `matplotlib <http://matplotlib.org/>`__
-  `NumPy <http://www.numpy.org/>`__
-  `pandas <http://pandas.pydata.org/>`__
-  `pytz <http://pytz.sourceforge.net>`__
-  `PyYAML <http://pyyaml.org/>`__
-  `requests <docs.python-requests.org/en/latest/>`__

**Recommended**

-  `coverage <https://pypi.python.org/pypi/coverage/>`__



Installation with Anaconda
==============
-  `Begin by cloning the git repository. <https://help.github.com/articles/cloning-a-repository/>`__
-  If desired, create a virtual environment. (This is the easiest and cleanest way to satisfy dependencies.)
-  Update the PATH variable on your system.
-  Finally, run *driver_parse.py* to begin data download and analysis.


Create Virtual Environment
-----------------
Create a virtual environment with `Anaconda <https://www.continuum.io/downloads>`__   using the `conda <http://conda.pydata.org/docs/>`__ package manager::

    conda create --name pdb_34 python=3.4.3 biopython requests pyyaml pytz pandas coverage

If using an IDE, remember to update your settings to use the new virtual environment. Otherwise, on Windows activate the environment with the command::

    conda activate pdb_34

On linux, activate the environment with the command::

    source activate pdb_34

Update PATH Variable
-----------------
Update your system path variable with the location of the PDB and lib directories as shown below.


**Windows**

- Non-persistent PATH update (disappears on reboot)::

    SET PATH="%path%;C:\\YourInstallationPath\\PDB";C:\\YourPath\\PDB\\pdb\\lib"

- Persistent PATH update (Stackoverflow): http://stackoverflow.com/a/28545224/3182836



**Linux/OSX (POSIX)**

- Non-persistent PATH update (disappears on reboot)::

    export PATH=$PATH:/YourInstallationPath/PDB:/YourInstallationPath/PDB/pdb/lib'

- Persistent PATH update (Stackoverflow): Add the export PATH command to ~/.profile



Analysis
==============
*driver_parse.py* is the analysis orchestrator and the entry point into the application. driver_parse does not currently accept any command-line arguments, therefore, to begin analysis run driver_parse as follows::

    python driver_parse.py

Logging options may be configured in *logging_config.yaml*.

The following logs are written to the user home directory:

-  pdb.log: General application message.
- uni_download_errors.log: Errors encountered when downloading FASTA files.
- missing_uniprots.log: Any missing UniProt IDs due to download errors.

The application will use existing data files when present. Therefore, on subsequent runs, remove any data files that you would like to have re-downloaded.

Note that if errors are encountered, or processing is interrupted, *driver_parse.py* may be re-run and will resume at the furthest possible point. If errors are encountered during one of these follow-up runs, the applicaiton may be trying to use zero-byte data left over from the previous run. Therefore remmove that file before continuing. Once removed, the application will re-download the file and resume processing. This will be handled automatically in a future release.
