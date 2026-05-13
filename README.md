\# Programming Language Project



This project is a Python-based grammar parser developed for a Programming Languages course assignment.



The program reads grammar rules and input sentences from text files, checks whether each sentence is valid according to the grammar, and generates parse tree, JSON, and error visualization outputs.



\## Project Description



The project uses a recursive parsing approach to analyze sentences according to given grammar rules.



For each grammar and sentence file pair, the program:



\- Reads grammar rules from text files

\- Reads input sentences from text files

\- Checks whether each sentence is valid or invalid

\- Generates parse tree visualizations for valid sentences

\- Generates JSON representations of parse trees

\- Generates error visualizations for invalid sentences



\## Project Files



| File | Description |

|---|---|

| `pl\_project.py` | Main Python source code |

| `grammar1.txt` | First grammar file |

| `grammar2.txt` | Second grammar file |

| `sentences1.txt` | Test sentences for the first grammar |

| `sentences2.txt` | Test sentences for the second grammar |

| `rapor.tex` | LaTeX report source |

| `rapor.pdf` | Final project report |



\## How to Run



Make sure Python is installed.



Install the required package:



```bash

pip install graphviz

