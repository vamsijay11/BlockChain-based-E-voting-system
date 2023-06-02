**Blockchain Based Voting System**

It is a simple decentralized blockchain based voting system that has security aspects. Everyone has the right to vote only once with their id. 
The system ensures that the information of all nodes is up to date. Nodes can operate as a voting system or a mining system. The network is written in flask.

**Master Node**
The system uses a master node to identify the rest of the nodes to the network. A new node sends its information to the master node at startup.

**The structure of a block**
> {
>     "index": 2,
>     "previous_hash": "d1a58a4282dc18cd726fbe25198b034588b959106458472b23473c9caddb589e",
>     "proof": 35293,
>     "timestamp": 1644346339.117375,
>     "votes": [
>         {
>             "person_id": "5e1f08494c9f50dbaf5a7fd864fe0722996094d8d9044418225ea9ad2debde6c",
>             "vote": "100"
>         }
>     ]
> }
