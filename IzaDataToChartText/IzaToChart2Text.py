import json
import numpy as np
from xml.dom import minidom
import re
import csv


titles = []
data_table = []
summaries = []
bar_chart_str = "bar_chart"


with open('chartID2plotInfo.json') as json_file:
    json_chart_data = json.load(json_file)


summaries_xml = minidom.parse('chart_summaries_b01_toktest2.xml')

ignore = False
topics = summaries_xml.getElementsByTagName('topic')
for topic in topics:
    ignore = False
    stories = topic.getElementsByTagName('story')
    topic_id = topic.attributes['topic_id'].value #re.sub('[a-z]', '', topic.attributes['topic_id'].value)

    # Writing Titles to text file   
    chart = json_chart_data[topic_id]

    # Writing data tables of charts to text file
    x_title = chart['general_figure_info']['x_axis']['label']['text']
    x_title = x_title.replace(" ", "_")
        
    if x_title == "":
        print('x_title empty: ', topic_id)
        ignore = True
        x_title = "type"
        
    y_title = chart['general_figure_info']['y_axis']['label']['text']
    y_title_final = ""
    for char in y_title:
        if(char == " "):
            y_title_final += "_"
        elif(char.isalnum()):
            y_title_final += char
    if(y_title_final[-1] == "_"):
        y_title_final = y_title_final[:-1]

    y_title = y_title_final
    if y_title == "":
        print('y_title empty: ', topic_id)
        ignore = True
        y_title = "type"

    pipe_separated_data_table = ""
    for x, y in zip(chart['models'][0]['x'], chart['models'][0]['y']):
        
        if(type(x) is str):
            x = x.replace(" ", "_")
        if(type(y) is str):
            y = y.replace(" ", "_")

        pipe_separated_data_table += x_title + '|' + str(x) + '|' + 'x' + '|' + bar_chart_str + " "
        pipe_separated_data_table += y_title + '|' + str(y) + '|' + 'y' + '|' + bar_chart_str + " "

    if(not ignore):
        for story in stories:
            summaries.append(story.getElementsByTagName('text')[0].getElementsByTagName('content')[0].firstChild.data)
            data_table.append(pipe_separated_data_table)
            titles.append(chart['general_figure_info']['title']['text'])

assert len(summaries) == len(data_table) == len(titles)
print(len(summaries))

# with open("data.txt", "w") as file:
#     for data in data_table:
#         file.write(data + "\n")
    
# with open("titles.txt", "w") as file:
#     for title in titles:
#         file.write(title + "\n")

# with open("captions.txt", "w") as file:
#     for summary in summaries:
#         file.write(summary + "\n")


for j in range(0, len(summaries)):
    f = open('dataset/'+'captions/'+str(j+1)+'.txt', 'w', encoding="utf-8")
    f.write(summaries[j])
    f.close()

    f = open('dataset/'+'titles/'+str(j+1)+'.txt', 'w', encoding="utf-8")
    f.write(titles[j])
    f.close()

    f = open('dataset/data/'+str(j+1)+'.csv', 'w', newline='', encoding="utf-8")
    datarow = data_table[j].split(' ')

    xLabel = datarow[0].split('|')[0]
    yLabel = datarow[1].split('|')[0]

    writer = csv.writer(f)
    writer.writerow([xLabel, yLabel])
    for i in range(0, len(datarow)-1, 2):
        try:
            x = datarow[i].split('|')[1]
            y = datarow[i+1].split('|')[1]
            writer.writerow([x, y])
        except:
            print(datarow)
            raise Exception("Sorry, no numbers below zero")

    f.close()




