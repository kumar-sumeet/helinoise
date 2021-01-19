# Installation
Follow these steps (tested on Ubuntu 16.04 lts):


## Prerequisites
Detailed instructions to install [SONATA](https://gitlab.lrz.de/HTMWTUM/SONATA) are available [here](https://gitlab.lrz.de/HTMWTUM/SONATA/-/blob/master/docs/installation.md). Correct installation of SONATA is absolutely essential. 

To check if everything has installed correctly, run `Master_acoustics.py`. If pytecplot is installed within the conda environment, corresponding `*.plt` files can also be generated to view the surface geometry in [TecPlot](https://www.tecplot.com/).  

For users at the Institute of Helicopter Technology, [SONATA-relevant libraries](https://gitlab.lrz.de/HTMWTUM/SONATA/-/blob/master/docs/installation.md) are already loaded and available in a separate conda environment called 'sonata'. Additionally, [pytecplot](https://www.tecplot.com/docs/pytecplot/) is needed if `*.plt`files generation capability is required for verifying the generated blade geometry.  
     
### Linux @ HT
    ```c
    $ module purge
    $ module load TecPlot/2019R1 anaconda/3.7
    $ source activate sonata
    $ spyder
    ```
Note: Spyder IDE is not essential to execution of the scripts. 
Once Spyder IDE is launched, `Master_acoustics.py` can be executed and should run based on CII sample data stored within pickle file `sample_CII_output_data_dict.p`. Alternately, you can provide paths to the CII output file as well. 

