# Musezen - AI Art Curator Powered by Snowflake Arctic

## Introduction

When you are visiting museums (or "musezens" 👀), have you ever wondered what else you can learn about that one painting where the plaque only writes "Oil on Canvas"? We have! And we always spend a bunch of time looking up information on the phone, which always feels like a very interrupted experience.

## Getting Started

To get started with [Musezen](https://musezen.streamlit.app/):

1. **Upload a Photo** (Optional): Take a picture of a painting and upload it to Musezen for analysis.
2. **Start a Conversation**: Begin chatting with Musezen about any art-related topics you're interested in.
3. **Explore and Learn**: Ask follow-up questions for a conversation with Musezen to enhance your understanding and appreciation of art.

## Features

Musezen is your personal art curator, designed to enhance your museum visits and art discovery experiences. Leveraging the knowledge of the Snowflake Arctic model, Musezen allows you to chat about different art styles and gain deeper insights into artworks. Here's what you can do with Musezen:

- **Chat About Art**: Start a conversation with Musezen about various art styles, artists, and historical contexts. Whether you're curious about Impressionism, Baroque, or modern art movements, Musezen has you covered.
  
- **Photo Uploads**: Upload a photo of a painting to get specific information about the artwork. Musezen can identify the art style, explain its significance, and provide more information to spark in-depth conversations..

- **Interactive Learning**: Use Musezen to explore art topics in a more engaging and interactive way, making your museum visits more informative and enjoyable.

## Future Enhancements

We are excited about the future of Musezen and have several enhancements planned to make it even more powerful and useful:

- **Art Database Connectivity**: Leveraging high-quality data will unlock the full potential of Arctic, making Snowflake an ideal platform for such applications with close access to both data and models. We plan to start by integrating extensive art databases such as the [National Gallery of Art Open Data Program](https://github.com/NationalGalleryOfArt/opendata) and [The Art Genome Project by Artsy](https://www.artsy.net/categories). Eventually, we aim to implement an easy way to allow smaller venues to set up their own versions of Musezen using their own data. This will make Musezen more context-aware, enriching the user experience no matter where they are.

- **Enhanced User Experience**: We plan to improve the user interface to make it more intuitive and user-friendly, ensuring it is easy to navigate and find the information the user needs. We also would love to support audio inputs and outputs to reduce the time needed to look at the device, thus allowing an even smoother experience in the venues. Finally, we would love to continue improve our image classification model to provide more detailed information about the user-presented painting. 

## How we built it

We built Musezen using Python with Snowflake Arctic as its core language model. Our goal was to keep the project lightweight, avoiding unnecessary packages, which means we needed to carry more weight developing some infrastructure. We designed an expandable class structure to support integration with different LLMs and to enable future tool use with a fine-tuned Arctic model. On the image classification side, we used ResNet-50 finetuned on the WikiArt style dataset for painting style classification [1][2].


## Challenges we ran into

Developing Musezen involved both an image classification component and a generative model component, which required us to work in parallel due to the tight timeframe. Each workstream presented its own challenges. For the image classification model, we had to determine an appropriate level of label granularity—detailed enough to be useful, yet feasible to train to adequate accuracy within the deadline. On the LLM side, we faced the challenge of integrating the classification model's output and providing as much insight as possible in response to user queries.

## What we learned

Tool use is a key ability for language models in order to enhance user interactions and providing comprehensive insights. Working on Musezen highlighted the importance of modular design and the value of integrating various technologies to create a cohesive and efficient system.

## Citations

1. Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. "Deep Residual Learning for Image Recognition." CoRR, abs/1512.03385, 2015. Available at [http://arxiv.org/abs/1512.03385](http://arxiv.org/abs/1512.03385).

2. Wei Ren Tan, Chee Seng Chan, Hernan Aguirre, and Kiyoshi Tanaka. "Improved ArtGAN for Conditional Synthesis of Natural Image and Artwork." IEEE Transactions on Image Processing, vol. 28, no. 1, pp. 394-409, 2019. Available at [https://doi.org/10.1109/TIP.2018.2866698](https://doi.org/10.1109/TIP.2018.2866698).

## Authors

- [@AOYW](https://github.com/AOYW): Andy is a data scientist who earned his B.A. in Economics and Data Science, alongside a B.S. in Chemical Biology from UC Berkeley. He also holds an M.A. in Economics from Duke University. During his academic tenure, Andy contributed to several university research groups. Beyond working and observing his two cats in their natural habitat, Andy enjoys exploring diverse cuisines. As an avid photographer, he captures and shares his experiences through his lens.

- [@mittyhainan](https://github.com/mittyhainan): Hainan is a data scientist with an S.M. from Harvard and a B.S. from UCSD. He has experience in diverse projects across different fields, ranging from e-commerce and healthcare to credit risk and business banking. Outside of the office, Hainan often spends his time skiing during the snow season. He enjoys traveling to different places to explore local cultures, hiking, and attending various music festivals (especially EDM).

We hope you enjoy using Musezen as much as we enjoyed creating it. Happy exploring!