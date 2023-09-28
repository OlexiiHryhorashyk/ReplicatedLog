# ReplicatedLog
Replicated log task for Distributed Systems cource on UCU Data Engineering ctrtification program. 
This is the first iteration of the task (ReplicatedLogV1).
Demonstration project for distributed message replication. 
For convenience I united this files in Pycharm project, but for deploy we will be using Docker.
Each python server file will be wrapped as separate docker container inside one network which communicates using http requests. 
For deployment of these containers created Docker compose .yml file.
Consist with 4 python files:
 - server.py - Master node, which can recive message from client as http POST request. Saves the message locally, and replicates the message to each secondary node with http POST request. Also can return to the client list of saved messages using http GET request.
 - sub_server1/sub_server2 - secondary nodes, can recieve and save the message form master node as POST request. Also return to the client list of saved messages as GET request.
 - terminal_client - simple file to simulate a client, which recieves messages from terminal and send it to master node as POST requests, also can list messages from each node by making GET request to master and secondary nodes.
Also consist of 3 Dockerfile for each node for separate container deployment. And one Docker compose file (docker-compose.yml) for running all three nodes together inside one network.
For running this progect you need:
1. Clone this repository.
2. docker-compose build
3. docker-compose up
4. Run terminal_client.py in Pycharm or in command shell: python terminal_client.py

   Terminal log will recive any message, and send it to master. Have 3 keywords: list/list master, list sub1, list sub2 - makes GET request to coresponding node, to list saved messages of the node.
   
   Logs of all three nodes can be seen in a terminal, where was executed docker-compose file. Logs of each separeted node can be viewed in Desktop or by running:
   
   docker logs main/node1/node2.
