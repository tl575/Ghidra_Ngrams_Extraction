import os
import sys
import string
#example python ghidra_single_out.py /home/pi/Desktop/testing/a7cc7869eba384d53a54c5ad14776fb7818280eaddbe8a8872a2252c3af4e50a_ghidra

def is_hex(s):
    hex_digits = set(string.hexdigits)
    return all(c in hex_digits for c in s)

def insert_dictionary(s, grams):
    if s not in grams:
        grams[s] = 1
    else:
        grams[s] += 1

def one_gram_write(grams, path_name, name):
    f = open( path_name + name, "w+")
    for key, value in grams.items():
        f.write(key + "," + str(value) + "\n")
    f.close()

def two_gram_write(grams, path_name, name):
    f = open(path_name + name, "w+")
    for key, value in grams.items():
        f.write(key[0] + "," + key[1] + "," + str(value) + "\n")
    f.close()

def three_gram(ghidra_file, path_name, assembly_names, system_call_names):
    one_grams = {}
    two_grams = {}
    three_grams = {}
    assembly_instances_1 = {}
    assembly_instances_2 = {}
    assembly_instances_3 = {}
    hex_name = ""
    current = None
    prev_1 = None
    prev_2 = None
    prev1_name = None
    prev2_name = None
    cur_name = None
    with open(ghidra_file) as f:
        for line in f:
            line = line.strip()
            line = line.split()
            if len(line) > 1:
                if is_hex(line[1]) and line[1] != "db":
                    #print line
                    for name in assembly_names:
                        if name in line:
                            prev2_name = prev1_name
                            prev1_name = cur_name
                            cur_name = name
                            if name == "call":
                                for sys_call in system_call_names:
                                    if sys_call in line:
                                        cur_name = name + "-" + sys_call
                            insert_dictionary(cur_name, assembly_instances_1)
                            if prev1_name != None and cur_name != None:
                                assembly_two_gram = (prev1_name, cur_name)
                                insert_dictionary(assembly_two_gram, assembly_instances_2)
                            if prev1_name != None and prev2_name != None and cur_name != None:
                                assembly_three_gram = (prev2_name, prev1_name, cur_name)
                                insert_dictionary(assembly_three_gram, assembly_instances_3)
                    prev_2 = prev_1
                    prev_1 = current
                    hex_name = line[1]
                    hex_name = hex_name.strip()
                    current = hex_name
                    insert_dictionary(hex_name, one_grams)
                    if prev_1 != None and current != None:
                        two_gram = (prev_1, current)
                        insert_dictionary(two_gram, two_grams)
                    if prev_1 != None and prev_2 != None and current != None:
                        three_gram = (prev_2, prev_1, current)
                        insert_dictionary(three_gram, three_grams)

        #print grams
        #print assembly_instances
        one_gram_write(one_grams, path_name, "ghidra_hex_one_gram")
        two_gram_write(two_grams, path_name, "ghidra_hex_two_gram")
        three_gram_write(three_grams, path_name, "ghidra_hex_three_gram")
        one_gram_write(assembly_instances_1, path_name, "ghidra_assembly_name_one_gram")
        two_gram_write(assembly_instances_2, path_name, "ghidra_assembly_name_two_gram")
        three_gram_write(assembly_instances_3, path_name, "ghidra_assembly_name_three_gram")

def three_gram_write(grams, path_name, name):
    f = open(path_name + name, "w+")
    for key, value in grams.items():
        f.write(key[0] + "," + key[1] + "," + key[2] + "," + str(value) + "\n")
    f.close()

def create_assembly_list(assembly_file, assembly_dictionary):
    with open(assembly_file) as f:
        for line in f:
            line = line.strip()
            line = line.lower()
            assembly_dictionary[line] = 0
    return assembly_dictionary

def create_system_list(system_file, system_dictionary):
    with open(system_file) as f:
        for line in f:
            line = line.strip()
            system_dictionary[line] = 0
    return system_dictionary

def get_dump(ghidra_file, path_name):
    ds_lines = []
    with open(ghidra_file) as f:
        for line in f:
            line = line.strip()
            line = line.split()
            if len(line) > 1:
                if "ds" in line[-2]:
                    if '"' in line[-1]:
                        line[-1] = line[-1].strip('"')
                        ds_lines.append(line[-1])
    if os.path.isfile(path_name + "ghidra_ds_dump"):
        os.remove(path_name + "ghidra_ds_dump")
    f = open(path_name + "ghidra_ds_dump", "w+")
    for item in ds_lines:
        f.write(item + "\n")
    f.close()
    #print ds_lines


def main():
    try:
        gfile = sys.argv[1]
        #pathname = sys.argv[2]
        path = str(gfile)
        path = path.split("/")
        pathname = "/".join(path[:-1]) + "/"

    except:
        print("Usage: python ghidra_single_out.py ghidra-file-path")
        exit(0)
    #data segment dump function    
    get_dump(gfile,pathname)
    
    #initialize dictionary of assembly and system call names for ngram datasets
    assembly_names = {}
    system_call_names = {}
    assembly_names = create_assembly_list('assembly_calls.csv', assembly_names)
    system_call_names = create_system_list('system_calls.csv', system_call_names)
    #producing 1 to 3 gram datasets
    three_gram(gfile,pathname,assembly_names,system_call_names)
    
if __name__ == "__main__":
    main()

