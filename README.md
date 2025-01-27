# Description 

S2ORC_Enhanced500v1 is an enriched subset of the [Semantic Scholar Open Research Corpus (S2ORC)](https://github.com/allenai/s2orc), specifically designed for metadata extraction tasks in natural language processing (NLP) and machine learning research. This dataset comprises 500 training samples, 100 validation samples, and additional 100 testing samples, each processed to include detailed metadata annotations that facilitate the extraction and analysis of scholarly article metadata.

# Dataset Composition
* Training Samples: 500
* Validation Samples: 100
* Testing Samples: 100
* Labels Included: `Title`, `Author`, `Affiliation`, `Venue`, `Abstract`, `Email`, `DOI`, `URI`, `Date`

# Data Structure

The dataset is organized into separate folders for training and validation. Each sample consists of:
1. A text file containing the original extracted text.
2. A JSON file containing metadata annotations (including their positions within the text).
3. An optional link file pointing to the original PDF document (not included in the dataset for copyright reasons).

Below is an example structure:
```
train/ ├── Annotations │ ├── file1__annotations.json │ ├── file2__annotations.json │ └── ... └── Texts ├── file1__original.txt ├── file1__link.txt ├── file2__original.txt ├── file2__link.txt └── ...

val/ ├── Annotations │ ├── file1__annotations.json │ ├── file2__annotations.json │ └── ... └── Texts ├── file1__original.txt ├── file1__link.txt ├── file2__original.txt ├── file2__link.txt └── ...
```

## Annotation Files
- Located under `train/Annotations/` and `val/Annotations/`.
- Each file follows the naming convention: `<filename>__annotations.json`.
- These JSON files contain detailed metadata values (e.g., Title, Author, etc.), along with their corresponding character or token positions in the text.

## Text Files
- Located under `train/Texts/` and `val/Texts/`.
- Each text file follows the naming convention: `<filename>__original.txt`.
- The text is extracted from PDF documents. Due to copyright restrictions, the original PDFs are not included in the dataset.

## Link Files
- For each text file, there is an accompanying link file named `<filename>__link.txt`.
- The link file contains a URL or reference to download the corresponding original PDF document.


# Purpose
S2ORC_Enhanced500v1 is designed to support researchers in developing and refining algorithms that automatically extract metadata from scholarly texts. This dataset is particularly prepared for the NFDI4DS shared task MESD, organized at the NLSP Workshop @ESWC 2025, where the focus is on enhancing the precision of metadata extraction techniques in academic literature.

# Access
Participants can access the S2ORC_Enhanced500v1 dataset by closing this repository. The test set will be released according the [timeline announced in the workshop page](https://nfdi4ds.github.io/nslp2025/docs/mesd_shared_task.html)

# Citation
Please cite the S2ORC_Enhanced500v1 dataset in any publications or presentations that derive results from this dataset:
```
@article{boukhers2025comparison,
  title={Comparison of Feature Learning Methods for Metadata Extraction from PDF Scholarly Documents},
  author={Boukhers, Zeyd and Yang, Cong},
  journal={arXiv preprint arXiv:2501.05082},
  year={2025}
}
```
Other related publications: 

```
@inproceedings{boukhers2022vision,
  title={Vision and natural language for metadata extraction from scientific PDF documents: a multimodal approach},
  author={Boukhers, Zeyd and Bouabdallah, Azeddine},
  booktitle={Proceedings of the 22nd ACM/IEEE Joint Conference on Digital Libraries},
  pages={1--5},
  year={2022}
}
```

```
@inproceedings{boukhers2021mexpub,
  title={Mexpub: Deep transfer learning for metadata extraction from german publications},
  author={Boukhers, Zeyd and Beili, Nada and Hartmann, Timo and Goswami, Prantik and Zafar, Muhammad Arslan},
  booktitle={2021 ACM/IEEE Joint Conference on Digital Libraries (JCDL)},
  pages={250--253},
  year={2021},
  organization={IEEE}
}
```

```
@inproceedings{boukhers2019end,
  title={An end-to-end approach for extracting and segmenting high-variance references from pdf documents},
  author={Boukhers, Zeyd and Ambhore, Shriharsh and Staab, Steffen},
  booktitle={2019 ACM/IEEE Joint Conference on Digital Libraries (JCDL)},
  pages={186--195},
  year={2019},
  organization={IEEE}
}
```

# Contact
Please get in touch with [Zeyd Boukhers](zeyd.boukhers@fit.fraunhofer.de) for further inquiries or additional information.


