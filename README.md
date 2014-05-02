Social Event Detection
======================
As social media content proliferate, finding digital content related to a social
event of interest is a difficult task, requiring to search large volumes of data, possibly at
different sources and sites. Algorithms that can support humans in this task are clearly
needed. In this project, we aim to discover event-related multimedia and organize them in
event-specific clusters, within a collection of Web multimedia. This may provide the
basis for aggregation and search applications that foster easier discovery, browsing and
querying of social events.


Data
====
1. Get data from [here](http://skuld.cs.umass.edu/traces/mmsys/2013/social2012/)
2. create folder ../res
3. Place \*\_events.txt, metadata.xml
4. create folder ../res/photos and place all the photos in it.


Running
=======
Order of scripts to be run
1. filter.py
2. feature_gen.py
3. feature_sift_gen.py
4. tfidf.py
5. distance_svm.py
6. cluster.py 
7. accuracy.py (optional)

Reference
=========
"Social Event Detection using Multimodal Clustering and Integrating Supervisory Signals", Georgios Petkos, Symeon Papadopoulos, Yiannis Kompatsiaris, ICMR ’12, June 5-8, Hong Kong, China
