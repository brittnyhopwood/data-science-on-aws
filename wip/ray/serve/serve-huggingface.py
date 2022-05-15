from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from ray import serve
import ray

ray.init(address="auto",
         ignore_reinit_error=True)

@serve.deployment(route_prefix="/sentiment", name="sentiment")
class SentimentDeployment:
    def __init__(self):
        tokenizer = AutoTokenizer.from_pretrained("roberta-base")
        model = AutoModelForSequenceClassification.from_pretrained("./transformer/")
        self.classifier = pipeline(task="text-classification", model=model, tokenizer=tokenizer)

    async def __call__(self, request):
        data = await request.body()
        [result] = self.classifier(str(data))
        return result["label"]

serve.start(detached=True, 
            http_options={"port": 8001})

SentimentDeployment.deploy()