# Ghidra_Ngrams_Extraction
Script used to develop ngram datasets from malware after they were exported through Ghidra 

Assembly instruction references are based off of ARM architecture. Instruction sets were primary taken and referenced from http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0204j/Cihedhif.html as all viruses compatible with a raspberry pi were ARM based.

File format for ghidra export needs to be virusname_ghidra to successfully be parsed and generate ngram datasets
Ran with Python 2.7

Usage: 

python ghidra_single_out.py /home/pi/Desktop/testing/a7cc7869eba384d53a54c5ad14776fb7818280eaddbe8a8872a2252c3af4e50a_ghidra

Report Outputs:

* ghidra assembly mnemonics one gram
* ghidra assembly mnemonics two gram
* ghidra assembly mnemonics three gram
* ghidra hexadecimal one gram
* ghidra hexadecimal two gram
* ghidra hexadecimal three gram
* ghidra ds dump (system calls)
* ghidra dump of mnemonics/opcodes
* ghidra dump of entire assembly opcodes and argument
