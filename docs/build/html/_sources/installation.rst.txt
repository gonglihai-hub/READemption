Installation
=============

Requirements
-------------
MODER was built using Python3.8, and based Linux system. There are two ways to install MODER easily, clone all source code to your linux system by git clone from github or install by pip from PyPi. If you choose to install MODER from source code, some Python package should be pre-installed. including ``cython``, ``numpy``, ``pystan``, ``pysam``, ``pandas``, ``plotnine`` and ``scipy``. If you don't want to install these packages by yourself, all of these packages will be installed if you choose to install MODER by pip. Except that, no matter which method you choose to install MODER, some bioinformatic software should be pre-installed, that's include ``samtools``, ``bedtools`` and ``bcftools``.


Dependency bioinfomatics software
-----------------------------------
1, install by apt
~~~~~~~~~~~~~~~~~~
with a Debian-based linux system, you can easily install all of dependency software by following command
::
        
        sudo apt install samtools
        sudo apt install bedtools
        sudo apt install bcftools

2, install by conda
~~~~~~~~~~~~~~~~~~~~
if you have installed anaconda or minconda, make you ``path_to_conda/bin`` has been add to ``PATH``, then these software can be installed by these command
::
        conda install samtools
        conda install bedtools
        conda install bcftools


3, by source code
~~~~~~~~~~~~~~~~~~~~
These software also can be install from their sorce code, we provide linkage to github package of these software, look up them for more information.

| ``samtools``: https://github.com/samtools/samtools
| ``bedtools``: https://github.com/arq5x/bedtools2
| ``bcftools``: https://github.com/samtools/bcftools


Installation from github
-------------------------
python package
~~~~~~~~~~~~~~~~
| These python package is must for using MODER to detect outliers

::        
        
        pip install cython numpy pystan pysam pandas plotnine scipy


download source code
~~~~~~~~~~~~~~~~~~~~~
download source code from github, then you can use MODER directly and don't need do anything else. But if you want to run MODER, you must know the path of MODER source code. Then you can run it with command **python /path/moder/moder.py -h** to get more information of how to use moder.
::

        git clone -b singleTissue https://github.com/Xu-Dong/mOutlierPipe.git


Installation with pip
----------------------
Installing MODER through pip is also very convenient, all you need to do is type the following command. But before you use MODER to detect outliers, please check wether all python package has been installed. according our test, pystan is hard to install. try to type **import pystan** in your python to make a check
::
        
        sudo pip install moder

