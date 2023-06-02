**Blockchain Based Voting System**

It is a simple decentralized blockchain based voting system that has security aspects. Everyone has the right to vote only once with their id. 
The system ensures that the information of all nodes is up to date. Nodes can operate as a voting system or a mining system. The network is written in flask.


**Master Node**
The system uses a master node to identify the rest of the nodes to the network. A new node sends its information to the master node at startup.


**The structure of a block**

```
{
    "index": 2,
    "previous_hash": "d1a58a4282dc18cd726fbe25198b034588b959106458472b23473c9caddb589e",
    "proof": 35293,
    "timestamp": 1644346339.117375,
    "votes": [
        {
            "person_id": "5e1f08494c9f50dbaf5a7fd864fe0722996094d8d9044418225ea9ad2debde6c",
            "vote": "100"
        }
    ]
}
```

**Installation**


First, make sure you have the following packages installed.

>sudo apt install python3-pip python3-venv


run run.py 


run blockchain.py 


**PROJECT SCRRENSHOTS**

<img width="704" alt="image" src="https://github.com/vamsijay11/BlockChain-based-E-voting-system/assets/63055979/64fe8cdd-d4fe-4083-85dd-9e930d697921">


<img width="694" alt="image" src="https://github.com/vamsijay11/BlockChain-based-E-voting-system/assets/63055979/faeb64fa-6ad3-4b76-b1ca-6b88f609ced2">

<img width="521" alt="image" src="https://github.com/vamsijay11/BlockChain-based-E-voting-system/assets/63055979/a1d08392-4408-4dca-8f1d-5a1593a20a74">


