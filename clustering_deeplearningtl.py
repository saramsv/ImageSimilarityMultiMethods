#python3 clustering_deeplearningtl.py data/UT06-12D # > resnet_clusters 
#cat resnet_clusters | sort --field-separator=":" --key=2 > resnet_clusters
import keras
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input
from keras.models import Sequential
from keras.layers import Dense, Flatten, GlobalAveragePooling2D
from keras.callbacks import TensorBoard
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import glob
import cv2
import sys
import matplotlib.pyplot as plt

imgs_path = sys.argv[1]

img_size = 224
resnet_weigth_path = 'data/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

clustering_model = Sequential()
clustering_model.add(ResNet50(include_top = False, pooling='ave', weights = resnet_weigth_path))
clustering_model.layers[0].trainable = False
clustering_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])

img_names = []
def extract_vector(path):
    resnet_feature_list = []
    for img in glob.glob(path + "*.JPG"):
        img_names.append(img)
        img_object = cv2.imread(img)
        img_object = cv2.resize(img_object, (img_size, img_size))
        img_object = np.array(img_object, dtype = np.float64)
        img_object = preprocess_input(np.expand_dims(img_object.copy(), axis = 0))
        resnet_feature = clustering_model.predict(img_object)
        resnet_feature = np.array(resnet_feature)
        resnet_feature_list.append(resnet_feature.flatten())
    return np.array(resnet_feature_list)


vectors = extract_vector(imgs_path)
model = TSNE(n_components=2, perplexity=50)
results = model.fit_transform(vectors)

plt.figure(figsize=(16,10))
plt.plot(results)
plt.show()
import bpython
bpython.embed(locals())
'''
sns.scatterplot(
    x="tsne-2d-one", y="tsne-2d-two",
    hue="y",
    palette=sns.color_palette("hls", 10),
    data=results,
    legend="full",
    alpha=0.3
)

kmeans = KMeans(n_clusters = 6)
kmeans.fit(vectors)
labels = kmeans.predict(vectors)

for index, label in enumerate(labels):
    print(img_names[index] , ":", label)

'''