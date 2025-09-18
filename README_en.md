# CDR3PairSearch

A CDR3 Sequence-Based Paired Chain Search Tool, specifically designed for immune repertoire data analysis. It supports exact and fuzzy matching of heavy/light chain V/J genes and CDR3 amino acid sequences.

## Project Overview

CDR3PairSearch is a professional tool for immunoglobulin (antibody) and T-cell receptor sequence analysis. It enables efficient searching of matched heavy and light chain paired data in large sequence databases based on Complementarity Determining Region 3 (CDR3) amino acid sequences and V/J gene information.

This tool is particularly suitable for:

- Finding paired chains of specific CDR3 sequences from high-throughput sequencing data
- Immune repertoire diversity analysis
- Antibody engineering and modification research
- Identification of disease-associated immune receptor sequences

## Core Features

### 1. Multi-Mode CDR3 Search

- Heavy chain CDR3-specific search
- Light chain CDR3-specific search
- Universal CDR3 sequence search (matches both heavy and light chains simultaneously)

### 2. Flexible Sequence Matching

- Hamming distance calculation: Suitable for comparing differences between sequences of equal length
- Edit distance (Levenshtein) calculation: Suitable for comparing sequences of unequal length, measuring insertions, deletions, and substitutions

### 3. Gene Matching System

- Supports exact matching of V genes and J genes
- Automatically ignores gene subtype information (e.g., extracts "IGHV1-69" from "IGHV1-69\*01" for matching)
- Enables composite condition search by combining genes and CDR3 sequences

### 4. Efficient Data Processing

- Supports chunked reading of large CSV files to reduce memory usage
- Automatically processes file comment lines, compatible with multiple data formats
- Results are automatically saved as structured CSV files for subsequent analysis

## Installation Methods

### Installation from GitHub (Recommended)

```bash
# Install the latest version
pip install git+https://github.com/yourusername/cdr3pairsearch.git

# Install a specific version (if needed)
pip install git+https://github.com/yourusername/cdr3pairsearch.git@v1.0.0
```

### Installation from Source Code

```bash
# Clone the repository
git clone https://github.com/yourusername/cdr3pairsearch.git
cd cdr3pairsearch

# Install the package
pip install .
```

## Quick Start

```python
from cdr3pairsearch import search_paired_chains

# Basic Usage: Search for a heavy chain CDR3 sequence
results = search_paired_chains(
    database_dir="./database",
    cdr3_aa_heavy="CARDTGGFDIW",
    threshold=1,
    distance_method="edit"
)

# Advanced Usage: Combined search with genes and CDR3
results = search_paired_chains(
    database_dir="./database",
    cdr3_aa_light="GTWHSSLSAWV",
    threshold=2,
    distance_method="hamming",
    v_call_light="IGLV1-51",
    j_call_light="IGLJ3",
    output_file="./results/light_chain_matches.csv",
    chunk_size=10000
)
```

## Parameter Details

The `search_paired_chains` function is the core of the tool. Below is a detailed description of its parameters:

| Parameter Name    | Type    | Default Value                        | Description                                                                                                                                                                                                        |
| ----------------- | ------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `database_dir`    | String  | Required (no default)                | Path to the database directory, which should contain one or more CSV-format data files. **Required parameter**.                                                                                                    |
| `cdr3_aa`         | String  | `None`                               | Universal CDR3 amino acid sequence, which will be compared with both heavy and light chain CDR3 sequences. Mutually exclusive with `cdr3_aa_heavy` and `cdr3_aa_light` (only one can be specified).                |
| `cdr3_aa_heavy`   | String  | `None`                               | Heavy chain CDR3 amino acid sequence, compared only with heavy chain CDR3 sequences in the database. Mutually exclusive with `cdr3_aa` and `cdr3_aa_light`.                                                        |
| `cdr3_aa_light`   | String  | `None`                               | Light chain CDR3 amino acid sequence, compared only with light chain CDR3 sequences in the database. Mutually exclusive with `cdr3_aa` and `cdr3_aa_heavy`.                                                        |
| `threshold`       | Integer | `0`                                  | Distance threshold. Only sequences with a distance less than or equal to this value are considered matches. A value of 0 indicates exact matching; larger values allow more differences.                           |
| `distance_method` | String  | `"edit"`                             | Distance calculation method. Optional values:<br>- `"hamming"`: Hamming distance (only for sequences of equal length)<br>- `"edit"`: Levenshtein distance (for sequences of any length)                            |
| `v_call_heavy`    | String  | `None`                               | Heavy chain V gene name (e.g., "IGHV1-69"). The tool automatically ignores subtype information (e.g., the "\*01" part).                                                                                            |
| `v_call_light`    | String  | `None`                               | Light chain V gene name (e.g., "IGLV1-51").                                                                                                                                                                        |
| `j_call_heavy`    | String  | `None`                               | Heavy chain J gene name (e.g., "IGHJ5").                                                                                                                                                                           |
| `j_call_light`    | String  | `None`                               | Light chain J gene name (e.g., "IGLJ3").                                                                                                                                                                           |
| `output_file`     | String  | `"./paired_chain_search_output.csv"` | Path to the result output file. If the file already exists, it will be overwritten.                                                                                                                                |
| `chunk_size`      | Integer | `None`                               | Number of records per chunk for chunked reading. For large files (with millions of records), it is recommended to set this to 10,000–100,000 to reduce memory usage. `None` means reading the entire file at once. |
| `ignore_subtype`  | Boolean | `True`                               | Whether to ignore gene subtype information. When set to `True`, "IGHV1-69*01" is considered a match for "IGHV1-69*02".                                                                                             |

## Detailed Processing Logic

The internal processing workflow of the `search_paired_chains` function is as follows:

### 1. Parameter Validation

- Checks the mutual exclusivity of CDR3 parameters (ensures only one CDR3 parameter is set)
- Validates the validity of the distance calculation method
- Verifies whether the database directory exists and contains CSV files

### 2. Database Reading

- Iterates through all CSV files in the specified directory
- For each file:
  - Skips the first line (treated as a comment line, if present)
  - Uses the second line as column names
  - Determines whether to use chunked reading or full-file reading based on the `chunk_size` parameter

### 3. Data Filtering

#### Gene Filtering: Filters data based on the provided V/J gene parameters

- Automatically processes gene names to remove subtype information (e.g., "\*01")
- Retains only records with matching genes

#### CDR3 Sequence Filtering:

- Calculates distances based on the specified CDR3 parameter (heavy chain, light chain, or universal)
- Computes the distance between each sequence and the query sequence (Hamming or Levenshtein distance)
- Retains only records with a distance less than or equal to the threshold

### 4. Result Processing

- Adds additional information columns to the results:
  - `query_cdr3`: Stores the CDR3 sequence used for the query
  - `cdr3_aa_dist_heavy`/`cdr3_aa_dist_light`: Calculated distance values
  - `inference_cdr3_type`: Marks the match type (heavy chain, light chain, or both)
- Merges all matching results
- Saves the final results to the specified output file

## Database Format Requirements

Database files must be in CSV format and contain at least the following fields (field names are case-sensitive):

### Heavy Chain-Related Fields

- `cdr3_aa_heavy`: Heavy chain CDR3 amino acid sequence
- `v_call_heavy`: Heavy chain V gene assignment result
- `j_call_heavy`: Heavy chain J gene assignment result

### Light Chain-Related Fields

- `cdr3_aa_light`: Light chain CDR3 amino acid sequence
- `v_call_light`: Light chain V gene assignment result
- `j_call_light`: Light chain J gene assignment result

> Note: CSV files must contain column names in the second line. The first line is treated as a comment line and will be skipped automatically.

## Example Output

The output file is a CSV file containing all matched records from the original data, with the following additional columns added:

| Added Column Name     | Description                                                   |
| --------------------- | ------------------------------------------------------------- |
| `query_cdr3`          | The CDR3 query sequence used for the search                   |
| `cdr3_aa_dist_heavy`  | Distance between the heavy chain CDR3 and the query sequence  |
| `cdr3_aa_dist_light`  | Distance between the light chain CDR3 and the query sequence  |
| `inference_cdr3_type` | Match type, with possible values: "heavy", "light", or "both" |

## License

This project is licensed under the MIT License — see the LICENSE file for details.

## Contribution Guidelines

Contributions to improve this tool are welcome via GitHub issues and pull requests. Before contributing, please ensure:

- All new features include corresponding tests
- Code adheres to the PEP 8 style guide
- Documentation is updated to reflect new features or changes
