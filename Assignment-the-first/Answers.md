# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label |
|---|---|
| 1294_S1_L008_R1_001.fastq.gz |R1|
| 1294_S1_L008_R2_001.fastq.gz | Index1 |
| 1294_S1_L008_R3_001.fastq.gz | Index2 |
| 1294_S1_L008_R4_001.fastq.gz |R4|

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    ![image](https://user-images.githubusercontent.com/65972843/89134073-d7fd1a00-d4d6-11ea-9975-7a7cdf0d4f7b.png)
    ![image](https://user-images.githubusercontent.com/65972843/89134084-f4995200-d4d6-11ea-82d2-39b66120a2ee.png)
    ![image](https://user-images.githubusercontent.com/65972843/89134134-4215bf00-d4d7-11ea-92fe-c05f59868892.png)
    ![image](https://user-images.githubusercontent.com/65972843/89134141-58237f80-d4d7-11ea-8554-06b5f67ff4c2.png)
    2. ```A good quality score cut off is >=20. At a score of 20 there is a 1% chance of error. For the index you need to make sure you have high confidence in each of the                 bases bing reported.```
    3. ```zcat 1294_S1_L008_R2_001.fastq.gz | grep "N" | wc -l total = 367223348
            zcat 1294_S1_L008_R3_001.fastq.gz | grep "N" | wc -l total = 366574786```
    
## Part 2
1. Define the problem
2. Describe output
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [4 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
