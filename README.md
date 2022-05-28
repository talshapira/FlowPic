# FlowPic: A Generic Representation for Encrypted Traffic Classification and Applications Identification

Identifying the type of a network flow or a specific application has many advantages, but become harder in recent years due to the use of encryption, e.g., by VPN and Tor. 
Current solutions rely mostly on handcrafted features and then apply supervised learning techniques for the classification. 
	
We introduce a novel approach for encrypted Internet traffic classification and application identification by transforming basic flow data into a picture, em a FlowPic, and then using known image classification deep learning techniques, Convolutional Neural Networks (CNNs), to identify the flow category (browsing, chat, video, etc.) and the application in use.  Our approach can classify traffic with high accuracy, both for a specific application, or a flow category, even for VPN and Tor traffic. Our classifier can even identify with high success new applications that were not part of the training phase for a category, thus, new versions or applications can be categorized without additional training.

A recent [work](https://arxiv.org/abs/2104.03182) by Yang et al. compared different recent methods for Internet Traffic Classification, and showed that our method achieves the best tradeoff between accuracy and model complexity, as shown below (FlowPic marked with [17]):

<p align="center">
<img src='http://talshapira.github.io/files/yang_2021_comaprison.png' width="400">
</p>

# Approach

1. Extract records from each flow, which comprised of a list of pairs, {IP packet size, time of arrival} for each packet in the flow.
2. Split each unidirectional flow to equal blocks (15/60 seconds).
3. Generate 2D-histogram. For simplicity, we set the 2D-histogram to be a square image.
4. Feed a Convolution Neural Network.

<img src='http://talshapira.github.io/files/FlowPic_sys.png'>


# FlowPics Exploration

<img src='http://talshapira.github.io/files/flowpic_categories.png'>

<p align="center">
<img src='http://talshapira.github.io/files/flowpic_apps.png' width="400">
</p>

# Dataset

We use labeled datasets of packet capture (pcap) files from the Uni. of New Brunswick (UNB): ["ISCX VPN-nonVPN traffic dataset" (ISCX-VPN)](https://www.unb.ca/cic/datasets/vpn.html) and ["ISCX Tor-nonTor dataset" (ISCX-Tor)](https://www.unb.ca/cic/datasets/tor.html), as well as our own small packet capture (TAU), and conduct different types of experiments; (1) multiclass classification experiments over non-VPN/VPN/Tor and merged dataset, (2) class vs. all classification experiments, (3) application identification, and (4) classification of an unknown application.

Each pcap file corresponds to a specific application, a traffic category and an encryption technique. However, all these captures also contain sessions of different traffic categories, since while performing one action in an application, many other sessions occur for different tasks simultaneously. For example, while using VoIP over Facebook, there is another STUN session taking place at the same time for adjusting and maintaining the VoIP conversation, as well as an HTTPS session of the Facebook site.

We use a combined dataset only from the five categories that contains enough samples: VoIP, Video, Chat, Browsing, and File Transfer. For these categories we have 3 encryption techniques: non VPN, VPN (for all classes except Browsing) and TOR.
Notice that our categories differ slightly from those suggested by UNB. All the applications that were captured in order to create the dataset, for each traffic category and encryption technique, are shown in the folowing table:

<p align="center">
<img src='http://talshapira.github.io/files/flowpic_dataset.png' width="600">
</p>

We parsed the pcap files and constructed for each combination of traffic category and encryption technique a CSV file with the following structure - 
|pcap_name|ip_src|port_src|ip_dst|port_dst|TCP/UDP|start_time|length|[timestamps_list]|[sizes_list]| , such that each entry corresponds to a specific unidirectional session.

# TrafficParser

Contains the code use to generate the dataset (npy files) per experiment.
If you choose to use our proceesed dataset (i.e. CSV files) directly, run the scripts in the following order:
1. Run traffic_csv_converter.py
2. Run datasets_generator.py

The other two scripts (generic_parser.py + traffic_csv_merger.py) used to generate the proceesed dataset.

# License

Our proceesed dataset (i.e. CSV files) is [publicly available](https://drive.google.com/file/d/1gz61vnMANj-4hKNvZv1KFK9LajR91X-m/view?usp=sharing) upon request for researchers. If you are using our dataset, please cite our related research paper, as well as UNB's related research papers:

* T. Shapira and Y. Shavitt, "FlowPic: A Generic Representation for Encrypted Traffic Classification and Applications Identification," in IEEE Transactions on Network and Service Management, doi: 10.1109/TNSM.2021.3071441.

* T. Shapira and Y. Shavitt, "FlowPic: Encrypted Internet Traffic Classification is as Easy as Image Recognition," IEEE INFOCOM 2019 - IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS), Paris, France, 2019, pp. 680-687.

* Gerard Drapper Gil, Arash Habibi Lashkari, Mohammad Mamun, Ali A. Ghorbani, "Characterization of Encrypted and VPN Traffic Using Time-Related Features", In Proceedings of the 2nd International Conference on Information Systems Security and Privacy(ICISSP 2016) , pages 407-414, Rome, Italy.

* Arash Habibi Lashkari, Gerard Draper-Gil, Mohammad Saiful Islam Mamun and Ali A. Ghorbani, "Characterization of Tor Traffic Using Time Based Features", In the proceeding of the 3rd International Conference on Information System Security and Privacy, SCITEPRESS, Porto, Portugal, 2017.
