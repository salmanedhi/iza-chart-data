import json
import numpy as np
from xml.dom import minidom
import re

bar_chart_str = "bar_chart"
titles = []
data_table = []
summaries = []
test_data_chart2text = []
chart_ids = []
traversed_chart_ids = []

# TODO:
#   read xml file, get all chart ids
#   get all chart summaries from the xml file
#   traverse those chart ids in the chartID2plotInfo.json and get data for each chart


### Reading the test id's of charts
test_ids_file = open("ids_test_a.txt", "r")
for chart_id in test_ids_file:
    chart_ids.append(chart_id)

test_ids_file.close()

print("Length of Chart Ids: ", len(chart_ids))

with open('chartID2plotInfo.json') as json_file:
    json_chart_data = json.load(json_file)


for chart_id in chart_ids:
    chart_id = chart_id.strip().split('-')[0]
    chart_id_temp = re.sub('[a-z]', '', chart_id) #getting only the main chart id
    if chart_id_temp not in traversed_chart_ids:
        # Writing Titles to text file
        chart = json_chart_data[chart_id]
        titles.append(chart_id_temp + " " + chart['general_figure_info']['title']['text'])

        # Writing data tables of charts to text file
        x_title = chart['general_figure_info']['x_axis']['label']['text']
        x_title = x_title.replace(" ", "_")
        
        if x_title == "":
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

        print(y_title_final) 
        y_title = y_title_final
        if y_title == "":
            y_title = "type"

        pipe_separated_data_table = ""
        for x, y in zip(chart['models'][0]['x'], chart['models'][0]['y']):
            
            if(type(x) is str):
                x = x.replace(" ", "_")
            if(type(y) is str):
                y = y.replace(" ", "_")

            pipe_separated_data_table += x_title + '|' + str(x) + '|' + 'x' + '|' + bar_chart_str + " "
            pipe_separated_data_table += y_title + '|' + str(y) + '|' + 'y' + '|' + bar_chart_str + " "

        data_table.append(pipe_separated_data_table)
        traversed_chart_ids.append(chart_id_temp)


with open("data_tables.txt", "w") as data_file:
    for data in data_table:
        data_file.write(data + "\n")

# with open("titles.txt", "w") as titles_file:
#     for title in titles:
#         titles_file.write(title + "\n")




# parse an xml file by name
summaries_xml = minidom.parse('chart_summaries_b01_toktest2.xml')

topics = summaries_xml.getElementsByTagName('topic')
for topic in topics:
    stories = topic.getElementsByTagName('story')
    topic_id = re.sub('[a-z]', '', topic.attributes['topic_id'].value)
    for story in stories:
        summaries.append({'id': topic_id, 'summary': story.getElementsByTagName('text')[0].getElementsByTagName('content')[0].firstChild.data})

# print(topics[0].getElementsByTagName('story')[0].getElementsByTagName('text')[0].getElementsByTagName('content')[0].firstChild.data)
# print(summaries)
print(len(traversed_chart_ids))
# with open("summaries.txt", "w") as summaries_file:
#     for summary in summaries:
#         if(summary['id'] in traversed_chart_ids):
#             summaries_file.write(summary['id'] + " " + summary['summary'] + "\n")
#             traversed_chart_ids.remove(summary['id'])



