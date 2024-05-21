# Musezen - AI Art Curator Powered by Snowflake Arctic

## Introduction

When visiting museums (or "musezens" 👀), have you ever wondered what more you could learn about a painting that only has "Oil on Canvas" written on its plaque? We have! Often, we end up looking up information on our phones, which feels like an interrupted experience. Musezen aims to change that.

## Getting Started

To get started with [Musezen](https://musezen.streamlit.app/):

1. **Upload a Photo** (Optional): Take a picture of a painting and upload it to Musezen for analysis.
2. **Start a Conversation**: Begin chatting with Musezen about any art-related topics you're interested in.
3. **Explore and Learn**: Ask follow-up questions to deepen your understanding and appreciation of art.

## Features

Musezen is your personal art curator, designed to enhance your museum visits and art discovery experiences. Leveraging the Snowflake Arctic model, Musezen allows you to chat about various art styles and gain deeper insights into artworks. Here's what you can do with Musezen:

- **Chat About Art**: Start a conversation with Musezen about different art styles, artists, and historical contexts. Whether you're curious about Impressionism, Baroque, or modern art movements, Musezen has you covered.
  
- **Photo Uploads**: Upload a photo of a painting to get specific information about the artwork. Musezen can identify the art style, explain its significance, and provide more information to spark in-depth conversations.

- **Interactive Learning**: Use Musezen to explore art topics in a more engaging and interactive way, making your museum visits more informative and enjoyable.

## Future Enhancements

We are excited about the future of Musezen and have several enhancements planned to make it even more powerful and useful:

- **Art Database Connectivity**: Leveraging high-quality data will unlock the full potential of Arctic, making Snowflake an ideal platform for such applications with close access to both data and models. We plan to start by integrating extensive art databases such as the [National Gallery of Art Open Data Program](https://github.com/NationalGalleryOfArt/opendata) and [The Art Genome Project by Artsy](https://www.artsy.net/categories). Eventually, we aim to implement an easy way to allow smaller venues to set up their own versions of Musezen using their own data. This will make Musezen more context-aware, enriching the user experience no matter where they are.

- **Enhanced User Experience**: We plan to improve the user interface to make it more intuitive and user-friendly, ensuring it is easy to navigate and find the information needed. We also hope to support audio inputs and outputs to reduce the time spent looking at the device, allowing an even smoother experience in the venues. Finally, we aim to continually improve our image classification model to provide more detailed information about the user-presented artwork. 

## How We Built It

We built Musezen using Python with Snowflake Arctic as its core language model. Our goal was to keep the project lightweight, avoiding unnecessary packages, which required developing some infrastructure ourselves. We designed an expandable class structure to support integration with different LLMs and to enable future tool use with a fine-tuned Arctic model. For image classification, we used ResNet-50 [1] fine-tuned on the WikiArt style dataset [2].

[1]: http://arxiv.org/abs/1512.03385 "Deep Residual Learning for Image Recognition by Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun"
[2]: https://doi.org/10.1109/TIP.2018.2866698 "Improved ArtGAN for Conditional Synthesis of Natural Image and Artwork by Wei Ren Tan, Chee Seng Chan, Hernan Aguirre, and Kiyoshi Tanaka"

## Challenges We Ran Into

Developing Musezen involved both an image classification component and a generative model component, requiring parallel workstreams due to the tight timeframe. Each presented its own challenges. For the image classification model, we had to determine an appropriate level of label granularity—detailed enough to be useful yet feasible to train to adequate accuracy within the deadline. On the LLM side, we faced the challenge of integrating the classification model's output to provide as much insight as possible in response to user queries.

## What We Learned

Tool use is a key ability for language models to enhance user interactions and provide comprehensive insights. Working on Musezen highlighted the importance of modular design and the value of integrating various technologies to create a cohesive and efficient system.

## References

1. Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. "Deep Residual Learning for Image Recognition." CoRR, abs/1512.03385, 2015. Available at [http://arxiv.org/abs/1512.03385](http://arxiv.org/abs/1512.03385).

2. Wei Ren Tan, Chee Seng Chan, Hernan Aguirre, and Kiyoshi Tanaka. "Improved ArtGAN for Conditional Synthesis of Natural Image and Artwork." IEEE Transactions on Image Processing, vol. 28, no. 1, pp. 394-409, 2019. Available at [https://doi.org/10.1109/TIP.2018.2866698](https://doi.org/10.1109/TIP.2018.2866698).

## Authors

- [@AOYW](https://github.com/AOYW): Andy is a data scientist with a B.A. in Economics and Data Science and a B.S. in Chemical Biology from UC Berkeley, along with an M.A. in Economics from Duke University. During his academic tenure, Andy contributed to several university research groups. Beyond working and observing his two cats, Andy enjoys exploring diverse cuisines and capturing experiences through photography.

- [@mittyhainan](https://github.com/mittyhainan): Hainan is a data scientist with an S.M. from Harvard and a B.S. from UCSD. He has experience in diverse projects across various fields, ranging from e-commerce and healthcare to credit risk and business banking. Outside the office, Hainan enjoys skiing during the snow season, traveling to explore local cultures, hiking, and attending music festivals, especially EDM.

We hope you enjoy using Musezen as much as we enjoyed creating it. Happy exploring!