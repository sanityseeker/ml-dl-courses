
# coding: utf-8

# **Задание 1**
# 
# Сколько различных категорий имеется в наборе данных 2017 Val annotations, у которых supercategory==animal?

# In[1]:


from pycocotools.coco import COCO


# In[2]:


coco = COCO('/data/annotations/instances_val2017.json')


# In[5]:


cats = coco.loadCats(coco.getCatIds())
cats


# In[26]:


animal_ids = set(item['id'] for item in cats if item['supercategory'] == 'animal')


# In[27]:


animal_ids


# In[28]:


len(animal_ids)


# **Задание 2**
# 
# Сколько изображений в наборе данных 2017 Val annotations содержит ровно 3 аннотированных человека?

#      person cat_id = 1

# Все данные лежат в директории `/data/`

# In[29]:


get_ipython().system(' ls /data/')


# In[49]:


person_id = 1


# In[31]:


img_ids = coco.getImgIds(catIds=[person_id])

imgs = coco.loadImgs(img_ids)

ann_ids = coco.getAnnIds(img_ids, catIds=[person_id = 1])


# In[44]:


imgs[0]


# In[39]:


annotations = coco.loadAnns(ann_ids)


# In[55]:


from collections import defaultdict
imgs_humans = defaultdict(int)

for ann in annotations:
    imgs_humans[ann['image_id']] += int(ann['category_id'] == person_id)


# In[60]:


target_human_number = 3
cnt = 0

for img_id, human_cnt in imgs_humans.items():
    if human_cnt == target_human_number:
        cnt += 1


# In[61]:


cnt


# Чтобы отправить  ответы,  запишите их  в формате  json в  файл   result.txt  и положите  его  в корневую директорию
# |
# Пример:

# In[62]:


res = {'task_1': len(animal_ids), 'task_2': cnt}

with open("result.txt", "w") as text_file:
    print(str(res), file=text_file)

