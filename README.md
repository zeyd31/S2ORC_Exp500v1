# Description 

S2ORC_Enhanced500v1 is an enriched subset of the [Semantic Scholar Open Research Corpus (S2ORC)](https://github.com/allenai/s2orc), specifically designed for metadata extraction tasks in natural language processing (NLP) and machine learning research. This dataset comprises 500 training samples, 100 validation samples, and additional 100 testing samples, each processed to include detailed metadata annotations that facilitate the extraction and analysis of scholarly article metadata.

# Dataset Composition
* Training Samples: 500
* Validation Samples: 100
* Testing Samples: 100
* Labels Included: `Title`, `Author`, `Affiliation`, `Venue`, `Abstract`, `Email`, `DOI`, `URI`, `Date`


## Directory Structure
The dataset maintains parallel structures for both training and validation sets, where all files for a single sample share the same base filename prefix:

```
dataset/
├── train/
│   ├── Annotations/
│   │   ├── <file1>_annotations.json
│   │   ├── <file2>_annotations.json
│   │   └── ...
│   └── Texts/
│   │   ├── <file1>_original.txt
│   │   ├── <file2>_original.txt
│   │   └── ...
│   └── PDF-Links/
│       ├── <file1>_link.txt
│       ├── <file2>_link.txt
│       └── ...
│
└── val/
    ├── Annotations/
    │   ├── <file1>_annotations.json
    │   ├── <file2>_annotations.json
    │   └── ...
    └── Texts/
    │   ├── <file1>_original.txt
    │   ├── <file2>_original.txt
    │   └── ...
    └── PDF-Links/
        ├── <file1>_link.txt
        ├── <file2>_link.txt
        └── ...
```

The `test` set follows the same structure and it will be released in this repository according to [the planned timeline](https://nfdi4ds.github.io/nslp2025/docs/mesd_shared_task.html) 

## File Components

### Annotation Files
Located in the `Annotations` directory, these files contain metadata and positional information:
* **Location**: `train/Annotations/` or `val/Annotations/`
* **Naming Convention**: `<filename>_annotations.json`
* **Content**: JSON-formatted metadata including:
  * Document attributes (Title, Author, etc.)
  * Character/token position mappings

### Text Files
Contains the extracted document content:
* **Location**: `train/Texts/` or `val/Texts/`
* **Naming Convention**: `<filename>_original.txt`
* **Content**: Plain text extracted from source PDF documents
* **Note**: Original PDF documents are excluded due to copyright restrictions

### Link Files
Provides references to source documents:
* **Location**: Adjacent to corresponding text files
* **Naming Convention**: `<filename>_link.txt`
* **Content**: URL or reference information for accessing the original PDF document


# Purpose
S2ORC_Enhanced500v1 is designed to support researchers in developing and refining algorithms that automatically extract metadata from scholarly texts. This dataset is particularly prepared for the NFDI4DS shared task MESD, organized at the [NLSP Workshop @ESWC 2025](https://nfdi4ds.github.io/nslp2025/docs/mesd_shared_task.html), where the focus is on enhancing the precision of metadata extraction techniques in academic literature.

# Access
Participants can access the S2ORC_Enhanced500v1 dataset by closing this repository. The test set will be released according the [timeline announced in the workshop page](https://nfdi4ds.github.io/nslp2025/docs/mesd_shared_task.html)


# Evaluation and Ranking
The evaluation of the results will focus on the extraction of attribute values, irrespective of their position in the document. This is particularly important for attributes, which may appear in multiple places within a document such as *title*.

The primary goal is to ensure highly accurate extraction of attribute values, allowing for minor variations. Therefore, correctness will be assessed based on **Levenshtein Similarity**, where a label is considered correctly extracted if its similarity score compared to the gold standard is at least 90%. This means that slight deviations are tolerated as long as the extracted text closely matches the source. The positions of the attributes **will not** be considered during evaluation.

The ranking of participants will be based on the `F1 score`, which provides a balanced measure of precision and recall.

## Gold Standard Quality
We acknowledge that there are some discrepancies in the dataset due to the annotation process and post-processing. To clarify specific cases:

* For DOIs, only the one occurring on the first page (referring to the paper) is relevant. Any additional DOIs can be ignored, as they will not be included in the evaluation.
* For authors, names may contain affiliation symbols, extra text, etc. Therefore, we strongly recommend considering them part of the name when extracting author information.
* Extra spaces will be removed during evaluation.
* Some character encoding issues may appear due to the PDF extraction process. This reflects real-world challenges in metadata extraction and must be accounted for by participants.

# Citation
Please cite the S2ORC_Exp500v1 dataset in any publications or presentations that derive results from this dataset:
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


