import { NetworkSettings } from "postchain-client";

export enum CHROMIA_CHAIN {
  MAINNET = "chromia-mainnet",
  // TESTNET = "chromia-testnet",
  LOCAL = "chromia-local",
}

export const chainConfig: {
  [key in CHROMIA_CHAIN]: NetworkSettings;
} = {
  [CHROMIA_CHAIN.MAINNET]: {
    directoryNodeUrlPool: [
      "https://dapps0.chromaway.com:7740",
      "https://chromia-mainnet.w3coins.io:7740",
      "https://mainnet-dapp1.sunube.net:7740",
      "https://chromia.01node.com:7740",
      "https://chromia-mainnet.caliber.build:443",
      "https://chromia.nocturnallabs.org:7740",
      "https://chromina-node.stablelab.xyz:7740"
    ],
    blockchainRid: "9E7D8243FE78287588E112384F8DC5F3E1CD35D48FD3BE41E46D8F17DD0BED65",
  },
  [CHROMIA_CHAIN.LOCAL]: {
    nodeUrlPool: ["http://localhost:7740"],
    blockchainIid: 0,
  },
};
