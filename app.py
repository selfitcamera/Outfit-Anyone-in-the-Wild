
from utils import *


def onUpload():
    return ""


def onClick(cloth_id, pose_image, pose_id, size, request: gr.Request):
    if pose_image is None:
        return None, "no pose image found !"
    pose_id, cloth_id = pose_id['label'], cloth_id['label']
    # print(pose_id, cloth_id, size, (pose_image is None), len(pose_id)>0)
    if len(pose_id)>0:
        res = get_result_example(cloth_id, pose_id)
        # print(res)
        assert os.path.exists(res), res
        # res = cv2.imread(res)
        return res, "Done! Use the pre-run results directly, the cloth size does not take effect "
    else:
        try:
            client_ip = request.client.host
            x_forwarded_for = dict(request.headers).get('x-forwarded-for')
            if x_forwarded_for:
                client_ip = x_forwarded_for
            timeId = int(  str(time.time()).replace(".", "")  )+random.randint(1000, 9999)
            isUpload = upload_pose_img(ApiUrl, OpenId, ApiKey, client_ip, timeId, pose_image)
            if isUpload==0:
                return None, "fail to upload"
            elif isUpload==-1:
                return None, "There is a running task already, please wait and check the history tab"
            elif isUpload==-2:
                return None, "can not creat task, you have exhausted free trial quota"

            taskId = publicClothSwap(ApiUrl, OpenId, ApiKey, client_ip, cloth_id, timeId, size)
            if taskId==0:
                return None, "fail to public you task"

            max_try = 1
            wait_s = 30
            for i in range(max_try):
                time.sleep(wait_s)
                state = getInfRes(ApiUrl, OpenId, ApiKey, client_ip, timeId)
                if state=='stateIs-1':
                    return None, "task failed, it may be that no human was detected, or there may be illegal content, etc. "
                elif state=='stateIs0':
                    return None, "task not public success"
                elif len(state)>20:
                    return state, "task finished"
                elif (not state.startswith('stateIs')):
                    # return None, 'task is in queue, position is '+str(state)
                    pass
                else:
                    return None, state
            return None, "task has been created successfully, you can refresh the page 5~15 mins latter, and check the following history tab"
        except Exception as e:
            print(e)
            return None, "fail to create task"

def onLoad(request: gr.Request):
    client_ip = request.client.host
    x_forwarded_for = dict(request.headers).get('x-forwarded-for')
    if x_forwarded_for:
        client_ip = x_forwarded_for
    his_datas = [None for _ in range(10)]
    try:
        infs = getAllInfs(ApiUrl, OpenId, ApiKey, client_ip)
        print(client_ip, 'history infs: ', len(infs))
        # print(infs)

        for i, inf in enumerate(infs):
            if i>4: continue
            pose = inf['pose']
            res = inf['res']
            # his_datas[i*2] = f"[pose]({pose})"+f"![pose]({pose})"
            # his_datas[i*2+1] = f"[res]({res})"+f"![res]({res})"  
            his_datas[i*2] = f"<img src=\"{pose}\" >"
            his_datas[i*2+1] = f"<img src=\"{res}\" >"

        time.sleep(3)
    except Exception as e:
        print(e)
    return his_datas


cloth_examples = get_cloth_examples()
pose_examples = get_pose_examples()


# Description
title = r"""
<h1 align="center">Outfit Anyone in the Wild: Get rid of Annoying Restrictions for Virtual Try-on Task</h1>
"""

description = r"""
<b>Official 🤗 Gradio demo</b> for <a href='https://github.com/selfitcamera/Outfit-Anyone-in-the-Wild' target='_blank'><b>Outfit Anyone in the Wild: Get rid of Annoying Restrictions for Virtual Try-on Task</b></a>.<br>
1. Clothing models are fixed in this demo, but you can create your own in SelfitCamera WeChat applet (for Chainese users).
2. You can upload your own pose photo, then click the run button and wait for 3~5 minutes to see the results.
3. After submitting the task, feel free to leave this page. Everytime you refresh this page, completed tasks will be displayed on the history tab (bind with your ip address).
4. Share your try-on photo with your friends and enjoy! 😊"""


css = """
.gradio-container {width: 85% !important}
"""
with gr.Blocks(css=css) as demo:
    # description
    gr.Markdown(title)
    gr.Markdown(description)

    with gr.Row():
        with gr.Column():
            with gr.Column():
                # cloth_image = gr.Image(type="numpy", value=cloth_examples[0][1], label="")
                cloth_image = gr.Image(sources='clipboard', type="filepath", label="", 
                    value=None)
                cloth_id = gr.Label(value=cloth_examples[0][0], label="Clothing 3D Model", visible=False)
                example = gr.Examples(inputs=[cloth_id, cloth_image],
                                      examples_per_page=3,
                                      examples = cloth_examples)
        with gr.Column():
            with gr.Column():
                # pose_image = gr.Image(source='upload', value=pose_examples[0][1], 
                #     type="numpy", label="")
                pose_image = gr.Image(value=None, 
                    type="numpy", label="")
                pose_id = gr.Label(value=pose_examples[0][0], label="Pose Image", visible=False)
                example_pose = gr.Examples(inputs=[pose_id, pose_image],
                                          examples_per_page=3,
                                          examples=pose_examples)
                size_slider = gr.Slider(-2.5, 2.5, value=1, interactive=True, label="clothes size")
                
        with gr.Column():
            with gr.Column():
                run_button = gr.Button(value="Run")
                init_res = get_result_example(cloth_examples[0][0], pose_examples[0][0])
                res_image = gr.Image(label="result image", value=None, type="filepath")
                # res_image = gr.Image(label="result image", value=None, type="numpy")
                # res_image = gr.Image(label="result image", value=cv2.imread(init_res), 
                #     type="numpy")
                gr.Markdown("If image does not display successfully after button clicked in your browser(mostly Mac+Chrome), try modelscope's [demo](https://www.modelscope.cn/studios/selfitcamera/OutfitAnyoneInTheWild/summary) please")
                info_text = gr.Textbox(value="", interactive=False, 
                    label='runtime information')
                
    with gr.Tab('history'):
        with gr.Row():
            his_pose_image1 = gr.HTML()
            his_res_image1 = gr.HTML()

        with gr.Row():
            his_pose_image2 = gr.HTML()
            his_res_image2 = gr.HTML()

        with gr.Row():
            his_pose_image3 = gr.HTML()
            his_res_image3 = gr.HTML()            

        with gr.Row():
            his_pose_image4 = gr.HTML()
            his_res_image4 = gr.HTML()            

        with gr.Row():
            his_pose_image5 = gr.HTML()
            his_res_image5 = gr.HTML()            

    run_button.click(fn=onClick, inputs=[cloth_id, pose_image, pose_id, size_slider], 
                     outputs=[res_image, info_text])

    pose_image.upload(fn=onUpload, inputs=[], outputs=[pose_id],)
    demo.load(onLoad, inputs=[], outputs=[his_pose_image1, his_res_image1,
        his_pose_image2, his_res_image2, his_pose_image3, his_res_image3,
        his_pose_image4, his_res_image4, his_pose_image5, his_res_image5,
        ])

if __name__ == "__main__":

    demo.queue(max_size=30)
    # demo.queue(concurrency_count=60)
    # demo.launch(server_name='0.0.0.0', server_port=225)
    demo.launch(server_name='0.0.0.0')
    