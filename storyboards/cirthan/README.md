# CIRThan
A Sketch+Text Composed Image Retrieval Dataset for Thangka

## Overview
<p align="center">
  <img src="dataset.png" width="600" />
</p>

**CIRThan** is a sketch+text composed image retrieval (CIR) dataset designed for culturally grounded and knowledge-specific visual domains.
 It focuses on Thangka imagery—a form of traditional Tibetan art characterized by complex compositions, dense symbolic elements, and domain-dependent semantic conventions.
 CIRThan contains 2,287 triplets, each consisting of a Thangka image, a corresponding human-drawn sketch, and three hierarchical textual descriptions.

Each textual description is provided at three semantic levels.
 **Level 3** is a detailed description written by annotators, **Level 2** removes background and decorative details while preserving essential semantic relations, and **Level 1** offers a concise description focusing on the primary subject and its most distinctive attributes.



## Dataset Statistics
<div align="center">

| Property                         | Value               |
|:---------------------------------|--------------------:|
| # Thangka Images                 | 2,287               |
| # Sketches                       | 2,287               |
| # Text Levels                    | 3                   |
| # Textual Descriptions           | 2,287 × 3           |
| Train / Test split               | 1,868 / 419         |
| Avg. image resolution            | 1,700 × 1,200       |
| Avg. text length (Level 1 / 2 / 3) | 13.16 / 23.10 / 34.13 |

</div>
The table summarizes the key statistics of the proposed dataset.
The dataset consists of 2,287 high-quality thangka images, each paired with one human-drawn sketch and a set of three hierarchical textual descriptions.

Following standard train–test split, we randomly assign 80% of the data for training, and 20% for test, comprising 1,868 sketch–text–image triplets for training and 419 triplets for testing.

The three textual levels exhibit progressively increasing semantic granularity and the average lengths of Level 1, Level 2, and Level 3 descriptions are 13.16, 23.10, and 34.13 words, respectively.
This controlled increase reflects systematic enrichment of semantic content rather than abrupt changes in linguistic structure, enabling principled analysis of retrieval performance under varying degrees of textual specificity.

## Download CIRThan Dataset
Start by cloning the repository:
```bash
git clone https://github.com/jinyuxu-whut/CIRThan.git
```
### Annotations
The annotations are provided in the captions folder. For each split, a JSON file contains the list of the corresponding annotations. Each annotation comprises the following fields:
* `sketch_id`: the id of the reference image (sketch image);
* `thangka_id`: the id of the target image (thangka image);
* `level3`: Level 3 caption corresponds to the original detailed description;
* `level2`: Level 2 caption removes background and decorative details while preserving essential relations based on Level3;
* `level1`: Level 1 caption provides a concise description focusing on the primary subject and its most distinctive attributes.

<details>
<summary>Click to see an annotation example</summary>

```json
    {
        "level3": "Samantabhadra Bodhisattva, white body, jeweled crown, slightly open eyes, transparent celestial robe, red skirt, adorned with ornaments, right hand on right knee, left hand on ground, right leg raised, left leg extended, golden moon disc faintly behind head.",
        "level2": "White Samantabhadra Bodhisattva, jeweled crown, transparent robe and red skirt, ornaments, right hand on knee, left hand on ground, right leg raised, left leg flat, golden moon disc behind head.",
        "level1": "White Samantabhadra, crown, red skirt, right hand on knee, left hand on ground, raised right leg, golden moon behind.",
        "sketch_id": "sketch62",
        "thangka_id": "thangka62"
    }
```
</details>

### Image_splits
The `image_split` folder contains the paths to the sketches and Thangka images in the dataset.

### Images
The CIRThan images include reference images (sketch) and target images (thangka). 
You can download the image from the Google Drive: https://drive.google.com/drive/folders/1M7_l2DiWpwqhlvGpP5EuVEY0eM7-nC3a?usp=sharing.

Please visit the link and download the dataset.
### Dataset file Structure
```bash
dataset
├── captions
│   ├── train.json
│   └── test.json
├── image_splits
│   ├── split.train.json
│   └── split.test.json
├── image
│   ├── 0.png
│   ├── 1.png
│   ├── 2.png
│   └── ...
└── sketch
    ├── 0.png
    ├── 1.png
    ├── 2.png
    └── ...
```

## Data Loader and Evaluation
### Dataloader
We provide a dedicated data loader (data_loader.py) to facilitate reading the CIRThan dataset, including Thangka images, corresponding sketches, and their associated text descriptions.
### Evaluation
Run validate.py to get the results.
```
python validate.py
```

## Licence
This project is licensed under the terms of the [LICENSE](LICENSE.md).

## Citation

```
@misc{xu2026sketchtextcomposedimageretrieval,
      title={A Sketch+Text Composed Image Retrieval Dataset for Thangka}, 
      author={Jinyu Xu and Yi Sun and Jiangling Zhang and Qing Xie and Daomin Ji and Zhifeng Bao and Jiachen Li and Yanchun Ma and Yongjian Liu},
      year={2026},
      eprint={2602.08411},
      archivePrefix={arXiv},
      primaryClass={cs.IR},
      url={https://arxiv.org/abs/2602.08411}, 
}
```
