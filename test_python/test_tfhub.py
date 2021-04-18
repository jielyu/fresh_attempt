import os
os.environ['TFHUB_CACHE_DIR'] = os.path.join(os.path.expanduser('~/.tfhub_models'))

import tensorflow as tf
import tensorflow_hub as hub

#tf.enable_eager_execution()

module_url = "https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1"
embed = hub.KerasLayer(module_url)
embeddings = embed(["A long sentence.", "single-word",
                    "http://example.com"])
print(embeddings.shape)  #(3,128)
print(embeddings[0][:20])

