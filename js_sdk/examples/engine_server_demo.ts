import express from 'express';
import { EngineClient } from '../src/EngineClient';
import { CHROMIA_CHAIN } from '../src/config';
import dotenv from 'dotenv';

dotenv.config();
// import { ENGINE_KEY } from './config';
const ENGINE_KEY = {
    pub: process.env.ENGINE_KEY_PUB!,
    priv: process.env.ENGINE_KEY_PRIV!
};

const app = express();
app.use(express.json());

const port = 8888;

console.log(ENGINE_KEY.pub);

async function main() {
    const engine = await EngineClient.init(ENGINE_KEY.priv, CHROMIA_CHAIN.MAINNET);

    const engineInstance = await engine.getEngine();
    if (!engineInstance) {
        console.error("Engine not found, please contact admin to create a new engine");
        process.exit(1);
    }
    console.log(engineInstance.id);
    console.log(engineInstance.address.toString("hex"));
    console.log(engineInstance.prefix);
    console.log(engineInstance.created_at);

    app.post('/api/v1/eval/evaluate-tweet-request', async (req, res) => {
        try {
            const hash = req.body.hash;
            const result = await engine.runTweetScoreEngine(hash, async (inputTweet, outputTweet) => {
                // Run some NLP Workflow here

                return {
                    finalScore: "0.55",
                    truthScore: "0.4",
                    accuracyScore: "0.5",
                    creativityScore: "0.6",
                    engagementScore: "0.7",
                    truthRationale: "Test",
                    accuracyRationale: "Test",
                    creativityRationale: "Test",
                    engagementRationale: "Test",
                    engagementImprovementTips: "Test",
                    recommendedResponse: "Test"
                }
            })
            res.json({
                result: result.result,
                tx: result.submittedTx
            });
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Internal server error' });
        }
    });

    app.listen(port, () => {
        console.log(`Engine server listening on port ${port}`);
    });
}

main();