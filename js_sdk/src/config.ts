import { NetworkSettings } from "postchain-client";

export enum CHROMIA_CHAIN {
  MAINNET = "chromia-mainnet",
  TESTNET = "chromia-testnet",
  LOCAL = "chromia-local",
}

export const chainConfig: {
  [key in CHROMIA_CHAIN]: NetworkSettings;
} = {
  [CHROMIA_CHAIN.MAINNET]: {
    directoryNodeUrlPool: [
      "https://dapps0.chromaway.com:7740",
      "https://chromia-mainnet.w3coins.io:7740",
    ],
    blockchainRid: "",
  },
  [CHROMIA_CHAIN.TESTNET]: {
    directoryNodeUrlPool: [
      "https://dapps0.chromaway.com:7740",
      "https://chromia-mainnet.w3coins.io:7740",
    ],
    blockchainRid: "",
  },
  [CHROMIA_CHAIN.LOCAL]: {
    nodeUrlPool: ["http://localhost:7740"],
    blockchainIid: 0,
  },
};
