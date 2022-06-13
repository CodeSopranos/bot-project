import yaml
from utils.predict import DummyModel, AccentModel
from utils.denoise import Denoiser

# define env variables
LANG_CONFIG_PATH = 'utils/config.yml'
SAMPLES_PATH = 'models/phrases.txt'
ACCENT_MODEL_PATH = 'models/accent_model_indian.onnx'

# load dummy model
dummy_model = DummyModel()

# load used languages config
with open(LANG_CONFIG_PATH, 'r') as file:
    docs = yaml.safe_load_all(file)
    labels = []
    benchmark = []
    for doc in docs:
        if doc['benchmark']:
            benchmark.append(doc)
        labels.append(doc['label'])
        print(doc)

# load accent recognition model
accent_model = AccentModel(model_path=ACCENT_MODEL_PATH,
                           samples_path=SAMPLES_PATH,
                           lang_names=labels,
                           benchmark_langs=benchmark)

# load denoising model
denoiser_model = Denoiser(model_1='models/model_1.onnx', model_2='models/model_2.onnx')
