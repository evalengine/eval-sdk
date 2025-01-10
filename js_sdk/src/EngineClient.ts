import { createClient, decodeTransactionToGtx, encodeTransaction, IClient, NetworkSettings, newSignatureProvider, Operation, SignatureProvider } from "postchain-client";
import { chainConfig, CHROMIA_CHAIN } from "./config";

interface UpdateTweetScoresArgs {
    finalScore: string;
    truthScore: string;
    accuracyScore: string;
    creativityScore: string;
    engagementScore: string;
    truthRationale: string;
    accuracyRationale: string;
    creativityRationale: string;
    engagementRationale: string;
    engagementImprovementTips: string;
    recommendedResponse: string;
}

export class EngineClient {
    protected static instance: EngineClient;
    client: IClient;
    signatureProvider: SignatureProvider;
    config: NetworkSettings;

    constructor(
        protected readonly privateKey: string,
        client: IClient,
        config: NetworkSettings
    ) {
        this.config = config;
        this.client = client;
        this.signatureProvider = newSignatureProvider({
            privKey: this.privateKey,
        });
    }

    static async init(
        privateKey: string,
        chain = CHROMIA_CHAIN.MAINNET
    ) {
        const client = await createClient({
            ...chainConfig[chain],
        });
        return new EngineClient(privateKey, client, chainConfig[chain]);
    }

    async getEngine() {
        return this.client.query<{
            id: string;
            name: string;
            prefix: string;
            address: Buffer;
            created_at: string;
        }>("get_engine_by_address", { address: this.signatureProvider.pubKey });
    }

    async checkEngineExists() {
        const engine = await this.getEngine();
        return engine !== undefined;
    }

    async runTweetScoreEngine(txHex: string, evaluatePromise: (inputTweet: string, outputTweet: string) => Promise<UpdateTweetScoresArgs>) {
        const txBuffer = Buffer.from(txHex, "hex");
        const tx = decodeTransactionToGtx(txBuffer);
        const operations = tx.operations;
        if (operations.length !== 1) {
            throw new Error("Invalid transaction");
        }

        const operation = operations[0];
        const operationName = operation.opName;
        const operationArgs = operation.args;
        if (operationName !== "evaluate_tweet_request") {
            throw new Error("Invalid operation");
        } else if (operationArgs === undefined || operationArgs.length !== 3) {
            throw new Error("Invalid operation arguments");
        }
        const requestUid = operationArgs[0] as string;
        const inputTweet = operationArgs[1] as string;
        const outputTweet = operationArgs[2] as string;
        const signedTx = await this.client.signTransaction(encodeTransaction(tx), this.signatureProvider);
        const submittedTx = await this.client.sendTransaction(signedTx);
        const result = await evaluatePromise(inputTweet, outputTweet);
        const uniqueIdentifier = tx.signers[0].toString("hex");
        await this.updateTweetScores(requestUid, uniqueIdentifier, result);
        return {
            result,
            submittedTx
        };
    }

    async updateTweetScores(
        requestUid: string,
        uniqueIdentifier: string,
        args: UpdateTweetScoresArgs 
    ) {
        const { finalScore, truthScore, accuracyScore, creativityScore, engagementScore, truthRationale, accuracyRationale, creativityRationale, engagementRationale, engagementImprovementTips, recommendedResponse } = args;
        return this.client.signAndSendUniqueTransaction({
            name: "update_tweet_scores",
            args: [
                requestUid,
                uniqueIdentifier,
                finalScore,
                truthScore,
                accuracyScore,
                creativityScore,
                engagementScore,
                truthRationale,
                accuracyRationale,
                creativityRationale,
                engagementRationale,
                engagementImprovementTips,
                recommendedResponse
            ]
        }, this.signatureProvider);
    }


}
