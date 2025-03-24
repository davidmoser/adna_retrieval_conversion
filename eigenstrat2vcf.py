import os

import yaml

"""
This script converts genetic data from Eigenstrat format to VCF format.
Reads .snp, .ind, and .geno files, processes the data, and writes to a VCF file.

Usage example:
python script.py -s input.snp -i input.ind -g input.geno -o output.vcf -sx 1000 -ix 100
"""


class SNP:
    def __init__(self, identifier, chromosome, position, reference_allele, alternate_allele):
        self.identifier = identifier
        self.chromosome = chromosome
        self.position = position
        self.reference_allele = reference_allele
        self.alternate_allele = alternate_allele


class Individual:
    def __init__(self, identifier, population, sex):
        self.identifier = identifier
        self.population = population
        self.sex = sex


def read_snp_file(snp_file, snp_max):
    # function to read .snp file and return SNP information
    snp_info = []
    with open(snp_file, "r") as file:
        for index, line in enumerate(file):
            if index == snp_max:
                break
            tokens = line.split()
            snp = SNP(
                identifier=tokens[0],
                chromosome=tokens[1],
                position=tokens[3],
                reference_allele=tokens[4],
                alternate_allele=tokens[5]
            )
            snp_info.append(snp)

    return snp_info


def read_ind_file(ind_file, ind_max):
    # function to read .ind file and return individual information
    individuals = []
    with open(ind_file, "r") as file:
        for index, line in enumerate(file):
            if index == ind_max:
                break
            tokens = line.split()
            snp = Individual(
                identifier=tokens[0],
                sex=tokens[1],
                population=tokens[2],
            )
            individuals.append(snp)

    return individuals


def convert_snp(snp):
    return snp.chromosome + "\t" + snp.position + "\t" + snp.identifier + "\t" + snp.reference_allele + "\t" + snp.alternate_allele


def convert_geno_line(geno_eig_line, ind_max):
    ind_max = ind_max or -1
    # function to parse a line from .geno file and return genotype information
    geno_vcf_line = ""
    for index, eigen_type in enumerate(geno_eig_line):
        geno_vcf_line += convert_geno_type(eigen_type)
        geno_vcf_line += "\t"
        if index == ind_max - 1:
            break
    return geno_vcf_line.rstrip()


def convert_geno_type(eigen_type):
    if eigen_type == "0":
        return "1/1"
    elif eigen_type == "1":
        return "1/0"
    elif eigen_type == "2":
        return "0/0"
    elif eigen_type == "9":
        return "."
    elif eigen_type == "\n":
        return ""
    else:
        raise Exception("Unknown genotype: " + eigen_type)


def create_vcf_header(individuals):
    # function to create VCF header lines
    # Include file format, source, reference, and column headers
    header = ("##fileformat=VCFv4.0\n"
              "##fileDate=20090805\n"
              "##source=eigenstrat2vcf.py\n"
              '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')

    # write column headers
    header += "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT"
    for individual in individuals:
        header += "\t" + individual.identifier
    header += "\n"
    return header


def eigenstrat_to_vcf(snp_file, ind_file, geno_file, anno_file, vcf_file_out, snp_file_out, ind_file_out, anno_file_out,
                      ind_max, snp_max):
    snp_info = read_snp_file(snp_file, snp_max)
    individuals = read_ind_file(ind_file, ind_max)

    output_dir = os.path.dirname(vcf_file_out)
    if output_dir:  # Avoid calling makedirs("") which causes an error
        os.makedirs(output_dir, exist_ok=True)

    # Open the GENO file and the output VCF file
    with open(geno_file, "r") as geno_file, open(vcf_file_out, "w") as vcf_out:
        # Write the VCF header
        vcf_out.write(create_vcf_header(individuals))

        # Iterate through the GENO file line by line
        print(f"Total lines: {len(snp_info)}")
        for geno_index, geno_line in enumerate(geno_file):
            if geno_index % 1000 == 0:
                print(geno_index)
            if geno_index == snp_max:
                break
            # Retrieve corresponding SNP information
            vcf_out.write(convert_snp(snp_info[geno_index]))
            vcf_out.write("\t1\tPASS\tNS=1\tGT\t")
            vcf_out.write(convert_geno_line(geno_line, ind_max))
            vcf_out.write("\n")

    # if output file names are given, copy or trim the corresponding meta csv files
    trim_file(snp_file, snp_file_out, len(snp_info), has_header=False)
    trim_file(ind_file, ind_file_out, len(individuals), has_header=False)
    trim_file(anno_file, anno_file_out, len(individuals), has_header=True)


def trim_file(input_path, output_path, no_rows, has_header=True):
    if not output_path: return
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
        end = no_rows + (1 if has_header else 0)
        trimmed_lines = lines[:end]

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(trimmed_lines)

    return output_path


def eigenstrat_to_vcf_yaml(file_path):
    # Load config and call the main function with appropriate parameters.
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)

    # Call the main function
    eigenstrat_to_vcf(
        snp_file=config.get("snp_file"),
        ind_file=config.get("ind_file"),
        geno_file=config.get("geno_file"),
        anno_file=config.get("anno_file", None), # Optional
        vcf_file_out=config.get("vcf_file_out"),
        snp_file_out=config.get("snp_file_out", None),  # Optional
        ind_file_out=config.get("ind_file_out", None),  # Optional
        anno_file_out=config.get("anno_file_out", None),  # Optional
        ind_max=config.get("ind_max", None),  # Optional
        snp_max=config.get("snp_max", None),  # Optional
    )


if __name__ == "__main__":
    eigenstrat_to_vcf_yaml("config/eigenstrat2vcf.yaml")
