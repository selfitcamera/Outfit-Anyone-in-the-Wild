<div align="center">
<h1>Outfit Anyone in the Wild: Get rid of Annoying Restrictions for Virtual Try-on Task</h1>

<a href='https://huggingface.co/spaces/selfit-camera/OutfitAnyoneInTheWild'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue'></a>
[![ModelScope](https://img.shields.io/badge/ModelScope-Studios-blue)](https://www.modelscope.cn/studios/selfitcamera/OutfitAnyoneInTheWild/summary)

</div>

Outfit InTheWild is a new state-of-the-art virtual try-on method to produce high-quality try-on result on street photos. It achievies a perfect balance between user's face ID retention and clothing detail consistency.

<img src='assets/applications.png'>


<!-- ### Comparison with Previous Works

<p align="center">
  <img src="assets/compare-a.png">
</p>

Comparison with existing tuning-free state-of-the-art techniques. InstantID achieves better fidelity and retain good text editability (faces and styles blend better).
 -->

## Api Usage Tips
- Get your own ```openId``` and ```apiKey``` in WeChat applet **SelfitCamera (赛飞相机)**
- Create your clothing model in WeChat applet **SelfitCamera (赛飞相机)**, record its ```clothId``` in details page.
- Upload your pose image with function ```upload_pose_img```, then public a cloth swap task ```publicClothSwap```
- Get result with ```getInfRes```


## Acknowledgements
- [openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) 
- [M3D-VTON](https://github.com/fyviezhao/M3D-VTON) 
- [GP-VTON](https://github.com/xiezhy6/GP-VTON) 
- [InstantID](https://github.com/InstantID/InstantID) 
- [street-tryon](https://github.com/cuiaiyu/street-tryon-benchmark) 
- [MeshGraphormer](https://github.com/microsoft/MeshGraphormer) 
- [HuggingFace](https://github.com/huggingface)
- [ModelScope](https://github.com/modelscope/modelscope) 

For any question, please feel free to contact us via jiangxiaoguo@selficamera.cn
