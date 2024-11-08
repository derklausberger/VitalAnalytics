import os

import wfdb

AFIB_PATH = os.path.join(os.getcwd(), os.pardir, "mit-bih-atrial-fibrillation-database-1.0.0")
ARRYTHMIA_PATH = os.path.join(os.getcwd(), os.pardir, "mit-bih-arrhythmia-database-1.0.0")

def read_train_data_from_files():
    print("reading data...")
    dir_path = ARRYTHMIA_PATH
    record_file_path = os.path.join(dir_path, "RECORDS")

    if os.access(record_file_path, os.R_OK):
        with open(record_file_path) as record_file:
            record_lines = record_file.readlines()

            X_train = []
            y_train = []
            normal_count = afib_count = 0
            for line in record_lines:
                record_name = line.strip()
                record_path = os.path.join(dir_path, record_name)
                try:
                    patient_record = wfdb.rdrecord(record_path)
                    annotation = wfdb.rdann(record_path, 'atr')

                    # plot wfdb:
                    #wfdb.plot_wfdb(patient_record, annotation)

                    normal_rhythm, afib_idxs = process_annotation(annotation)

                    if normal_rhythm:
                        print(f"{record_name} has normal rhythm. length: {patient_record.p_signal.size}", end="\r")
                        X_train.append(patient_record.p_signal)
                        y_train.append("N")
                        normal_count += 1
                    elif len(afib_idxs) > 0:
                        print(f"{record_name} has afib at {afib_idxs}. length: {patient_record.p_signal.size}", end="\r")
                        X_train.append(patient_record.p_signal)
                        y_train.append("AFIB")
                        afib_count += 1
                except Exception as e:
                    print(e)

            print('\033[K', end='')
            print(f"{normal_count} normal records, {afib_count} records with afib")

            return X_train, y_train
    else:
        print(f'can not access file {record_file_path}')


def process_annotation(annotation):
    normal_rhythm = True
    afib_idxs = []
    for idx, (symbol, aux) in enumerate(zip(annotation.symbol, annotation.aux_note)):
        if symbol == '+' and aux.rstrip('\x00') != '(N':
            normal_rhythm = False
            if 'AFIB' in aux:
                afib_idxs.append(idx)
                # print(f"{record_name}: {aux}") #N, P, AFIB, B, SBR
    return normal_rhythm, afib_idxs
