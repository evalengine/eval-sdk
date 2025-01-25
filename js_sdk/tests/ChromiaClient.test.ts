import { decodeTransactionToGtx } from "postchain-client";
import { EvalClient } from "../src/EvalClient";
import { CHROMIA_CHAIN } from "../src/config";

const OWNER_KEY = "01010101010101010101010101010101010101010101010101010101010101012";
const ENGINE_OWNER_KEY = "01010101010101010101010101010101010101010101010101010101010101013";
const DEVELOPER_KEY = "01010101010101010101010101010101010101010101010101010101010101014";

describe("ChromiaClient", () => {

  let developer: EvalClient;

  beforeAll(async () => {
    developer = await EvalClient.init(
      DEVELOPER_KEY,
      CHROMIA_CHAIN.LOCAL,
      {
        url: "http://localhost:8888",
        prefix: "TEST",
        pub: developer.signatureProvider.pubKey.toString("hex")
      }
    );
  });

  it("should be able to sign and submit a transaction", async () => {
    const signedTx = await developer.signEvaluateTweetRequest(
      "Hello input",
      "Hello output"
    );

    const decodedTx = decodeTransactionToGtx(Buffer.from(signedTx, "hex"))
    const signerKey = developer.signatureProvider.pubKey.toString("hex")
    expect(decodedTx.signers[0].toString("hex")).toBe(signerKey);
  });

});
