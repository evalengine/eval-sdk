
import { CHROMIA_CHAIN } from "../src/config";
import { EvalClient } from "../src/EvalClient";
import { ENGINE_KEY, USER_KEY } from "./config";

console.log(USER_KEY.pub);

async function main() {
    const evalClient = await EvalClient.init(USER_KEY.priv, CHROMIA_CHAIN.MAINNET, {
        url: "https://api.evalengine.ai/api",
        prefix: "EVA",
        pub: "026822066B64608E0A6E071D8AE76BDE509011FF823DBBF9FD6AC2E1F202904A0A"
    });

    const engine = await evalClient.getEngine();
    console.log("engine", engine);

    const txHash = await evalClient.signEvaluateTweetRequest("Hello input 2", "Hello output 2");
    console.log("txHash", txHash);
    const response = await evalClient.submitEvaluateTweetRequest(txHash);
    console.log("response", JSON.stringify(response, null, 2));
}

main();

