import uuid
from dataclasses import dataclass
from typing import Dict, Any, TypeVar, Type
from urllib.parse import urljoin, urlparse

from postchain_client_py import BlockchainClient, SignatureProvider, NetworkSettings

@dataclass
class EngineConfig:
    url: str
    prefix: str
    pub: str

T = TypeVar('T', bound='EvaClient')

class EvaClient:
    def __init__(
        self,
        private_key: str,
        client: BlockchainClient,
        config: NetworkSettings,
        engine: EngineConfig
    ):
        self.private_key = private_key
        self.config = config
        self.client = client
        self.signature_provider = SignatureProvider(priv_key=private_key)
        
        # Ensure URL doesn't end with '/'
        url = engine.url[:-1] if engine.url.endswith('/') else engine.url
        self.engine = EngineConfig(
            url=url,
            prefix=engine.prefix,
            pub=engine.pub
        )

    @classmethod
    async def init(
        cls: Type[T],
        private_key: str,
        chain_config: Dict[str, Any],
        engine: EngineConfig
    ) -> T:
        client = await BlockchainClient.create(chain_config)
        return cls(private_key, client, chain_config, engine)

    async def get_engine(self) -> Dict[str, Any]:
        engine = await self.client.query("get_engine_by_address", {"address": self.engine.pub})
        return engine

    def _generate_request_uid(self) -> str:
        return f"{self.engine.prefix}-{str(uuid.uuid4())}"

    async def sign_evaluate_tweet_request(self, input_tweet: str, output_tweet: str) -> str:
        request_uid = self._generate_request_uid()
        operation = {
            "name": "evaluate_tweet_request",
            "args": [request_uid, input_tweet, output_tweet]
        }
        
        signed_tx = await self.client.sign_transaction(
            operations=[operation],
            signers=[
                self.signature_provider.pub_key,
                bytes.fromhex(self.engine.pub)
            ],
            signature_provider=self.signature_provider
        )
        return signed_tx.hex()

    async def submit_evaluate_tweet_request(self, tx_hash: str) -> str:
        engine_path = urlparse(self.engine.url).path
        endpoint = 'eval/evaluate-tweet-request'
        full_url = urljoin(self.engine.url, f"{engine_path}/{endpoint}")
        
        print(full_url)
        async with self.client.rest_client.session.post(
            full_url,
            json={"hash": tx_hash},
            headers={"Content-Type": "application/json"}
        ) as response:
            data = await response.text()
            print(data)
            return data
