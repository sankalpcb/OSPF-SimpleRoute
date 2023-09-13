

 - Before starting clear all the previous
```bash
make clean
```
 - Before starting clear all the previous and create a new output folder
```bash
make all
```
 - Here is a sample input to run all the routers using multiprocessing:
```bash
python3 main.py -f infile -o outfile -t 1 -a 5 -s 10
```
 - If you want to run each router.py induvidually then use the command below
```bash
python3 router.py -i 3 -f infile -o outfile -t 1 -a 5 -s 10
```
 - (Not important) You can also generate a input file using the below command 
```bash
python3 inputfilegenerator.py 8 20 input_file_name
```
here 8 is number of nodes and 20 is number fo links

## Output
 - You can find  all the output files in the output folder

