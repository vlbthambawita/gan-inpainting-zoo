import argparse
import os
import time

class TestOptions:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.initialized = False

    def initialize(self):
        self.parser.add_argument('--dataset', type=str, default='barretts',
                                 help='The dataset of the experiment.')
        self.parser.add_argument('--data_file', type=str, default='/work/vajira/DATA/hyper_kvasir/data_new/splits/split_0', help='the file storing testing file paths')
        self.parser.add_argument('--test_dir', type=str, default='/work/vajira/DATA/polyps_inpainting/hyper-kvasir/split_0', help='models are saved here')

        # added by Vajira
        self.parser.add_argument('--sub_dir', type=str, default='barretts', help="sub directory (category) to convert into inpainted images")
        self.parser.add_argument('--data_dir', type=str, default='/work/vajira/DATA/hyper_kvasir/data_new/splits/split_0', help='the file storing testing file paths')
        self.parser.add_argument('--out_dir_img', type=str, default='/work/vajira/DATA/polyps_inpainting/hyper-kvasir-BB/inpainted_images/split_0', help='main directory to output inpainted images')
        self.parser.add_argument('--out_dir_mask', type=str, default='/work/vajira/DATA/polyps_inpainting/hyper-kvasir-BB/mask_images/split_0', help='main directory to outpuyt maks images')
        self.parser.add_argument('--out_dir_csv', type=str, default='/work/vajira/DATA/polyps_inpainting/hyper-kvasir-BB/mask_csv/split_0', help='main directory to output csv files')


        self.parser.add_argument('--load_model_dir', type=str, default='./checkpoints', help='pretrained models are given here')
        self.parser.add_argument('--load_model_path', type=str, default='', help='Exact model to load for finetunning')
        self.parser.add_argument('--seed', type=int, default=1, help='random seed')
        self.parser.add_argument('--gpu_ids', type=str, default='0')

        self.parser.add_argument('--mask_dir', type=str , default="/work/vajira/DATA/CVC_ClinicDB/data/CVC_ClinicDB/gt", help="A folder with mask images")

        self.parser.add_argument('--model', type=str, default='gmcnn')
        self.parser.add_argument('--random_mask', type=int, default=0,
                                 help='using random mask')

        self.parser.add_argument('--img_shapes', type=str, default='256,256,3',
                                 help='given shape parameters: h,w,c or h,w')
        self.parser.add_argument('--mask_shapes', type=str, default='64,64',
                                 help='given mask parameters: h,w')
        self.parser.add_argument('--mask_type', type=str, default='rect')
        self.parser.add_argument('--test_num', type=int, default=10)
        self.parser.add_argument('--mode', type=str, default='save')
        self.parser.add_argument('--phase', type=str, default='test')

        # for generator
        self.parser.add_argument('--g_cnum', type=int, default=32,
                                 help='# of generator filters in first conv layer')
        self.parser.add_argument('--d_cnum', type=int, default=32,
                                 help='# of discriminator filters in first conv layer')

    def parse(self):
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()

        if self.opt.data_file != '':
            self.opt.dataset_path = self.opt.data_file

        #if os.path.exists(self.opt.test_dir) is False:
        #    os.mkdir(self.opt.test_dir)

        assert self.opt.random_mask in [0, 1]
        self.opt.random_mask = True if self.opt.random_mask == 1 else False

        assert self.opt.mask_type in ['rect', 'stroke']

        str_img_shapes = self.opt.img_shapes.split(',')
        self.opt.img_shapes = [int(x) for x in str_img_shapes]

        str_mask_shapes = self.opt.mask_shapes.split(',')
        self.opt.mask_shapes = [int(x) for x in str_mask_shapes]

        # model name and date
        
        self.opt.date_str = 'test_'+time.strftime('%Y%m%d-%H%M%S')
        self.opt.model_folder = self.opt.date_str + '_' + self.opt.dataset + '_' + self.opt.model
        self.opt.model_folder += '_s' + str(self.opt.img_shapes[0]) + 'x' + str(self.opt.img_shapes[1])
        self.opt.model_folder += '_gc' + str(self.opt.g_cnum)
        self.opt.model_folder += '_randmask-' + self.opt.mask_type if self.opt.random_mask else ''
        if self.opt.random_mask:
            self.opt.model_folder += '_seed-' + str(self.opt.seed)
        self.opt.saving_path = os.path.join(self.opt.test_dir, self.opt.model_folder)

        #if os.path.exists(self.opt.saving_path) is False and self.opt.mode == 'save':
        #    os.mkdir(self.opt.saving_path)
        
        args = vars(self.opt)

        print('------------ Options -------------')
        for k, v in sorted(args.items()):
            print('%s: %s' % (str(k), str(v)))
        print('-------------- End ----------------')

        return self.opt