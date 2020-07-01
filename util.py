import numpy as np
import cv2
from PIL import Image

COLORS_10 =[(144,238,144),(178, 34, 34),(221,160,221),(  0,255,  0),(  0,128,  0),(210,105, 30),(220, 20, 60),
            (192,192,192),(255,228,196),( 50,205, 50),(139,  0,139),(100,149,237),(138, 43,226),(238,130,238),
            (255,  0,255),(  0,100,  0),(127,255,  0),(255,  0,255),(  0,  0,205),(255,140,  0),(255,239,213),
            (199, 21,133),(124,252,  0),(147,112,219),(106, 90,205),(176,196,222),( 65,105,225),(173,255, 47),
            (255, 20,147),(219,112,147),(186, 85,211),(199, 21,133),(148,  0,211),(255, 99, 71),(144,238,144),
            (255,255,  0),(230,230,250),(  0,  0,255),(128,128,  0),(189,183,107),(255,255,224),(128,128,128),
            (105,105,105),( 64,224,208),(205,133, 63),(  0,128,128),( 72,209,204),(139, 69, 19),(255,245,238),
            (250,240,230),(152,251,152),(  0,255,255),(135,206,235),(  0,191,255),(176,224,230),(  0,250,154),
            (245,255,250),(240,230,140),(245,222,179),(  0,139,139),(143,188,143),(255,  0,  0),(240,128,128),
            (102,205,170),( 60,179,113),( 46,139, 87),(165, 42, 42),(178, 34, 34),(175,238,238),(255,248,220),
            (218,165, 32),(255,250,240),(253,245,230),(244,164, 96),(210,105, 30)]


def draw_bbox(img, box, cls_name, identity=None, offset=(0,0)):
    '''
        draw box of an id
    '''
    x1,y1,x2,y2 = [int(i+offset[idx%2]) for idx,i in enumerate(box)]
    # set color and label text
    color = COLORS_10[identity%len(COLORS_10)] if identity is not None else COLORS_10[0]
    label = '{} {}'.format(cls_name, identity)
    # box text and bar
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
    cv2.rectangle(img,(x1, y1),(x2,y2),color,0.5)
    cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
    cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 1, [255,255,255], 1)
    return img




def draw_bboxes(img, bbox, identities=None, offset=(0,0)):
    for i,box in enumerate(bbox):
        x1,y1,x2,y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        print("coor: ", x1, " ", x2, " ", y1, " ", y2)
        # box text and bar
        id = int(identities[i]) if identities is not None else 0    
        color = COLORS_10[id%len(COLORS_10)]
        
        cv2.rectangle(img,(x1, y1),(x2,y2),color,5)

        label = '{}{:d}'.format("Person ", id)
        
        #getTextSize( text, font, fontScale=font_scale, thickness=1 )
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
        
        #cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])

        cv2.rectangle(img,(x1, y1),(x1+t_size[0]+2,y1+t_size[1]+3), color,-1)
        cv2.putText(img,label,(x1,y1+t_size[1]+2), cv2.FONT_HERSHEY_PLAIN, 2, [255,255,255], 2)

    return img
    
def x1y1_x2y2_conf(bbox,cls_conf):
    nbbox = []
    for i,box in enumerate(bbox):
        xc,yc,w,h = [int(i) for i in box]
        conf = cls_conf[i]
        x1 = xc - w//2
        y1 = yc - h//2
        x2 = xc + w//2
        y2 = yc + h//2
        nbbox.append([x1,y1,x2,y2,conf])
    return nbbox



def write_results(filename, results):
        save_format = '{frame},{id},{x1},{y1},{w},{h},1,-1,-1,-1\n'
        with open(filename, 'w') as f:
            for frame_id, tlwhs, track_ids in results:
                for tlwh, track_id in zip(tlwhs, track_ids):
                    if track_id[0] < 0:
                        continue
                    x1, y1, w, h = tlwh
                    x2, y2 = x1 + w, y1 + h
                    line = save_format.format(frame=frame_id, id=track_id[0], x1=x1, y1=y1, x2=x2, y2=y2, w=w, h=h)
                    f.write(line)
        #logger.info('save results to {}'.format(filename))
    
def draw_simple_bboxes(img, bbox, offset=(0,0)):
    for i,box in enumerate(bbox):
        x1,y1,x2,y2,conf = [i for i in box]
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        
        cv2.rectangle(img,(x1, y1),(x2,y2),(0,0,255),3)
        label = '{:.2f}'.format(conf)
        #label = '{:.2f}'.format(x1)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2 , 2)[0]
        cv2.rectangle(img,(x1, y1),(x1+t_size[0]+1,y1+t_size[1]+1), (0,0,0),-1)
        cv2.putText(img,label,(x1,y1+t_size[1]+2), cv2.FONT_HERSHEY_PLAIN, 1.5, [255,255,255], 2)
        
    return img
    

def crop_simple_bboxes(img,bbox,path,cu_index):
    for i,box in enumerate(bbox):
        x1,y1,x2,y2,conf = [i for i in box]
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        
        filename = path + "/nfs4/ajaym/Downloads/cendeep_sort_pytorch-master/debugresult/images/{}_{}.jpg".format(cu_index,i)
        print(img.shape)
        img_c = img[max(0,y1):max(0,y2),max(0,x1):max(0,x2)]
        print(img.shape)
        print("box_dim: ", x1," ", x2," ",y1," ", y2 )
        cv2.imwrite(filename, img_c)
        cv2.imshow("image",img_c)
        cv2.waitKey(0)
    return None

def softmax(x):
    assert isinstance(x, np.ndarray), "expect x be a numpy array"
    x_exp = np.exp(x*5)
    return x_exp/x_exp.sum()

def softmin(x):
    assert isinstance(x, np.ndarray), "expect x be a numpy array"
    x_exp = np.exp(-x)
    return x_exp/x_exp.sum()



if __name__ == '__main__':
    x = np.arange(10)/10.
    x = np.array([0.5,0.5,0.5,0.6,1.])
    y = softmax(x)
    z = softmin(x)
    import ipdb; ipdb.set_trace()
