
import { CHROMIA_CHAIN } from "../src/config";
import { EvaClient } from "../src/EvaClient";
import { ENGINE_KEY, USER_KEY } from "./config";

console.log(USER_KEY.pub);

async function main() {
    const evaClient = await EvaClient.init(USER_KEY.priv, CHROMIA_CHAIN.LOCAL, {
        url: "http://localhost:8888/api/v1",
        prefix: "TEST2",
        pub: ENGINE_KEY.pub
    });

    const engine = await evaClient.getEngine();
    console.log("engine", engine);

    const txHash = await evaClient.signEvaluateTweetRequest("Hello input", "Hello output");
    console.log(txHash);

    const response = await evaClient.submitEvaluateTweetRequest(txHash);
    console.log(response);
    
}

main();

