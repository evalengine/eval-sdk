import { createClient, IClient, NetworkSettings, newSignatureProvider, SignatureProvider } from "postchain-client";
import { chainConfig, CHROMIA_CHAIN } from "./config";
import { v4 as uuidv4 } from 'uuid';

interface EngineConfig {
  url: string;
  prefix: string;
  pub: string;
}

export interface EvalTweetResponse {
  input_hash: string
  output_hash: string
  truth_score: number
  accuracy_score: number
  creativity_score: number
  engagement_score: number
  final_score: number
  truth_rationale: string
  accuracy_rationale: string
  creativity_rationale: string
  engagement_rationale: string
  engagement_improvement_tips: string
  recommended_response: string
}

export class EvalClient {
  protected static instance: EvalClient;
  public engine: EngineConfig;
  public client: IClient;
  public signatureProvider: SignatureProvider;
  public config: NetworkSettings;

  constructor(
    protected readonly privateKey: string,
    client: IClient, 
    config: NetworkSettings,
    engine: EngineConfig
  ) {
    this.config = config;
    this.client = client;
    this.signatureProvider = newSignatureProvider({
      privKey: this.privateKey,
    });
    this.engine = {    
      url: engine.url.endsWith('/') ? engine.url.slice(0, -1) : engine.url,
      prefix: engine.prefix,
      pub: engine.pub
    }
  }

  static async init<T extends EvalClient>(
    this: new (privateKey: string, client: IClient, config: NetworkSettings, engine: EngineConfig) => T,
    privateKey: string,
    chain: CHROMIA_CHAIN,
    engine: EngineConfig
  ): Promise<T> {
    const client = await createClient({
      ...chainConfig[chain],
    });
    const instance = new this(privateKey, client, chainConfig[chain], engine);
    return instance as T;
  }

  async getEngine() {
    const engine = await this.client.query("get_engine_by_address", { address: this.engine.pub });
    return engine;
  }

  private generateRequestUid(): string {
    return this.engine.prefix + "-" + uuidv4();
  }

  async signEvaluateTweetRequest(inputTweet: string, outputTweet: string): Promise<string> {
    const requestUid = this.generateRequestUid();
    const operation = {
        name: "evaluate_tweet_request",
        args: [requestUid, inputTweet, outputTweet]
    };
    const nopOperation = {
      name: "nop",
      args: []
  };

    const signedTx = await this.client.signTransaction({
        operations: [
            operation,
            nopOperation
        ],
        signers: [
            this.signatureProvider.pubKey,
            Buffer.from(this.engine.pub, "hex")
        ]
    }, this.signatureProvider);
    return signedTx.toString("hex");
  }

  async submitEvaluateTweetRequest(txHash: string): Promise<EvalTweetResponse> {
    const engineUrl = new URL(this.engine.url).pathname + '/eval/evaluate-tweet-request';
    const fullUrl = new URL(engineUrl, this.engine.url).toString();
    const response = await fetch(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ hash: txHash })
    });
    if (!response.ok) {
      throw new Error(`Failed to submit evaluate tweet request: ${response.statusText}`);
    }
    const data: EvalTweetResponse = await response.json();
    return data;

  }
}
