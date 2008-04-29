from xml.etree.ElementTree import Element, SubElement, dump

window = Element("window")

title = SubElement(window, "title", font="large")
title.text = "A sample text window"

text = SubElement(window, "text", wrap="word")

box = SubElement(window, "buttonbox")
SubElement(box, "button").text = "OK"
SubElement(box, "button").text = "Cancel"

dump(window)