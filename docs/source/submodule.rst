submodule
==========

module1: Expression Data Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module is designed to analysis gene expression data. The basic command line arguments and descriptions as follows. More available parameters refer to `RNA-SeQC <http://bioinf.wehi.edu.au/subread-package/SubreadUsersGuide.pdf>`_ and `PEER <https://github.com/gonglihai-hub/mOutlierPipe/blob/singleTissue/doc/peer.md>`_ 

**command line arguments**

===============   ===============
args              description
===============   ===============
--expression      assign mode to analysis Gene Expression data
-i,--input        txt file with all input bam file path (required)
--gtf             genome annotation file in GTF format (required)
-o,--output       directory to store all resulting files<br><font color='red'>(optional and default output dir is current directory)</font>
-p,--parallel     parallel number <br><font color='red'>(optional and defalut value is 1)</font>
--threshold       threshold of z_score, used to filter results' value larger than threshold<br><font color='red'>(optional and default value is 2)</font>
===============   ===============

**running example**
::
        
        python mOutlierPipe.py --expression 
                --parallel 8 
	        --input file_path.txt
	        --gtf sample_annotation.gtf
	        --threshold 2


module2: Splicing Data Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is designed to analysis splicing data. The basic command line arguments and descriptions as follows. More available parameters refer to `leafcutter <https://github.com/gonglihai-hub/mOutlierPipe/blob/singleTissue/doc/leafcutter.md>`_, `SPOT <https://github.com/gonglihai-hub/mOutlierPipe/blob/singleTissue/doc/SPOT.md>`

**command line arguments**


===============   ===============
args              description
===============   ===============
--splicing        assign mode to analysis Splicing data
-i , --input      txt file with all input bam file path (required)
--gtf             genome annotation file in GTF format, used to translate cluster id to gene id (required)
-o , --output     directory to store all resulting files<br><font color='red'>(optional and default output dir is current directory)</font>
-p , --parallel   parallel number <br><font color='red'>(optional and default value is 1)<font>
--threshold       threshold of z_score, in splicing analysis pipeline, the value of z will be translated to p<br><font color='red'>(optional and default value is 0.0027)<font>
===============   ===============

 **running example**

::
        
        python mOutlierPipe.py --splicing 
                --parallel 8
	        --input file_path.txt
	        --gtf genome_annotation.gtf
	        --threshold 2



module3: Allele Specific Expression Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is designed to analysis allele specific expression data. The basic command line arguments and descriptions as follows. More available parameters refer to `phASER`

**command line arguments**


===============   ===============
args              description
===============   ===============
--ase             assign mode to analysis ASE data
-i , --input      txt file with all input bam file path (required)
--gtf             genome annotation file in GTF format, used to translate cluster id to gene id (required)
--vcf             Variant Call Format file, include variation information about the genome (required)
--variant         tissue-specific estimates of genetic variation in gene dosage (required)
-o , --output     directory to store all resulting files<br><font color='red'>(optional and default output dir is current directory)</font>
-p , --parallel   parallel number <br><font color='red'>(optional and default value is 1)<font>
--threshold       threshold of z_score, in ase analysis pipeline, the value of z will be translated to p<br><font color='red'>(optional and default value is 0.0027)<font>
===============   ===============

**running example**

::

        python mOutlierPipe.py --ase
	        --parallel 8
	        --input file_path.txt
	        --gtf genome_annotation.gtf
	        --vcf sample.vcf
	        --variant Vg_GTEx_v8.txt
	        --threshold 2
