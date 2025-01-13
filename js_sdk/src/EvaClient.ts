import { createClient, IClient, NetworkSettings, newSignatureProvider, SignatureProvider } from "postchain-client";
import { chainConfig, CHROMIA_CHAIN } from "./config";
import { v4 as uuidv4 } from 'uuid';

interface EngineConfig {
  url: string;
  prefix: string;
  pub: string;
}

export class EvaClient {
  protected static instance: EvaClient;
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

  static async init<T extends EvaClient>(
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
    const signedTx = await this.client.signTransaction({
        operations: [
            operation
        ],
        signers: [
            this.signatureProvider.pubKey,
            Buffer.from(this.engine.pub, "hex")
        ]
    }, this.signatureProvider);
    return signedTx.toString("hex");
  }

  async submitEvaluateTweetRequest(txHash: string): Promise<{
    result: any,
    tx: string
  }> {
    const engineUrl = new URL(this.engine.url).pathname + '/eval/evaluate-tweet-request';
    const fullUrl = new URL(engineUrl, this.engine.url).toString();
    const response = await fetch(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ hash: txHash })
    });
    const data = await response.json();
    return data;

  }
}
