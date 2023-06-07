# A24
  Aaradhya Verma (2022004)
  Aditya Moza    (2022035)
  Aditya Prasad  (2022036)
  Medha Kashyap  (2022292)

GitHub repo for CSE112 Group A24 project

In this we are programming an assembler in python language for the mentioned ISA and assembly. Here we are taking input to the assembler in a text file containing assembly instructions and the assembler generate a binary output text file. Assembler is generating error notifications along with line number (on which error is encountered) as an output text file.
The programmed assembler is capable of handling all supported instructions, labels, variables and 
returns a syntax error for any illegal instruction. We are generating a "General Syntax Error" for all the error conditions that are mentioned in the question.

In another section of this project, we have developed a simulator for the mentioned assembler with the provided ISA. This simulator involves reading the file developed by the assembler program and simulates the ISA processes to produce an output. Each binary is in binary at the input stage and is first read individually to provude an appropriate program counter output. The code is executed for every instruction till 'hlt' is reached. Output is of the following form: 7 bit program counter and 8, space separated, 16 bit binary numbers denoting the value of registers. After 'halting', the code prints the memory dump.
