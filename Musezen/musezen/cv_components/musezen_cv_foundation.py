# -*- coding: utf-8 -*-
"""musezen_cv_foundation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17i7imITXVc0GnuVUuA7XW-reEfbVHMiZ
"""

import torchvision.models as models
from torchvision import transforms
import torch.nn as nn
import os
import torch
from PIL import Image
from io import BytesIO


class musezen_cv:
    def __init__(
        self,
        model_weight_path=os.path.join(
            "Musezen", "musezen", "cv_components", "model_weights_freezed.pt"
        ),
    ):
        self.model = models.resnet50(pretrained=False)
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, 27)
        state_dict = torch.load(model_weight_path)
        self.model.load_state_dict(state_dict)
        self.idx_to_class = {
            0: "Abstract_Expressionism",
            1: "Action_painting",
            2: "Analytical_Cubism",
            3: "Art_Nouveau_Modern",
            4: "Baroque",
            5: "Color_Field_Painting",
            6: "Contemporary_Realism",
            7: "Cubism",
            8: "Early_Renaissance",
            9: "Expressionism",
            10: "Fauvism",
            11: "High_Renaissance",
            12: "Impressionism",
            13: "Mannerism_Late_Renaissance",
            14: "Minimalism",
            15: "Naive_Art_Primitivism",
            16: "New_Realism",
            17: "Northern_Renaissance",
            18: "Pointillism",
            19: "Pop_Art",
            20: "Post_Impressionism",
            21: "Realism",
            22: "Rococo",
            23: "Romanticism",
            24: "Symbolism",
            25: "Synthetic_Cubism",
            26: "Ukiyo_e",
        }

        self.transform = transforms.Compose(
            [
                transforms.Resize((256, 256)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def classify(self, img_bytes):
        image = Image.open(img_bytes).convert("RGB")
        img_tensor = self.transform(image)
        img_tensor = img_tensor.unsqueeze(0)
        self.model.eval()
        output = self.model(img_tensor)
        _, predicted = torch.max(output, 1)
        classified = self.idx_to_class[int(predicted)]
        return classified
