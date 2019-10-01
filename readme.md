aas_table_reader
================

`aas_table_reader` is a simple script to read fixed-width text tables downloaded from AAS journals (AJ, ApJ, ApJS, ApJL) into `astropy` tables.

So far, I have only tested this code on one table. If it breaks when you apply it to a Different table and you are feeling like doing some community service, please make  whatever generalization  is necessary in the code so it will work for the AAS table you are trying to read. Add your table (or a slimmed down version  with most "easy to read" rows removed) to the test directory and `test()` function, make sure you  can run `test()` without errors, and submit a pull request.

You will need `numpy` and `astropy`.

Quick start:

```
import aas_table_reader as reader
path = 'tests/richey-yowell2019.txt'
tbl = reader.read_aas_txt_table(path)
print(tbl)
```

Pretty simple.
