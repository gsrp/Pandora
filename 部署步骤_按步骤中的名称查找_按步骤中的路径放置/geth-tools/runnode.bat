
geth --datadir D:\gsrpchain init gsrp.json
geth --datadir D:\gsrpchain --allow-insecure-unlock --targetgaslimit 10712388 --nat none  --rpccorsdomain "*"  --rpc --rpcport 21024 --rpcaddr "0.0.0.0" --rpcapi db,eth,net,web3,personal,miner,clique,admin,txpool --syncmode full
