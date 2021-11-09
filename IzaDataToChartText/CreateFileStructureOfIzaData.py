# this file creates a folder structure for topics/charts/summaries of iza data
from xml.dom import minidom
import json
import csv


summaries_xml = minidom.parse('chart_summaries_b01_toktest2.xml')

topics = summaries_xml.getElementsByTagName('topic')

topicsArr = ['01_01', '02_01', '03_01', '04_01', '05_01', '06_01', '07_01', '08_01', '09_01', '10_01', '11_01', '11_02', '12_01', '12_02', '13_01', '13_02', '01_02', '03_02', '02_02', '14_01', '14_02', '05_02', '07_02', '08_02', '10_02', '09_02', '11_02c', '14_01a', '14_01b', '12_01a', '12_01b', '18_01a', '18_01b', '16_01a', '16_01b', '17_01a', '17_01b', '05_01c', '01_02b', '01_02a', '01_02c', '15_01b', '15_01a', '09_01a', '09_01b', '09_02c', '10_02c']
titlesArr = []

#getting all the summaries 
for topic in topics:
    topic_id = topic.attributes['topic_id'].value.split('_')[0]
    chart_id = topic.attributes['topic_id'].value.split('_')[1]
    stories = topic.getElementsByTagName('story')
    
    # count = 1
    # for story in stories:
    #     with open('./structured_chart_iza_data/' +  str(topic_id) + '/' + str(chart_id) + '/' + str(count) + '.txt', mode='wt', encoding='utf8') as myfile1:
    #         myfile1.write(story.getElementsByTagName('text')[0].getElementsByTagName('content')[0].firstChild.data)
    #     count = count+1


# getting the titles
with open('chartID2plotInfo.json') as json_file:
    json_chart_data = json.load(json_file)

for topic in topicsArr:
    topic_id = topic.split('_')[0]
    chart_id = topic.split('_')[1]
    
    chart = json_chart_data[topic]

    # Writing data tables of charts to text file
    x_title = chart['general_figure_info']['x_axis']['label']['text']
    x_title = x_title.replace(" ", "_")
        
    if x_title == "":
        print('x_title empty: ', topic_id, chart_id)
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
        print('y_title empty: ', topic_id, chart_id)
        ignore = True
        y_title = "type"
    
    f = open('./structured_chart_iza_data/' +  str(topic_id) + '/' + str(chart_id) + '/data.csv', 'w', newline='', encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow([x_title, y_title])

    for x, y in zip(chart['models'][0]['x'], chart['models'][0]['y']):
        if(type(x) is str):
            x = x.replace(" ", "_")
        if(type(y) is str):
            y = y.replace(" ", "_")
        try:
            writer.writerow([x, y])
        except:
            print(x, y)
            raise Exception("Sorry, no numbers below zero")
    
    f.close() 

    # with open('./structured_chart_iza_data/' +  str(topic_id) + '/' + str(chart_id) + '/title.txt', mode='wt', encoding='utf8') as myfile1:
    #     myfile1.write(chart['general_figure_info']['title']['text'])
    
