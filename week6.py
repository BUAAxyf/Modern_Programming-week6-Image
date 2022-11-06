from winreg import EnumValue
from PIL import Image, ImageFilter
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

class Filter:
    '''
    滤波类
    所有滤波操作的父类
    '''
    def __init__(self,image,arg):
        '''
        image为图片实例, arg为长宽构成的元组/列表
        '''
        self.image=image
        self.arg=arg
    def filter(self):
        pass

class EDGE(Filter):
    '''
    边缘提取滤波
    '''
    def __init__(self,image,arg):
        Filter.__init__(self,image,arg)
    def filter(self):
        return self.image.filter(ImageFilter.FIND_EDGES)

class DETAIL(Filter):
    '''
    细节滤波 
    '''
    def __init__(self,image,arg):
        Filter.__init__(self,image,arg)
    def filter(self):
        return self.image.filter(ImageFilter.DETAIL)

class ENHANCE(Filter):
    '''
    边缘增强滤波
    '''
    def __init__(self,image,arg):
        Filter.__init__(self,image,arg)
    def filter(self):
        return self.image.filter(ImageFilter.EDGE_ENHANCE)

class DEEPENHANCE(Filter):
    '''
    深度边缘增强滤波
    '''
    def __init__(self,image,arg):
        Filter.__init__(self,image,arg)
    def filter(self):
        return self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)

class SHARPEN(Filter):
    '''
    锐化滤波
    '''
    def __init__(self,image,arg):
        Filter.__init__(self,image,arg)
    def filter(self):
        return self.image.filter(ImageFilter.SHARPEN)

class VAGUE(Filter):
    '''
    模糊滤波
    '''
    def __init__(self,image,arg):
        Filter.__init__(self,image,arg)
    def filter(self):
        return self.image.filter(ImageFilter.BLUR)

class RESIZE(Filter):
    '''
    调整大小滤波
    '''
    def __init__(self,image,arg):
        Filter.__init__(self,image,arg)
    def filter(self):
        return self.image.resize((self.arg[0],self.arg[1]),Image.ANTIALIAS)#高品质

class ImageShop:
    '''
    集成功能
    '''
    def __init__(self):
        self.format,self.path='',''

    def load_image(self,path):
        '''
        应加载文件或目录中的所有特定格式图片
        '''
        self.path=path
        if os.path.isdir(path):#判断path是否为目录
            self.file_names=os.listdir(path)
            self.images=[Image.open(path+'/'+name) for name in self.file_names]
        elif os.path.isfile(path):#判断path是否为文件
            self.file_names=[os.path.basename(path)]
            self.images=[Image.open(path)]
        print('image loded')

    def __batch_ps(self):
        '''
        利有某个过滤器对所有图片进行处理
        '''
        for i in range(len(self.process)):
            self.images[i]=self.process[i].filter()

    def batch_ps(self,lis_operation,*arg):
        '''
        批量处理图片的对外公开方法
        '''
        for operation in tqdm(lis_operation,desc='operating...'):
            self.process=self.images
            for i in range(len(self.images)):
                func=eval(operation.upper())
                self.process[i]=func(self.images[i],arg[0])
            self.__batch_ps()
        print('batch_ps over')

    def display(self,row=3,column=4,maxnum=64):
        '''
        显示处理效果
        '''
        num=row*column
        if num>maxnum:
            num=maxnum
            row,column=8,8
        for i in range(num):
            plt.subplot(row,column,i+1)
            plt.imshow(self.images[i])
        plt.show()

    def save(self,path):
        '''
        保存处理结果
        path为目录名
        '''
        for i in tqdm(range(len(self.images)),desc='saving...'):
            self.images[i].save(path+'/'+self.file_names[i])
        print('Images have been saved')

def main():
    path="D:/Project/Python/week6Image/test/20210117000927_1.jpg"
    operations=['RESIZE']
    save_path="D:/Project/Python/week6Image/save"
    arg=[1000,1000]
    shop=ImageShop()
    shop.load_image(path)
    shop.batch_ps(operations,arg)
    shop.save(save_path)
    
if __name__=='__main__': main()