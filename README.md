<div align="center">
<h1>Outfit Anyone in the Wild: Get rid of Annoying Restrictions for Virtual Try-on Task</h1>

<a href='https://huggingface.co/spaces/selfit-camera/OutfitAnyone-in-the-Wild'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue'></a>
[![ModelScope](https://img.shields.io/badge/ModelScope-Studios-blue)](https://www.modelscope.cn/studios/selfitcamera/OutfitAnyoneInTheWild/summary)
[![Open in OpenXLab](https://cdn-static.openxlab.org.cn/app-center/openxlab_app.svg)](https://openxlab.org.cn/apps/detail/jiangxiaoguo/OutfitAnyone-in-the-Wild)

</div>


<font color='red'>**Go to [heybeauty](https://www.producthunt.com/posts/heybeauty)for free try-on now!**</font> :stuck_out_tongue_winking_eye:


OutfitAnyone in the Wild is a new state-of-the-art virtual try-on method to produce high-quality try-on result on street photos. It achievies a perfect balance between user's face ID retention and clothing detail consistency.

<img src='assets/show.JPG'>

## Other Demo
- [IDM PLUS OUTFITANYONE](https://huggingface.co/spaces/selfit-camera/IDM-VTON-PLUS)

## Test results on real user photos
- [man01](https://heybeautify.online/ClothData/Publics/Shows/shows/man_v2/man_v2.html) 
- [woman01](https://heybeautify.online/ClothData/Publics/Shows/shows/cider/cider_0403.html) 
- [woman02](https://heybeautify.online/ClothData/Publics/Shows/shows/baifa/baifa_0408.html) 

## UPDATE

* 2024.03.18 We believe that the gpt-3 time for try-on has arrived. We will soon release an API to create clothing models and try-on.
* 2024.03.01 The hand generation problem is solved, algorithm will almost never get misshapen hands.
* 2024.02.05 We have added skin color matching, and the algorithm effect is more friendly to people of all races.
* 2023.12.28 We have added many innovative tricks to solve the problem of user facial id consistency.
* 2023.11.12 The algorithm process of user try-on is implemented for the first time, and the robustness of the try-on effect under different poses amazed us all.
* 2023.07.20 After countless attempts, we successfully found a way to embed clothing information into the human body parametric model.
* 2023.03.06 After burning nearly $750,000, a massive 3D human body dataset was collected.
* 2022.12.15 Several PhDs got together for dinner, and one of them proposed to develop a try-on algorithm that has no restrictions on user photos. 


## Abstract
Virtual Try-On task aims to transfer an in-shop garment image onto a target person. Existing methods focus on improving metrics on the fitting data set, they often overlook the diversity of user poses and complexity of environments in street photos. In addition, how to maintain the consistency of user IDs and clothing style details is also a more tricky topic. All the above problems prevent virtual try-on tasks from being implemented in real scenes and online e-commerce. 

In this paper, we propose OutfitAnyone in-the-wild, which achieves a perfect balance between image harmony, clothing detail consistency, and user's face ID retention.
We first model human bodies in the user's photo and clothing photo through our pre-trained human body reconstruction large model. Then deformation on posture and figure is performed in parameter space to match the user's picture. As a part of our human body parametric model, clothing appearance follows the deformation of the human body, and changes under physical laws, so that they can fit the user's human body harmoniously. The rendered image will finally go through a detect-and-refine network that can repair discordant factors in human body images. 

Extensive experiments on an in-the-wild test set demonstrate the superiority of our method, surpassing state-of-the-art methods both qualitatively and quantitatively

## Acknowledgements
- [openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) 
- [M3D-VTON](https://github.com/fyviezhao/M3D-VTON) 
- [GP-VTON](https://github.com/xiezhy6/GP-VTON) 
- [OutfitAnyone](https://github.com/HumanAIGC/OutfitAnyone) 
- [InstantID](https://github.com/InstantID/InstantID) 
- [street-tryon](https://github.com/cuiaiyu/street-tryon-benchmark) 
- [MeshGraphormer](https://github.com/microsoft/MeshGraphormer) 
- [HuggingFace](https://github.com/huggingface)
- [ModelScope](https://github.com/modelscope/modelscope) 

For any question, please feel free to contact us via jiangxiaoguo@heybeautify.online

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=selfitcamera/Outfit-Anyone-in-the-Wild&type=Date)](https://star-history.com/#selfitcamera/Outfit-Anyone-in-the-Wild&Date)
