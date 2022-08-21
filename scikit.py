import pandas as pd
import os, sys
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

models = {
    "DenseNet169": ["densenet169"],
    "DenseNet121": ["densenet121"],
    "ResNet50": ["resnet50"],
    "VGG16": ["vgg16"],
    "VGG19": ["vgg19"]
}

current_loc = "/Users/stefan/data_analysis"

files = os.listdir(f"{current_loc}/{sys.argv[1]}/{sys.argv[2]}")

features = {
    "#convs": ["Launch Conv", "End Conv"],
    "#fcs": ["MatMul"],
    "#softms": ["Softmax"],
    "#relus": ["Relu", "Relu6"],
    "#mpools": ["Max Pool"],
    "#apools": ["Average Pool"],
    "#merges": ["Merge Add"],
    "#biases": ["Bias"]
}

df = None

if not os.path.exists(f"{current_loc}/{sys.argv[2]}.pkl"):
    df = pd.DataFrame(columns=features.keys())

    for f in files:

        if f.split('.')[-1] == "zip":
            break

        res = features.copy()
        for k in res:
            res[k] = 0

        for m in models:
            if (f.split("_")[0] in models[m]):
                print(f"{m} - {f}")
                for line in open(f"{current_loc}/{sys.argv[1]}/{sys.argv[2]}/{f}", 'r'):
                    operator = line.split(",")[-1].strip("\n")
                    for o in features.keys():
                        if (operator in features[o]):
                            res[o] += 1
                res["target"] = m

        res = pd.DataFrame.from_dict(data=[res])
        df = pd.concat([df, res], ignore_index=True, sort=False)

        df.to_pickle(f"{current_loc}/{sys.argv[2]}.pkl")

else:
    df = pd.read_pickle(f"{current_loc}/{sys.argv[2]}.pkl")

x = df.loc[:, list(features.keys())].values
y = df.loc[:, ['target']].values
# x = normalize(x, norm="l1")
x = StandardScaler().fit_transform(x)

print(x)
print(y)

pca = PCA(n_components=2)
comp = pca.fit_transform(x)
prinDF = pd.DataFrame(data=comp, columns=["Comp#1", "Comp#2"])

finalDf = pd.concat([prinDF, df[['target']]], axis=1)

print(finalDf)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_title('2 component PCA', fontsize=20)
colors = ['r', 'orange', 'g', 'b', 'purple']
for target, color in zip(list(models.keys()), colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'Comp#1'],
               finalDf.loc[indicesToKeep, 'Comp#2'], c=color, s=50)
ax.legend(list(models.keys()))
ax.grid()
plt.savefig(f"{sys.argv[2]}.pdf")

print(pd.DataFrame(pca.components_,columns=df.loc[:, list(features.keys())].columns,index = ['Comp#1','Comp#2']))

"""
for f in files:
    feats = []
    for o in features:
        command = os.popen(f"grep -o '{o}' results/{f} | wc -l")
        res = int(command.read())
        feats.append(res)

    df = df.append({
        "RunCallableHelper": feats[0], #skip
        "Bias": feats[1], #biases
        "Softmax": feats[2], #softms
        "Relu": feats[3], #relus
        "Tanh": feats[4], #skip
        "Sigmoid": feats[5], #skip
        "Relu6": feats[6], #relus
        "Softplus": feats[7], #skip
        "Softsign": feats[8], #skip
        "Selu": feats[9], #skip
        "Elu": feats[10], #skip
        "Launch Conv": feats[11], #convs
        "MatMul": feats[12], #fcs
        "Max Pool": feats[13], #mpool
        "Merge Add": feats[14], #merges
        "Average Pool": feats[15], #apools
        "Concat": feats[16],
        "End Conv": feats[17] #convs
    }, ignore_index=True)
"""

# x = df.loc[:, features].values
# y = files

# x = StandardScaler().fit_transform(x)

# pca = PCA(n_components=2)
# PC = pca.fit_transform(x)

# done = pd.DataFrame(
#     data = PC,
#     columns = ["X", "Y"]
# )

# done['Models'] = files

# print(done)
