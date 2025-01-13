
import { CHROMIA_CHAIN } from "../src/config";
import { EvaClient } from "../src/EvaClient";
import { ENGINE_KEY, USER_KEY } from "./config";

console.log(USER_KEY.pub);

async function main() {
    const evaClient = await EvaClient.init(USER_KEY.priv, CHROMIA_CHAIN.MAINNET, {
        url: "http://localhost:8888/api/v1",
        prefix: "EVA",
        pub: "026822066B64608E0A6E071D8AE76BDE509011FF823DBBF9FD6AC2E1F202904A0A"
    });

    const engine = await evaClient.getEngine();
    console.log("engine", engine);

    const txHash = await evaClient.signEvaluateTweetRequest("Hello input", "Hello output");
    const response = await evaClient.submitEvaluateTweetRequest(txHash);
    
}

main();

