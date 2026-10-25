# CIRThan paper (arxiv 2602.08411)
Source: arxiv.org/html/2602.08411v2

A Sketch+Text Composed Image Retrieval Dataset for Thangka
Report GitHub Issue
Title:
Content selection saved. Describe the issue below:
Description:
Submit without GitHub
Submit in GitHub
arXiv is now an independent nonprofit!
Learn more
Back to arXiv
Why HTML?
Report Issue
Back to Abstract
Download PDF
Abstract.
Introduction
Related Work
Sketch-based & Text-based Image Retrieval
Composed Image Retrieval
The CIRThan Dataset
Sketch+Text CIR Task Definition
Data Construction
Dataset Statistics and Analysis
Overview
Scale Diversity of Thangka Imagery
Semantic Diversity and Long-Tailed Subject Distribution
Experiments
Baselines
Experimental Settings
Results
Supervised CIR on CIRThan.
Zero-shot CIR on CIRThan.
Impact of textual granularity.
Analysis of Different MLLMs.
Potential Research Directions
Conclusion
Acknowledgements
References
License: CC BY-NC-ND 4.0
arXiv:2602.08411v2 [cs.IR] 18 Apr 2026
A Sketch+Text Composed Image Retrieval Dataset for Thangka
Conference:
Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval; July 20–24, 2026; Melbourne, VIC, Australia
Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR ’26), July 20–24, 2026, Melbourne, VIC, Australia
10.1145/3805712.3808581
979-8-4007-2599-9/2026/07
Information systems Multimedia and multimodal retrieval
Information systems Test collections
Jinyu Xu
Affiliation:
Wuhan University of Technology
email:
jinyxu@whut.edu.cn
Yi Sun
Affiliation:
Wuhan University of Technology
email:
syi1005@whut.edu.cn
Jiangling Zhang
Affiliation:
Wuhan University of Technology
email:
zhangjiangling@whut.edu.cn
Qing Xie
Corresponding authors.
Affiliation:
Wuhan University of Technology
email:
felixxq@whut.edu.cn
Daomin Ji
Affiliation:
RMIT University
Melbourne
Australia
email:
daomin.ji@student.rmit.edu.au
Zhifeng Bao
Affiliation:
The University of Queensland
Brisbane
Australia
email:
zhifeng.bao@uq.edu.au
Jiachen Li
Affiliation:
Wuhan University of Technology
email:
lijiachen@whut.edu.cn
Yanchun Ma
Affiliation:
Wuhan Vocational College of Software and Engineering
email:
mayanchun@whvcse.edu.cn
Yongjian Liu
Affiliation:
Wuhan University of Technology
email:
liuyj@whut.edu.cn
Abstract.
Composed Image Retrieval (CIR) enables image retrieval by combining multiple query modalities, but existing benchmarks predominantly focus on general-domain imagery and rely on reference images with short textual modifications.
As a result, they provide limited support for retrieval scenarios that require fine-grained semantic reasoning, structured visual understanding, and domain-specific knowledge.
In this work, we introduce
CIRThan
, a sketch+text
omposed
etrieval dataset for
gka imagery, a culturally grounded and knowledge-specific visual domain characterized by complex structures, dense symbolic elements, and domain-dependent semantic conventions.
CIRThan contains 2,287 high-quality Thangka images, each paired with a human-drawn sketch and hierarchical textual descriptions at three semantic levels, enabling composed queries that jointly express structural intent and multi-level semantic specification.
We provide standardized data splits, comprehensive dataset analysis, and benchmark evaluations of representative supervised and zero-shot CIR methods.
Experimental results reveal that existing CIR approaches, largely developed for general-domain imagery, struggle to effectively align sketch-based abstractions and hierarchical textual semantics with fine-grained Thangka images, particularly without in-domain supervision.
We believe CIRThan offers a valuable benchmark for advancing sketch+text CIR, hierarchical semantic modeling, and multimodal retrieval in cultural heritage and other knowledge-specific visual domains.
The dataset is publicly available at
https://github.com/jinyuxu-whut/CIRThan
Keywords:
Composed Image Retrieval; Sketch and Text; Thangka Imagery
cc-license:
by-nc-nd
Introduction
With the increasing demand for fine-grained image retrieval, users rely on multimodal queries to express search intents that cannot be captured by a single modality alone.
To address this need, composed image retrieval (CIR)
Vo et al., 2019
Liu et al., 2021
Baldrati et al., 2022a
Saito et al., 2023
Baldrati et al., 2023a
Sun et al., 2024
Sun et al., 2026
has emerged as an important paradigm, typically combining a reference image with a relative textual description.
While most existing CIR studies focus on general-domain natural images, users often encounter retrieval scenarios that require domain-specific knowledge and detailed semantic reasoning, posing challenges to existing CIR benchmarks.
A representative example is Thangka imagery
Wang et al., 2021
Li et al., 2026
, a form of traditional Tibetan art characterized by highly structured compositions, dense elements, and extremely fine textures along with profound cultural meanings.
As an important component of cultural heritage and digital humanities, Thangka imagery plays a crucial role in the digital organization, analysis, and dissemination of cultural collections
Hu et al., 2025
Wang et al., 2021
Dong et al., 2023
Ren et al., 2024
This highlights the need for a CIR benchmark specifically designed for knowledge-specific visual domains such as Thangka.
Nevertheless, existing CIR benchmarks remain limited in several important aspects.
Figure 1
Comparison of composed query examples from FashionIQ, CSTBIR, and the proposed CIRThan dataset.
(1) Limitation of the visual reference.
Existing CIR benchmarks such as FashionIQ
Wu et al., 2021
, CIRR
Liu et al., 2021
, and CIRCO
Baldrati et al., 2023a
are constructed on general-domain image collections, where images depict common objects with loosely structured and readily interpretable visual semantics (Figure
Accordingly, conventional CIR assumes that users can identify a suitable reference image that is already semantically close to the desired target and express the remaining differences using a short textual description.
However, these assumptions become fragile when applied to complex scenarios or domain-specific visual collections such as Thangka imagery, where identifying an appropriate reference image is inherently difficult.
As an alternative, sketches provide an intuitive and flexible way for users to express visual intent, allowing them to abstract away irrelevant details and focus on salient structures and shape cues.
While sketches have been explored as an alternative reference modality, existing sketch+text CIR benchmarks (e.g., CSTBIR
Gatti et al., 2024
in Figure
) typically employ coarse or category-level sketches that mainly convey object presence.
Such sketches are insufficient to support fine-grained composed image retrieval, where detailed structural configurations and subtle visual semantic cues are critical.
(2) Limitation of the textual description.
Textual descriptions in existing CIR benchmarks
Wu et al., 2021
Liu et al., 2021
Baldrati et al., 2023a
are primarily designed for general-domain imagery and typically focus on coarse semantic cues that can be easily expressed in brief natural language.
As a result, they provide limited support for retrieval scenarios that require domain-specific and fine-grained semantic descriptions, such as those involving complex structures, instance-level attributes, or knowledge-dependent semantic details.
Furthermore, in practical retrieval scenarios, the level of semantic detail expressed in textual queries often varies across users, reflecting differences in domain knowledge and retrieval intent.
However, current CIR datasets do not explicitly model the hierarchical nature of textual descriptions, which further restricts their applicability to knowledge-specific and fine-grained composed image retrieval.
These limitations reveal that existing CIR benchmarks are insufficient to support composed image retrieval scenarios where satisfying retrieval intent requires precise semantic matching between the composed query and target images, particularly in knowledge-specific scenarios that demand domain-aware semantics, detailed structural understanding, and multi-level semantic specification.
Although sketch+text composed image retrieval has recently attracted initial attention, existing studies remain limited, leaving sketch+text CIR insufficiently explored as a benchmark setting for such demanding retrieval scenarios.
Motivated by these limitations, we introduce
CIRThan
, a new sketch+text
omposed
etrieval dataset for
gka imagery.
To address
Limitation (1)
, CIRThan adopts fine-grained human-drawn sketches as the visual reference modality, enabling users to convey salient objects, structural layouts, and shape-related cues that are difficult to express using a semantically close natural image or a coarse category-level sketch.
To address
Limitation (2)
, CIRThan provides hierarchical textual descriptions grounded in domain knowledge and retrieval intent, explicitly modeling different levels of semantic granularity to accommodate user variability in domain knowledge and expressive detail.
Overall, fine-grained sketches and hierarchical text form an expressive query formulation tailored to CIR in knowledge-specific visual domains.
In summary, our contributions are:
) We introduce
CIRThan
, a new sketch+text composed image retrieval dataset for Thangka imagery, which serves as a knowledge-specific benchmark for evaluating composed retrieval under strict semantic matching requirements;
) We design a curated data construction pipeline that integrates fine-grained human-drawn sketches with hierarchical textual descriptions grounded in domain knowledge, enabling composed queries that capture detailed visual intent and multi-level semantic specification;
) We conduct extensive benchmarks of representative supervised and zero-shot CIR methods on CIRThan, revealing several quantitative findings:
1) a substantial performance gap between supervised and zero-shot CIR, with the best supervised method achieving 52.03% R@1 while zero-shot methods remain below 8% R@1 on average;
2) consistent performance gains with increased textual granularity across all methods, highlighting the importance of hierarchical semantic specification; and
3) limited effectiveness of current MLLM-based zero-shot CIR approaches in aligning sketch+text composed queries with domain-specific semantics, underscoring the challenges of fine-grained CIR in knowledge-specific visual domains.
Related Work
Sketch-based & Text-based Image Retrieval
Sketch-based image retrieval (SBIR) and text-based image retrieval (TBIR) are two classical paradigms that allow users to express retrieval intent through a single modality.
In SBIR
Qi et al., 2016
Seddati et al., 2017
Bui et al., 2018
Collomosse et al., 2019
Lei et al., 2020
Xu et al., 2026
, sketches provide a flexible and human-centered visual abstraction that emphasizes shape, contour, and structural cues, making them effective when retrieval intent is primarily defined by visual structure rather than detailed appearance
Sun et al., 2022
Ling et al., 2022
Sain et al., 2023
Zheng et al., 2021
However, sketches alone provide limited access to explicit semantic information, such as object identity, attributes, or symbolic meaning, which restricts their applicability in finer-grained matching scenarios.
Lülf et al., 2024
Huo et al., 2024
Jiang and Ye, 2023
enables semantic matching between images and natural language descriptions by learning joint visual–textual representations.
Although recent vision–language models
Radford et al., 2021
Jia et al., 2021
Yao et al., 2022
have substantially improved TBIR performance in general-domain settings, text alone often struggles to convey structural layout, spatial relations, or domain-specific visual conventions.
As a result, neither sketches nor text alone is sufficient to express complex retrieval intent that requires both structural precision and rich semantic understanding, motivating composed image retrieval.
Composed Image Retrieval
Composed Image Retrieval (CIR) extends single-modality retrieval by combining a reference image with a textual description to retrieve a target image that satisfies a specified modification.
Existing CIR methods can be broadly categorized into supervised methods
Baldrati et al., 2022a
Baldrati et al., 2022b
trained on annotated triplets and zero-shot methods
Saito et al., 2023
Suo et al., 2024
Wang et al., 2025
that leverage weakly labeled image-text data or pretrained vision-language models, with recent work further exploring training-free settings using large language models (LLMs)
Yang et al., 2024a
Sun et al., 2025
Karthik et al., 2024
Most existing CIR benchmarks, including FashionIQ
Wu et al., 2021
, CIRR
Liu et al., 2021
, CIRCO
Baldrati et al., 2023a
, and GeneCIS
Vaze et al., 2023
, are constructed on general-domain imagery and primarily rely on textual descriptions to specify attribute- or object-level modifications. In these datasets, reference images often provide limited fine-grained semantic guidance, and retrieval performance largely depends on textual cues rather than precise semantic correspondence between reference and target images. For instance, CIRR
Liu et al., 2021
constructs reference-target pairs based on visual similarity without careful human verification and subsequently annotates semantic differences using text, which may result in reference–target image pairs that differ substantially from each other. As a consequence, retrieval often relies more heavily on textual cues than on precise semantic correspondence between the reference and the target, limiting the evaluation of fine-grained CIR.
To alleviate the difficulty of acquiring suitable reference images, sketch+text CIR has recently been explored, allowing users to express visual intent more flexibly through sketches.
However, existing sketch+text benchmarks
Koley et al., 2024
Gatti et al., 2024
predominantly employ coarse or category-level sketches and focus on general-domain scenarios, leaving fine-grained structural semantics and knowledge-specific domains largely underexplored.
In contrast, our work investigates sketch+text CIR in a knowledge-specific visual domain, emphasizing fine-grained sketches and hierarchical textual specification to support more precise semantic alignment.
The CIRThan Dataset
This section introduces the proposed CIRThan dataset.
We first formalize the sketch+text composed image retrieval (CIR) task and then detail the data construction pipeline.
Then, we present a comprehensive statistical analysis to characterize the dataset.
Sketch+Text CIR Task Definition
Let us define a composed query as
\{\mathcal{I}_{s},\mathcal{T}\}
, where
\mathcal{I}_{s}
denotes a reference sketch that conveys salient visual cues and fine-grained visual details that are difficult to articulate precisely using natural language, and
\mathcal{T}
denotes a natural language description specifying semantic attributes and complementary information.
Given an image database
\mathcal{D}
consisting of Thangka images, the objective of the sketch+text composed image retrieval task is to retrieve a target image
\mathcal{I}_{t}\in\mathcal{D}
that precisely matches the visual intent conveyed by
\mathcal{I}_{s}
while preserving the semantic content expressed in
\mathcal{T}
This formulation is model-agnostic and serves as a benchmark setting for evaluating sketch+text composed image retrieval in knowledge-specific visual domains.
Data Construction
Figure 2
The data construction pipeline of the CIRThan dataset.
The Thangka images in CIRThan are provided by the
Tibet Thangka Art and Culture Association
All images are obtained with permission from the source institutions or are publicly available under appropriate usage conditions.
The collection comprises high-quality photographs collected from monasteries, museums, and individual artists across Tibet, ensuring both cultural authenticity and visual diversity.
To construct a high-quality and semantically reliable CIR dataset, we design a standardized annotation pipeline that integrates human expertise with large language model (LLM) assistance.
As a culturally visual domain, Thangka imagery involves various characters, symbolic objects, and visual configurations rooted in Buddhist philosophy.
Accordingly, our annotation pipeline emphasizes terminological standardization, semantic precision, and cross-modal consistency across sketches, texts, and images.
The pipeline consists of four sequential steps:
(1) sketch drawing,
(2) detailed textual description,
(3) hierarchical text simplification, and
(4) verification and refinement.
Each Thangka image is paired with one human-drawn sketch and three hierarchical textual descriptions (Level 1–3).
Figure
illustrates the overall workflow.
Sketch Drawing.
Annotators draw a free-form sketch to capture discriminative visual cues of the input Thangka, such as characteristic contours, distinctive shape patterns, local texture, and salient structural configurations.
Depending on the content, sketches may include coarse surrounding structures to convey global spatial organization.
Rather than exhaustively depicting all entities, sketches reflect a selective abstraction that aligns with realistic user behavior in composed retrieval.
Distribution of text lengths
Image area distribution
Subject distribution
Figure 3
Statistical analysis of image resolution and subject distribution in the dataset.
Detailed Textual Description.
To complement the sketch modality, annotators provide a detailed natural language description to specify the semantic content of salient entities depicted in Thangka imagery.
The description explicitly identifies key characters, symbolic objects, and other relevant visual elements, together with their attributes (e.g., color and ornamentation) and characteristics.
In addition, it captures contextual cues, semantic relationships and other semantic details that are difficult to convey reliably through sketches alone.
To ensure terminological accuracy and consistency, we provide annotation guidelines with standardized vocabulary and manage the labeling process using
Label Studio
Hierarchical Text Simplification.
To model variability in user expertise and query specificity, we construct three levels of textual descriptions via controlled simplification.
This step does not introduce new semantic content; instead, it systematically reduces descriptive detail while preserving the core semantic structure of the original description.
We use Qwen-3 as an assisting LLM under strict constraints: the primary semantics must be retained, while simplification is limited to secondary attributes, decorative details, and redundant expressions.
Specifically,
Level 3
is the original detailed description,
Level 2
removes background and decorative details while preserving essential relations, and
Level 1
provides a concise description focusing on the primary subject and its most distinctive attributes.
Verification and Refinement.
In the final stage, all sketches and textual descriptions undergo expert verification to ensure semantic correctness, terminological consistency, and cross-modal alignment.
Domain experts in Thangka art and culture review the annotations against the standardized vocabulary and validate the correspondence among sketches, texts, and images.
All LLM-generated descriptions are manually verified and refined by domain experts to ensure semantic correctness and consistency.
This process improves annotation quality and helps ensure that CIRThan provides a robust benchmark for sketch+text composed image retrieval in knowledge-specific domains.
Dataset Statistics and Analysis
3.3.1.
Overview
summarizes the key statistics of CIRThan.
The dataset contains 2,287 Thangka images, each paired with one human-drawn sketch and three hierarchical textual descriptions, forming sketch–text–image triplets.
Following a standard train–test split, we allocate 80% of the data for training and 20% for test, resulting in 1,868 training triplets and 419 testing triplets.
The three textual levels are designed to represent progressively increasing semantic specificity.
As shown in Figure
), the average lengths of Level 1, Level 2, and Level 3 descriptions are 13.16, 23.10, and 34.13 words, respectively.
Importantly, this increase reflects controlled semantic enrichment rather than abrupt changes in linguistic structure, allowing systematic evaluation of CIR models under different degrees of semantic detail.
This hierarchical design supports systematic study of retrieval behavior under varying degrees of semantic granularity in composed queries.
Although CIRThan is relatively small in scale, it is designed for fine-grained, knowledge-intensive retrieval scenarios where annotation quality and semantic precision are more critical than data quantity.
Table 1
Summary statistics of CIRThan.
Property
# Thangka Images
# Sketches
# Text Levels
# Textual Descriptions
2,287\times 3
Train / Test split
1,868 / 419
Avg. image resolution
1,700\times 1,200
Avg. text length (Level 1 / 2 / 3)
13.16 / 23.10 / 34.13
3.3.2.
Scale Diversity of Thangka Imagery
Figure
) compares the normalized distribution of image areas between CIRThan and the existing sketch+text CIR dataset CSTBIR
Gatti et al., 2024
CIRThan exhibits a substantially broader distribution, spanning nearly four orders of magnitude in image area, with a median size of approximately
1.46\times 10^{6}
pixels.
By contrast, images in CSTBIR are concentrated around a much smaller median area of
1.87\times 10^{5}
pixels, resulting in a sharply peaked distribution.
This difference reflects the characteristics of Thangka arts, where high-resolution digitization is commonly adopted to preserve semantically meaningful details, such as intricate line work, dense decorative patterns, and layered compositional structures.
As a result, CIRThan includes significant variation in spatial scale, providing a realistic benchmark for studying CIR robustness under heterogeneous visual conditions commonly encountered in domain-specific and cultural heritage image collections.
3.3.3.
Semantic Diversity and Long-Tailed Subject Distribution
Figure
) illustrates the distribution of visual subjects in CIRThan, which follows a pronounced long-tailed pattern.
While a small number of subjects appear frequently, a large portion of subject categories occur only a few times.
In particular, the aggregated “Others” category contains 267 distinct subject types and 789 images, accounting for approximately 34.5% of the dataset.
This long-tailed distribution reflects the inherent semantic diversity of Thangka imagery, where imagery spans a wide range of rare and specialized subjects, and symbolic elements.
Such a distribution poses substantial challenges for retrieving Thangka images containing rare and specialized subjects, especially under strict semantic matching requirements, and makes CIRThan a realistic and domain-specific benchmark for studying CIR beyond dominant or frequently occurring semantic categories.
Experiments
Table 2
Retrieval results on the CIRThan test set.
Supervised methods are trained on the CIRThan training split, whereas zero-shot methods are pre-trained on external image-text data or applied in a training-free manner.
Method
Level1
Level2
Level3
Average
Supervised CIR Methods
Combiner
Baldrati et al., 2022b
Combiner-FT
Baldrati et al., 2022a
CLIP4Cir
Baldrati et al., 2023b
Blip4CIR
Liu et al., 2024
Bi-Blip4CIR
Liu et al., 2024
Jiang et al., 2024
ENCODER
Li et al., 2025
Zero-Shot CIR Methods
Sketch-only
Text-only
Pic2Word
Saito et al., 2023
LinCIR
Gu et al., 2024
Context-I2W
Tang et al., 2024
Yang et al., 2024b
Yang et al., 2024a
OSrCIR
Tang et al., 2025
Sun et al., 2025
Baselines
We evaluate representative CIR baselines under both supervised training and zero-shot transfer, to assess in-domain performance and cross-domain generalization on CIRThan.
Supervised CIR.
We include widely adopted supervised CIR baselines trained with annotated triplets, including three variants of CLIP4Cir: Combiner
Baldrati et al., 2022b
, Combiner-FT
Baldrati et al., 2022a
, and CLIP4Cir
Baldrati et al., 2023b
two variants of Bi-Blip4CIR: Blip4CIR and Bi-Blip4CIR
Liu et al., 2024
as well as CaLa
Jiang et al., 2024
and ENCODER
Li et al., 2025
Zero-shot CIR.
We evaluate representative ZS-CIR methods that transfer pretrained vision-language models to CIRThan without using task-specific supervision.
These methods differ in whether they require lightweight adaptation or perform retrieval in a fully training-free manner.
(i) Training-based ZS-CIR
methods require lightweight training on generic image-text data (without using CIRThan), including Pic2Word
Saito et al., 2023
, LinCIR
Gu et al., 2024
, and Context-I2W
Tang et al., 2024
In contrast,
(ii) Training-free ZS-CIR
methods directly adopt LLMs/MLLMs to compose textual queries without any additional training, including LDRE
Yang et al., 2024b
, SEIZE
Yang et al., 2024a
, OSrCIR
Tang et al., 2025
, and CoTMR
Sun et al., 2025
In addition, we report sketch-only and text-only retrieval as reference settings by directly computing similarities in the CLIP embedding space.
Experimental Settings
Dataset.
All experiments are conducted on the proposed CIRThan dataset.
Each Thangka image corresponds to one human-drawn sketch and three hierarchical textual descriptions (Level 1-Level 3), which describe the same target image with increasing semantic specificity.
During training and evaluation, each sketch is paired with one text level at a time, forming three composed queries per target with different semantic granularity.
This design allows us to systematically study how retrieval performance varies with the level of textual detail, while keeping the visual reference and target image fixed.
The dataset is split into 1,868 training images and 419 test images, and the corresponding sketch-text queries at all three levels are used consistently within each split.
All dataset splits and query constructions are publicly released to support reproducibility.
Implementation details.
All experiments are implemented in PyTorch
Paszke et al., 2019
and conducted on a single NVIDIA RTX 4090 GPU.
Baseline models follow the default settings provided in their original implementations, without dataset-specific hyperparameter tuning.
Supervised CIR models are trained on the CIRThan training set and evaluated on the test set.
For zero-shot methods, training-based ZS-CIR approaches follow their original training protocols and are trained on large-scale generic image-text datasets (e.g., CC3M
Sharma et al., 2018
), without using any CIRThan training data, and are then evaluated on the CIRThan test set.
Training-free ZS-CIR baselines rely on pretrained MLLMs without task-specific training.
We adopt Qwen2-VL-7B
Wang et al., 2024
, as the default MLLM for all training-free baselines, unless otherwise specified.
Evaluation Metrics.
Following common practice in composed image retrieval, we evaluate all methods using Recall@K (R@K).
For each composed query, all Thangka images in the gallery are ranked by similarity, and retrieval is considered successful if the ground-truth target Thangka appears within the top-K results.
We report R@K for
K\in\{1,3,5\}
, as each query in CIRThan has a single ground-truth target.
Results
We report the retrieval performance of representative supervised and zero-shot CIR baselines on CIRThan in Table
Overall, supervised methods substantially outperform zero-shot counterparts, and retrieval accuracy consistently improves with richer textual descriptions.
Our analysis focuses on how existing CIR paradigms behave in a culturally grounded retrieval scenario that requires domain-specific knowledge and fine-grained matching between sketch+text composed queries and target Thangka images.
4.3.1.
Supervised CIR on CIRThan.
Supervised CIR methods trained on CIRThan achieve markedly stronger performance than zero-shot baselines.
As shown in Table
, ENCODER attains the highest average R@1 of 52.03%, outperforming CLIP4Cir (39.94%) and other CIR methods by a large margin.
Across all supervised models, retrieval accuracy consistently increases from Level 1 to Level 3.
For instance, ENCODER improves from 49.88% at Level 1 to 54.65% at Level 3 in R@1.
This trend indicates that richer textual descriptions provide increasingly informative semantic constraints for distinguishing visually similar Thangka images.
Overall, although supervised models benefit from in-domain training, their performance remains far from satisfactory, highlighting the intrinsic difficulty of fine-grained semantic matching in CIRThan, where many images share similar global composition and discriminative cues are embedded in subtle attributes, symbolic elements, and structured semantic relations that require fine-grained understanding.
4.3.2.
Zero-shot CIR on CIRThan.
Zero-shot CIR methods exhibit substantially lower performance than supervised models.
The strongest zero-shot baseline achieves an average R@1 below 8%, compared to over 50% for supervised methods, revealing a pronounced domain gap between generic image–text training data and Thangka imagery.
Single-modality baselines perform particularly poorly, with sketch-only and text-only retrieval achieving average R@1 scores of 4.30% and 6.44%, respectively.
This observation confirms that neither modality alone is sufficient to capture the complex semantic information of Thangka images, which often require both structural visual cues and explicit textual specification.
Although multi-modal zero-shot methods consistently outperform single-modality settings, their overall accuracy remains limited.
For instance, LinCIR achieves the highest zero-shot average R@1 of 7.96%, while training-free approaches such as SEIZE and LDRE yield comparable results.
These findings indicate that existing ZS-CIR methods struggle to achieve fine-grained alignment between composed sketch+text queries and Thangka without in-domain supervision, underscoring CIRThan as a challenging benchmark for cross-domain generalization.
4.3.3.
Impact of textual granularity.
Across both supervised and zero-shot settings, retrieval performance generally improves as textual descriptions become more detailed.
More detailed descriptions provide richer semantic specification, which helps disambiguate visually similar Thangka images, particularly when differences lie in attributes, symbolic elements, or subtle relational cues.
Importantly, this trend is consistent across different CIR paradigms, suggesting that hierarchical textual specification is a fundamental factor for composed image retrieval in knowledge-specific domains.
These findings validate the design choice of CIRThan to include multi-level textual descriptions and highlight the importance of modeling semantic granularity when studying fine-grained CIR.
Table 3
The performance of different MLLMs of CoTMR on CIRThan test set.
Method
Level3
Qwen2-VL-7B
Qwen2.5-VL-72B
GPT-4o mini
GPT-4.1
4.3.4.
Analysis of Different MLLMs.
compares the performance of different multimodal large language models (MLLMs) when used within the CoTMR framework.
We select four representative MLLMs: Qwen2-VL-7B
Wang et al., 2024
, Qwen2.5-VL-72B
Bai et al., 2025
, GPT-4o mini
OpenAI, 2024
, GPT-4.1
OpenAI, 2025
Despite substantial differences in model scale and pretraining data, retrieval performance varies only marginally across MLLMs.
These results suggest that current MLLMs, even at larger scales, remain limited in their ability to jointly reason over sketch-based visual abstractions and domain-specific textual descriptions for CIR.
The challenge appears to stem not from language modeling capacity alone, but from the difficulty of grounding composed sketch+text queries in culturally specific visual semantics.
Overall, these observations further emphasize that CIRThan poses challenges that go beyond generic multimodal understanding, requiring advances in cross-modal fine-grained alignment, sketch understanding, and domain-aware reasoning.
Potential Research Directions
CIRThan is designed to advance CIR in culturally grounded and knowledge-specific visual domains by integrating free-form sketches, hierarchical texts, and Thangka images under fine-grained matching requirements.
It enables several research directions that are insufficiently supported by existing CIR benchmarks.
(1) User-centric sketch+text CIR.
Sketch+text CIR remains an early-stage research direction with limited benchmarks.
In CIRThan, sketches provide a flexible and intuitive way for users to express fine-grained visual intent through selective abstraction and visual cues, while hierarchical textual descriptions explicitly model variations in the complexity and specificity of user retrieval intent.
This design enables systematic study of user-centric multimodal query formulation and composition, as well as how retrieval models integrate complementary visual and textual semantics under realistic intent expression.
(2) Knowledge-specific retrieval with dense and structured semantics.
Thangka imagery contains multiple semantically meaningful entities, symbolic objects, and culturally grounded configurations organized in highly structured compositions.
CIRThan therefore supports research on composed retrieval beyond coarse attribute modification, requiring models to align sketch+text queries with instance-level attributes, symbolic details, and their structural relations.
This setting enables investigation of fine-grained cross-modal matching in knowledge-specific visual domains.
(3) Limitations of MLLMs in knowledge-specific domains.
Experimental results on CIRThan reveal a substantial performance gap between supervised methods and zero-shot approaches based on MLLMs.
Despite their strong general vision–language understanding capabilities, current MLLMs (e.g., Qwen-VL, GPT-based models) struggle to achieve reliable semantic alignment between sketch-based abstractions, domain-specific textual semantics, and fine-grained Thangka images.
This suggests that existing MLLMs have limited capacity to interpret non-natural visual inputs such as sketches and to integrate culturally grounded domain knowledge under fine-grained matching requirements.
CIRThan therefore motivates research on improving MLLM-based retrieval in knowledge-specific domains, including domain adaptation, knowledge-aware representation learning, and retrieval-augmented reasoning.
Conclusion
In this work, we introduced
CIRThan
, a sketch+text composed image retrieval dataset for Thangka imagery, a knowledge-specific visual domain where successful retrieval requires fine-grained semantic alignment between composed sketch+text queries and visually complex images.
CIRThan consists of 2,287 high-quality Thangka images, each paired with a human-drawn sketch and hierarchical textual descriptions at three semantic levels, enabling expressive and structured multimodal queries.
We provide standardized data splits, comprehensive dataset analysis, and benchmark evaluations of representative supervised and zero-shot CIR methods.
Experimental results show that existing CIR approaches, largely developed on general-domain imagery, face substantial challenges when applied to sketch+text queries and knowledge-specific domains, particularly in the absence of in-domain supervision.
We believe CIRThan offers a valuable benchmark for advancing research on sketch+text composed image retrieval, hierarchical semantic query modeling, and multimodal retrieval in cultural heritage and other knowledge-specific visual domains.
Acknowledgements.
This research is partially supported by National Natural Science Foundation of China (Grant No. 62271360) and National Key Research and Development Program of China (2024YFF0907002)
References
et al.
(2025)
S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, H. Zhong, Y. Zhu, M. Yang, Z. Li, J. Wan, P. Wang, W. Ding, Z. Fu, Y. Xu, J. Ye, X. Zhang, T. Xie, Z. Cheng, H. Zhang, Z. Yang, H. Xu, and J. Lin
Qwen2.5-vl technical report
arXiv preprint arXiv:2502.13923
Cited by:
§4.3.4
Baldrati
et al.
(2023a)
A. Baldrati, L. Agnolucci, M. Bertini, and A. Del Bimbo
Zero-shot composed image retrieval with textual inversion
Proceedings of the IEEE/CVF International Conference on Computer Vision
pp. 15292–15301
Cited by:
Baldrati
et al.
(2022a)
A. Baldrati, M. Bertini, T. Uricchio, and A. Del Bimbo
Conditioned and composed image retrieval combining and partially fine-tuning clip-based features
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 4959–4968
Cited by:
Table 2
Baldrati
et al.
(2022b)
A. Baldrati, M. Bertini, T. Uricchio, and A. Del Bimbo
Effective conditioned and composed image retrieval combining clip-based features
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 21466–21474
Cited by:
Table 2
Baldrati
et al.
(2023b)
A. Baldrati, M. Bertini, T. Uricchio, and A. Del Bimbo
Composed image retrieval using contrastive learning and task-oriented clip-based features
ACM Transactions on Multimedia Computing, Communications and Applications
pp. 1–24
Cited by:
Table 2
et al.
(2018)
T. Bui, L. Ribeiro, M. Ponti, and J. Collomosse
Sketching out the details: sketch-based image retrieval using convolutional neural networks with multi-stage regression
Computers & Graphics
pp. 77–87
Cited by:
Collomosse
et al.
(2019)
J. Collomosse, T. Bui, and H. Jin
LiveSketch: query perturbations for guided sketch-based visual search
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 2874–2882
Cited by:
et al.
(2023)
G. Dong, Q. Xie, J. Li, Y. Ma, Y. Liu, and Y. Liu
A multi-scale and dense object detector for tibetan thangka images
Proceedings of the 5th ACM International Conference on Multimedia in Asia
pp. 1–7
Cited by:
et al.
(2024)
P. Gatti, K. Parikh, D. P. Paul, M. Gupta, and A. Mishra
Composite sketch+text queries for retrieving objects with elusive names and complex interactions
Proceedings of the AAAI Conference on Artificial Intelligence
pp. 1869–1877
Cited by:
§3.3.2
et al.
(2024)
G. Gu, S. Chun, W. Kim, Y. Kang, and S. Yun
Language-only efficient training of zero-shot composed image retrieval
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 13225–13234
Cited by:
Table 2
et al.
(2025)
A. Hu, Y. Sun, J. Li, Y. Ma, Q. Xie, and Y. Liu
TOVect: topology-optimized vectorization for intangible cultural heritage thangka element line art
Proceedings of the 7th ACM International Conference on Multimedia in Asia
pp. 1–7
Cited by:
et al.
(2024)
Y. Huo, Q. Qin, J. Dai, L. Wang, W. Zhang, L. Huang, and C. Wang
Deep semantic-aware proxy hashing for multi-label cross-modal retrieval
IEEE Transactions on Circuits and Systems for Video Technology
pp. 576–589
Cited by:
et al.
(2021)
C. Jia, Y. Yang, Y. Xia, Y. Chen, Z. Parekh, H. Pham, Q. Le, Y. Sung, Z. Li, and T. Duerig
Scaling up visual and vision-language representation learning with noisy text supervision
International Conference on Machine Learning
pp. 4904–4916
Cited by:
Jiang and Ye (2023)
D. Jiang and M. Ye
Cross-modal implicit relation reasoning and aligning for text-to-image person retrieval
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 2787–2797
Cited by:
et al.
(2024)
X. Jiang, Y. Wang, M. Li, Y. Wu, B. Hu, and X. Qian
CaLa: complementary association learning for augmenting comoposed image retrieval
Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval
pp. 2177–2187
Cited by:
Table 2
Karthik
et al.
(2024)
S. Karthik, K. Roth, M. Mancini, and Z. Akata
Vision-by-language for training-free compositional image retrieval
International Conference on Learning Representations
Cited by:
et al.
(2024)
S. Koley, A. K. Bhunia, A. Sain, P. N. Chowdhury, T. Xiang, and Y. Song
You’ll never walk alone: a sketch and text duet for fine-grained image retrieval
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 16509–16519
Cited by:
et al.
(2020)
J. Lei, Y. Song, B. Peng, Z. Ma, L. Shao, and Y. Song
Semi-heterogeneous three-way joint embedding network for sketch-based image retrieval
IEEE Transactions on Circuits and Systems for Video Technology
pp. 3226–3237
Cited by:
et al.
(2026)
J. Li, H. Wang, X. Peng, J. Xu, Q. Xie, Y. Ma, W. Jiang, and M. Tang
Guided by principles of composition: a domain-specific priors based detector for recognizing ritual implements in thangka
IET Image Processing
pp. e70271
Cited by:
et al.
(2025)
Z. Li, Z. Chen, H. Wen, Z. Fu, Y. Hu, and W. Guan
Encoder: entity mining and modification relation binding for composed image retrieval
Proceedings of the AAAI Conference on Artificial Intelligence
pp. 5101–5109
Cited by:
Table 2
et al.
(2022)
Z. Ling, Z. Xing, J. Li, and L. Niu
Multi-level region matching for fine-grained sketch-based image retrieval
Proceedings of the 30th ACM International Conference on Multimedia
pp. 462–470
Cited by:
et al.
(2021)
Z. Liu, C. Rodriguez-Opazo, D. Teney, and S. Gould
Image retrieval on real-life images with pre-trained vision-and-language models
Proceedings of the IEEE/CVF International Conference on Computer Vision
pp. 2105–2114
Cited by:
et al.
(2024)
Z. Liu, W. Sun, Y. Hong, D. Teney, and S. Gould
Bi-directional training for composed image retrieval via text prompt learning
Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision
pp. 5753–5762
Cited by:
Table 2
Table 2
et al.
(2024)
C. Lülf, D. M. Lima Martins, M. A. Vaz Salles, Y. Zhou, and F. Gieseke
CLIP-branches: interactive fine-tuning for text-image retrieval
Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval
pp. 2719–2723
Cited by:
OpenAI (2024)
OpenAI
GPT-4o mini model
External Links:
Cited by:
§4.3.4
OpenAI (2025)
OpenAI
GPT-4.1 model
External Links:
Cited by:
§4.3.4
Paszke
et al.
(2019)
A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, A. Desmaison, A. Köpf, E. Yang, Z. DeVito, M. Raison, A. Tejani, S. Chilamkurthy, B. Steiner, L. Fang, J. Bai, and S. Chintala
Pytorch: an imperative style, high-performance deep learning library
Cited by:
et al.
(2016)
Y. Qi, Y. Song, H. Zhang, and J. Liu
Sketch-based image retrieval via siamese convolutional neural network
2016 IEEE International Conference on Image Processing
pp. 2460–2464
Cited by:
Radford
et al.
(2021)
A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, G. Krueger, and I. Sutskever
Learning transferable visual models from natural language supervision
International Conference on Machine Learning
pp. 8748–8763
Cited by:
et al.
(2024)
H. Ren, K. Sun, F. Zhao, and X. Zhu
Dunhuang murals image restoration method based on generative adversarial network
Heritage Science
pp. 39
Cited by:
et al.
(2023)
A. Sain, A. K. Bhunia, S. Koley, P. N. Chowdhury, S. Chattopadhyay, T. Xiang, and Y. Song
Exploiting unlabelled photos for stronger fine-grained sbir
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 6873–6883
Cited by:
et al.
(2023)
K. Saito, K. Sohn, X. Zhang, C. Li, C. Lee, K. Saenko, and T. Pfister
Pic2Word: mapping pictures to words for zero-shot composed image retrieval
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 19305–19314
Cited by:
Table 2
Seddati
et al.
(2017)
O. Seddati, S. Dupont, and S. Mahmoudi
Triplet networks feature masking for sketch-based image retrieval
International Conference on Image Analysis and Recognition
pp. 296–303
Cited by:
Sharma
et al.
(2018)
P. Sharma, N. Ding, S. Goodman, and R. Soricut
Conceptual captions: a cleaned, hypernymed, image alt-text dataset for automatic image captioning
Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
pp. 2556–2565
Cited by:
et al.
(2022)
H. Sun, J. Xu, J. Wang, Q. Qi, C. Ge, and J. Liao
DLI-net: dual local interaction network for fine-grained sketch-based image retrieval
IEEE Transactions on Circuits and Systems for Video Technology
pp. 7177–7189
Cited by:
et al.
(2024)
S. Sun, F. Ye, and S. Gong
Training-free zero-shot composed image retrieval with local concept reranking
External Links:
2312.08924
Cited by:
et al.
(2026)
Y. Sun, J. Xu, Q. Xie, J. Li, Y. Ma, and Y. Liu
SDR-cir: semantic debias retrieval framework for training-free zero-shot composed image retrieval
Proceedings of the ACM Web Conference 2026
pp. 2149–2159
Cited by:
et al.
(2025)
Z. Sun, D. Jing, and Z. Lu
CoTMR: chain-of-thought multi-scale reasoning for training-free zero-shot composed image retrieval
Proceedings of the IEEE/CVF International Conference on Computer Vision
pp. 22675–22684
Cited by:
Table 2
et al.
(2024)
Y. Suo, F. Ma, L. Zhu, and Y. Yang
Knowledge-enhanced dual-stream zero-shot composed image retrieval
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 26941–26952
Cited by:
et al.
(2024)
Y. Tang, J. Yu, K. Gai, J. Zhuang, G. Xiong, Y. Hu, and Q. Wu
Context-i2w: mapping images to context-dependent words for accurate zero-shot composed image retrieval
Proceedings of the AAAI Conference on Artificial Intelligence
pp. 5180–5188
Cited by:
Table 2
et al.
(2025)
Y. Tang, J. Zhang, X. Qin, J. Yu, G. Gou, G. Xiong, Q. Lin, S. Rajmohan, D. Zhang, and Q. Wu
Reason-before-retrieve: one-stage reflective chain-of-thoughts for training-free zero-shot composed image retrieval
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 14400–14410
Cited by:
Table 2
et al.
(2023)
S. Vaze, N. Carion, and I. Misra
GeneCIS: a benchmark for general conditional image similarity
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 6862–6872
Cited by:
et al.
(2019)
N. Vo, L. Jiang, C. Sun, K. Murphy, L. Li, L. Fei-Fei, and J. Hays
Composing text and image for image retrieval - an empirical odyssey
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 6432–6441
Cited by:
et al.
(2025)
L. Wang, W. Ao, V. N. Boddeti, and S. Lim
Generative zero-shot composed image retrieval
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 29690–29700
Cited by:
et al.
(2021)
N. Wang, W. Wang, W. Hu, A. Fenster, and S. Li
Thanka mural inpainting based on multi-scale adaptive partial convolution and stroke-like mask
IEEE Transactions on Image Processing
pp. 3720–3733
Cited by:
et al.
(2024)
P. Wang, S. Bai, S. Tan, S. Wang, Z. Fan, J. Bai, K. Chen, X. Liu, J. Wang, W. Ge, Y. Fan, K. Dang, M. Du, X. Ren, R. Men, D. Liu, C. Zhou, J. Zhou, and J. Lin
Qwen2-vl: enhancing vision-language model’s perception of the world at any resolution
arXiv preprint arXiv:2409.12191
Cited by:
§4.3.4
et al.
(2021)
H. Wu, Y. Gao, X. Guo, Z. Al-Halah, S. Rennie, K. Grauman, and R. Feris
Fashion iq: a new dataset towards retrieving images by natural language feedback
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
pp. 11302–11312
Cited by:
et al.
(2026)
J. Xu, Q. Xie, J. Li, Z. Bao, Y. Ma, and Y. Liu
Enhancing fine-grained sketch-based image retrieval through contextual information
IEEE Transactions on Multimedia
pp. 1–12
Cited by:
et al.
(2024a)
Z. Yang, S. Qian, D. Xue, J. Wu, F. Yang, W. Dong, and C. Xu
Semantic editing increment benefits zero-shot composed image retrieval
Proceedings of the 32nd ACM International Conference on Multimedia
pp. 1245–1254
Cited by:
Table 2
et al.
(2024b)
Z. Yang, D. Xue, S. Qian, W. Dong, and C. Xu
LDRE: llm-based divergent reasoning and ensemble for zero-shot composed image retrieval
Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval
pp. 80–90
Cited by:
Table 2
et al.
(2022)
L. Yao, R. Huang, L. Hou, G. Lu, M. Niu, H. Xu, X. Liang, Z. Li, X. Jiang, and C. Xu
FILIP: fine-grained interactive language-image pre-training
International Conference on Learning Representations
Cited by:
et al.
(2021)
Y. Zheng, H. Yao, and X. Sun
Deep semantic parsing of freehand sketches with homogeneous transformation, soft-weighted loss, and staged learning
IEEE Transactions on Multimedia
pp. 3590–3602
Cited by:
Experimental support, please
view the build logs
for errors. Generated by
Instructions for reporting errors
We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile
support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the
methods listed below:
Click the "Report Issue"
button, located in the page header.
You can select the relevant text first, to include it in your report.
Our team has already identified
the following issues
. We appreciate your time reviewing and reporting rendering errors we
may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability
should not be a barrier to accessing research. Thank you for your continued support in championing open access for
Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a
list of packages that need conversion
, and welcome
developer contributions
We gratefully acknowledge support from
major funders
member institutions
and all contributors.
Contact
Subscribe
Copyright
Privacy
Accessibility
Operational Status
(opens in new tab)
Major funding support from