from astropy import table, units as u
import numpy as np

def read_aas_txt_table(path):
    with open(path) as f:
        lines = f.readlines()

    # seek column descriptors
    i = 0
    while True:
        if 'byte-by-byte' in lines[i].lower():
            break
        else:
            i += 1
    i += 4 # this will get me to the first descriptor line

    # read in info from the column descriptors
    columns = [[] for _ in range(6)]
    starts, ends, formats, units, names, descriptions = columns
    while True:
        if lines[i].startswith('-------'):
            break
        line = lines[i]

        start = int(line[:4]) - 1
        starts.append(start)

        end = int(line[5:8])
        ends.append(end)

        format = line[9:13].strip()
        formats.append(format)

        unit = line[16:22].strip()
        if '---' in unit:
            unit  = ''
        units.append(unit)

        name = line[23:35].strip()
        names.append(name)

        description = line[36:].strip()
        descriptions.append(description)

        i += 1

    j = 0
    while j < len(names):
        description = descriptions[j]
        if description.startswith('Sign of'):
            starts[j+1] -= 1
            [x.pop(j) for x in columns]
        j += 1

    # seek data
    i += 1
    while True:
        if lines[i].startswith('-------'):
            i += 1
            break
        i += 1

    # now read in the actual rows
    rows = []
    mask = []
    for line in lines[i:]:
        if line == '':
            break
        row = []
        maskrow = []
        for start, end, fmt in zip(starts, ends, formats):
            value_str = line[start:end]
            if 'A' in fmt:
                if value_str == ' '*len(value_str):
                    value = ''
                else:
                    value = value_str
            if 'I' in fmt:
                if value_str == ' '*len(value_str):
                    value = np.nan
                else:
                    value = int(value_str)
            if 'F' in fmt or 'E' in  fmt:
                if value_str == ' '*len(value_str):
                    value = np.nan
                else:
                    value = float(value_str)

            row.append(value)

            if value in [np.nan, '']:
                maskrow.append(True)
            else:
                maskrow.append(False)

        rows.append(row)
        mask.append(maskrow)

    # make astropy table
    tbl = table.Table(rows=rows, names=names, masked=True)
    mask_by_column = zip(*mask)
    tbl.mask = mask_by_column
    for name, unit, description in zip(names, units, descriptions):
        tbl[name].unit = u.Unit(unit)
        tbl[name].description = description

    return tbl