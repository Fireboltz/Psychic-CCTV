import torch
from utils import *
from PIL import Image, ImageDraw, ImageFont
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def super_res(img):
    ## SRRESNET
    srresnet_checkpoint = "./checkpoint_srresnet.pth.tar"
    srresnet = torch.load(srresnet_checkpoint,map_location=device)['model']
    srresnet.eval()

    hr_img = Image.open(img, mode="r")
    hr_img.show()
    hr_img = hr_img.convert('RGB')



    sr_img_srresnet = srresnet(convert_image(hr_img, source='pil', target='imagenet-norm').unsqueeze(0).to(device))
    sr_img_srresnet = sr_img_srresnet.squeeze(0).cpu().detach()
    sr_img_srresnet = convert_image(sr_img_srresnet, source='[-1, 1]', target='pil')
    sr_img_srresnet.show()


    ## SRGAN
    srgan_checkpoint = "./checkpoint_srgan.pth.tar"
    srgan_generator = torch.load(srgan_checkpoint,map_location=device)['generator']
    srgan_generator.eval()

    sr_img_srgan = srgan_generator(convert_image(hr_img, source='pil', target='imagenet-norm').unsqueeze(0).to(device))
    sr_img_srgan = sr_img_srgan.squeeze(0).cpu().detach()
    sr_img_srgan = convert_image(sr_img_srgan, source='[-1, 1]', target='pil')

    sr_img_srgan.show()


if __name__ == '__main__':
    img=input()
    super_res(img)
    