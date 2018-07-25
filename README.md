# ewasm testnet coordination / documentation repo

### Test net differences from main net

Supports executing EVM 1.0 (Byzantium) **and** eWASM bytecode. The chain id is set to 0x42 (66).

There are two differences:
- code size limit introduced by Spurious Dragon has been lifted and there is no upper limit
- zero bytes in contract bytecode are not subsidised anymore during deployment (they cost the same as non-zero bytes)


### Docker

To get up and running quickly using Docker, simply `docker build -t ethereum/ewasm-testnet .`.

The `docker run` command should be parameterized (i.e., using the `-e` flag to set environment variables in the running container). The following parameters are currently exposed:

| Environment Variable      | Description                                               | Default                                                                                   |
|---                        |---                                                        |---                                                                                        |
| `BASE_PATH`               | prefix where blockchain lives on disk                     | the directory containing the running instance of `cpp-eth.sh`
| `CHAIN`                   | name of the chain; useful when this matches a ref in git  | master
| `CHAIN_SPEC`              | path to the chain spec JSON                               | `${BASE_PATH}/ewasm-spec.json`
| `CHAIN_SPEC_URL`          | arbitrary URL from which the chain spec JSON will be read | https://raw.githubusercontent.com/ewasm/testnet/${CHAIN}/ewasm-testnet-cpp-config.json
| `PEER_SET`                | list of enodes for p2p discovery                          | the contents of `./enodes.txt`, if it exists
| `DB_PATH`                 | path to the chain-specific database                       | `${BASE_PATH}/${CHAIN}`
| `EVMC_FALLBACK`           | EVM-C `fallback` option                                   | true
| `ASK`                     | tx ask price, in wei                                      | 0
| `BID`                     | tx bid price, in wei                                      | 20000000000
| `COINBASE`                | address to which block rewards will be sent               | 0x0000000000000000000000000000000000000000
| `IPC_PATH`                | path to the domain socket                                 | `${BASE_PATH}/geth.ipc`
| `JSON_RPC_PORT`           | port on which the JSON-RPC proxy will listen              | 8545
| `JSON_RPC_PROXY_PY`       | path to the JSON-RPC proxy python file                    | /usr/local/bin/jsonrpcproxy.py
| `JSON_RPC_PROXY_URL`      | endpoint where the JSON-RPC proxy will be listening       | http://0.0.0.0:8545
| `LISTEN_IP`               | local ip on which node accepts inbound p2p connections    | 0.0.0.0
| `LISTEN_PORT`             | local port where node accepts inbound p2p connections     | 30303
| `LOG_VERBOSITY`           | log level                                                 | 2
| `LOG_PATH`                | path to logfile                                           | `${BASE_PATH}/cpp-ethereum.log`
| `MINING`                  | whether or not the node is mining                         | on
| `MINING_THREADS`          | number of threads to allocate to mining                   | 1
| `NETWORK_ID`              | network id                                                | 66
| `MODE`                    | full or peer                                              | full
| `PORT`                    | remote p2p port                                           | 30303
| `PUBLIC_IP`               | IP address to advertise for disco                         | public IP address resolved using ipify.org
| `VM`                      | path to the VM lib                                        | /usr/local/lib/libhera.so


### cpp-ethereum

To build cpp-ethereum with the recent eWASM changes use [ewasm](https://github.com/ethereum/cpp-ethereum/tree/ewasm).

The `eth`, `ethvm` and `testeth` contain options to run them with [Hera eWASM VM](https://github.com/ewasm/hera):

- `--vm hera` enables Hera only,
- `--evmc fallback=true` enables fallback to EVM 1.0 Interpreter when EVM bytecode is detected.

### Run eth node

The config is in [ewasm-testnet-cpp-config.json](ewasm-testnet-cpp-config.json).

Example node with mining on single CPU core, with no bootstrap:

```sh
eth \
--vm hera \
--evmc fallback=true \
-d /tmp/ewasm-node/4201 \
--listen 4201 \
--no-bootstrap \
-m on \
-t 1 \
-a 0x031159dF845ADe415202e6DA299223cb640B9DB0 \
--config ewasm-testnet-cpp-config.json \
--peerset "required:61e5475e6870260af84bcf61c02b2127a5c84560401452ae9c99b9ff4f0f343d65c9e26209ec32d42028b365addba27824669eb70c73f69568964f77433afbbe@127.0.0.1:1234"
```

### JSON-RPC over HTTP

The cpp-ethereum (eth) does not have the HTTP server built in, the JSON-RPC requests are served only via an Unix Socket file.
By default, the location of the socket file is `<data-dir>/geth.ipc` (yes, **geth**).

The cpp-ethereum repo includes a Python3 script called jsonrpcproxy.py located in [scripts/jsonrpcproxy.py](https://github.com/ethereum/cpp-ethereum/blob/develop/scripts/jsonrpcproxy.py).

Run it as

```sh
./jsonrpcproxy.py <data-dir>/geth.ipc
```

See `jsonrcpproxy.py --help` for more options.

## Tests

Learn how to create and run ewasm tests [here](https://github.com/ewasm/tests/blob/06e0c19e117b48adcc6dd07def286d65b7e63f41/src/GeneralStateTestsFiller/stEWASMTests/README.md).
