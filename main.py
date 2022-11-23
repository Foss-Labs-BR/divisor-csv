import os
import glob
import csv
from time import time
from math import ceil
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv

load_dotenv()

has_header = True if os.getenv('HAS_HEADER') == '1' else False
write_header = True if os.getenv('WRITE_HEADER') == '1' else False
split_method = os.getenv('SPLIT_METHOD')
num_lines = int(os.getenv('NUM_LINES'))
num_parts = int(os.getenv('NUM_PARTS'))

output_dir = '/out'
splits_folder = 'splits-{}'.format(int(time()))
splits_path = os.path.join(output_dir, splits_folder)
in_path = os.path.abspath('in')

os.mkdir(splits_path)

def print_log(txt, level = 1):
    global splits_path

    timezone_offset = -3.0 # America/Sao_Paulo em horário normal sem ser de verão
    tzinfo = timezone(timedelta(hours=timezone_offset))

    full_txt = '[{}] {}{}\n'.format(datetime.now(tzinfo).strftime("%d/%m/%Y %H:%M:%S"), (level - 1) * 2 * ' ', txt)

    log_fh = open( os.path.join(splits_path, 'logs.txt'), 'a+')
    log_fh.write(full_txt)
    log_fh.close()

    print(full_txt)

print_log('Tem cabeçalho: {}'.format(has_header))
print_log('Imprime cabeçalho: {}'.format(write_header))
print_log('Metodo de divisão: {}'.format(split_method))

if split_method == 'lines':
    print_log('Número de linhas: {}'.format(num_lines))
elif split_method == 'parts':
    print_log('Número de partes: {}'.format(num_parts))

for csv_file in glob.glob('in/**/*.csv', recursive=True):

    csv_abs_path = os.path.abspath(csv_file)
    csv_rel_path = os.path.relpath(csv_abs_path, in_path)

    csv_filename = csv_rel_path.replace('/', '-')
    csv_basename = os.path.splitext(
        os.path.basename(os.path.basename(csv_file)))[0]
    csv_file_folder_path = os.path.join(splits_path, csv_filename)

    print_log("Criando diretório '{}'...".format(csv_file_folder_path), 2)

    os.mkdir(csv_file_folder_path)

    print_log("Abrindo '{}'...".format(csv_file), 2)

    csv_num_lines = 0
    csv_lines = []
    csv_header = None

    with open(csv_file, 'r') as csv_file_r_fh:
        csv_reader = csv.reader(csv_file_r_fh)

        for index, row in enumerate(csv_reader):
            if (index == 0) and has_header:
                csv_header = row
                continue

            row_parts = []

            for row_part in row:
                trimmed_row_part = row_part.replace('\n', '<novalinha>')
                row_parts.append(trimmed_row_part)

            csv_lines.append(row_parts)
            csv_num_lines += 1

    print_log("Número de linhas de '{}': {}".format(csv_file, csv_num_lines), 2)

    if split_method == 'lines':

        num_rounds = ceil(csv_num_lines / num_lines)
        print_log('Usando o método de divisão por linhas: {} linhas/arquivo.'.format(num_lines), 2)
        filenumber_denominator = num_lines
    elif split_method == 'parts':
        num_rounds = num_parts
        filenumber_denominator = ceil(csv_num_lines / num_parts)
        print_log('Usando o método de divisão por partes: {} linhas/arquivo ({} partes).'.format( ceil(csv_num_lines / num_rounds), num_parts), 2)

    old_filenumber = 0

    for index, line in enumerate(csv_lines):

        filenumber = (index // filenumber_denominator) + 1

        zfill_size = len(str(num_rounds))
        formatted_filenumber = str(filenumber).zfill(zfill_size)

        csv_file_write_file = '{}-{}.csv'.format(
            csv_basename, formatted_filenumber)
        csv_file_write_path = os.path.join(
            csv_file_folder_path, csv_file_write_file)

        csv_file_w_fh = open(csv_file_write_path, 'a+')
        csv_writer = csv.writer(csv_file_w_fh)

        if old_filenumber != filenumber:
            print_log("Escrevendo '{}'...".format(csv_file_write_path), 3)

            if write_header and has_header:
                csv_writer.writerow(csv_header)

            old_filenumber = filenumber

        csv_writer.writerow(line)
        csv_file_w_fh.close()

print_log('CONCLUIDO!')
