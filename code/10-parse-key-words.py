import pandas as pd
import xml.etree.ElementTree as ET


diagnostics = './results/fine-scale/mallet-models/STEM/400-topic-files/3-400-topics-diagnostics.xml'

tree = ET.parse(diagnostics)
root = tree.getroot()

len(root)
# 200

element = root[0]
element.tag
element.text
element.attrib
#element.get()

df = []

for child in root:
    info = {"Topic":child.attrib["id"]}

    for (i,grandchild) in enumerate(child):
        info[str(i) + "_word"] = grandchild.text

    df.append(info)

df = pd.DataFrame(df)

df.to_csv("./results/fine-scale/mallet-models/STEM/400-topic-files/3-400-keywords.csv", index = False)
